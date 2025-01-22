import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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
        # Extract the 'a' tag for ID, title, and URL
        a_tag = div.find("a")
        if a_tag:
            bill_id = a_tag.text.strip()
            bill_title = a_tag.next_sibling.strip() if a_tag.next_sibling else None
            bill_url = base_url + a_tag["href"]

            # Extract the status (if available)
            status_tag = div.find("span", class_="tag")
            bill_status = status_tag.text.strip() if status_tag else "Unknown"

            # Append the extracted data
            bills.append({
                "id": bill_id,
                "title": bill_title,
                "url": bill_url,
                "status": bill_status,
            })

    return bills

def scrape_bill_details(driver, bills):
    """Scrape individual bill details."""
    bill_details = []
    for bill in bills:
        driver.get(bill["url"])
        time.sleep(2)  # Allow page to load
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract subtitle
        subtitle = soup.select_one("div.main-col h3")
        subtitle_text = subtitle.text.strip() if subtitle else "N/A"
        
        # Extract summary
        summary = soup.select_one("div.bill_summary p")
        summary_text = summary.text.strip() if summary else "N/A"
        
        # Extract full text URL (if available)
        full_text_link = soup.select_one("a[href*='DocumentViewer']")
        full_text_url = full_text_link["href"] if full_text_link else "N/A"
        
        # Append detailed information
        bill_details.append({
            "id": bill["id"],
            "title": bill["title"],
            "bill_url": bill["url"],
            "status": bill["status"],
            "subtitle": subtitle_text,
            "summary": summary_text,
            "full_text_url": full_text_url,
        })

    return bill_details

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Initialize WebDriver
    driver = get_chromedriver()

    try:
        # Step 1: Scrape the list of bills
        bills = scrape_bills_list(driver)
        print(f"Scraped {len(bills)} bills.")

        # Step 2: Scrape details for each bill
        detailed_bills = scrape_bill_details(driver, bills)
        print(f"Scraped details for {len(detailed_bills)} bills.")

        # Save results to a JSON file
        save_to_json(detailed_bills, "bills_details.json")
        print("Saved detailed bill data to 'bills_details.json'.")

    finally:
        driver.quit()
