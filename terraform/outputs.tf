output "elastic_beanstalk_url" {
  value = aws_elastic_beanstalk_environment.my_env.endpoint_url
}
