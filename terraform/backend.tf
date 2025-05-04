terraform {
  backend "s3" {
    bucket = "terraform-state-ledgerpay-diakitejunior1"  # Use your actual S3 bucket name
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}
