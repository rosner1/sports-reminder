data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_package"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "score_checker" {
    function_name = "score-checker"
    runtime = "python3.13"
    handler = "lambda.lambda_handler"

    filename = data.archive_file.lambda_zip.output_path
    source_code_hash = data.archive_file.lambda_zip.output_base64sha256

    role = aws_iam_role.lambda_role.arn
    timeout = 30
    memory_size = 256

    environment {
        variables = {
            TABLE_NAME = aws_dynamodb_table.notifications.name,
            EMAIL_ADDRESS = var.email_address,
            WNBA_ID = 5,
            NBA_ID = 11
        }
    }
}