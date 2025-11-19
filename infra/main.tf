terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# PROVIDER AWS CONFIGURÉ POUR MINIO (LOCAL)

provider "aws" {
  region = "us-east-1"

  # Identifiants MinIO 
  access_key = "minioadmin"
  secret_key = "minioadmin"

  # On désactive les vérifications AWS réelles
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Important pour MinIO (style d’URL /bucket/objet)
  s3_use_path_style = true

  # le service S3 pointe vers MinIO en local
  endpoints {
    s3 = "http://localhost:9000"
  }
}


# 1. BUCKET S3 POUR STOCKER LES DOCUMENTS
#    (créé dans MinIO)


resource "aws_s3_bucket" "documents_bucket" {
  bucket = "docdrop-documents-meriem-makhfouf"
}

# Optionnel : activer la protection / versioning
resource "aws_s3_bucket_versioning" "documents_bucket_versioning" {
  bucket = aws_s3_bucket.documents_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}


