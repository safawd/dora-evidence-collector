resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
    labels = {
      environment = "production"
      managed-by  = "terraform"
      project     = "dora-pfe"
    }
  }
}

resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
    labels = {
      environment = "production"
      managed-by  = "terraform"
      project     = "dora-pfe"
    }
  }
}
