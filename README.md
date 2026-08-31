# sports-reminder

AWS-hosted service that sends reminders for close games of specified teams.

## Overview

This repository contains a small AWS Lambda-based system and Terraform configuration
to deploy it. The Lambda function notifies users about close games for tracked teams.

## Repository layout

- `lambda.py` - convenience script (root) for local invocation or quick reference.
- `lambda_package/` - packaged Lambda runtime (dependencies and function code).
- `terraform/` - Terraform configuration to provision the Lambda, DynamoDB, EventBridge rules, and IAM resources.

Key Terraform files:
- `archive_file.tf` - prepares the Lambda deployment artifact
- `lambda.tf` - Lambda function and associated resources
- `dynamodb.tf` - persistence for tracked teams and reminder state
- `eventbridge.tf` - scheduling/event rules
- `iam.tf` - IAM roles and policies

## Requirements

- Python 3.8+ (for packaging or local testing)
- Terraform 1.0+
- An AWS account with credentials configured (see `aws configure`)

The repository includes a vendored `lambda_package/` folder so you can deploy without installing dependencies locally.

## Deploying

1. From the project root, create the Lambda deployment archive (Terraform may also do this automatically):

```bash
cd terraform
# If the repo's archive_file.tf uses a local path, ensure lambda_package is zipped as expected
zip -r ../lambda.zip ../lambda_package
```

2. Initialize and apply Terraform (confirm changes):

```bash
cd terraform
terraform init
terraform plan -out plan.tfplan
terraform apply "plan.tfplan"
```

3. After apply completes, the Lambda and supporting resources will be created in your AWS account.

## Configuration

- Edit `terraform/terraform.tfvars` to set `email_address` — the email address that will receive reminders. No other values in `terraform.tfvars` need to be modified for a basic deployment.

Example `terraform/terraform.tfvars`:

```hcl
email_address = "you@example.com"
```

Do not commit production email addresses or secrets to source control; use a secure mechanism for sensitive values when possible.

## Local testing

You can invoke the Lambda handler locally using the packaged `lambda_package` and `lambda.py` helper. Example:

```bash
python lambda.py
```

Or invoke the deployed function using AWS CLI:

```bash
aws lambda invoke --function-name <function-name> --payload '{}' response.json
cat response.json
```

## License

This project is licensed under the terms in the `LICENSE` file.

