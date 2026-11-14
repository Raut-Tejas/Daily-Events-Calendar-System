
import os

from dotenv import load_dotenv
from services.email_service import send_email

load_dotenv()

recipient = os.getenv("SES_TEST_RECIPIENT")

if not recipient:
    print("Error: SES_TEST_RECIPIENT is missing from .env")

else:
    result = send_email(
        to_email=recipient,
        subject="Campus Event Notification - Test Email",
        text_body="""
Hello Student,

This is a test email from the Cloud-Based Campus Event
Notification System.

AWS SES email integration is being tested successfully.

Regards,
Campus Event Notification System
        """,
        html_body="""
        <html>
            <body>
                <h2>Campus Event Notification System</h2>
                <p>Hello Student,</p>
                <p>
                    This is a test email sent through
                    <strong>Amazon SES</strong>.
                </p>
                <p>AWS SES email integration test.</p>
                <p>Regards,<br>Campus Event Notification System</p>
            </body>
        </html>
        """
    )

    if result["success"]:
        print("Email submitted successfully!")
        print("Message ID:", result["message_id"])
    else:
        print("Email sending failed!")
        print("Error:", result["message"])
