import requests
from bs4 import BeautifulSoup

CIVIC_ENGAGEMENT = "1831"
ENVIRONMENT = "1156"
SOCIAL_GOOD = "186"
LEARNINGS_AND_LECTURES = "166"

def scrape_filtered_boston_events(pages=3, event_type_ids=["1831", "1156", "186", "166"]):
    """
    1831: Civic engagement
    1156: Envionment and green living
    186: Social good
    166: Learnings and lectures
    """
    all_events = []

    for page in range(pages):
        base_url = "https://www.boston.gov/events"
        params = [("page", page)]
        for event_type_id in event_type_ids:
            params.append(("field_event_type_target_id[]", event_type_id))

        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select("article.calendar-listing-wrapper")
        print(f"Page {page}: {len(articles)} events found")

        for article in articles:
            title = article.select_one(".title")
            time = article.select_one(".time-range")
            address = article.select_one(".detail-item__field_address .addr-a")
            email_tag = article.select_one(".detail-item__field_email a[href^='mailto:']")
            phone_tag = article.select_one(".detail-item__field_phone_number a[href^='tel:']")
            price_tag = article.select_one(".dl-i .dl-d")
            desc_tag = article.select_one(".description .intro-text")
            link_tag = article.select_one("a.button[href^='/node/']")

            link = "https://www.boston.gov" + link_tag.get("href") if link_tag else None
        full_description = "No full description"

        if link:
            try:
                detail_resp = requests.get(link)
                detail_soup = BeautifulSoup(detail_resp.content, "html.parser")

                # Try to get og:description first
                og_desc_tag = detail_soup.find("meta", property="og:description")
                if og_desc_tag and og_desc_tag.get("content"):
                    full_description = og_desc_tag["content"]
                else:
                    # Try to get full detail from page
                    full_desc_tag = detail_soup.find("div", class_="field--name-body")
                    if full_desc_tag and full_desc_tag.get_text(strip=True):
                        full_description = full_desc_tag.get_text(strip=True)
                    else:
                        # Check for external event website link
                        external_link_tag = detail_soup.select_one("div.external-link a.button[href^='http']")
                        if external_link_tag and external_link_tag.get("href"):
                            full_description = f"See event site: {external_link_tag.get('href')}"

            except Exception as e:
                print(f"Error getting full description for {link}: {e}")

            all_events.append({
                "title": title.get_text(strip=True) if title else "No title",
                "time": time.get_text(strip=True) if time else "No time",
                "address": address.get_text(strip=True) if address else "No address",
                "email": email_tag.get("href").replace("mailto:", "") if email_tag else "No email",
                "phone": phone_tag.get("href").replace("tel:", "") if phone_tag else "No phone",
                "price": price_tag.get_text(strip=True) if price_tag else "No price",
                "description": desc_tag.get_text(strip=True) if desc_tag else "No short description",
                "full_description": full_description,
                "link": link if link else "No link"
            })

    return all_events

# Example use
events = scrape_filtered_boston_events(pages=1, event_type_ids=[LEARNINGS_AND_LECTURES])
for e in events:
    print(f"{e['title']} ({e['time']})")
    print(f"{e['address']} | {e['email']} | {e['phone']}")
    print(f"{e['price']}")
    print(f"Short: {e['description']}")
    print(f"Full: {e['full_description']}")
    print(f"{e['link']}")
    print("-" * 60)
