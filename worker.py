from email.message import EmailMessage
import json
import os
import google.generativeai as genai
import requests

# ==========================================
# SECURE CONFIGURATION (Your Credentials)
# ==========================================
GEMINI_API_KEY = "AQ.Ab8RN6JLmuHfYXnrXAJIBrjbSGH1dDo1EqUFDqQ6djMgXhPOIw"

# Notification Emails
GMAIL_SENDER = "syedirfanakbarrehan@gmail.com"
GMAIL_APP_PASSWORD = "oqao lctc sekf dwmx"
GMAIL_RECIPIENT = "syedirfanakbarrehan@gmail.com"

# PayPal Live Credentials
PAYPAL_CLIENT_ID = (
    "BAAb9PaLBwHFolqFzDlAB0mqmQ_N75zZn_aR43PEuM7NkS42Dw-iS3iKymgeJTMivNPRHphLLJGYAJucZw"
)
PAYPAL_SECRET = (
    "EIcLF1CBIpi_0FlfstGfWC0cigYrkrL0UCGl2tDqT3JWc5rZ37t14Y8YemK6mUrACB9uJu_j7TUp1hNG"
)
PAYPAL_ACCOUNT_EMAIL = "syedirfanakbarmashadi@gmail.com"
PAYPAL_API_BASE = "https://api-m.paypal.com"  # Live environment

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ==========================================
# 1. PayPal Live Connection Check
# ==========================================
def verify_paypal_account():
  """Authenticates with PayPal Live API to ensure your account is active."""
  url = f"{PAYPAL_API_BASE}/v1/oauth2/token"
  headers = {"Accept": "application/json", "Accept-Language": "en_US"}
  data = {"grant_type": "client_credentials"}

  try:
    response = requests.post(
        url,
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        headers=headers,
        data=data,
    )
    if response.status_code == 200:
      return (
          True,
          f"PayPal Live API Connected Successfully for ({PAYPAL_ACCOUNT_EMAIL})",
      )
    else:
      return False, f"PayPal Auth Error: {response.text}"
  except Exception as e:
    return False, f"PayPal Connection Exception: {e}"


# ==========================================
# 2. AI Lead Generation & Task Management
# ==========================================
def fetch_raw_leads():
  """Target business listings for automated outreach."""
  return [
      {
          "name": "Urban Style Boutique",
          "city": "Lahore",
          "contact": "info@urbanstyle.pk",
          "services": "Retail clothing store",
      },
      {
          "name": "Apex Fitness Gym",
          "city": "Islamabad",
          "contact": "contact@apexfitness.pk",
          "services": "Gym and personal training",
      },
  ]


def process_leads_with_gemini(raw_leads):
  """Uses Gemini to clean and write personalized outreach pitches."""
  prompt = f"""
    You are an expert sales assistant. Analyze these business listings:
    {json.dumps(raw_leads, indent=2)}
    
    Tasks:
    1. Write a 1-sentence personalized sales pitch offering an automated digital service.
    2. Return a clean bulleted summary with business name, contact info, and proposed pitch.
    """
  response = model.generate_content(prompt)
  return response.text


# ==========================================
# 3. Send Report via Gmail
# ==========================================
def send_gmail_report(report_text, paypal_status_msg):
  """Sends the daily briefing straight to your Gmail inbox."""
  msg = EmailMessage()
  msg.set_content(
      f"🤖 DAILY AI & EARNINGS BRIEFING\n\n"
      f"----------------------------------------\n"
      f"PAYPAL STATUS: {paypal_status_msg}\n"
      f"----------------------------------------\n\n"
      f"{report_text}\n\n"
      f"--- \n"
      f"Generated automatically by your 24/7 background worker."
  )

  msg["Subject"] = "🤖 Daily AI Assistant Earnings & Lead Briefing"
  msg["From"] = GMAIL_SENDER
  msg["To"] = GMAIL_RECIPIENT

  try:
    import smtplib

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Email report successfully sent to syedirfanakbarrehan@gmail.com!")
  except Exception as e:
    print("Failed to send email:", e)


if __name__ == "__main__":
  print("Starting daily background worker job...")

  # Check PayPal Live connection
  paypal_ok, paypal_msg = verify_paypal_account()
  print(paypal_msg)

  # Process AI Tasks
  leads = fetch_raw_leads()
  ai_report = process_leads_with_gemini(leads)

  # Send Summary via Gmail
  send_gmail_report(ai_report, paypal_msg)
  print("Job complete!")