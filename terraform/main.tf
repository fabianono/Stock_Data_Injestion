terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "dezoomcamp-project2025" {
  name     = var.gcs_bucket_name
  location = var.location
}

resource "google_compute_instance" "default" {
  name         = var.gcs_vm_name
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-2004-focal-v20250213"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}

resource "google_dataproc_cluster" "simplecluster" {
  name   = var.gcs_dataproc_name
  region = var.region

  cluster_config {
    gce_cluster_config {
      zone = var.zone
    }
    software_config {
      image_version      = "2.2-debian12"
      optional_components = [
        "DOCKER"
      ]
    }

    // Master node configuration
    master_config {
      num_instances = 1
      machine_type  = "n2-standard-4"
    }

    // Worker node configuration (0 workers)
    worker_config {
      num_instances = 0
    }
  }
}
