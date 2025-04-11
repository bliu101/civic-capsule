# import time
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup

# def scrape_volunteer():
#     # Setup selenium webdriver (make sure you have chromedriver installed)
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Running in headless mode for scraping without GUI
#     driver = webdriver.Chrome(options=options)

#     # Define the URL of the site to scrape
#     url = "https://www.volunteermatch.org/search/?l=Boston,%20MA,%20USA"

#     # Navigate to the page
#     driver.get(url)
#     time.sleep(5)  # Allow the page to fully load

#     # Scroll down to load more opportunities (if needed)
#     # You can adjust the number of times the page scrolls for more results
#     for _ in range(3):  # Scroll 3 times (adjust as necessary)
#         driver.execute_script("window.scrollBy(0, 1000);")
#         time.sleep(2)

#     # Parse the page source with BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Find all opportunities (list items with volunteering opportunities)
#     opportunities = soup.find_all('li')
#     print("OPPORTUNITIES? ", opportunities)

#     # Create a list to hold the scraped data
#     data = []

#     # Loop through each opportunity and extract relevant information
#     for opp in opportunities:
#         opp_id = opp.get('id', '')
#         title = opp.find('a', class_='pub-srp-opps__title').text.strip()
#         link = 'https://www.volunteermatch.org' + opp.find('a', class_='pub-srp-opps__title')['href']
#         org_name = opp.find('a', class_='blue-drk').text.strip()
#         location = opp.find('div', class_='pub-srp-opps__loc').text.strip()
#         description = opp.find('p', class_='pub-srp-opps__desc').text.strip()
#         date_posted = opp.find('div', class_='pub-srp-opps__posted').text.strip()

#         # Create a dictionary for each opportunity
#         opportunity = {
#             'id': opp_id,
#             'title': title,
#             'link': link,
#             'organization': org_name,
#             'location': location,
#             'description': description,
#             'date_posted': date_posted
#         }

#         # Add this opportunity to the data list
#         data.append(opportunity)

#     # Close the browser once done
#     driver.quit()

#     # Print the data or upload it to a database
#     for opp in data:
#         print(opp)

# # You can also save this data to a database, for example:
# # 1. Connect to your MongoDB or SQL database.
# # 2. Insert each opportunity into the respective table/collection.

# if __name__ == "__main__":
#     results = scrape_volunteer()

#     # if results:
#     #     save_petitions_to_mongo(results)

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.volunteermatch.org"
SEARCH_URL = f"{BASE_URL}/search/?l=Boston,%20MA,%20USA"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_volunteer():
    response = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container div
    container = soup.find('div', class_='col-md-8 pub-srp-opps')

    # Now find the ul inside it (the first ul should be the opportunities list)
    ul = container.find('ul')

    # Then find all li elements inside that ul
    opportunities = ul.find_all('li', recursive=False)

    results = []

    for opp in opportunities:
        try:
            title_tag = opp.find('a', class_='pub-srp-opps__title')
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            link = BASE_URL + title_tag['href'] if title_tag else "N/A"
            opp_id = opp.get('id')
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
            print(f"Error parsing opportunity: {e}")

    # Print results
    for r in results:
        print(r)

if __name__ == "__main__":
    results = scrape_volunteer()

    # if results:
    #     save_petitions_to_mongo(results)
