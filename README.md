# Weather-Man: Automated Weather Data Collection and Analysis ☀️☁️

Weather-Man is an automated pipeline designed to fetch, store, and analyze weather data from the National Weather Service (NWS) API. It supports multiple U.S. locations and seamlessly integrates with cloud infrastructure for efficient and scalable operations.

## Features ✨

- **Automated Data Collection**: Fetches hourly forecast and observation data from the NWS API.
- **Multi-Location Support**: Configurable locations to monitor weather trends across the U.S.
- **Data Storage**: Efficiently stores forecast and observation data for historical analysis.
- **Error Monitoring and Alerts**: Provides robust monitoring with alerts via email for quick issue resolution.
- **Serverless Architecture**: Built with AWS Lambda for cost-effective scalability.
- **Infrastructure as Code**: Entire infrastructure is managed using Terraform for consistent deployments.

---

## Setup Guide 🚀

### Prerequisites

To get started, ensure you have the following:

1. **AWS Account**: Ensure appropriate permissions for Lambda, EventBridge, CloudWatch, and S3.
2. **Terraform**: Installed locally for infrastructure setup.
3. **Python 3.9**: Required for running the application.
4. **PostgreSQL Database**: A database instance for storing weather data.
5. **NWS API Token**: Required to access the National Weather Service API.

### Environment Variables

Set the following environment variables in your `.env` file or system:

```
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<database>
NWS_OBSERVATION_API_TOKEN=<your_token_here>
AWS_ACCESS_KEY_ID=<your_aws_access_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_key>
ALERT_EMAIL=<your_alert_email>
```

---

### Deployment Steps

1. **Clone the Repository**:

```bash
git clone https://github.com/yourusername/weather-pipeline.git
cd weather-pipeline
```

2. **Initialize Terraform**:

```bash
cd infrastructure
terraform init
```

3. **Create Deployment Package**:

```bash
mkdir -p package
pip install -r requirements.txt -t package/
cp -r src/ package/
zip -r deployment_package.zip package/
```

4. **Deploy Infrastructure**:

```bash
cd infrastructure
terraform plan
terraform apply
```

---

## Libraries and Technologies Used 🔧

### Core Libraries and Frameworks

- **Python 3.9**: Core programming language.
- **SQLAlchemy (Async)**: Database ORM for handling PostgreSQL.
- **Asyncio**: Enables asynchronous operations.
- **Nest-Asyncio**: Enables async support in environments like Jupyter.

### AWS Services

- **Lambda**: Serverless compute for running Python code.
- **EventBridge**: Schedules hourly weather data collection.
- **CloudWatch**: Monitors infrastructure and application performance.
- **SNS**: Sends alerts and notifications.
- **S3**: Stores Terraform state.
- **IAM**: Manages permissions and security.

### Infrastructure Management

- **Terraform**: Used to define and manage the cloud infrastructure.

---

## Contributing

We welcome contributions! Feel free to fork the repository and submit a pull request with your enhancements or fixes.

---
