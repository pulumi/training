# Base Infrastructure

This Pulumi project creates base Azure infrastructure including a resource group.

## Configuration

Set the required configuration values:

```bash
# Set the base name for resources
pulumi config set baseName <your-base-name>

# Set the Azure location
pulumi config set azure-native:location <azure-region>
```

## Pulumi Commands

```bash
# Preview changes
pulumi preview

# Deploy infrastructure
pulumi up

# Refresh state from actual resources
pulumi refresh

# Import existing resource
pulumi import azure-native:resources:ResourceGroup <resource-name> <azure-resource-id>

# Destroy infrastructure
pulumi destroy
```

### Command Descriptions

- **`pulumi config set`**: Sets configuration values that your Pulumi program can access. These values are stored per stack and can be used to customize deployments for different environments.

- **`pulumi preview`**: Shows what changes will be made to your infrastructure without actually applying them. This is a dry-run that helps you understand the impact before deployment.

- **`pulumi up`**: Deploys your infrastructure by creating, updating, or deleting resources as needed. Prompts for confirmation before applying changes.

- **`pulumi refresh`**: Synchronizes your Pulumi state with the actual state of resources in Azure. Use this if resources were modified outside of Pulumi.

- **`pulumi import`**: Imports an existing Azure resource into Pulumi management. Use this to adopt resources that were created outside of Pulumi.

- **`pulumi destroy`**: Removes all resources managed by this Pulumi stack. Prompts for confirmation before deletion.

## Import Example

To import an existing resource group into this Pulumi stack:

```bash
# Import a resource group that already exists in Azure
pulumi import azure-native:resources:ResourceGroup my-existing-rg /subscriptions/<subscription-id>/resourceGroups/<existing-rg-name>
```

Replace `<subscription-id>` with your Azure subscription ID and `<existing-rg-name>` with the name of the existing resource group.

## Common Command Modifiers

### Targeting Specific Resources

```bash
# Target only specific resources
pulumi up --target urn:pulumi:stack::project::type::name
pulumi destroy --target urn:pulumi:stack::project::type::name

# Exclude specific resources
pulumi up --exclude urn:pulumi:stack::project::type::name
pulumi destroy --exclude urn:pulumi:stack::project::type::name
```

### Other Useful Modifiers

```bash
# Skip confirmation prompts (use with caution)
pulumi up --yes
pulumi destroy --yes

# Run any custom logic in the Pulumi program during a destroy
pulumi destroy --run-program

# Show detailed diff information
pulumi preview --diff
pulumi up --diff
```

### Modifier Descriptions

- **`--target`**: Limits the operation to specific resources only. Useful for updating or destroying individual resources without affecting others.

- **`--exclude`**: Excludes specific resources from the operation. All other resources will be processed normally.

- **`--yes`**: Automatically approves the operation without prompting for confirmation. Use carefully, especially with `destroy`.

- **`--run-program`**: Forces Pulumi to run the full program even during operations like refresh and destroy that normally rely only on state. Useful when you need fresh program output for these operations.

- **`--diff`**: Shows detailed differences between current and desired state, including property-level changes.

## Outputs

- `ResourceGroupName`: The name of the created resource group
