using Pulumi;
using Pulumi.AzureNative.Storage;
using System.Collections.Generic;

public class StorageComponentArgs : ResourceArgs
{
    public Input<string> ResourceGroupName { get; set; } = null!;
    public Input<string> BaseName { get; set; } = null!;
}

public class StorageComponent : ComponentResource
{
    public Output<string> StorageAccountName { get; private set; }
    public Output<string> ContainerName { get; private set; }

    public StorageComponent(string name, StorageComponentArgs args, ComponentResourceOptions? options = null)
        : base("custom:StorageComponent", name, options)
    {
        var storageAccount = new StorageAccount($"{args.BaseName}-storage", new StorageAccountArgs
        {
            ResourceGroupName = args.ResourceGroupName,
            AccountName = args.BaseName.Apply(name => $"{name}storage"),
            Kind = Kind.StorageV2,
            Sku = new Pulumi.AzureNative.Storage.Inputs.SkuArgs
            {
                Name = SkuName.Standard_LRS
            }
        }, new CustomResourceOptions { Parent = this });

        var storageContainer = new BlobContainer($"{args.BaseName}-container", new BlobContainerArgs
        {
            ResourceGroupName = args.ResourceGroupName,
            AccountName = storageAccount.Name,
            ContainerName = "data",
            PublicAccess = PublicAccess.None
        }, new CustomResourceOptions { Parent = this });

        this.StorageAccountName = storageAccount.Name;
        this.ContainerName = storageContainer.Name;

        this.RegisterOutputs(new Dictionary<string, object?>
        {
            ["storageAccountName"] = this.StorageAccountName,
            ["containerName"] = this.ContainerName
        });
    }
}