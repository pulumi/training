from pulumi_azure_native import resources, containerservice
import pulumi_azuread as azuread
import pulumi_kubernetes as k8s
from pulumi import Output
import base64

## Exercise 4
## Move the config and stuff to a config.py file and import here.
## Also need to add "config." to the variables that are from the config.py file.
## E.g. "password" below is not referenced as "config.password"
import config

resource_group = resources.ResourceGroup('rg')

ad_app = azuread.Application('app', display_name='app')
ad_sp = azuread.ServicePrincipal('service-principal',
    application_id=ad_app.application_id)
ad_sp_password = azuread.ServicePrincipalPassword('sp-password',
    service_principal_id=ad_sp.id,
    value=config.password,
    end_date='2099-01-01T00:00:00Z')

k8s_cluster = containerservice.ManagedCluster('cluster',
    resource_group_name=resource_group.name,
    addon_profiles={
        'KubeDashboard': {
            'enabled': True,
        },
    },
    agent_pool_profiles=[{
        'count': config.node_count,
        'max_pods': 20,
        'mode': 'System',
        'name': 'agentpool',
        'node_labels': {},
        'os_disk_size_gb': 30,
        'os_type': 'Linux',
        'type': 'VirtualMachineScaleSets',
        'vm_size': config.node_size,
    }],
    dns_prefix=resource_group.name,
    enable_rbac=True,
    kubernetes_version=config.k8s_version,
    linux_profile={
        'admin_username': config.admin_username,
        'ssh': {
            'publicKeys': [{
                'keyData': config.ssh_public_key,
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
creds = Output.all(resource_group.name, k8s_cluster.name).apply(
    lambda args:
    containerservice.list_managed_cluster_user_credentials(
        resource_group_name=args[0],
        resource_name=args[1]))

# The "list_managed_cluster_user_credentials" function returns an array of base64 encoded kubeconfigs.
# So decode the kubeconfig for our cluster.
## Exercise 2/2a
## How to programmatically create a secret: Use `pulumi.Output.secret()`
kubeconfig = Output.secret(creds.kubeconfigs[0].value.apply(
    lambda enc: base64.b64decode(enc).decode()))

# The K8s provider which supplies the helm chart resource needs to know how to talk to the K8s cluster.
# So, instantiate a K8s provider using the retrieved kubeconfig.
k8s_provider = k8s.Provider('k8s-provider', kubeconfig=kubeconfig)

## Exercise 4 
## For parity with Exercise 2, we'll create a local copy of the password so main can export it.
## The nice thing is that it's secrecy attribute is maintained.
password = config.password