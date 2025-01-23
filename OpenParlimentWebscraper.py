import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_chromedriver():
    """Initialize ChromeDriver for Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service("/usr/bin/chromedriver")  # Update this to your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_bills_list(driver):
    """Scrape the main bills page."""
    base_url = "https://openparliament.ca"
    driver.get(base_url + "/bills/")
    time.sleep(2)  # Allow page to load

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find all bill containers
    bill_divs = soup.select("div.column.column-block.twoline.overflowtip")

    # Extract bill data
    bills = []
    for div in bill_divs:
        a_tag = div.find("a")
        if a_tag:
            bill_id = a_tag.text.strip()
            bill_title = a_tag.next_sibling.strip() if a_tag.next_sibling else None
            bill_url = base_url + a_tag["href"]
            status_tag = div.find("span", class_="tag")
            bill_status = status_tag.text.strip() if status_tag else "Unknown"

            bills.append({
                "id": bill_id,
                "title": bill_title,
                "url": bill_url,
                "status": bill_status,
            })

    return bills

def scrape_bill_details(bill):
    """Scrape detailed information for a single bill."""
    driver = get_chromedriver()
    try:
        driver.get(bill["url"])
        time.sleep(2)  # Allow page to load
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract subtitle
        subtitle_tag = soup.find("h3")
        bill["subtitle"] = subtitle_tag.text.strip() if subtitle_tag else "No subtitle available"

        # Extract summary
        summary_tag = soup.select_one("div.bill_summary p")
        bill["summary"] = summary_tag.text.strip() if summary_tag else "No summary available"
    finally:
        driver.quit()

    return bill

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    driver = get_chromedriver()
    try:
        # Step 1: Scrape the list of bills
        bills = scrape_bills_list(driver)
        print(f"Scraped {len(bills)} bills from the main page.")

        # Step 2: Scrape detailed info for each bill in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:  # Reduced to 4 threads
            detailed_bills = list(executor.map(scrape_bill_details, bills))

        # Step 3: Save the detailed bills to a JSON file
        save_to_json(detailed_bills, "detailed_bills.json")
        print("Saved detailed bill data to 'detailed_bills.json'.")
    finally:
        driver.quit()
