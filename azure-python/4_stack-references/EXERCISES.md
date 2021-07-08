# Set Up Environment

- Create two directories for each project: `mkdir base_cluster app`
- Pull down the base_infra project:
  - `cd base_cluster`
  - `pulumi new <base_cluster-URL>`
  - `pulumi up`
- Pull down the app project:
  - `cd ../app`
  - `pulumi new <app-URL>`

# Exercise 1
Add stack references to the `app` project to get the kubeconfig from the the `base_cluster` stack.  

Related Docs:
- Stack References: https://www.pulumi.com/docs/intro/concepts/stack/#stackreferences


