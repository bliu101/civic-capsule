from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_volunteer():
    # Setup headless browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    # Load the VolunteerMatch Boston page
    url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
    driver.get(url)

    # Wait for JS to load
    # time.sleep(5)
    # Wait up to 10 seconds for at least one opportunity to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li"))
    )


    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Now find the container
    container = soup.find('div', class_='col-md-8 pub-srp-opps')
    ul = container.find('ul') if container else None
    opportunities = ul.find_all('li', recursive=False) if ul else []
    print("OPPORTUNITIES ", opportunities)

    # Extract info
    results = []

    for i, opp in enumerate(opportunities):
        try:
            title_tag = opp.find('a', class_='pub-srp-opps__title')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = "https://www.volunteermatch.org" + title_tag.get('href', '')

            opp_id = opp.get('id', f'unknown_{i}')
            org_tag = opp.find('a', class_='blue-drk')
            organization = org_tag.get_text(strip=True) if org_tag else "N/A"

            location = opp.find('div', class_='pub-srp-opps__loc')
            location_text = location.get_text(strip=True) if location else "N/A"

            desc = opp.find('p', class_='pub-srp-opps__desc')
            description = desc.get_text(strip=True) if desc else "N/A"

            posted = opp.find('div', class_='pub-srp-opps__posted')
            posted_date = posted.get_text(strip=True).replace("Date Posted: ", "") if posted else "N/A"

            results.append({
                "id": opp_id,
                "title": title,
                "link": link,
                "organization": organization,
                "location": location_text,
                "description": description,
                "posted_date": posted_date
            })

        except Exception as e:
            print(f"Error parsing opp {i}: {e}")

    # Print results
    for r in results:
        print(r)


# You can also save this data to a database, for example:
# 1. Connect to your MongoDB or SQL database.
# 2. Insert each opportunity into the respective table/collection.

if __name__ == "__main__":
    results = scrape_volunteer()

    # if results:
    #     save_petitions_to_mongo(results)