using Pulumi;
using Pulumi.AzureNative.Resources;

class ComponentsStackRefsBaseInfra : Stack
{
    public ComponentsStackRefsBaseInfra()
    {
        // Get required configuration value for resource naming
        var config = new Config();
        var baseName = config.Require("baseName");

        // Create the foundational resource group that other stacks will reference
        var resourceGroup = new ResourceGroup($"{baseName}-rg");

        // Export the resource group name so other stacks can reference it via StackReference
        this.ResourceGroupName = resourceGroup.Name;
    }

    [Output] public Output<string> ResourceGroupName { get; set; }
}