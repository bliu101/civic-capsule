from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["volunteer"]

def scrape_volunteermatch_boston():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
    driver.get(url)

    time.sleep(5)
    print(driver.page_source)

    # Wait up to 15 seconds for the results to load
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps"))
        )
    except Exception as e:
        print("❌ Timed out waiting for opportunities to load.")
        driver.quit()
        return []

    # Give extra time just in case content is still rendering
    time.sleep(2)

    container = driver.find_element(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps")
    cards = container.find_elements(By.CSS_SELECTOR, "li")
    print(f"✅ Found {len(cards)} volunteer cards")

    opportunities = []

    for card in cards:
        try:
            title_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
            org_elem = card.find_element(By.CSS_SELECTOR, ".pub-srp-opps__org-name")
            location_elem = card.find_element(By.CSS_SELECTOR, ".pub-srp-opps__loc")

            opportunity = {
                "title": title_elem.text.strip(),
                "organization": org_elem.text.strip(),
                "location": location_elem.text.strip(),
                "link": title_elem.get_attribute("href"),
            }
            opportunities.append(opportunity)
        except Exception as e:
            print(f"⚠️ Error parsing one card: {e}")

    driver.quit()
    return opportunities

# def stealth_scrape_volunteermatch(pages=5):
#     options = uc.ChromeOptions()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = uc.Chrome(options=options)

#     all_opportunities = []

#     for page in range(1, pages + 1):
#         url = f"https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA&p={page}"
#         print(f"\n🌐 Scraping page {page} → {url}")
#         driver.get(url)
#         time.sleep(5)

#         try:
#             container = driver.find_element(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps")
#             cards = container.find_elements(By.CSS_SELECTOR, "li")
#             print(f"✅ Found {len(cards)} cards on page {page}")

#             for card in cards:
#                 try:
#                     title_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
#                     org_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__org-name")
#                     loc_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__loc")

#                     opportunity = {
#                         "title": title_elem.text.strip(),
#                         "organization": org_elems[0].text.strip() if org_elems else "N/A",
#                         "location": loc_elems[0].text.strip() if loc_elems else "N/A",
#                         "link": title_elem.get_attribute("href"),
#                     }
#                     all_opportunities.append(opportunity)

#                 except Exception as e:
#                     print(f"⚠️ Skipped one card: {e}")

#         except Exception as e:
#             print(f"❌ Could not scrape page {page}: {e}")

#     driver.quit()
#     return all_opportunities

def stealth_scrape_volunteermatch():
    base_url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get(base_url)
    time.sleep(5)

    # Open the category filter popup
    cause_button = driver.find_element(By.CSS_SELECTOR, "li.causeareas button")
    cause_button.click()
    time.sleep(2)

    # Grab the original list of categories
    original_categories = driver.find_elements(By.CSS_SELECTOR, "#cat_form .js-cat-cell")
    print(f"🔍 Found {len(original_categories)} categories.")
    print("ORIGINAL CATEGORIES:", original_categories)

    all_opportunities = []

    for i in range(len(original_categories)-1):
        # Reopen the base page each time to avoid stale references
        driver.get(base_url)
        # time.sleep(5)

        WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.spinner-mask__spinner"))
        )

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.causeareas button"))
        ).click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#cat_form .js-cat-cell"))
        )

        # cause_button = driver.find_element(By.CSS_SELECTOR, "li.causeareas button")
        # cause_button.click()
        # # time.sleep(10)

        categories = driver.find_elements(By.CSS_SELECTOR, "#cat_form .js-cat-cell")
        cat = categories[i]
        cat_id = cat.get_attribute("id").split("_")[-1]
        cat_name = cat.text.strip()
        print(f"\n🌱 Scraping category: {cat_name} (ID: {cat_id})")

        # Visit the category page
        category_url = f"{base_url}&categories={cat_id}"
        driver.get(category_url)
        time.sleep(5)

        # Scrape one page of results
        try:
            container = driver.find_element(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps")
            cards = container.find_elements(By.CSS_SELECTOR, "li")
            print(f"✅ Found {len(cards)} cards in {cat_name}")

            for card in cards:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
                    org_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__org-name")
                    loc_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__loc")

                    opportunity = {
                        "title": title_elem.text.strip(),
                        "organization": org_elems[0].text.strip() if org_elems else "N/A",
                        "location": loc_elems[0].text.strip() if loc_elems else "N/A",
                        "url": title_elem.get_attribute("href"),
                        "category": cat_name,
                    }
                    all_opportunities.append(opportunity)
                except Exception as e:
                    print(f"⚠️ Skipped one card in {cat_name}: {e}")
        except Exception as e:
            print(f"❌ No opportunities found for {cat_name}: {e}")

    driver.quit()
    return all_opportunities

def save_volunteering_to_mongo(volunteers):
    existing_count = collection.count_documents({})
    inserted_count = 0

    for i, volunteer in enumerate(volunteers, start=1):
        volunteer_id = f"V{existing_count + i:04d}"  # e.g. V0001
        volunteer["volunteer_id"] = volunteer_id
        volunteer["url"] = volunteer.pop("link")  # Rename 'link' → 'url'

        if not collection.find_one({"url": volunteer["url"]}):
            collection.insert_one(volunteer)
            inserted_count += 1
            print(f"✅ Inserted: {volunteer_id}")
        else:
            print(f"⚠️ Already exists: {volunteer['url']} — skipped")

    print(f"\n📦 Done. Total inserted: {inserted_count}")

if __name__ == "__main__":
    # results = scrape_volunteermatch_boston()
    # for r in results:
    #     print(r)
    results = stealth_scrape_volunteermatch()
    for opp in results:
        print(f"\n📝 {opp['title']}\n📍 {opp['location']} | 🏢 {opp['organization']}\n🔗 {opp['link']}")

    if results:
        save_volunteering_to_mongo(results)