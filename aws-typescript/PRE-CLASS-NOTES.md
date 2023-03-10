# Pre Class Notes
To ensure the most efficient use of workshop time, each student should go through the following steps to set up the environment to use for the workshop.

## Prerequisites
1. Go through the AWS getting started for typescript found here: https://www.pulumi.com/docs/get-started/aws/ 

## Set Up Workshop Environments
This will install the base workshop code and related typescript packages. 
When done you should have a directory structure like this:
```
aws-typescript-workshop
|- stack-basics
|- stack-advanced-topics
|- component-resources
|- stack-references
   |- base-infra
   |- app
```

1. `mkdir aws-typescript-workshop && cd aws-typescript-workshop`

**NOTE:** When running `pulumi new` below, if you are going to use your Pulumi organization account instead of your personal Pulumi account, use `YOUR-ORGANIZATION-NAME/YOUR-NAME` when prompted for a stack name. This will create the stack in your organization and by using your name will avoid stack naming conflicts.

2. `mkdir stack-basics && cd stack-basics`
3. `pulumi new https://github.com/pulumi/training/tree/main/aws-typescript/1_stack-basics`
4. `cd ..`
5. `mkdir stack-advanced-topics && cd stack-advanced-topics`
6. `pulumi new https://github.com/pulumi/training/tree/main/aws-typescript/2_stack-advanced-topics`
7. `cd ..`
8. `mkdir component-resources && cd component-resources`
9. `pulumi new https://github.com/pulumi/training/tree/main/aws-typescript/3_component-resources`
10. `cd ..`
11. `mkdir stack-references && cd stack-references`
12. `mkdir base-infra && cd base-infra`
13. `pulumi new https://github.com/pulumi/training/tree/main/aws-typescript/4_stack-references/base-infra`
14. `cd ..`
15. `mkdir app && cd app`
16. `pulumi new https://github.com/pulumi/training/tree/main/aws-typescript/4_stack-references/app`

