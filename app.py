
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import pandas as pd

# Streamlit app layout
st.title("Credit Card Information Extractor")

# User inputs
api_key = st.text_input("Enter your OpenAI API Key")
url_input = st.text_area("Enter URLs (one per line)")
if st.button("Extract Data"):
    if not api_key or not url_input:
        st.warning("Please provide both API Key and URLs.")
    else:
        data = []
        urls = url_input.split('\n')
        for url in urls:
            try:
                # Scraping web page content
                response = requests.get(url)
                content = response.text

                # OpenAI API request for each piece of data
                openai.api_key = api_key
                questions = ["What is the annual fee?", 
                             "What is the purchase interest rate?",
                             "What is the cash advance interest rate?",
                             "What is the additional card holder fee?"]

                answers = []
                for question in questions:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=f"Extract the following information from the text: {question}\n\n{content}",
                        max_tokens=50
                    )
                    answers.append(response.choices[0].text.strip())

                # Appending results
                data.append([url] + answers)
            except Exception as e:
                st.error(f"Error processing {url}: {str(e)}")

        # Creating DataFrame and downloading Excel file
        df = pd.DataFrame(data, columns=["URL", "Annual Fee", "Purchase Interest Rate", 
                                         "Cash Advance Interest Rate", "Additional Card Holder Fee"])
        st.dataframe(df)
        df.to_excel("credit_card_info.xlsx", index=False)
        st.download_button("Download Data", "credit_card_info.xlsx")


