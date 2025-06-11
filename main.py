import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from datetime import datetime

# Extended list of search phrases for dev + design + localization
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

# Max tweets per keyword
max_results = 100

# Store results
results = []

print("Searching Twitter for leads...")

for keyword in keywords:
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

# Save to Excel
df = pd.DataFrame(results)
file_name = "leads.xlsx"
df.to_excel(file_name, index=False)
print(f"Saved {len(df)} leads to {file_name}")
