"""An Azure RM Python Pulumi program"""

## Exercise 1: Export the resource group name as a stack output
# Doc: https://www.pulumi.com/docs/intro/concepts/stack/#outputs

## Exercise 2: Use stack configuration to set the resource group name instead of the hard-coded 'resource_group'
# Doc: https://www.pulumi.com/docs/intro/concepts/config/#code
# Hint: Require a configuration parameter named "base_name" that you can then use as a basis for resource names.

## (Optional) Exercise 3: Use explicit naming for the resource group instead of autonaming.
# Note: This means you have to prevent resource naming conflicts.
# Hint: Resources have a "_name" property that allows you to override autonaming.
# Doc: https://www.pulumi.com/docs/reference/pkg/azure-native/resources/resourcegroup/

import pulumi
from pulumi_azure_native import resources

## Exercise 2 ##
config = pulumi.Config()
base_name = config.require("base_name")
## Exercise 2 ##


# Create an Azure Resource Group
## Exercise 3 ##
resource_group = resources.ResourceGroup(f"{base_name}-rg",
  resource_group_name=base_name)
## Exercise 3 ##

## Exercise 1 ##
pulumi.export("rg_name", resource_group.name)
## Exercise 1 ##

