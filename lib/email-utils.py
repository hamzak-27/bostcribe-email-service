import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration
EMAIL_ADDRESS = "hello@botscribe.info"  # Your Google Workspace email
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Get from environment variable
ADMIN_EMAILS = ["ihamzakhan89@gmail.com", "sondeadeeb@gmail.com"]

def send_email(subject, html_content, recipients, reply_to=None):
    """Send an email to the specified recipients."""
    if not EMAIL_PASSWORD:
        return {"success": False, "message": "Email password not configured"}
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_ADDRESS
    message["To"] = ", ".join(recipients)
    
    if reply_to:
        message["Reply-To"] = reply_to
    
    # Add HTML content
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    
    # Create secure connection and send email
    try:
        # For Google Workspace, use smtp.gmail.com
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipients, message.as_string())
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"success": False, "message": str(e)}