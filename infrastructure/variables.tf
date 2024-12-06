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

variable "nws_token" {
  description = "NWS Observation API token"
  type        = string
  sensitive   = true
}
