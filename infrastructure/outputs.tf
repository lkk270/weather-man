output "lambda_function_name" {
  description = "Name of the created Lambda function"
  value       = aws_lambda_function.weather_pipeline.function_name
}

output "lambda_function_arn" {
  description = "ARN of the created Lambda function"
  value       = aws_lambda_function.weather_pipeline.arn
}
