zip -r "flaskbb_deploy-081273d-20250429145730.zip" ./flaskbb ./.ebextensions wsgi.py setup.py setup.cfg requirements.txt flaskbb.cfg celery_worker.py

aws s3 cp "flaskbb_deploy-081273d-20250429145730.zip" s3://adama1945-ledgerpay

aws elasticbeanstalk create-application-version --application-name flaskbb --source-bundle S3Bucket="adama1945-ledgerpay",S3Key="flaskbb_deploy-081273d-20250429145730.zip" --version-label "ver-$1" --description "file permissions" --region "us-east-2"

aws elasticbeanstalk update-environment --environment-name flaskbb-environment --version-label "ver-$1" --region "us-east-2"
#ASSIGMNENT FI