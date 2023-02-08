variable "region" {
    type = string
    default = "us-east-1" 
}

variable "lambda_names"{
    type = list
    default=["ingestion_lambda","uploading_lambda","aggregation_lambda"]
}

variable "dynamo-table-name"{
    type = string
    default = "weather-dynamodb-table"
}