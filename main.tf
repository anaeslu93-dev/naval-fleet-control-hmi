# 1. DEFINICIÓN DE PROVEEDORES
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

# 2. CONFIGURACIÓN DEL PROVEEDOR
provider "docker" {
  host = "npipe:////./pipe/dockerDesktopLinuxEngine"
}

# 3. CREACIÓN DEL VOLUMEN DE ALMACENAMIENTO AISLADO
resource "docker_volume" "db_volume" {
  name = "postgres_naval_data"
}

# 4. CREACIÓN DEL CONTENEDOR DE LA BASE DE DATOS SEGURA (CIS)
resource "docker_container" "postgres_container" {
  name  = "naval_fleet_postgres_db"
  image = "postgres:17-alpine"

  env = [
    "POSTGRES_USER=ana_admin",
    "POSTGRES_PASSWORD=password_proyecto_123",
    "POSTGRES_DB=naval_fleet_db"
  ]

  ports {
    internal = 5432
    external = 5433
  }

  volumes {
    volume_name    = docker_volume.db_volume.name
    container_path = "/var/lib/postgresql/data"
  }

  # --- HARDENING CIS EN IACT (TERRAFORM) ---
  user = "70:70"
  
  security_opts = [
    "no-new-privileges:true"
  ]

  read_only = true

  tmpfs = {
    "/run/postgresql" = "mode=777"
    "/tmp"            = "mode=777"
  }
}