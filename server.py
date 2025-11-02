import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
from bs4 import BeautifulSoup
import httpx


SENDER_EMAIL = "asdadarya2222@gmail.com"
RECEIVER_EMAIL = "rambharats963@gmail.com"
APP_PASSWORD = "hcqsyrovxujbpnoj"  # Use your Gmail App Password, not your real password

# === Website Setup ===
url = "https://sih.gov.in/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def get_clean_text():
    """Fetch site and extract clean visible text"""
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        response = client.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts, styles, and metadata
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text only
    text = soup.get_text(separator=" ", strip=True)
    return text

# === Initial fetch ===
old_data = get_clean_text()
print("🔍 Monitoring started...")

# === Continuous Monitoring ===
while True:
    time.sleep(60)  # check every 60 seconds
    new_data = get_clean_text()

    if old_data== new_data:
        print("✅ No visible changes detected.")
    else:
        print("⚠️ Real change detected! Sending alert email...")

        # === Send Email ===
        message = MIMEMultipart("alternative")
        message["Subject"] = "⚠️ SIH Website Updated!"
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        text = f"The visible content on the SIH website has changed.\n\nURL: {url}"
        message.attach(MIMEText(text, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
            print("📧 Email alert sent successfully!")
        except Exception as e:
            print("❌ Failed to send email:", e)

        # Update stored data
        old_data = new_data
