# data "archive_file" "lambda_zip" {
#   type        = "zip"
#   source_file = "../lambda.py"
#   output_path = "${path.module}/lambda.zip"
# }