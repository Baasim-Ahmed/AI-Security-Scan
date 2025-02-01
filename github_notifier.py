import json
import os
import requests
import smtplib
from email.mime.text import MIMEText

github_token = os.getenv("GITHUB_TOKEN")
github_repo = os.getenv("GITHUB_REPOSITORY")
github_event_path = os.getenv("GITHUB_EVENT_PATH")
email_recipient = os.getenv("EMAIL_RECIPIENT")
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")

def get_pull_request_number():
    with open(github_event_path, "r") as f:
        event_data = json.load(f)
    return event_data.get("pull_request", {}).get("number")

def post_comment(pr_number, comment):
    url = f"https://api.github.com/repos/{github_repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_sender
    msg["To"] = email_recipient
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_recipient, msg.as_string())
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    pr_number = get_pull_request_number()
    if not pr_number:
        print("No PR found, skipping notification.")
        return
    
    with open("scan_results.json", "r") as f:
        vulnerabilities = json.load(f)
    
    if not vulnerabilities:
        print("No vulnerabilities found.")
        return
    
    comment_body = "🚨 **Security Alert: Vulnerabilities Detected!**\n\n"
    email_body = "Security Alert: The following vulnerabilities were detected in your code:\n\n"
    
    for v in vulnerabilities:
        issue_details = f"### File: `{v['file']}`\n- **Vulnerability:** {v['vulnerability']}\n- **Line:** {v['line']}\n- **Fix:** {v['fix']}\n\n"
        comment_body += issue_details
        email_body += issue_details
    
    status, response = post_comment(pr_number, comment_body)
    print(f"Comment posted with status {status}: {response}")
    
    send_email("Security Alert: Vulnerabilities Detected", email_body)

if __name__ == "__main__":
    main()
