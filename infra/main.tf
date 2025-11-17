terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"   # Paris
}


# 1. BUCKET S3 POUR STOCKER LES DOCUMENTS

resource "aws_s3_bucket" "documents_bucket" {
  bucket = "docdrop-documents-meriem-makhfouf"
}

# Optionnel : activer la protection contre suppression accidentelle
resource "aws_s3_bucket_versioning" "documents_bucket_versioning" {
  bucket = aws_s3_bucket.documents_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}


# 2. TABLE DYNAMODB POUR STOCKER LES METADONNEES

resource "aws_dynamodb_table" "documents_table" {
  name         = "docdrop-documents"
  billing_mode = "PAY_PER_REQUEST"   

  hash_key = "documentId"

  attribute {
    name = "documentId"
    type = "S"
  }
}
