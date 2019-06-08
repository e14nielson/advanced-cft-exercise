#!/bin/bash
region="us-west-2"
stack_name="advanced"
package="package-template.yaml"
deploy_profile="mine"
templates_bucket="cft-deployments"

taskcat -c ci/taskcat.yml -l -P mine
echo ""
echo "Building deployment package ${package} for stack ${stack_name}"
echo "---"
aws cloudformation package \
  --profile ${deploy_profile} \
  --region ${region} \
  --template-file templates/main.yaml \
  --s3-bucket ${templates_bucket} \
  --s3-prefix ${stack_name} \
  --output-template-file ${package}

tags="Team=DivvyDataTeam"
params="ClassB=0"
capabilities="CAPABILITY_NAMED_IAM"
echo ""
echo "Deploying package ${package} for stack ${stack_name}"
echo "---"
aws cloudformation deploy \
    --profile ${deploy_profile} \
    --region ${region} \
    --template-file ${package} \
    --stack-name ${stack_name} \
    --s3-bucket ${templates_bucket} \
    --s3-prefix ${stack_name} \
    --parameter-overrides ${params} \
    --capabilities ${capabilities} \
    --tags ${tags}
rm -rf ${package}