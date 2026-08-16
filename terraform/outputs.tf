output "cluster_name" {
  description = "Nom du cluster Kubernetes"
  value       = var.cluster_name
}

output "app_namespace" {
  description = "Namespace de l'application"
  value       = var.app_namespace
}

output "monitoring_namespace" {
  description = "Namespace de monitoring"
  value       = kubernetes_namespace.monitoring.metadata[0].name
}

output "argocd_namespace" {
  description = "Namespace ArgoCD"
  value       = kubernetes_namespace.argocd.metadata[0].name
}
