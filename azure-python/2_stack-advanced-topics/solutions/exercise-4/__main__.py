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
## be imported into the main program and referenced accordingly.

import pulumi
from pulumi import ResourceOptions
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts

## Exercise 4
## Move the cluster and related bits to a cluster.py file and import here.
## Modify references to add "cluster." as needed.
## This means the main can focus on deploying the Helm chart to the K8s cluster without worrying
## about the nuances of creating a cluster.
## It also means I can swap out the cluster.py file for one which deploys to, say, AWS EKS and this code
## doesn't have to change.
import cluster

# Create a chart resource to deploy apache using the k8s provider instantiated above.
apache = Chart('apache-chart',
    ChartOpts(
        chart='apache',
        version='8.3.2',
        fetch_opts={'repo': 'https://charts.bitnami.com/bitnami'}),
    opts=ResourceOptions(provider=cluster.k8s_provider))

# Get the helm-deployed apache service IP which isn't known until the chart is deployed.
apache_service_ip = apache.get_resource('v1/Service', 'apache-chart').apply(
    lambda res: res.status.load_balancer.ingress[0].ip)

pulumi.export('resource_group_name', cluster.resource_group.name)
pulumi.export('cluster_name', cluster.k8s_cluster.name)
pulumi.export('apache_service_ip', apache_service_ip)

## Exercise 3
# Same results in a couple of different ways.
# using "concat()"
pulumi.export('apache_url_using_concat', pulumi.Output.concat('http://', apache_service_ip)) 
# using "apply()"
pulumi.export('apache_url_using_apply', apache_service_ip.apply(lambda ip: f'http://{ip}'))

## Exercise 4
## Now that kubeconfig and password come via the cluster module, the export is updated to reference it as such.
pulumi.export('kubeconfig', cluster.kubeconfig)
pulumi.export('password', cluster.password)