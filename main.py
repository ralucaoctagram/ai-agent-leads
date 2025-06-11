import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import time

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
    # ... restul keyword-urilor tale ...
]

max_results = 100
results = []

print("Searching Twitter for leads...")

for keyword in keywords:
    query = f"{keyword} lang:en"
    print(f"Searching for: {keyword}")
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= max_results:
                break
            try:
                text = tweet.content
                date = tweet.date.strftime("%Y-%m-%d %H:%M")
                username = tweet.user.username if tweet.user else "unknown"
                link = f"https://twitter.com/{username}/status/{tweet.id}"
                email_match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
                email = email_match.group(0) if email_match else ""

                results.append({
                    "Date": date,
                    "Platform": "Twitter",
                    "Username": username,
                    "Tweet": text,
                    "Email": email,
                    "Link": link
                })
            except Exception as e:
                print(f"Error processing tweet: {e}")
                continue
        # Optional delay ca să nu suprasoliciți Twitter
        time.sleep(5)
    except Exception as e:
        print(f"Error scraping keyword '{keyword}': {e}")
        continue

# Salvare în Excel
df = pd.DataFrame(results)
file_name = "leads.xlsx"
df.to_excel(file_name, index=False)
print(f"Saved {len(df)} leads to {file_name}")
