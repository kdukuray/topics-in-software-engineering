provider "aws" {
  region     = "us-east-2"  # Set this to your desired AWS region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}
