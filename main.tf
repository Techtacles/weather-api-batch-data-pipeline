provider "aws" {
  region = var.region
}


resource "aws_iam_role" "iam_for_lambda" {
  name = "aggregation_iam"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

resource "aws_lambda_function" "lambda_fn" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
   for_each = toset(var.lambda_names)
  function_name = each.value
  role          = aws_iam_role.iam_for_lambda.arn
  count=3
   environment {
    variables = {
      access_key="access_key"
      secret_key="secret_key"
      api_key="api_key"
    }
  }
}


resource "aws_glue_job" "glue_job" {
  name     = "weather-api-glue-job"
  role_arn = aws_iam_role.example.arn

  command {
    script_location = "<path to python script>"
  }
}


resource "aws_dynamodb_table" "dynamodb" {
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "table_hash_key"
  name             = var.dynamo-table-name

  attribute {
    name = "psf"
    type = "S"
  }

resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier = "weather-api-redshift"
  database_name      = "your_database_name"
  master_username    = "username"
  master_password    = "pass"
  node_type          = "dc1.large"
  cluster_type       = "single-node"
}

resource "aws_sns_topic" "sns_topic" {
  name = "weather-api-topic"
}

resource "aws_sqs_queue" "terraform_queue" {
  name                      = "weather-api-sqs-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
    maxReceiveCount     = 4
  })

  tags = {
    Environment = "production"
  }
}

resource "aws_sns_topic_subscription" "subscribe_sqs" {
  topic_arn = "your_topic_arn"
  protocol  = "sqs"
  endpoint  = "your_endpoint"
}