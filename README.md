# Cloud Native Web Application for CI-CD pipeline.

## Overview
CSYE 6225: Network Structures and Cloud Computing involved a deep dive into the domain of cloud architecture on Google Cloud Platform utilizing [HashiCorp](https://www.linkedin.com/company/hashicorp/) Terraform. From setting up customized VPCs and subnets to managing dynamic instance groups and load balancers, each task presented a new learning opportunity.

Here’s a glimpse of the topics covered as a part of the course: 

🚀 **API Development**

- Developed a robust RESTful API using Spring Boot and Hibernate.
- Utilized REST Assured for comprehensive integration testing, ensuring reliability and performance.

🔧 **Custom Compute Image Creation**

- Crafted custom compute engine images using [HashiCorp](https://www.linkedin.com/company/hashicorp/) Packer.
- Implemented systemd service files for smooth application startup.

🌐 **Secure Infrastructure Setup**

- Established secure VPCs, subnets, and CloudSQL instances.
- Enabled VPC peering and private service access for enhanced security.

🔍 **Enhanced Observability**

- Leveraged Cloud DNS for seamless domain resolution.
- Configured Ops Agent for streamlined application logging, ensuring observability and troubleshooting ease.

📨 **Automated Email Verification**

- Orchestrated message publication to Google Pub/Sub topics.
- Triggered Cloud Functions for automated email verification using [Sinch Mailgun](https://www.linkedin.com/company/mailgun/).

⚙️ **Infrastructure Orchestration with Terraform**

- Engineered compute instance templates, managed instance groups, and load balancers.
- Implemented SSL certificates managed by GCP.
- Enabled automated rolling updates on merge to ensure seamless deployment.

## Infrastructure Architecture

![Architecture Diagram](CSYE6225_architecture_diagram.drawio.svg)


## Terraform code Repository 
https://github.com/siddharthdashcsye6225/tf-gcp-infra

## Serverless Function Repository 

https://github.com/siddharthdashcsye6225/serverless

----------------------------------------------------
# Below is a detailed breakdown of each assignment
-----------------------------------------------------

# Assignment 9: Continuous Deployment with GitHub Actions

### Overview
The objective of Assignment 9 was to establish continuous deployment for your infrastructure using GitHub Actions. This process automates the deployment of new instance templates and performs rolling updates on your GCP environment.

### Steps Taken
1. **Image Creation with Packer**:
   - Configured GitHub Actions to trigger Packer to build a new custom image for your infrastructure.

2. **Update Instance Template**:
   - Utilized `gcloud` commands within GitHub Actions to set the new custom image as the source for an updated instance template.
   
3. **Perform Rolling Update**:
   - Leveraged `gcloud` commands to initiate a rolling update using the updated instance template.
   - Configured the GitHub Action to wait until the rolling update process is complete before proceeding.

### Automation Workflow
- **GitHub Actions Integration**:
  - Integrated GitHub Actions to automate the deployment process triggered by Packer image creation.

- **Instance Template Management**:
  - Dynamically updated the instance template with the newly created custom image using `gcloud` commands.

- **Rolling Update Execution**:
  - Initiated a rolling update on the managed instance group to apply the changes using the updated instance template.

### Benefits and Outcomes
- **Efficient Deployment**: Enabled continuous deployment of infrastructure changes triggered by Packer image builds.
- **Automated Updates**: Streamlined the process of updating instance templates and performing rolling updates using GitHub Actions and `gcloud` commands.
- **Improved Deployment Workflow**: Enhanced reliability and scalability of the deployment workflow by automating critical tasks.


# Assignment 8: Autoscaling Web Application and Load Balancer Setup

## Overview

Implemented autoscaling for our web application and set up a load balancer to enhance its reliability and scalability. Following the assignment requirements, I performed the following tasks:

## Autoscaling Web Application

1. **Created Regional Compute Instance Template**:
   - Utilized the Google Cloud Console to create a regional compute instance template matching our current VM deployment configuration. This template was designed to replace the existing compute instance resource managed by Terraform.

2. **Configured Compute Health Check**:
   - Created a compute health check in the Google Cloud Console to monitor the `/healthz` endpoint of our web application. This health check is crucial for ensuring the availability and health of our application instances.

3. **Set Up Compute Autoscaler**:
   - Configured a compute autoscaler resource to automatically scale up the number of instances when CPU usage exceeds 5%. This autoscaler helps maintain optimal performance and availability during periods of increased traffic or workload.

4. **Created Regional Compute Instance Group Manager**:
   - Established a regional compute instance group manager using the Google Cloud Console. This manager incorporates the regional compute instance template and the compute autoscaler, ensuring efficient management and scaling of our application instances.

5. **Updated Firewall Ingress Rules**:
   - Revised firewall ingress rules to restrict access to the endpoints on virtual machines. Only the load balancer is permitted to access these endpoints, enhancing security by preventing external access via public IPs.

## Load Balancer

1. **Deployed External Application Load Balancer**:
   - Created an external Application Load Balancer supporting HTTPS protocol only. This load balancer efficiently distributes incoming traffic to our application instances, enhancing performance and reliability.

2. **Configured SSL Certificates**:
   - Utilized Google-managed SSL certificates to enable HTTPS encryption for secure communication between clients and our web application. This ensures the confidentiality and integrity of data transmitted over the network.

3. **Enabled HTTPS Access**:
   - Ensured that the APIs are accessible using HTTPS protocol on the default port 443, providing a secure communication channel for clients accessing our web application.

4. **Updated DNS Records**:
   - Updated DNS records to point the domain to the IP address of the load balancer. This ensures that users can access our web application securely via the load balancer's HTTPS endpoint.

## Implementation Steps

1. Created Compute Instance Template on Google Cloud Console.
2. Configured Compute Health Check on Google Cloud Console, determining the required parameters for monitoring the `/healthz` endpoint.
3. Set up Autoscaler Resource to automatically scale up instances based on CPU usage.
4. Created Compute Instance Group Manager on Google Cloud Console, incorporating the compute instance template and autoscaler.
5. Deployed Load Balancer with HTTPS Protocol to efficiently distribute traffic and provide HTTPS encryption.
6. Configured SSL Certificates using Google-managed certificates for secure communication.
7. Ensured APIs are accessible using HTTPS protocol on default port 443 for enhanced security.
8. Updated DNS records to point the domain to the load balancer's IP address, enabling secure access to the web application.

By completing these tasks, our web application is now equipped with autoscaling capabilities and secured behind a load balancer, ensuring reliability, scalability, and data protection.


# Assignment 7: Cloud Pub/Sub, Email Verification, and User Authorization
### Overview
Assignment 7 focused on implementing cloud pub/sub messaging for email verification and user authorization workflows within the web application.

### Steps Taken
1. **Cloud Pub/Sub Integration**: Configured cloud pub/sub to send messages triggering subsequent actions, such as email verification.
2. **Email Sending Functionality**: Developed a cloud function triggered by pub/sub messages to send an email with a verification link to newly created users.
3. **Token Tracking**: Implemented a new table to track tokens generated during email sending, ensuring verification within a specific timeframe (e.g., 2 minutes) to prevent link expiration.

### Benefits and Outcomes
- **Automated Email Verification**: Enabled automated email verification for newly registered users, enhancing user authentication and security.
- **Event-Driven Architecture**: Adopted an event-driven architecture using cloud pub/sub, improving application responsiveness and scalability.

# Assignment 6: Implementing Comprehensive Logging for WebApp with GCP Ops Agent
## Overview
The code snippet provided implements comprehensive logging functionality for a web application using the Winston logging library. The goal is to seamlessly integrate logging into Google Cloud Logging services, enabling efficient monitoring and troubleshooting.

## Code Elaboration
### Logger Configuration
- **Logger Setup**: The `configure_logging()` function sets up the logger with two handlers: a console handler and a file handler.
- **Console Handler**: Sends log messages to the terminal for real-time visibility during application execution.
- **File Handler**: Writes log messages to a file, facilitating long-term storage and analysis.
- **Formatter**: Utilizes a custom JSON formatter (`StackdriverJsonFormatter`) to format log messages in JSON format, enhancing compatibility with Google Cloud Logging.

### Custom JSON Formatter
- **`StackdriverJsonFormatter` Class**: Overrides the default behavior of the `JsonFormatter` class to add custom fields to log records, such as `severity` and `time`.
- **`process_log_record()` Method**: Modifies the log record to include the `severity` field based on the log level.
- **`add_fields()` Method**: Adds additional fields to log records, including the current timestamp.

### Log File Path Resolution
- Determines the appropriate log file path based on the execution environment:
  - If running locally or in a GitHub Actions environment, logs are written to a local file (`myapp_local.log`).
  - If running in a production environment, logs are written to `/var/log/webapp/webapp.log`.

## Benefits and Outcomes
- **Efficient Monitoring**: Enables real-time monitoring of application logs through both console output and log files.
- **Compatibility with Google Cloud Logging**: Log messages are formatted in JSON format, ensuring compatibility with Google Cloud Logging services for centralized logging and analysis.
- **Environment Flexibility**: The logger adapts to different execution environments, allowing seamless transition between local development and production environments.

## Source
- **Class Overwrite**: The `StackdriverJsonFormatter` class overwrites the `JsonFormatter` class. Source: [Engineering Ziff Media](https://engineering.ziffmedia.com/formatting-python-logs-for-stackdriver-5a5ddd80761c)

With this comprehensive logging setup, the web application is well-equipped for efficient monitoring, troubleshooting, and scalability in a DevOps environment.


# Assignment 5: Create private Cloud SQL and connect the instance using PSC
## Overview
This assignment delved deeper into Terraform usage, with a primary focus on infrastructure updates. Our goal was to implement Cloud SQL and establish private service connectivity for secure database access.

As part of the process, we streamlined the web application setup by removing the local database installation step during image creation. This optimization enhances the efficiency and reliability of the infrastructure while ensuring seamless integration with cloud-based services.

# Assignment 4: Custom Image Creation with Packer
## Overview
# Custom Image Creation with Packer

## Overview
This document outlines the process of creating a custom image for deploying a web application using Packer. The base image utilized is CentOS Stream 8. The custom image includes all the necessary dependencies and configurations for seamless deployment of the web application.

## Packer Configuration
### `packer/` Directory
This directory contains the Packer configuration files required for building the custom image.

#### `packer.pkr.hcl`
This file specifies the Packer configuration for building the custom image. Here's an overview of the configuration:
- **Required Plugins**: Specifies the required Google Cloud Platform (GCP) plugin.
- **Variables**: Defines variables for project ID, PostgreSQL password, source image, zone, machine type, and SSH username.
- **Source Block**: Configures the Google Compute Engine source block with details such as project ID, source image, zone, instance name, disk size, disk type, SSH username, machine type, tags, and network.
- **Build Block**: Specifies the build steps, including provisioning files and executing shell commands to set up the environment, install dependencies, and configure the web application.
- **Provisioners**: Utilizes various provisioners such as `file` to copy files, and `shell` to execute shell commands for setting up the environment and configuring the web application.

## GitHub Actions Workflow
### `.github/workflows/` Directory
This directory contains the GitHub Actions workflow files responsible for validating the Packer template and building the custom image.

#### `packer-validate.yml`
This workflow validates the Packer template format and configuration before proceeding with the image build process. It performs the following tasks:
1. Installs Packer and Google Cloud Platform SDK.
2. Authenticates with GCP using service account credentials.
3. Checks the format of the Packer template using `packer fmt -check`.
4. Validates the Packer template using `packer validate`.

#### `packer-build.yml`
This workflow builds the custom image using Packer after merging changes into the main branch. It executes the following steps:
1. Installs dependencies and sets up the environment for Packer.
2. Authenticates with GCP using service account credentials.
3. Installs Packer and Google Cloud Platform SDK.
4. Validates the Packer template.
5. Builds the custom image using Packer.
6. Creates an instance template from the custom image.
7. Starts a rolling update for the managed instance group to apply the new image.

## Note
- Ensure that the necessary secrets and environment variables are configured in the GitHub repository settings for authentication with GCP and other required services.
- Verify network configurations and firewall rules in GCP to allow traffic to the web application port.
- Update the `gcp-credentials` secret to enable the GitHub Actions workflows to authenticate with GCP.

With these configurations and workflows in place, you can seamlessly create and deploy a custom image for your web application using Packer and GitHub Actions.


# Assignment 3: Integration Testing for Web Application
## Overview
# Integration Testing for FastAPI Application

## Overview
This document outlines the integration testing strategy for a FastAPI web application, covering both unit and integration tests. The aim is to ensure the reliability and functionality of the application by testing various scenarios including user creation, retrieval, and updating.

## Testing Approach
### Unit Tests
Unit tests focus on testing individual components or units of code in isolation. In the context of a FastAPI application, unit tests can be written for specific routes, models, or helper functions.

#### Test Scenario
- **Health Check Endpoint**: Verifies the health status of the application.

#### Dependencies
- **Testing Framework**: `pytest` for writing and executing unit tests.
- **HTTP Client**: `TestClient` from FastAPI to simulate HTTP requests.

#### Running Tests
- Execute unit tests using the command: `pytest csye6225project/csye6225/tests/test_basic.py`

### Integration Tests
Integration tests verify interactions between various components of the application, ensuring that different parts work together as expected. In the context of a FastAPI application, integration tests can cover scenarios such as user lifecycle management.

#### Test Scenarios
- **User Lifecycle**: Tests user creation, retrieval, and updating functionality.
  
#### Dependencies
- **Testing Framework**: `pytest` for writing and executing integration tests.
- **HTTP Client**: `TestClient` from FastAPI to simulate HTTP requests.
- **Database**: PostgreSQL database for storing user data.
- **Encryption**: `base64` for encoding user credentials.

#### Running Tests
- Execute integration tests using the command: `pytest csye6225project/csye6225/tests/test_integration.py`

## Continuous Integration (CI)
### GitHub Actions Workflow
To ensure the continuous integration of tests, GitHub Actions workflows have been set up to automatically trigger tests on pull requests to the main branch.

#### Unit Tests Workflow (tests.yml)
- **Trigger**: Executes on pull requests to the main branch.
- **Job**: Performs a health check of the database and runs unit tests.
- **Dependencies Installation**: Installs PostgreSQL and Python dependencies.
- **Testing**: Executes unit tests using `pytest`.

#### Integration Tests Workflow (integration_tests.yml)
- **Trigger**: Executes on pull requests to the main branch.
- **Job**: Performs a health check of the database and runs integration tests.
- **Dependencies Installation**: Installs PostgreSQL and Python dependencies.
- **Testing**: Executes integration tests using `pytest`.

### Conclusion
By employing unit and integration testing strategies along with continuous integration workflows, the FastAPI application ensures robustness and reliability, thereby enhancing the overall quality of the software product.

# Assignment 2: Enhancing Users API, Continuous Integration, and Git Setup

In this assignment, the primary objective is to expand the API functionality by introducing additional endpoints that facilitate the creation, retrieval, and modification of user data in the Postgres API. Concurrently, we are leveraging GitHub for project management and implementing continuous integration actions.

## Features

### Users Endpoints

- The Users endpoints encompass three fundamental operations: POST, GET, and PUT.
- Usernames are unique and are defined by email ID, ensuring that multiple users cannot share the same email ID.

#### Create User

- The POST API at /v1/user initiates the creation of a new user and provides relevant responses for different scenarios:
  - Responds with 400 for missing fields or an invalid body.
  - Responds with 409 if the username already exists.
  - Handles other potential errors with an internal server error (500).

#### Get self User

- The GET API at /v1/user/self verifies the presence of a basic authentication token through middleware.
  - If authorized, returns user data.
  - If unauthorized, sends an unauthorized message with a 400 status code.

#### Update self user

- The PUT API at /v1/user/self checks for the presence of updatable fields along with an authentication token.
  - If authorized, updates the user data accordingly.
  - If unauthorized, sends an unauthorized message with a 400 status code.

# Assignment 1: Building a Basic API with FASTApi, SQLAlchemy, and PostgreSQL

In this assignment, the goal is to create a simple API to test the connection to a local database. The project utilizes FASTApi, SQLAlchemy, and PostgreSQL to showcase the required functionality.

## Features

### Healthz Endpoint
- The API includes a `healthz` endpoint designed to perform a database connection test.
- To start database server use `Postgres` desktop app
- To verify the connection status, you can use the following curl request:
```bash
curl -vvvv http://localhost:8080/healthz
```
- This request returns either "OK" or "Service Unavailable" based on the connection status.
  
## Middleware Blocking Other HTTP Methods
- The healthz endpoint has been secured by middleware to allow only specific HTTP methods.
- To test this middleware, you can use the following curl requests:
  - PUT request:
  ```bash 
  curl -vvvv -X PUT http://localhost:8080/healthz
  ```
  - POST request:
  ```bash 
  curl -vvvv -X PUT http://localhost:8080/healthz
  ```
  - DELETE request:
  ```bash 
  curl -vvvv -X DELETE http://localhost:8080/healthz
  ```
  - PATCH request:
  ```bash 
  curl -vvvv -X PATCH http://localhost:8080/healthz
  ```
