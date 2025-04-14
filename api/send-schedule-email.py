from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.email_utils import send_email, ADMIN_EMAILS

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            name = data.get('name')
            email = data.get('email')
            date = data.get('date')
            time = data.get('time')
            phone = data.get('phone', "Not provided")
            
            # Validate required fields
            if not all([name, email, date, time]):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Missing required fields"}).encode())
                return
            
            # Format the date
            formatted_date = datetime.fromisoformat(date.replace('Z', '+00:00')).strftime("%A, %B %d, %Y")
            
            # Email to admins
            admin_subject = f"New Meeting Request: {name}"
            admin_html = f"""
            <h1>New Meeting Request</h1>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Date:</strong> {formatted_date}</p>
            <p><strong>Time:</strong> {time}</p>
            """
            
            admin_result = send_email(admin_subject, admin_html, ADMIN_EMAILS, reply_to=email)
            
            # Email to client
            client_subject = "Meeting Request Confirmation - BotScribe"
            client_html = f"""
            <h1>Meeting Request Confirmation</h1>
            <p>Dear {name},</p>
            <p>Thank you for scheduling a meeting with BotScribe. We have received your request for:</p>
            <p><strong>Date:</strong> {formatted_date}</p>
            <p><strong>Time:</strong> {time}</p>
            <p>Our team will review your request and confirm the meeting shortly.</p>
            <p>If you need to make any changes, please contact us at hello@botscribe.info.</p>
            <p>Best regards,<br>The BotScribe Team</p>
            """
            
            client_result = send_email(client_subject, client_html, [email])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Meeting scheduled successfully! We've sent you a confirmation email."}).encode())
            
        except Exception as e:
            print(f"Error scheduling meeting: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Failed to schedule meeting. Please try again or contact us directly."}).encode())