terraform {
  required_version = ">= 1.6.0"
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.29" }
  }
}

variable "namespace" { type = string, default = "agents" }
variable "kubeconfig" { type = string, default = "~/.kube/config", sensitive = true }
provider "kubernetes" { config_path = var.kubeconfig }

resource "kubernetes_namespace" "agents" {
  metadata { name = var.namespace }
}

resource "kubernetes_secret" "agents" {
  metadata { name = "agents-secrets", namespace = kubernetes_namespace.agents.metadata[0].name }
  data = { LIVE_TRADING_ENABLED = "false" }
  type = "Opaque"
}
