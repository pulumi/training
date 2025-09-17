using Pulumi;
using Pulumi.AzureNative.Storage;
using System.Collections.Generic;

/// <summary>
/// Arguments for the custom StorageComponent
/// </summary>
public class StorageComponentArgs : ResourceArgs
{
    public Input<string> ResourceGroupName { get; set; } = null!;
    public Input<string> BaseName { get; set; } = null!;
}

/// <summary>
/// Custom Pulumi ComponentResource that creates Azure Storage Account and Blob Container
/// </summary>
public class StorageComponent : ComponentResource
{
    public Output<string> StorageAccountName { get; private set; }
    public Output<string> ContainerName { get; private set; }

    public StorageComponent(string name, StorageComponentArgs args, ComponentResourceOptions? options = null)
        : base("custom:StorageComponent", name, options)
    {
        // Create Azure Storage Account with Standard LRS redundancy
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

        // Create private blob container within the storage account
        var storageContainer = new BlobContainer($"{args.BaseName}-container", new BlobContainerArgs
        {
            ResourceGroupName = args.ResourceGroupName,
            AccountName = storageAccount.Name,
            ContainerName = "data",
            PublicAccess = PublicAccess.None
        }, new CustomResourceOptions { Parent = this });

        this.StorageAccountName = storageAccount.Name;
        this.ContainerName = storageContainer.Name;

        // Register outputs for this component resource
        this.RegisterOutputs(new Dictionary<string, object?>
        {
            ["storageAccountName"] = this.StorageAccountName,
            ["containerName"] = this.ContainerName
        });
    }
}