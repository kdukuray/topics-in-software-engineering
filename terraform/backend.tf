terraform {
  backend "s3" {
    bucket = "terraform-state-ledgerpay-adama" 
    key    = "core/terraform.tfstate"
    region = "us-east-2"
  }
}