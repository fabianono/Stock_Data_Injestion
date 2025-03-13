variable "credentials" {
    description = "My Credentials"
    default     = "~/Desktop/DE_Zoomcamp_2025/Project/keys/sa_adminadmin.json"
}


variable "project" {
    description = "Project"
    default     = "dezoomcamp-project2025"
}

variable "region" {
    description = "Region"
    default     = "us-central1"
}

variable "location" {
    description = "Project Location"
    default     = "US"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    default     = "dezoomcamp_project2025"
}

variable "machine_type" {
    description = "VM Machine Type"
    default     = "e2-medium"
    }

variable "zone" {
    description = "zone"
    default = "us-central1-a"
}

variable "gcs_vm_name" {
    description = "VM machine name"
    default     = "dezoomcamp-project2025-vm"
}

variable "gcs_dataproc_name" {
    description = "Dataproc name"
    default     = "dezoomcamp-project2025-dataproc"
}