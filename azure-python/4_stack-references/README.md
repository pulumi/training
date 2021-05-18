# Stack References

Use stack references to pass information from one stack to another.  
There are two project directories:

- base_cluster: stands up a base AKS cluster and exports the kubeconfig.
- app: deploys a simple app on a K8s cluster.

## Main Exercise Steps

- Create two directories for each project: `mkdir base_infra app`
- Pull down the base_infra project:
  - `cd base_cluster`
  - `pulumi new <base_cluster-URL>`
  - `pulumi up`
- Pull down the app project:
  - `cd ../app`
  - `pulumi new <app-URL>`
  - Add stack references to the `app` project to get the kubeconfig from the the `base_cluster` stack.  
    Docs: https://www.pulumi.com/docs/intro/concepts/stack/#stackreferences
  - `pulumi up`

See the `solutions` folder for the answers.
