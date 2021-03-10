output "dynamodb-table-name" {
  value = aws_dynamodb_table.scrumnest-dynamodb-table.name
}

output "dynamodb-table-arn" {
  value = aws_dynamodb_table.scrumnest-dynamodb-table.arn
}
