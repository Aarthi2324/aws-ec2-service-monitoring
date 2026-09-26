# AWS EC2 Service Monitoring & Auto-Recovery

## Overview

Automated monitoring and recovery of services running on AWS EC2 instances using **Python, Boto3, AWS Systems Manager (SSM), Docker, and IAM**.

A dedicated monitoring EC2 instance runs a Dockerized Python agent that continuously checks service status on configured EC2 instances. If a service becomes inactive, the agent automatically triggers a restart through SSM.

## Architecture

```text
Monitoring EC2
      │
Docker + Python
      │
 Boto3 + SSM
      │
 ┌────┴────┐
 ▼         ▼
EC2-1     EC2-2
httpd     httpd
   │        │
   └─ Auto-Recovery
```

## Workflow

```text
Check Service
     ↓
Service Active?
  ↙       ↘
Yes        No
 ↓          ↓
Continue   SSM Restart
              ↓
        Service Restored
```

## Technologies

**AWS EC2 | AWS SSM | IAM | Python | Boto3 | Docker | Linux**

## Key Features

* Automated service health monitoring
* Automatic service recovery
* Secure IAM-based AWS access
* Dockerized monitoring agent
* Reduced manual intervention

## Docker

```bash
docker build -t service-monitor .
docker run -d --name service-monitor --env-file .env service-monitor
docker logs -f service-monitor
```

## Outcome

Demonstrates automated **service-level failure detection and recovery** using AWS services, Python automation, Docker, and Linux service management.
