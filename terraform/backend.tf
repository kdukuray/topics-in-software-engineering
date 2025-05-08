terraform {
  backend "s3" {
    bucket = "terraform-state-ledgerpay-gizmo1547"
    key    = "core/terraform.tfstate"
    region = "us-east-1"
  }
}