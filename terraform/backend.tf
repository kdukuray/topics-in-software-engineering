terraform {
  backend "s3" {
    # my bucket name in aws s3
    bucket = "terraform-state-ledgerpay-kdukuray-assignment-3"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}
