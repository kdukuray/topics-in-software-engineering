resource "aws_elastic_beanstalk_application" "application" {
  name = "ledgerpay"
}

resource "aws_elastic_beanstalk_environment" "environment" {
  name                = "Django-environment"
  cname_prefix        = "gizmo1547"
  application         = aws_elastic_beanstalk_application.application.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.1 running Python 3.11"

  //platform_arn        = "arn:aws:elasticbeanstalk:us-east-1::platform/Python 3.11 running on 64bit Amazon Linux 2023/4.0.0"
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  }
}