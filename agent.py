import logging
import os
import time

import boto3

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

region = os.getenv("AWS_REGION", "ap-south-2")

instance_ids = [
    instance_id.strip()
    for instance_id in os.getenv("INSTANCE_IDS", "").split(",")
    if instance_id.strip()
]

service_name = os.getenv("SERVICE_NAME", "httpd")

ssm = boto3.client(
    "ssm",
    region_name=region
)

while True:
    try:
        for instance_id in instance_ids:

            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": [
                        f"systemctl is-active {service_name}"
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

            logging.info(
                "%s: %s status = %s",
                instance_id,
                service_name,
                status
            )

            if status != "active":

                logging.warning(
                    "%s: %s stopped. Restarting...",
                    instance_id,
                    service_name
                )

                ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={
                        "commands": [
                            f"systemctl restart {service_name}"
                        ]
                    }
                )

                logging.info(
                    "%s: %s restart requested",
                    instance_id,
                    service_name
                )

    except Exception:
        logging.exception("Service monitoring failed")

    time.sleep(10)
