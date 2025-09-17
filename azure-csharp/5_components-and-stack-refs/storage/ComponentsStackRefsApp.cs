using Pulumi;

class ComponentsStackRefsApp : Stack
{
    public ComponentsStackRefsApp()
    {
        var config = new Config();
        var baseName = config.Require("baseName");
        var baseStackProjectName = config.Require("baseStackProjectName");
        var baseStackName = config.Require("baseStackName");

        // Build the full stack reference path: org/project/stack
        var stackName = Pulumi.Deployment.Instance.StackName;
        var orgName = Pulumi.Deployment.Instance.OrganizationName;
        var baseStackFullName = $"{orgName}/{baseStackProjectName}/{baseStackName}";

        // Create reference to the base infrastructure stack
        var baseStackRef = new StackReference(baseStackFullName);

        // Get the resource group name from the base stack's outputs
        var resourceGroupName = stackOutput(baseStackRef, "ResourceGroupName");

        // Create storage resources using the custom component
        var storage = new StorageComponent("storage", new StorageComponentArgs
        {
            ResourceGroupName = resourceGroupName,
            BaseName = baseName
        });

        this.StorageAccountName = storage.StorageAccountName;
        this.ContainerName = storage.ContainerName;
    }

    /// <summary>
    /// Helper method to extract and format stack reference outputs
    /// </summary>
    private static Output<string> stackOutput(StackReference stackref, string stackOutputName)
    {
        return Output.Format($"{stackref.RequireOutput(stackOutputName).Apply(v => v.ToString())}");
    }

    [Output] public Output<string> StorageAccountName { get; set; }
    [Output] public Output<string> ContainerName { get; set; }
}