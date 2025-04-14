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
            subject = data.get('subject')
            message = data.get('message')
            
            # Validate required fields
            if not all([name, email, subject, message]):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Missing required fields"}).encode())
                return
            
            # Email to admins
            admin_subject = f"New Contact Form Submission: {subject}"
            admin_html = f"""
            <h1>New Contact Form Submission</h1>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            """
            
            admin_result = send_email(admin_subject, admin_html, ADMIN_EMAILS, reply_to=email)
            
            # Email to client
            client_subject = "We've Received Your Message - BotScribe"
            client_html = f"""
            <h1>Thank You for Contacting Us</h1>
            <p>Dear {name},</p>
            <p>We have received your message regarding "{subject}". Our team will review it and get back to you as soon as possible.</p>
            <p>If you have any urgent matters, please contact us directly at hello@botscribe.info.</p>
            <p>Best regards,<br>The BotScribe Team</p>
            """
            
            client_result = send_email(client_subject, client_html, [email])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Message sent successfully! We'll get back to you soon."}).encode())
            
        except Exception as e:
            print(f"Error processing contact form: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "message": "Failed to send message. Please try again or contact us directly."}).encode())