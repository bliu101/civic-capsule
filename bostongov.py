import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient
from hashlib import md5

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["events"]

category_lookup = {
    "1831": "Civic Engagement",
    "1156": "Environment and Green Living",
    "186": "Social Good",
    "166": "Learnings and Lectures"
}

def scrape_filtered_boston_events(pages=1, event_type_ids=None):
    if event_type_ids is None:
        event_type_ids = list(category_lookup.keys())

    for event_type_id in event_type_ids:
        category = category_lookup.get(event_type_id, "Unknown")
        print(f"\nScraping category: {category} (ID: {event_type_id})")
        
        for page in range(pages):
            base_url = "https://www.boston.gov/events"
            params = [("page", page), ("field_event_type_target_id[]", event_type_id)]

            response = requests.get(base_url, params=params)
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.select("article.calendar-listing-wrapper")
            print(f"Page {page}: {len(articles)} events found")

            for article in articles:
                title_tag = article.select_one(".title")
                time_tag = article.select_one(".time-range")
                address_tag = article.select_one(".detail-item__field_address .addr-a")
                email_tag = article.select_one(".detail-item__field_email a[href^='mailto:']")
                phone_tag = article.select_one(".detail-item__field_phone_number a[href^='tel:']")
                price_tag = article.select_one(".dl-i .dl-d")
                desc_tag = article.select_one(".description .intro-text")
                link_tag = article.select_one("a.button[href^='/node/']")
                external_link_tag = article.select_one("a.button[href^='http']")

                if link_tag:
                    link = "https://www.boston.gov" + link_tag.get("href")
                elif external_link_tag:
                    link = external_link_tag.get("href")
                    full_description = f"See event site: {link}"
                else:
                    link = None
                    full_description = "No full description"

                full_description = "No full description"

                if link and link.startswith("https://www.boston.gov/node"):
                    try:
                        detail_resp = requests.get(link)
                        detail_soup = BeautifulSoup(detail_resp.content, "html.parser")

                        og_desc_tag = detail_soup.find("meta", property="og:description")
                        if og_desc_tag and og_desc_tag.get("content"):
                            full_description = og_desc_tag["content"]
                        else:
                            full_desc_tag = detail_soup.find("div", class_="field--name-body")
                            if full_desc_tag and full_desc_tag.get_text(strip=True):
                                full_description = full_desc_tag.get_text(strip=True)
                            else:
                                external_link_tag = detail_soup.select_one("div.external-link a.button[href^='http']")
                                if external_link_tag and external_link_tag.get("href"):
                                    full_description = f"See event site: {external_link_tag.get('href')}"

                    except Exception as e:
                        print(f"Error getting full description for {link}: {e}")

                # Build document
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                time = time_tag.get_text(strip=True) if time_tag else "No time"
                address = address_tag.get_text(strip=True) if address_tag else "No address"
                email = email_tag.get("href").replace("mailto:", "") if email_tag else "No email"
                phone = phone_tag.get("href").replace("tel:", "") if phone_tag else "No phone"
                price = price_tag.get_text(strip=True) if price_tag else "No price"
                short_desc = desc_tag.get_text(strip=True) if desc_tag else "No short description"

                _id = md5((title + time).encode("utf-8")).hexdigest()  # Create unique hash

                document = {
                    "title": title,
                    "category": category,
                    "time": time,
                    "address": address,
                    "email": email,
                    "phone": phone,
                    "price": price,
                    "description": {
                        "short": short_desc,
                        "full": full_description
                    },
                    "link": link if link else "No link"
                }
                if collection.find_one({"title": title}):
                    print(f"⚠️ Skipping duplicate event: {title}")
                    continue
                try:
                    collection.insert_one(document)
                    print(f"✅ Inserted: {title}")
                except Exception as e:
                    print(f"⚠️ Error inserting {title}: {e}")

scrape_filtered_boston_events(pages=2)