resource "aws_lambda_function" "score_checker" {
    function_name = "score-checker"
    runtime = "python3.13"
    handler = "lambda_function.lambda_handler"
    filename = "lambda.zip"

    role = aws_iam_role.lambda_role.arn
    timeout = 30
    memory_size = 256

    environment {
        variables = {
            TABLE_NAME = aws_dynamodb_table.notifications.name
        }
    }
}