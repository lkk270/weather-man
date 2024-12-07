variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "database_url" {
  description = "PostgreSQL database connection URL"
  type        = string
  sensitive   = true  # This marks the variable as sensitive in logs
}

variable "nws_observation_api_token" {
  description = "NWS Observation API token"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email address for Lambda error notifications"
  type        = string
}

variable "force_update_value" {
  default = ""
  description = "A dynamic value to trigger a forced update for the Lambda function."
}