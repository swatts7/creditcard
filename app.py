import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        data = []

        # Extracting required information
        labels = soup.find_all('span', class_='cmp-banner-product-right-aligned__feature--subtext cmp-text')
        values = soup.find_all('span', class_='cmp-banner-product-right-aligned__feature--text--number')

        for label, value in zip(labels, values):
            if 'Annual Fee' in label.text:
                data.append(value.text.strip())
            elif 'Interest: Purchases' in label.text:
                data.append(value.text.strip())
            elif 'Interest: Cash Advance' in label.text:
                data.append(value.text.strip())
            elif 'Additional Cardholder' in label.text:
                data.append(value.text.strip())

        return data
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main(urls):
    # CSV file headers
    headers = ['URL', 'Annual Fee', 'Purchase Interest Rate', 'Cash Advance Interest Rate', 'Additional Cardholder Fee']

    with open('credit_card_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for url in urls:
            data = scrape_data(url)
            if data:
                writer.writerow([url] + data)

# List of URLs to scrape
urls = [
    # Add your URLs here
]

main(urls)
