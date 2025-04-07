from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["moveon_petitions"]

def scrape_moveon_petitions(driver, url):
    driver.get(url)
    time.sleep(3)

    # Scroll to load more results (simulate infinite scroll)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):  # Adjust number of scrolls as needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find all petition cards
    petitions = driver.find_elements(By.CSS_SELECTOR, "li > div.petition-horizontal")

    # Extract data
    petition_links = []
    for petition in petitions:
        try:
            title_element = petition.find_element(By.CSS_SELECTOR, "a.title.petition-title")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")
            creator = petition.find_element(By.CSS_SELECTOR, "div.petition-creator span.name").text.strip()
            signature_info = petition.find_element(By.CSS_SELECTOR, "div.petition-signatures").text.strip()
            petition_links.append({
                "title": title,
                "url": url,
                "creator": creator,
                "signature_info": signature_info
            })
        except Exception as e:
            print(f"Error collecting petition info from list page: {e}")
            continue

    results = []
    for item in petition_links:
        try:
            driver.get(item["url"])
            time.sleep(2)

            full_description = driver.find_element(By.CSS_SELECTOR, "div.intro-copy.what").text.strip()
            try:
                why_section = driver.find_element(By.CSS_SELECTOR, "div.why").text.strip()
            except:
                why_section = ""

            try:
                category_elements = driver.find_elements(By.CSS_SELECTOR, "#petition-categories-section a.capsule")
                categories = [cat.text.strip() for cat in category_elements]
            except:
                categories = []

            item.update({
                "full_description": full_description,
                "why_section": why_section,
                "categories": categories
            })
            results.append(item)
        except Exception as e:
            print(f"Error parsing petition detail page: {e}")
            continue

    # driver.quit()
    print("RESULTS::", results)
    return results

def scrape_moveon_multiple_pages(keyword="boston", pages=2):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    all_results = []
    try:
        for page in range(1, pages + 1):
            print(f"\n--- Scraping Page {page} ---")
            url = f"https://sign.moveon.org/petitions/search?page={page}&query={keyword}"
            page_results = scrape_moveon_petitions(driver, url)
            all_results.extend(page_results)
    finally:
        driver.quit()

    print(f"\n✅ Finished scraping {len(all_results)} petitions from {pages} pages.")
    return all_results

def save_petitions_to_mongo(petitions):
    existing_count = collection.count_documents({})
    for i, petition in enumerate(petitions, start=1):
        petition_id = f"P{existing_count + i:04d}"  # e.g. P0001
        petition["petition_id"] = petition_id

        # Optional: avoid duplicate by checking URL
        if not collection.find_one({"url": petition["url"]}):
            collection.insert_one(petition)
            print(f"✅ Inserted: {petition_id}")
        else:
            print(f"⚠️ Already exists: {petition['url']} — skipped")

    print(f"\n📦 Done. Total inserted: {len(petitions)}")


# Example usage
if __name__ == "__main__":
    # petitions = scrape_moveon_multiple_pages(keyword='boston', pages=10)
    # filename = "moveon_petitions.txt"
    
    # with open(filename, mode="w", encoding="utf-8") as file:
    #     for p in petitions:
    #         file.write(f"Title: {p['title']}\n")
    #         file.write(f"URL: {p['url']}\n")
    #         file.write(f"Creator: {p['creator']}\n")
    #         file.write(f"Signatures: {p['signature_info']}\n")
    #         file.write(f"Description: {p['full_description']}\n")
    #         file.write(f"Why: {p['why_section']}\n")
    #         file.write(f"Categories: {p['categories']}\n")
    #         file.write("\n" + "-"*80 + "\n\n")
    
    # print(f"\n✅ Petition data written to {filename}")
    results = scrape_moveon_multiple_pages(keyword='boston', pages=10)

    if results:
        save_petitions_to_mongo(results)