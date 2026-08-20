resource "aws_dynamodb_table" "notifications" {
    name         = "sports-notifications"
    billing_mode = "PAY_PER_REQUEST"
    hash_key     = "eventId"

    attribute {
        name = "eventId"
        type = "S"
    }
}