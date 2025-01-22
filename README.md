# OpenParliament Webscraper 🕵️‍♂️

This project is a web scraper for [OpenParliament.ca](https://openparliament.ca), designed to extract information about Canadian parliamentary bills, their statuses, and related summaries. The project leverages Python, Selenium, and BeautifulSoup for web scraping and was developed with AI assistance to streamline the development process.

## Features
- **Scrapes a list of bills** from OpenParliament.ca.
- **Extracts detailed information** from each bill's page, including:
  - Bill ID and title
  - Status (e.g., Law, Pending, Dormant)
  - Summary and subtitle
  - Sponsor details
  - Related links (e.g., full text of the bill).
- **Generates a structured JSON output**, making the data easy to use in other applications or analyses.
- Built with **support for parallelization** to improve scraping performance.

## Technologies Used
- **Python 3**
- **Selenium**: For automated browsing.
- **BeautifulSoup (bs4)**: For HTML parsing and data extraction.
- **Chromium and ChromeDriver**: To support Selenium-based automation.
- **Threading and Queue**: For parallelization to speed up the scraping process.

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Chromium and ChromeDriver installed. If you're using WSL, follow these steps:
  ```bash
  sudo apt update
  sudo apt install -y chromium-browser chromedriver


## Steps
Clone the repository:

git clone https://github.com/your-username/OpenParliamentWebscraper.git
cd OpenParliamentWebscraper

Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Verify your installation:
Ensure chromium-browser and chromedriver are installed:

chromium-browser --version
chromedriver --version

Confirm that chromedriver is in /usr/bin/chromedriver

## Running the Script
To run the scraper:

python OpenParliamentWebscraper.py

## Example Output:

The script generates 2 JSON files (bills_list.json), (bill_details.json) with the following structure:

[
  {
    "id": "C-40",
    "title": "Miscarriage of Justice Review Commission Act",
    "bill_url": "https://openparliament.ca/bills/44-1/C-40/",
    "status": "Law",
    "subtitle": "An Act to amend the Criminal Code...",
    "summary": "This enactment amends the Criminal Code to...",
    "full_text_url": "https://www.parl.ca/documentviewer/en/44-1/bill/C-40/royal-assent"
  }

   {
        "id": "C-79",
        "title": "",
        "bill_url": "https://openparliament.ca/bills/44-1/C-79/",
        "status": "Law",
        "subtitle": "An Act for granting to His Majesty certain sums of money for the federal public administration for the fiscal year ending March 31, 2025",
        "summary": "This enactment grants the sum of $21,632,370,126 towards defraying charges and expenses of the federal public administration for the fiscal year ending March 31, 2025 that are not otherwise provided for.",
        "full_text_url": "https://www.parl.ca/DocumentViewer/en/13531587"
    },
]
