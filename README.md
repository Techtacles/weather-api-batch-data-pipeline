# weather-api-batch-data-pipeline
This is a full  event driven batch pipeline on AWS , deployed using Terraform.
<br>The architecture for this is shown below.

![architecture](https://user-images.githubusercontent.com/57522480/217503397-604e8046-377e-4612-a396-801492b94a7b.png)
<br>
### PROCESSES
This project makes use of three lambda functions. The first lambda function(ingestion_lambda.py) extracts the weather information from an API every hour, scheduled using AWS cloud watch events.
The architecture flow diagram for this is shown below.

<img width="613" alt="ingestion_lambda" src="https://user-images.githubusercontent.com/57522480/217504067-78a9ef2a-b84a-4ee5-92c3-7a7e6249b50f.png">
<br>
These events are then stored in a raw s3 bucket in JSON format. Transformations are done on this raw S3 bucket and the results are sent out to another S3 bucket in CSV format.<br><br>
The second lambda function (upload_lambda.py) receives events from the transformed bucket , processes it and sends the results to a DynamoDb table and an SNS topic.<br> The diagram for this is shown below
<img width="853" alt="upload_lambda" src="https://user-images.githubusercontent.com/57522480/217504784-1d217fd3-e068-4c63-9949-f4e26b3f4bed.png">
<br> An SQS queue is subscribed to the SNS topic and a third lambda function aggregates the messages of this on a daily basis.<br>
A redshift cluster is also queried on the Dynamodb table for visualization on AWS Quicksight.
<br>The visualization is shown below.<br><img width="1436" alt="Final viz" src="https://user-images.githubusercontent.com/57522480/217505077-2562bf6f-7706-4dd0-8ceb-cec971dad6a2.png">
<br>
The resources can be fired up by running the command <b>terraform plan <b> and <b>terraform apply</b>
