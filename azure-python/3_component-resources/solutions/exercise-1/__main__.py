## Exercise 1: Move the AKS Cluster Related Resources into a component resource module.
## Hint: The block of resources to move is marked with "### AKS Cluster Resoures"
## It should take as input parameters: 
## - config values used by the resources.
## - resource group name
## It should provide the following outputs: 
## - K8s kubeconfig
# Component Resources Doc: https://www.pulumi.com/docs/intro/concepts/resources/#components
# Example Code: https://github.com/pulumi/examples/blob/master/azure-py-virtual-data-center/spoke.py

## Exercise 2: Add the "protect" resource option to the "cluster" resource and do a `pulumi up` and then a `pulumi destroy`
## Note how the component resource children get the protect option enabled.
## Note how you can't destroy the stack as long as protect is true.
# Doc: https://www.pulumi.com/docs/intro/concepts/resources/#protect
# Doc: https://www.pulumi.com/docs/reference/cli/pulumi_state_unprotect/

import pulumi
from pulumi import Config, ResourceOptions
from pulumi_azure_native import resources
import pulumi_kubernetes as k8s
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts
import pulumi_random as random

import cluster

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

# Exercise 1
# Create a cluster resource using our custom component resource class
cluster = cluster.Cluster('k8scluster', cluster.ClusterArgs(
    resource_group_name=resource_group.name,
    password=password,
    node_count=node_count,
    node_size=node_size,
    k8s_version=k8s_version,
    admin_username=admin_username,
))

# The K8s provider which supplies the helm chart resource needs to know how to talk to the K8s cluster.
# So, instantiate a K8s provider using the retrieved kubeconfig.
k8s_provider = k8s.Provider('k8s-provider', kubeconfig=cluster.kubeconfig)

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