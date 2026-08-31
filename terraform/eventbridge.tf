# 2 PM - 11:59 PM Eastern
resource "aws_cloudwatch_event_rule" "score_checker_evening" {
  name                = "sports-checker-evening"
  description         = "Checks scores from 2 PM to midnight Eastern"
  schedule_expression = "cron(* 18-23 ? * * *)"
}

# 12 AM - 1 AM Eastern
resource "aws_cloudwatch_event_rule" "score_checker_night" {
  name                = "sports-checker-night"
  description         = "Checks scores from midnight to 1 AM Eastern"
  schedule_expression = "cron(* 0-6 ? * * *)"
}

resource "aws_cloudwatch_event_target" "score_checker_evening" {
  rule = aws_cloudwatch_event_rule.score_checker_evening.name
  arn  = aws_lambda_function.score_checker.arn
}

resource "aws_cloudwatch_event_target" "score_checker_night" {
  rule = aws_cloudwatch_event_rule.score_checker_night.name
  arn  = aws_lambda_function.score_checker.arn
}

resource "aws_lambda_permission" "allow_eventbridge_evening" {
  statement_id  = "AllowExecutionFromEventBridgeEvening"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.score_checker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.score_checker_evening.arn
}

resource "aws_lambda_permission" "allow_eventbridge_night" {
  statement_id  = "AllowExecutionFromEventBridgeNight"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.score_checker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.score_checker_night.arn
}
