## Exercise 1: Move the AKS Cluster Related Resources into the provided "cluster" component resource module shell.
## Hint: The block of resources to move is marked with "### AKS Cluster Related Resoures"
## It should take as input parameters: 
## - the various config values used by the resources
## - resource group name
## It should provide the following output: 
## - K8s kubeconfig
# Component Resources Doc: https://www.pulumi.com/docs/intro/concepts/resources/#components
# Example Code: https://github.com/pulumi/examples/blob/master/azure-py-virtual-data-center/spoke.py

## Exercise 2: Add the "protect" resource option to the "cluster" resource and do a `pulumi up` and then a `pulumi destroy`
## Note how the component resource children get the protect option enabled.
## Note how you can't destroy the stack as long as protect is true.
# Doc: https://www.pulumi.com/docs/intro/concepts/resources/#protect
# Doc: https://www.pulumi.com/docs/reference/cli/pulumi_state_unprotect/

import base64
import pulumi
from pulumi import Config, ResourceOptions
from pulumi_tls import PrivateKey
from pulumi_azure_native import resources, containerservice
import pulumi_azuread as azuread
import pulumi_kubernetes as k8s
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts
import pulumi_random as random

# Config values or defaults
config = Config()
k8s_version = config.get('k8sVersion') or '1.18.14'
admin_username = config.get('adminUserName') or 'testuser'
node_count = config.get_int('nodeCount') or 2
node_size = config.get('nodeSize') or 'Standard_D2_v2'
password = config.get_secret("password")
if not password:
    rando_password=random.RandomPassword('password',
        length=16,
        special=True,
        override_special='@_#',
        )
    password=rando_password.result 

# Resource Group
resource_group = resources.ResourceGroup('rg')

### AKS Cluster Related Resources
generated_key_pair = PrivateKey('ssh-key',
    algorithm='RSA', rsa_bits=4096)
ssh_public_key = generated_key_pair.public_key_openssh

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
# So decode the kubeconfig for our cluster but mark it as a secret so Pulumi treats it accordingly.
kubeconfig = pulumi.Output.secret(creds.kubeconfigs[0].value.apply(
    lambda enc: base64.b64decode(enc).decode()))
### End of AKS Cluster Related Resources

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

# Correct option using "concat()"
pulumi.export('Apache_URL', pulumi.Output.concat('http://', apache_service_ip)) 