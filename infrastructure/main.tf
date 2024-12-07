# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

# Create an IAM role for the Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "github-weather-man-lambda-role-prod"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "weather-pipeline-lambda-role"
    Environment = "prod"
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}

# Add CloudWatch logging permissions
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create Lambda function
resource "aws_lambda_function" "weather_pipeline" {
  filename         = "../deployment_package.zip"
  function_name    = "github-weather-man-lambda-prod"
  role            = aws_iam_role.lambda_role.arn
  handler         = "main.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  memory_size     = 256

  environment {
    variables = {
      DATABASE_URL = var.database_url
      NWS_OBSERVATION_API_TOKEN = var.nws_observation_api_token
      ENVIRONMENT = "prod"
    }
  }

  tags = {
    Name        = "weather-pipeline"
    Environment = "prod"
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}

# Allow EventBridge to invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather_pipeline.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.hourly.arn
}

# Create CloudWatch Event rule (runs at the start of every hour)
resource "aws_cloudwatch_event_rule" "hourly" {
  name                = "hourly-weather-pipeline-${terraform.workspace}"
  description         = "Triggers weather pipeline at the start of every hour"
  schedule_expression = "cron(0 * * * ? *)"  # Run at minute 0 of every hour

  tags = {
    Name        = "weather-pipeline-trigger"
    Environment = terraform.workspace
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}

# Set Lambda as target for CloudWatch Event
resource "aws_cloudwatch_event_target" "weather_pipeline_target" {
  rule      = aws_cloudwatch_event_rule.hourly.name
  target_id = "WeatherPipeline"
  arn       = aws_lambda_function.weather_pipeline.arn
}

# Create CloudWatch Log Group with retention
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.weather_pipeline.function_name}"
  retention_in_days = 14  # Adjust retention as needed

  tags = {
    Name        = "weather-pipeline-logs"
    Environment = terraform.workspace
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}

# Create SNS Topic for notifications
resource "aws_sns_topic" "lambda_alerts" {
  name = "github-weather-man-alerts-prod"
  
  tags = {
    Name        = "weather-pipeline-alerts"
    Environment = terraform.workspace
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}

# Add email subscription
resource "aws_sns_topic_subscription" "lambda_alerts_email" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email  # We'll add this variable
}

# Add CloudWatch Alarm for Lambda errors
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "weather-pipeline-errors-${terraform.workspace}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace          = "AWS/Lambda"
  period             = "300"  # 5 minutes
  statistic          = "Sum"
  threshold          = "0"
  alarm_description  = "Monitors Lambda function errors"
  alarm_actions      = [aws_sns_topic.lambda_alerts.arn]
  
  dimensions = {
    FunctionName = aws_lambda_function.weather_pipeline.function_name
  }

  tags = {
    Name        = "weather-pipeline-alarm"
    Environment = terraform.workspace
    ManagedBy   = "terraform"
    Project     = "weather-man"
  }
}
