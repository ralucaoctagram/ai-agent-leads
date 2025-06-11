import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import time
from datetime import datetime

keywords = [
    # lista ta de keyword-uri (la fel ca înainte)
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

max_results = 100
results = []

print("Searching Twitter for leads...")

for keyword in keywords:
    print(f"Searching for: {keyword}")
    try:
        query = f"{keyword} lang:en"
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
    except Exception as e:
        print(f"Error scraping keyword '{keyword}': {e}")

    # Pauză de 5 secunde între fiecare căutare pentru a evita blocarea
    time.sleep(5)

df = pd.DataFrame(results)
file_name = "leads.xlsx"
df.to_excel(file_name, index=False)
print(f"Saved {len(df)} leads to {file_name}")
