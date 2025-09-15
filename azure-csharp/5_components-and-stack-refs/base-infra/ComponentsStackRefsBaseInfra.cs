using Pulumi;
using Pulumi.AzureNative.Resources;

class ComponentsStackRefsBaseInfra : Stack
{
    public ComponentsStackRefsBaseInfra()
    {
        var config = new Config();
        var baseName = config.Require("baseName");

        var resourceGroup = new ResourceGroup($"{baseName}-rg");

        this.ResourceGroupName = resourceGroup.Name;
    }

    [Output] public Output<string> ResourceGroupName { get; set; }
}