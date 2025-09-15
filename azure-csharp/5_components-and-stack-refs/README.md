# Components and Stack References Example

This example demonstrates how to use Pulumi component resources combined with stack references in Azure.

## Architecture

This example consists of two separate Pulumi stacks:

### Base Infrastructure (`base-infra/`)
- **ComponentsStackRefsBaseInfra Stack**: Creates a simple Azure Resource Group

### Storage Stack (`storage/`)
- **StorageComponent**: Encapsulates Azure Storage Account and Blob Container creation
- **ComponentsStackRefsApp Stack**: References the base infrastructure stack and uses the storage component

## Key Features

1. **Component Resources**: Storage infrastructure is organized into a reusable component (`StorageComponent`)
2. **Stack References**: The storage stack references the resource group from the base infrastructure stack
3. **Simplified Architecture**: Focused on demonstrating component and stack reference patterns
4. **Separation of Concerns**: Infrastructure and storage deployment are separated into different stacks

## Usage

### 1. Deploy Base Infrastructure
```bash
cd base-infra
pulumi stack init dev
pulumi config set baseName <your-base-name>
pulumi up
```

### 2. Deploy Storage
```bash
cd ../storage
pulumi stack init dev
pulumi config set baseName <your-base-name>
pulumi config set baseStackProjectName components-stack-refs-base-infra
pulumi up
```

## Components Created

### StorageComponent
- Azure Storage Account (Standard_LRS)
- Blob Container named "data" with private access

### Stack Outputs
The base infrastructure stack outputs:
- `ResourceGroupName`

The storage stack outputs:
- `StorageAccountName`
- `ContainerName`

The storage stack uses the resource group from the base infrastructure via stack references.

## Benefits

1. **Modularity**: The storage component can be reused across different projects
2. **Stack Separation**: Infrastructure and storage concerns are separated
3. **Component Encapsulation**: Storage account and container are managed together as a logical unit
4. **Maintainability**: Clear separation of resources makes maintenance easier