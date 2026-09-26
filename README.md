# AWS EC2 Service Monitoring & Auto-Recovery

This project provides an automated solution for monitoring and recovering Linux services running on AWS EC2 instances. A Python-based monitoring agent runs inside a Docker container on a dedicated monitoring EC2 instance and uses AWS Systems Manager (SSM) to remotely check the status of services running on two monitored EC2 instances. When a service is active, the agent continues monitoring without taking any action. If a service becomes inactive, the agent automatically sends a restart command through SSM to restore the service.

The project uses AWS IAM roles to provide secure permissions without storing AWS access keys in the application. The monitored EC2 instances use the `AmazonSSMManagedInstanceCore` policy, while the monitoring instance uses permissions such as `ssm:SendCommand` and `ssm:GetCommandInvocation`. Environment variables are used to configure the AWS region, monitored EC2 instance IDs, and service name.

### Technologies

AWS EC2, AWS IAM, AWS Systems Manager (SSM), Python, Boto3, Docker, and Linux.

### Workflow

```text
EC2-3 Monitoring Server
        |
   Docker + Python
        |
       SSM
     /     \
    ▼       ▼
 EC2-1    EC2-2
 Service  Service
    |       |
    └───┬───┘
        |
   Auto Recovery
```

The monitoring agent continuously checks the configured services and automatically performs recovery when a service stops, providing a simple and secure approach to EC2 service monitoring and automation.

