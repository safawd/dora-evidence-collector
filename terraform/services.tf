# Service Registry (Eureka)
resource "kubernetes_deployment" "service_registry" {
  metadata {
    name      = "service-registry"
    namespace = var.app_namespace
    labels = {
      app        = "service-registry"
      managed-by = "terraform"
    }
  }
  spec {
    replicas = var.replica_count
    selector {
      match_labels = {
        app = "service-registry"
      }
    }
    template {
      metadata {
        labels = {
          app = "service-registry"
        }
      }
      spec {
        container {
          name              = "service-registry"
          image             = "service-registry"
          image_pull_policy = "Never"
          port {
            container_port = 8761
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "service_registry" {
  metadata {
    name      = "service-registry"
    namespace = var.app_namespace
  }
  spec {
    selector = {
      app = "service-registry"
    }
    port {
      port        = 8761
      target_port = 8761
    }
  }
}

# API Gateway
resource "kubernetes_deployment" "api_gateway" {
  metadata {
    name      = "api-gateway"
    namespace = var.app_namespace
    labels = {
      app        = "api-gateway"
      managed-by = "terraform"
    }
  }
  spec {
    replicas = var.replica_count
    selector {
      match_labels = {
        app = "api-gateway"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-gateway"
        }
      }
      spec {
        container {
          name              = "api-gateway"
          image             = "api-gateway"
          image_pull_policy = "Never"
          port {
            container_port = 8080
          }
          env {
            name  = "EUREKA_HOST"
            value = "service-registry"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_gateway" {
  metadata {
    name      = "api-gateway"
    namespace = var.app_namespace
  }
  spec {
    selector = {
      app = "api-gateway"
    }
    type = "NodePort"
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
