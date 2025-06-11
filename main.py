import time
import random
import snscrape.modules.twitter as sntwitter
import re
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Cuvinte cheie pentru căutare
keywords = [
    # Development & WordPress
    "looking for a web designer",
    "need a wordpress site",
    "wordpress developer wanted",
    "custom wordpress theme",
    "website designer needed",
    "need a developer for my site",
    "freelance wordpress expert",
    "hire a wordpress developer",
    "woocommerce expert needed",
    "help with wordpress plugin",

    # General web help
    "website help needed",
    "looking for wordpress freelancer",
    "anyone build websites?",
    "website redesign needed",
    "create a blog on wordpress",
    "help with my website",

    # Logo & graphic design
    "need a logo designer",
    "logo design request",
    "logo designer needed",
    "looking for graphic designer",
    "custom logo needed",

    # Banner design & localization
    "need banner design",
    "create facebook banners",
    "banner localization",
    "multilingual banner design",
    "ad banner design needed",

    # Video & localization
    "video localization services",
    "need subtitles for video",
    "translate video content",
    "localize my video",
    "video editing with subtitles",

    # Figma / UI/UX
    "figma designer needed",
    "looking for figma expert",
    "need figma UI design",
    "ui ux design request",
    "website figma mockup",
    "redesign in figma"
]

max_results = 100

def get_google_sheets_service():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS secret is missing.")

    creds_dict = json.loads(creds_json)
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service

def save_to_sheets(data, spreadsheet_id, sheet_name='Sheet1'):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()

    values = [["Date", "Platform", "Username", "Tweet", "Email", "Link"]]
    for item in data:
        values.append([
            item["Date"],
            item["Platform"],
            item["Username"],
            item["Tweet"],
            item["Email"],
            item["Link"]
        ])

    sheet.values().clear(spreadsheetId=spreadsheet_id, range=sheet_name).execute()

    sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

def main():
    results = []
    print("Căutăm lead-uri pe Twitter...")

    for keyword in keywords:
        query = f"{keyword} lang:en"
        print(f"🔍 Caut: {keyword}")
        try:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= max_results:
                    break

                text = tweet.content
                date = tweet.date.strftime("%Y-%m-%d %H:%M")
                link = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
                email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
                email = email_match.group(0) if email_match else ""

                results.append({
                    "Date": date,
                    "Platform": "Twitter",
                    "Username": tweet.user.username,
                    "Tweet": text,
                    "Email": email,
                    "Link": link
                })

            delay = random.randint(8, 15)
            print(f"⏳ Pauză {delay}s...\n")
            time.sleep(delay)

        except Exception as e:
            print(f"⚠️ Eroare la keyword '{keyword}': {e}")

    print(f"✅ Gata! Am găsit {len(results)} rezultate.")

    # ID-ul foii tale Google Sheets
    SPREADSHEET_ID = "1MjZoDMg8ehjmUPk7XLKRXLHXJCt6UdIH-vUX10z7IdA"

    save_to_sheets(results, SPREADSHEET_ID)
    print("✅ Datele au fost salvate în Google Sheets!")

if __name__ == "__main__":
    main()
