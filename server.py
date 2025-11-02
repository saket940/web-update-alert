import httpx
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://sih.gov.in/"
CHECK_INTERVAL = 300  # seconds (5 minutes)
SENDER_EMAIL = "asdadarya2222@gmail.com"
RECEIVER_EMAIL = "rambharats963@gmail.com"
APP_PASSWORD = "hcqsyrovxujbpnoj"  # Use your Gmail App Password, not your real password


def send_email_alert():
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "⚠️ SIH Website Updated"
    body = "The content of https://sih.gov.in/ has changed!"
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    print("📧 Email alert sent successfully!")

def get_clean_text():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://google.com",
    }

    try:
        response = httpx.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        print("✅ Site fetched successfully!")
        return response.text.strip()
    except httpx.HTTPStatusError as e:
        print(f"⚠️ HTTP Error: {e}")
        print("🔄 Retrying in 60 seconds with alternate headers...")
        time.sleep(60)
        return get_clean_text()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        time.sleep(60)
        return get_clean_text()

print("🔍 Monitoring started...")

old_data = get_clean_text()

while True:
    time.sleep(CHECK_INTERVAL)
    new_data = get_clean_text()

    if new_data != old_data:
        print("⚠️ Changes detected! Sending alert email...")
        send_email_alert()
        old_data = new_data
