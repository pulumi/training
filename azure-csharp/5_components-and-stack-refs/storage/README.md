# Storage Project - Components and Stack References

This project demonstrates two key Pulumi concepts: **Components** and **Stack References** through a practical Azure storage implementation.

## Components

Pulumi Components are reusable infrastructure building blocks that encapsulate related resources and create abstractions for common patterns.

### StorageComponent (`StorageComponent.cs`)

The `StorageComponent` class demonstrates a custom component that:

- **Encapsulates** an Azure Storage Account and Blob Container
- **Inherits** from `ComponentResource` with type `"custom:StorageComponent"`
- **Accepts** configuration through `StorageComponentArgs`
- **Exposes** outputs like `StorageAccountName` and `ContainerName`
- **Registers** outputs using `RegisterOutputs()` for consumption by other stacks

**Key Benefits:**
- Reusable across multiple projects
- Enforces consistent storage configuration
- Simplifies complex resource relationships
- Enables sharing of best practices

## Stack References

Stack References allow programmatic access to outputs from other Pulumi stacks at runtime, enabling modular infrastructure design.

### Implementation (`ComponentsStackRefsApp.cs`)

This project uses stack references to:

1. **Reference** a base infrastructure stack using `StackReference`
2. **Retrieve** the Resource Group name from the base stack
3. **Pass** the referenced value to the storage component

```csharp
var baseStackRef = new StackReference(baseStackFullName);
var resourceGroupName = stackOutput(baseStackRef, "ResourceGroupName");
```

**Configuration Required:**
- `baseName`: Base name for storage resources
- `baseStackProjectName`: Name of the base infrastructure project
- `baseStackName`: Name of the base infrastructure stack

**Key Benefits:**
- Enables modular, interconnected infrastructure
- Supports dynamic value sharing between stacks
- Simplifies multi-environment deployments
- Promotes separation of concerns

## Usage Pattern

This project follows a common pattern where:

1. **Base Infrastructure Stack** provisions shared resources (Resource Groups, Networks)
2. **Application Stack** (this project) references base outputs and creates application-specific resources
3. **Components** provide reusable building blocks for consistent resource creation

This approach enables teams to manage infrastructure at different layers while maintaining dependencies and ensuring consistency across environments.