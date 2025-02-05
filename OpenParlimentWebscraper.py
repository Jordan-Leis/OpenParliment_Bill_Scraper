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
    """Scrape the main bills page and collect basic info."""
    base_url = "https://openparliament.ca"
    driver.get(base_url + "/bills/")
    time.sleep(2)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    bill_divs = soup.select("div.column.column-block.twoline.overflowtip")

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
    """Scrape detailed information for a single bill, including status."""
    driver = get_chromedriver()
    try:
        driver.get(bill["url"])
        time.sleep(3)  # Allow page to load completely
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract subtitle
        subtitle_tag = soup.find("h3")
        bill["subtitle"] = subtitle_tag.text.strip() if subtitle_tag else "No subtitle available"

        # Extract summary
        summary_tag = soup.select_one("div.bill_summary p")
        bill["summary"] = summary_tag.text.strip() if summary_tag else "No summary available"

        # ✅ Extracting Status
        status_div = soup.find("h2", string="Status")
        if status_div:
            status_p = status_div.find_next("div", class_="main-col").find("p")
            if status_p:
                bill["status"] = status_p.text.strip()
            else:
                bill["status"] = "Unknown (Status header found, but no text)"
        else:
            bill["status"] = "Unknown (No 'Status' section found)"

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
        bills = scrape_bills_list(driver)
        print(f"Scraped {len(bills)} bills from the main page.")

        # ✅ Multi-threaded processing for faster scraping (keep around 4 threads)
        with ThreadPoolExecutor(max_workers=4) as executor:
            detailed_bills = list(executor.map(scrape_bill_details, bills))

        save_to_json(detailed_bills, "detailed_bills.json")
        print("✅ Successfully saved data to 'detailed_bills.json'.")
    finally:
        driver.quit()
