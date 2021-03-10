resource "aws_dynamodb_table" "scrumnest-dynamodb-table" {
  name           = "scrumnest_${terraform.workspace}"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "nestId"
  range_key      = "nestComponent"

  attribute {
    name = "nestId"
    type = "S"
  }

  attribute {
    name = "nestComponent"
    type = "S"
  }
}
