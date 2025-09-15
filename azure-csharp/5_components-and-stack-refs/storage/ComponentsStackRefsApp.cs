using Pulumi;

class ComponentsStackRefsApp : Stack
{
    public ComponentsStackRefsApp()
    {
        var config = new Config();
        var baseName = config.Require("baseName");
        var baseStackProjectName = config.Require("baseStackProjectName");
        var baseStackName = config.Require("baseStackName");

        var stackName = Pulumi.Deployment.Instance.StackName;
        var orgName = Pulumi.Deployment.Instance.OrganizationName;
        var baseStackFullName = $"{orgName}/{baseStackProjectName}/{baseStackName}";
        var baseStackRef = new StackReference(baseStackFullName);

        var resourceGroupName = stackOutput(baseStackRef, "ResourceGroupName");

        var storage = new StorageComponent("storage", new StorageComponentArgs
        {
            ResourceGroupName = resourceGroupName,
            BaseName = baseName
        });

        this.StorageAccountName = storage.StorageAccountName;
        this.ContainerName = storage.ContainerName;
    }

    private static Output<string> stackOutput(StackReference stackref, string stackOutputName)
    {
        return Output.Format($"{stackref.RequireOutput(stackOutputName).Apply(v => v.ToString())}");
    }

    [Output] public Output<string> StorageAccountName { get; set; }
    [Output] public Output<string> ContainerName { get; set; }
}