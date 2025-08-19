import streamlit as st
import pandas as pd
import re
import base64
from json import loads
from lead_gen import LeadScraper
from gemini_chatbot import chatbot


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "collected_data" not in st.session_state:
    st.session_state.collected_data = {
        "search_query": None, "platforms": [], "max_results": 10}
if "leads" not in st.session_state:
    st.session_state.leads = None


@st.cache_data
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{b64_encoded});
                background-size: cover;
            }}
            </style>
        """
        st.markdown(style, unsafe_allow_html=True)


st.set_page_config(page_title="Lead Geneartion AI ChatBot")
st.title("🤖 Lead Generation Ai Chatbot")
set_background('bg.jpg')


with st.chat_message("ai"):
    st.markdown(
        """Hi there! I'm your Lead Generation Ai Assistant Chatbot. 
    Just tell me what kind of leads you're looking for, which platforms to 
    search (Facebook, Instagram, LinkedIn), and how many results you want.""")


for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])


user_input = st.chat_input("Ask me to find leads for you...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    response = chatbot(user_input)
    st.chat_message("ai").markdown(response)
    st.session_state.chat_history.append({"role": "ai", "text": response})

    try:
        match = re.search(r"\{.*?\}", response, re.DOTALL)
        if match:
            data = loads(match.group(0))
            st.session_state.collected_data = data

            with st.spinner("Starting to generate your desired leads, please wait..."):
                scraper = LeadScraper(headless=True)
                leads = scraper.scrape_leads(
                    data["search_query"],
                    data["platform_domains"],
                    max_results=int(data.get("max_results", 10))
                )
            scraper.close()
            st.session_state.leads = leads

    except Exception as e:
        st.error("Something went wrong while interpreting your request or scraping.")
        st.exception(e)


if st.session_state.leads:
    leads_df = pd.DataFrame(st.session_state.leads)
    st.success(f"Success! {len(leads_df)+1} Leads Collected!")
    st.dataframe(leads_df)

    csv = leads_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "lead_information.csv", "text/csv")
