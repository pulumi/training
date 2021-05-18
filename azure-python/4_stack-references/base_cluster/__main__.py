## Exercise 1: See the `app` directory.

import pulumi
from pulumi import Config, ResourceOptions
from pulumi_azure_native import resources
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

# Create a cluster resource using our custom component resource class
cluster = cluster.Cluster('k8scluster', cluster.ClusterArgs(
    resource_group_name=resource_group.name,
    password=password,
    node_count=node_count,
    node_size=node_size,
    k8s_version=k8s_version,
    admin_username=admin_username,
))

# Export the kubeconfig 
pulumi.export("kubeconfig", cluster.kubeconfig)