from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc



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

def stealth_scrape_volunteermatch():
    options = uc.ChromeOptions()
    # Don't use headless for now — VolunteerMatch may detect it
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"
    driver.get(url)

    # Wait for content to load
    time.sleep(5)

    # Find the container and list items
    try:
        container = driver.find_element(By.CSS_SELECTOR, "div.col-md-8.pub-srp-opps")
        cards = container.find_elements(By.CSS_SELECTOR, "li")
        print(f"✅ Found {len(cards)} opportunity cards")

        for card in cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
                org_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__org-name")
                loc_elems = card.find_elements(By.CSS_SELECTOR, ".pub-srp-opps__loc")

                opportunity = {
                    "title": title_elem.text.strip(),
                    "organization": org_elems[0].text.strip() if org_elems else "N/A",
                    "location": loc_elems[0].text.strip() if loc_elems else "N/A",
                    "link": title_elem.get_attribute("href"),
                }
            except Exception as e:
                print(f"⚠️ Skipped one card: {e}")

    except Exception as e:
        print(f"❌ Could not find container: {e}")

    driver.quit()

if __name__ == "__main__":
    # results = scrape_volunteermatch_boston()
    # for r in results:
    #     print(r)
    stealth_scrape_volunteermatch()