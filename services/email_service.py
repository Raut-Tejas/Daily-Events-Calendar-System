
import os

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# AWS SES Configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
SES_SENDER_EMAIL = os.getenv("SES_SENDER_EMAIL")


def get_ses_client():
    """
    Create an AWS SES client using credentials from .env.
    """

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS credentials are missing from the .env file."
        )

    return boto3.client(
        "ses",
        region_name=AWS_REGION,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )


def send_email(to_email, subject, text_body, html_body=None):
    """
    Send an email using Amazon Simple Email Service (SES).

    Args:
        to_email: Recipient email address.
        subject: Email subject.
        text_body: Plain-text email content.
        html_body: Optional HTML email content.

    Returns:
        Dictionary containing success status and message details.
    """

    if not SES_SENDER_EMAIL:
        return {
            "success": False,
            "message": "SES_SENDER_EMAIL is missing from .env"
        }

    if not to_email or not subject or not text_body:
        return {
            "success": False,
            "message": "Recipient, subject and text body are required."
        }

    try:
        client = get_ses_client()

        # Prepare email body
        message_body = {
            "Text": {
                "Data": text_body,
                "Charset": "UTF-8"
            }
        }

        if html_body:
            message_body["Html"] = {
                "Data": html_body,
                "Charset": "UTF-8"
            }

        # Send email through AWS SES
        response = client.send_email(
            Source=SES_SENDER_EMAIL,
            Destination={
                "ToAddresses": [to_email]
            },
            Message={
                "Subject": {
                    "Data": subject,
                    "Charset": "UTF-8"
                },
                "Body": message_body
            }
        )

        return {
            "success": True,
            "message_id": response.get("MessageId"),
            "message": "Email submitted successfully to Amazon SES."
        }

    except (ClientError, BotoCoreError, ValueError) as error:
        return {
            "success": False,
            "message": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "message": f"Unexpected email error: {error}"
        }
