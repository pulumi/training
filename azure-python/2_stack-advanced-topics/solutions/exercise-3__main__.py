## Exercise 1: Create and use a configuration secret for a password, and create a stack output with the value. 
## NOTE: The code as written now will fail since there is a reference to a password variable that is not set.
## The goal of this exercise is to address that by storing the password in the stack config as a secret
## and then getting the value in the code. 
## And, when exported as a stack output, you will see that Pulumi will keep it as a secret.
## Furthermore, secrets are not displayed in logs or in the Pulumi Console (SaaS).
# Config Doc: https://www.pulumi.com/docs/intro/concepts/config/ 
# Secrets Doc: https://www.pulumi.com/docs/intro/concepts/secrets/

## Exercise 2: Programmatically set the kubeconfig obtained from the K8s cluster as a secret in the code and make it a stack output.
## Exercise 2a: See the secret output's value.
# Programmatic Secrets Doc: https://www.pulumi.com/docs/intro/concepts/secrets/#programmatically-creating-secrets
# Stack Outputs Doc: https://www.pulumi.com/docs/intro/concepts/stack/#outputs
# Seeing Stack Secret Outputs Doc: https://www.pulumi.com/docs/reference/cli/pulumi_stack/

## Exercise 3: Create a URL with the "apache_service_ip" and make it an output.
## Bonus: Solve this in two ways.
# Hint: The value of "apache_service_ip" is not known until after deployment. So it's an "Output<T>" type.
# Inputs and Outputs Doc: https://www.pulumi.com/docs/intro/concepts/inputs-outputs

## Exercise 4: Make the code more modular and readable by moving config and related set up to it's own file
## and move the cluster decalration and related bits to it's own file. 
## Hint: This is simply using python constructs whereby code blocks can be put in separate files, 
## be imported into the main program and referenced accordingly..

import base64
import pulumi
from pulumi import Config, ResourceOptions
from pulumi_tls import PrivateKey
from pulumi_azure_native import resources, containerservice
import pulumi_azuread as azuread
import pulumi_kubernetes as k8s
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts

config = Config()
k8s_version = config.get('k8sVersion') or '1.18.14'
admin_username = config.get('adminUserName') or 'testuser'
node_count = config.get_int('nodeCount') or 2
node_size = config.get('nodeSize') or 'Standard_D2_v2'

## Exercise 1
## Suggestion: Take a look at the stack config file (e.g. Pulumi.dev.yaml) to confirm you stored the password as a secret.
password = config.require_secret("password")
pulumi.export('password', password)
## Exercise 1

generated_key_pair = PrivateKey('ssh-key',
    algorithm='RSA', rsa_bits=4096)
ssh_public_key = generated_key_pair.public_key_openssh

resource_group = resources.ResourceGroup('rg')

ad_app = azuread.Application('app', display_name='app')
ad_sp = azuread.ServicePrincipal('service-principal',
    application_id=ad_app.application_id)
ad_sp_password = azuread.ServicePrincipalPassword('sp-password',
    service_principal_id=ad_sp.id,
    value=password,
    end_date='2099-01-01T00:00:00Z')

k8s_cluster = containerservice.ManagedCluster('cluster',
    resource_group_name=resource_group.name,
    addon_profiles={
        'KubeDashboard': {
            'enabled': True,
        },
    },
    agent_pool_profiles=[{
        'count': node_count,
        'max_pods': 20,
        'mode': 'System',
        'name': 'agentpool',
        'node_labels': {},
        'os_disk_size_gb': 30,
        'os_type': 'Linux',
        'type': 'VirtualMachineScaleSets',
        'vm_size': node_size,
    }],
    dns_prefix=resource_group.name,
    enable_rbac=True,
    kubernetes_version=k8s_version,
    linux_profile={
        'admin_username': admin_username,
        'ssh': {
            'publicKeys': [{
                'keyData': ssh_public_key,
            }],
        },
    },
    node_resource_group='node-resource-group',
    service_principal_profile={
        'client_id': ad_app.application_id,
        'secret': ad_sp_password.value,
    })

# Obtaining the kubeconfig from an Azure K8s cluster requires using the "list_managed_clsuter_user_credentials"
# function.
# That function requires passing values that are not be known until the resources are created.
# Thus, the use of "apply()" to wait for those values before calling the function.
creds = pulumi.Output.all(resource_group.name, k8s_cluster.name).apply(
    lambda args:
    containerservice.list_managed_cluster_user_credentials(
        resource_group_name=args[0],
        resource_name=args[1]))

# The "list_managed_cluster_user_credentials" function returns an array of base64 encoded kubeconfigs.
# So decode the kubeconfig for our cluster.
## Exercise 2/2a
## How to programmatically create a secret: Use `pulumi.Output.secret()`
kubeconfig = pulumi.Output.secret(creds.kubeconfigs[0].value.apply(
    lambda enc: base64.b64decode(enc).decode()))
## How to get the unecrypted value from the stack outputs: `pulumi stack output kubeconfig --show-secret`
pulumi.export('kubeconfig', kubeconfig)
## Exercise 2

# The K8s provider which supplies the helm chart resource needs to know how to talk to the K8s cluster.
# So, instantiate a K8s provider using the retrieved kubeconfig.
k8s_provider = k8s.Provider('k8s-provider', kubeconfig=kubeconfig)

# Create a chart resource to deploy apache using the k8s provider instantiated above.
apache = Chart('apache-chart',
    ChartOpts(
        chart='apache',
        version='8.3.2',
        fetch_opts={'repo': 'https://charts.bitnami.com/bitnami'}),
    opts=ResourceOptions(provider=k8s_provider))

# Get the helm-deployed apache service IP which isn't known until the chart is deployed.
apache_service_ip = apache.get_resource('v1/Service', 'apache-chart').apply(
    lambda res: res.status.load_balancer.ingress[0].ip)

pulumi.export('resource_group_name', resource_group.name)
pulumi.export('cluster_name', k8s_cluster.name)
pulumi.export('apache_service_ip', apache_service_ip)

## Exercise 3
# Showing the WRONG way so one can see how it outputs
pulumi.export('apache_url_wrong', f'http://{apache_service_ip}')
# Correct option using "concat()"
pulumi.export('apache_url_using_concat', pulumi.Output.concat('http://', apache_service_ip)) 
# Correct option using "apply()"
pulumi.export('apache_url_using_apply', apache_service_ip.apply(lambda ip: f'http://{ip}'))