# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# import time
# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient

# load_dotenv()

# MONGO_URI = os.getenv("MONGODB_URI")
# DB_NAME = os.getenv("DB_NAME", "rocketchat")

# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# collection = db["volunteer"]

# def scrape_volunteer():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = webdriver.Chrome(options=options)

#     url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
#     driver.get(url)
#     time.sleep(3)

#     # Scroll to load more results (simulate infinite scroll)
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     for _ in range(3):  # Adjust number of scrolls as needed
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

#     # Find all petition cards
#     volunteering_events = driver.find_elements(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps ul li")

#     # Now find the container
#     # container = soup.find('div', class_='col-md-8 pub-srp-opps')
#     # ul = container.find('ul') if container else None
#     # opportunities = soup.find_all("div", class_="pub-srp-opps__opp")
#     opportunities = volunteering_events

#     print("OPPORTUNITIES ", opportunities)

#     # Extract info
#     results = []

#     for i, opp in enumerate(opportunities):
#         try:
#             title_tag = opp.find('a', class_='pub-srp-opps__title')
#             if not title_tag:
#                 continue
#             title = title_tag.get_text(strip=True)
#             link = "https://www.volunteermatch.org" + title_tag.get('href', '')

#             opp_id = opp.get('id', f'unknown_{i}')
#             org_tag = opp.find('a', class_='blue-drk')
#             organization = org_tag.get_text(strip=True) if org_tag else "N/A"

#             location = opp.find('div', class_='pub-srp-opps__loc')
#             location_text = location.get_text(strip=True) if location else "N/A"

#             desc = opp.find('p', class_='pub-srp-opps__desc')
#             description = desc.get_text(strip=True) if desc else "N/A"

#             posted = opp.find('div', class_='pub-srp-opps__posted')
#             posted_date = posted.get_text(strip=True).replace("Date Posted: ", "") if posted else "N/A"

#             results.append({
#                 "id": opp_id,
#                 "title": title,
#                 "link": link,
#                 "organization": organization,
#                 "location": location_text,
#                 "description": description,
#                 "posted_date": posted_date
#             })

#         except Exception as e:
#             print(f"Error parsing opp {i}: {e}")

#     # Print results
#     for r in results:
#         print(r)


# # You can also save this data to a database, for example:
# # 1. Connect to your MongoDB or SQL database.
# # 2. Insert each opportunity into the respective table/collection.

# if __name__ == "__main__":
#     results = scrape_volunteer()

#     # if results:
#     #     save_petitions_to_mongo(results)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def scrape_volunteermatch_boston():
    options = Options()
    options.add_argument("--headless")  # run headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
    driver.get(url)
    time.sleep(5)  # give it time to load

    opportunities = []

    try:
        # All opportunity cards are list items inside a <ul>
        cards = driver.find_elements(By.CSS_SELECTOR, "ul.pub-srp-opps__list > li")

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
                print(f"Error parsing one card: {e}")

    finally:
        driver.quit()

    return opportunities

if __name__ == "__main__":
    results = scrape_volunteermatch_boston()
    for r in results:
        print(r)
