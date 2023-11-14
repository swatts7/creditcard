
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting data using the specified classes
        data = {}
        data['URL'] = url
        data['Annual Fee'] = soup.find("span", class_="cmp-banner-product-right-aligned__feature--text--number", string="Annual Fee").find_next_sibling("span").text.strip()
        data['Purchase Interest Rate'] = soup.find("span", class_="cmp-banner-product-right-aligned__feature--text--number", string="Interest: Purchases").find_next_sibling("span").text.strip()
        data['Cash Advance Interest Rate'] = soup.find("span", class_="cmp-banner-product-right-aligned__feature--text--number", string="Interest: Cash Advance").find_next_sibling("span").text.strip()
        data['Additional Cardholder Fee'] = soup.find("span", class_="cmp-banner-product-right-aligned__feature--text--number", string="Additional Cardholder").find_next_sibling("span").text.strip()
        return data
    except Exception as e:
        return {"URL": url, "Error": str(e)}

def main():
    st.title("Credit Card Info Extractor")
    
    # Text area for input URLs
    urls = st.text_area("Enter the URLs (one per line)")
    if urls:
        url_list = urls.split("\n")
        
        # Button to start scraping
        if st.button("Scrape Data"):
            results = [scrape_data(url) for url in url_list]
            df = pd.DataFrame(results)
            st.write(df)
            
            # Download link for CSV
            csv = df.to_csv(index=False)
            st.download_button(label="Download data as CSV",
                               data=csv,
                               file_name='credit_card_data.csv',
                               mime='text/csv')

if __name__ == "__main__":
    main()
