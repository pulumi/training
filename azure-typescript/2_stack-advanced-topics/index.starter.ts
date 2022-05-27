import * as containerservice from "@pulumi/azure-native/containerservice";
import * as resources from "@pulumi/azure-native/resources";
import * as azuread from "@pulumi/azuread";
import * as k8s from "@pulumi/kubernetes";
import * as pulumi from "@pulumi/pulumi";
import * as tls from "@pulumi/tls";

const config = new pulumi.Config();
const baseName = config.get("baseName") || pulumi.getStack();
const k8sVersion = config.get("k8sVersion") || "1.19.11";
const nodeCount = config.getNumber("nodeCount") || 2;
const nodeSize = config.get("nodeSize") || "Standard_D2_v2";

const generatedKeyPair = new tls.PrivateKey("ssh-key", {
    algorithm: "RSA",
    rsaBits: 4096,
});
const sshPublicKey = generatedKeyPair.publicKeyOpenssh;

const resourceGroup = new resources.ResourceGroup(`${baseName}-rg`);

const adApp = new azuread.Application(`${baseName}-app`, {
    displayName: "app",
});

const adSp = new azuread.ServicePrincipal(`${baseName}-sp`, {
    applicationId: adApp.applicationId,
});

const adSpPassword = new azuread.ServicePrincipalPassword(`${baseName}-passwd`, {
    servicePrincipalId: adSp.id,
});

const k8sCluster = new containerservice.ManagedCluster(`${baseName}-k8s`, {
    resourceGroupName: resourceGroup.name,
    agentPoolProfiles: [{
        count: nodeCount,
        maxPods: 110,
        mode: "System",
        name: "agentpool",
        nodeLabels: {},
        osDiskSizeGB: 30,
        osType: "Linux",
        type: "VirtualMachineScaleSets",
        vmSize: nodeSize,
    }],
    dnsPrefix: resourceGroup.name,
    enableRBAC: true,
    kubernetesVersion: k8sVersion,
    linuxProfile: {
        adminUsername: adminUserName,
        ssh: {
            publicKeys: [{
                keyData: sshPublicKey,
            }],
        },
    },
    nodeResourceGroup: "node-resource-group",
    servicePrincipalProfile: {
        clientId: adApp.applicationId,
        secret: adSpPassword.value,
    },
});

const creds = containerservice.listManagedClusterUserCredentialsOutput({
    resourceGroupName: resourceGroup.name,
    resourceName: k8sCluster.name,
});

const kubeconfig =
    creds.kubeconfigs[0].value
        .apply(enc => Buffer.from(enc, "base64").toString());

const k8sProvider = new k8s.Provider("k8s-provider", {
    kubeconfig: kubeconfig,
});

const apache = new k8s.helm.v3.Chart(`${baseName}-apache`,
    {
        chart: "apache",
        version: "8.3.2",
        fetchOpts: {
            repo: "https://charts.bitnami.com/bitnami",
        },
    },
    { provider: k8sProvider },
);

export let apacheServiceIP = apache
    .getResourceProperty("v1/Service", "apache-chart", "status")
    .apply(status => status.loadBalancer.ingress[0].ip);