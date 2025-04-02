import requests
from bs4 import BeautifulSoup

def scrape_filtered_boston_events(pages=3, event_type_ids=["1831", "1156", "186"]):
    all_events = []

    for page in range(pages):
        base_url = "https://www.boston.gov/events"
        params = {
            "page": page,
            "field_event_type_target_id[]": event_type_ids
        }

        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select("article.calendar-listing-wrapper")

        for article in articles:
            title = article.select_one(".title")
            time = article.select_one(".time-range")
            address = article.select_one(".detail-item__field_address .addr-a")
            email_tag = article.select_one(".detail-item__field_email a[href^='mailto:']")
            phone_tag = article.select_one(".detail-item__field_phone_number a[href^='tel:']")
            price_tag = article.select_one(".dl-i .dl-d")
            desc_tag = article.select_one(".description .intro-text")
            link_tag = article.select_one("a.button[href^='/node/']")

            all_events.append({
                "title": title.get_text(strip=True) if title else "No title",
                "time": time.get_text(strip=True) if time else "No time",
                "address": address.get_text(strip=True) if address else "No address",
                "email": email_tag.get("href").replace("mailto:", "") if email_tag else "No email",
                "phone": phone_tag.get("href").replace("tel:", "") if phone_tag else "No phone",
                "price": price_tag.get_text(strip=True) if price_tag else "No price",
                "description": desc_tag.get_text(strip=True) if desc_tag else "No description",
                "link": "https://www.boston.gov" + link_tag.get("href") if link_tag else "No link"
            })

    return all_events

# Example use:
events = scrape_filtered_boston_events(pages=2)
for e in events:
    print(f"{e['title']} ({e['time']})")
    print(f"{e['address']} | {e['email']} | {e['phone']}")
    print(f"{e['price']} | {e['description']}")
    print(f"{e['link']}")
    print("-" * 50)
