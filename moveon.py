from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def scrape_moveon_petitions(keyword="boston"):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for speed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the search page
    search_url = f"https://sign.moveon.org/petitions/search?query={keyword}"
    driver.get(search_url)
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
    results = []
    for petition in petitions:
        try:
            title_element = petition.find_element(By.CSS_SELECTOR, "a.title.petition-title")
            title = title_element.text.strip()
            url = "https://sign.moveon.org" + title_element.get_attribute("href")
            description = petition.find_element(By.CSS_SELECTOR, "div.petition-why").text.strip()
            creator = petition.find_element(By.CSS_SELECTOR, "div.petition-creator span.name").text.strip()
            signature_info = petition.find_element(By.CSS_SELECTOR, "div.petition-signatures").text.strip()
            
            results.append({
                "title": title,
                "url": url,
                "description": description,
                "creator": creator,
                "signature_info": signature_info
            })
        except Exception as e:
            print(f"Error parsing petition: {e}")
            continue

    driver.quit()
    print("RESULTS::", results)
    return results


# Example usage
if __name__ == "__main__":
    keyword = "boston"
    petitions = scrape_moveon_petitions(keyword)
    for p in petitions:
        print(f"Title: {p['title']}")
        print(f"URL: {p['url']}")
        print(f"Creator: {p['creator']}")
        print(f"Description: {p['description']}\n")
