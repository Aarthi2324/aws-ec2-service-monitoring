import logging
import time

import boto3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

region = "ap-south-2"

# Apache servers
instance_ids = [
    "i-0b59cc3009d067172",  # Apache Server 1
    "i-090de2cdc55f2bb35",  # Apache Server 2
]

ssm = boto3.client(
    "ssm",
    region_name=region
)


def check_httpd(instance_id):
    try:
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "systemctl is-active httpd"
                ]
            }
        )

        command_id = response["Command"]["CommandId"]

        time.sleep(2)

        result = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )

        status = result.get(
            "StandardOutputContent",
            ""
        ).strip()

        if status == "active":

            logging.info(
                "%s: Apache is running",
                instance_id
            )

        else:

            logging.warning(
                "%s: Apache is DOWN. Restarting...",
                instance_id
            )

            restart_httpd(instance_id)

    except Exception:
        logging.exception(
            "Apache check failed for %s",
            instance_id
        )


def restart_httpd(instance_id):

    try:

        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "systemctl restart httpd"
                ]
            }
        )

        command_id = response["Command"]["CommandId"]

        logging.warning(
            "%s: Apache restart requested. Command ID: %s",
            instance_id,
            command_id
        )

    except Exception:

        logging.exception(
            "Failed to restart Apache on %s",
            instance_id
        )


while True:

    for instance_id in instance_ids:

        check_httpd(instance_id)

    time.sleep(10)
