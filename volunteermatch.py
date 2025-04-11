from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from bs4 import BeautifulSoup
import requests

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["volunteering"]

# def soup():
#     url = 'https://www.volunteermatch.org/search?l=Boston%2C+MA%2C+USA'
#     headers = {'User-Agent': 'Mozilla/5.0'}

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find all opportunity items
#     opportunities = soup.find_all('li', class_='pub-srp-opps__opp')

#     print(f'Found {len(opportunities)} opportunities.')
#     for opp in opportunities:
#         title_tag = opp.find('a', class_='pub-srp-opps__title')
#         title = title_tag.get_text(strip=True) if title_tag else 'No Title'
#         link = 'https://www.volunteermatch.org' + title_tag['href'] if title_tag and title_tag.get('href') else 'No Link'

#         desc_tag = opp.find('p', class_='pub-srp-opps__desc')
#         desc = desc_tag.get_text(strip=True) if desc_tag else 'No Description'

#         org_tag = opp.find('div', class_='pub-srp-opps__org')
#         org = org_tag.get_text(strip=True).replace('Organization:', '') if org_tag else 'No Organization'

#         print(f'Title: {title}\nOrganization: {org}\nLink: {link}\nDescription: {desc[:100]}...\n')

def scrape_volunteering():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # Wait for search results to load
    time.sleep(3)

    base_url = "https://www.volunteermatch.org/search/?l=Boston%2C+MA%2C+USA&v=true"
    all_data = []

    for page_num in range(1, 6):  # Pages 1 through 5
        url = f"{base_url}&p={page_num}"
        print(f"🌐 Scraping page {page_num}: {url}")
        driver.get(url)
        time.sleep(3)  # Allow page to load

        try:
            # Find the UL within the known container
            container = driver.find_elements(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps")
            ul = container.find_element(By.TAG_NAME, "ul")
            listings = ul.find_elements(By.TAG_NAME, "li")
        except Exception as e:
            print(f"⚠️ Couldn't find opportunity list on page {page_num}. Error: {e}")
            continue

        for li in listings:
            try:
                title_elem = li.find_element(By.CSS_SELECTOR, "a.pub-srp-opps__title span")
                org_elem = li.find_element(By.CSS_SELECTOR, ".pub-srp-opps__org a")
                desc_elem = li.find_element(By.CLASS_NAME, "pub-srp-opps__desc")
                loc_elem = li.find_element(By.CLASS_NAME, "pub-srp-opps__loc")
                date_elem = li.find_element(By.CLASS_NAME, "pub-srp-opps__posted")
                url_path = li.find_element(By.CSS_SELECTOR, "a.pub-srp-opps__title").get_attribute("href")

                all_data.append({
                    "title": title_elem.text.strip(),
                    "organization": org_elem.text.strip(),
                    "description": desc_elem.text.strip(),
                    "location": loc_elem.text.strip(),
                    "date_posted": date_elem.text.strip().replace("Date Posted: ", ""),
                    "url": url_path
                })
            except Exception as e:
                print(f"❌ Error scraping a listing: {e}")

    driver.quit()
    return all_data

def save_volunteering_to_mongo(opps):
    existing_count = collection.count_documents({})
    for i, opp in enumerate(opps, start=1):
        opp_id = f"V{existing_count + i:04d}"  # e.g. V0001
        opp["volunteering_id"] = opp_id

        # Avoid duplicate by checking title + org
        if not collection.find_one({"title": opp["title"], "organization": opp["organization"]}):
            collection.insert_one(opp)
            print(f"✅ Inserted: {opp_id}")
        else:
            print(f"⚠️ Already exists: {opp['title']} — skipped")

    print(f"\n📦 Done. Total inserted: {len(opps)}")


# Example usage
if __name__ == "__main__":

    results = scrape_volunteering()
    # results = soup()
    print(results)

    # if results:
    #     save_petitions_to_mongo(results)