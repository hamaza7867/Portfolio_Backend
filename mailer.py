import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

class Mailer:
    def send_report(self, user_name, user_email, project_type, budget_est, chat_summary):
        params = {
            "from": "Portfolio AI <onboarding@resend.dev>",
            "to": "Hamaza7867@gmail.com",
            "subject": f"New Project Inquiry from {user_name}",
            "html": f"""
                <div style="font-family: sans-serif; padding: 20px; background: #0A0A0B; color: #E5E7EB; border-radius: 20px; border: 1px solid #00F5D4;">
                    <h1 style="color: #00F5D4;">New Project Lead</h1>
                    <p><strong>Client Name:</strong> {user_name}</p>
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Estimated Project Type:</strong> {project_type}</p>
                    <p><strong>Estimated Budget:</strong> {budget_est}</p>
                    <hr style="border: 0.5px solid #2D2D30; margin: 20px 0;"/>
                    <h3 style="color: #BD93F9;">Chat Transcription / Summary:</h3>
                    <p style="white-space: pre-wrap; font-size: 14px; line-height: 1.6;">{chat_summary}</p>
                </div>
            """
        }
        
        try:
            r = resend.Emails.send(params)
            return r
        except Exception as e:
            print(f"Failed to send email: {e}")
            return None
