resource "aws_elastic_beanstalk_application" "my_app" {
  name        = "my-django-app"
  description = "Django app deployed with Terraform"
}

resource "aws_elastic_beanstalk_environment" "my_env" {
  name                = "my-django-env"
  application         = aws_elastic_beanstalk_application.my_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.1 running Python 3.9"

  setting {
    name      = "IamInstanceProfile"
    namespace = "aws:autoscaling:launchconfiguration"
    value     = "aws-elasticbeanstalk-ec2-role"
  }

  tags = {
    Name = "my-django-env"
  }

  wait_for_ready_timeout = "20m"
}
