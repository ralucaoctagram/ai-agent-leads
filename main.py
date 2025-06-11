import os
import time
import re
import snscrape.modules.twitter as sntwitter
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIG ---

keywords = [
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
    "website help needed",
    "looking for wordpress freelancer",
    "anyone build websites?",
    "website redesign needed",
    "create a blog on wordpress",
    "help with my website",
    "need a logo designer",
    "logo design request",
    "logo designer needed",
    "looking for graphic designer",
    "custom logo needed",
    "need banner design",
    "create facebook banners",
    "banner localization",
    "multilingual banner design",
    "ad banner design needed",
    "video localization services",
    "need subtitles for video",
    "translate video content",
    "localize my video",
    "video editing with subtitles",
    "figma designer needed",
    "looking for figma expert",
    "need figma UI design",
    "ui ux design request",
    "website figma mockup",
    "redesign in figma"
]

max_results = 50
delay_between_keywords = 10

SPREADSHEET_ID = "1MjZoDMg8ehjmUPk7XLKRXLHXJCt6UdIH-vUX10z7IdA"
SHEET_NAME = "Sheet1"

import json
creds_json = os.getenv("GOOGLE_CREDENTIALS")
if not creds_json:
    raise Exception("Env var GOOGLE_CREDENTIALS nu este setat!")

with open("service_account.json", "w") as f:
    f.write(creds_json)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def append_to_sheet(data):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=f"{SHEET_NAME}!A1:F").execute()
    existing_values = result.get('values', [])

    headers = ["Date", "Platform", "Username", "Tweet", "Email", "Link"]

    if not existing_values:
        print("Sheet gol, scriu header...")
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [headers]}
        ).execute()
        start_row = 2
    else:
        start_row = len(existing_values) + 1

    values = [[
        row["Date"],
        row["Platform"],
        row["Username"],
        row["Tweet"],
        row["Email"],
        row["Link"]
    ] for row in data]

    if not values:
        print("Nu am date noi de adăugat.")
        return

    range_to_write = f"{SHEET_NAME}!A{start_row}"
    body = {
        "values": values
    }

    response = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_to_write,
        valueInputOption="RAW",
        body=body
    ).execute()
    print(f"Am adăugat {len(values)} rânduri în Google Sheet, începând cu rândul {start_row}.")

def main():
    results = []

    print("Încep căutarea pe Twitter...")

    for keyword in keywords:
        print(f"Caută: {keyword}")
        query = f"{keyword} lang:en"
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
            print(f" - Găsite {min(max_results, i+1)} tweeturi pentru '{keyword}'")
        except Exception as e:
            print(f"Error scraping keyword '{keyword}': {e}")
        time.sleep(delay_between_keywords)

    print(f"Total tweeturi găsite: {len(results)}")

    append_to_sheet(results)

if __name__ == "__main__":
    main()
