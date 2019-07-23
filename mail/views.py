from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from hotel_management.settings import SENDGRID_API_KEY, DEFAULT_FROM_EMAIL


def send_mail(to_emails, subject, html_content, from_email=DEFAULT_FROM_EMAIL):

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
    )

    try:
        sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        response = {
            "body": response.body,
            "headers": response.headers,
            "status_code": response.status_code
        }
        return True, response
    except Exception as e:
        print(e)
        error_message = e
        return False, error_message
