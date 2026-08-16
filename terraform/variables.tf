variable "mysql_root_password" {
  description = "Mot de passe root MySQL"
  type        = string
  default     = ""
  sensitive   = true
}

variable "app_namespace" {
  description = "Namespace principal de l'application"
  type        = string
  default     = "default"
}

variable "cluster_name" {
  description = "Nom du cluster Kubernetes"
  type        = string
  default     = "dora-cluster"
}

variable "replica_count" {
  description = "Nombre de replicas par service"
  type        = number
  default     = 1
}
