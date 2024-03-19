import smtplib
from email.mime.text import MIMEText
import fire
from dotenv import load_dotenv
import os

load_dotenv('/Users/user/scheduler/.env')

def send_email(topic, subtopic=""):
    sender = os.getenv("EMAIL_SENDER")
    receiver = "yuhsuan.ting@admazes.com"
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    if topic == 'error':
        title = f"IG CRAWLER {topic}: {subtopic} error"
        message = f"IG CRAWLER {topic}: {subtopic} error"
    else:
        title = f"IG CRAWLER {topic}: Script Execution Complete"
        message = f"Your script {topic} has finished running."
    
    msg = MIMEText(message)
    msg["Subject"] = title
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
    print("email send")

if __name__ == "__main__":
    fire.Fire(send_email)


# chmod +x scheduler.sh
#crontab -e
#55 22 * * * /Users/user/code/scheduler.sh > /Users/user/code/logs/$(date +\%Y-\%m-\%d)-scheduler.log 2>&1
# crontab -l

