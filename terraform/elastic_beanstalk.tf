resource "aws_elastic_beanstalk_application" "django_app" {
  name        = "ledgerpay"
  description = "Elastic Beanstalk Application for Django App"
}

resource "aws_elastic_beanstalk_environment" "django_env" {
  name                = "ledgerpay-env"
  cname_prefix        =  "kdukurayledgerpayassignment3"
  application         = aws_elastic_beanstalk_application.django_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.1 running Python 3.11"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }
}
