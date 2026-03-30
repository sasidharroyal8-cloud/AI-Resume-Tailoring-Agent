import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "recruiter@example.com")

def send_email(job, attachment_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Application: {job['title']} at {job['company']}"
        msg["From"] = EMAIL
        msg["To"] = RECIPIENT_EMAIL

        body = f"""
Subject: Application for {job['title']} Position

Dear Hiring Manager,

I am writing to express my interest in the {job['title']} position at {job['company']}.

Position Details:
- Job Title: {job['title']}
- Company: {job['company']}
- Job URL: {job['url']}

I have tailored my resume specifically for this role, highlighting my relevant experience and skills that align with your requirements. Please find my customized resume attached.

I would welcome the opportunity to discuss how my background and expertise can contribute to your team's success.

Best regards,
Alex Morgan
Full-Stack Developer
Email: alex.morgan@email.com
Phone: (555) 123-4567
"""

        msg.set_content(body)

        with open(attachment_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(attachment_path)
            )

        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60)
        try:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
            smtp.quit()
        except KeyboardInterrupt:
            print(f"[WARNING] Email sending interrupted for {job['title']}")
            try:
                smtp.close()
            except:
                pass
            return
        except Exception as smtp_error:
            try:
                smtp.close()
            except:
                pass
            raise smtp_error

        print(f"[OK] Email sent for {job['title']}")
        print(f"  To: {RECIPIENT_EMAIL}")
        print(f"  Subject: {msg['Subject']}")
        print(f"  Attachment: {os.path.basename(attachment_path)}")

    except Exception as e:
        print(f"[WARNING] Email failed for {job['title']}: {str(e)[:100]}")