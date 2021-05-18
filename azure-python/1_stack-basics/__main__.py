## Exercise 1: Export the resource group name as a stack output
# Doc: https://www.pulumi.com/docs/intro/concepts/stack/#outputs

## Exercise 2: Use stack configuration to set the resource group name instead of using the hard-coded, string 'resource_group'
# Doc: https://www.pulumi.com/docs/intro/concepts/config/#code
# Hint: Require a configuration parameter named "base_name" that you can then use as a basis for resource names.

## (Optional) Exercise 3: Use explicit naming for the resource group instead of autonaming.
# Note: This does mean you have to prevent resource naming conflicts.
# Hint: Resources have a "name" property that allows you to override autonaming.
# Doc: https://www.pulumi.com/docs/reference/pkg/azure-native/resources/resourcegroup/

import pulumi
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("resource_group")

