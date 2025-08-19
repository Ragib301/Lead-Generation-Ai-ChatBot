from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
from time import sleep
import streamlit as st
import re
import os


class LeadScraper:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")

        user_dir = os.path.expanduser("~")
        profile_path = os.path.join(
            user_dir, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
        firefox_profile_path = os.path.join(
            profile_path, "jdp28fs1.default-release")
        profile = FirefoxProfile(firefox_profile_path)

        if not os.path.exists(firefox_profile_path):
            raise FileNotFoundError(f"Firefox profile not found at: {firefox_profile_path}")

        options.profile = profile
        self.driver = webdriver.Firefox(options=options)
        self.driver.maximize_window()

        self.progress_bar = st.progress(
            0, text="Lead Generation in Progress...")


    def _build_google_query(self, search_query, platform_domains):
        domains = " OR ".join([f'site:{d}' for d in platform_domains])
        emails = '"@gmail.com" OR  "@yahoo.com" OR "@outlook.com"'
        return f'{domains} "{search_query}" {emails}'


    def _visit_page(self, url):
        self.driver.get(url)
        sleep(5)
        if re.search(r'facebook\.com', url, re.IGNORECASE):
            try:
                see_more_buttons = self.driver.find_elements(
                    By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/span/div")
                for btn in see_more_buttons:
                    self.driver.execute_script("arguments[0].click();", btn)

            except Exception as e:
                print(f"[Facebook See More Error: {e}]")

        elif re.search(r'instagram\.com', url, re.IGNORECASE):
            try:
                see_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/section/main/div/header/section[4]/div/span/span/div/span")
                    )
                )
                self.driver.execute_script(
                    "arguments[0].click();", see_more_button)

            except Exception as e:
                print(f"[Instagram See More giving Error!]")
        sleep(2)


    def _scrape_contact_info(self, primary_info):
        final_info = []
        for info_dict in primary_info:
            name = info_dict['name']
            url = info_dict['url']

            self._visit_page(url)
            text = self.driver.find_element(By.TAG_NAME, "body").text

            email_pattern = re.compile(
                r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.IGNORECASE)
            phone_pattern = re.compile(
                r'(?:(?:\+?\d{1,3}[-.\s]*)?(?:\(?\d{2,4}\)?[-.\s]*)?\d{3,4}[-.\s]?\d{4})'
            )
            website_pattern = re.compile(
                r'(https?://(?:www\.)?[^\s/$.?#].[^\s]*)', re.IGNORECASE
            )

            emails = list(set(email_pattern.findall(text)))
            phones = list(set(phone_pattern.findall(text)))
            websites = list(set(
                w for w in website_pattern.findall(text)
                if not url.lower().startswith(w.lower())
            ))

            final_info_dict = {
                "name": name,
                "url": url,
                "emails": emails,
                "phones": phones,
                "websites": websites,
            }
            final_info.append(final_info_dict)
            self.progress_bar.progress((len(final_info)/len(primary_info)),
                                       text=f"Leads Collected: {len(final_info)}/{len(primary_info)+1}...")

        return final_info


    def scrape_leads(self, search_query, platform_domains, max_results=20):
        query = self._build_google_query(search_query, platform_domains)
        url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"
        self.driver.get(url)
        sleep(5)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        listings = soup.find_all('div', class_='b8lM7')

        st.markdown("Start fetching primary infos...")
        if listings:
            primary_info = []
            for listing in listings:
                name_div = listing.find('span', class_='VuuXrf').text
                match = re.search(r'·\s*(.+)', name_div)
                name = match.group(1) if match else ''

                a_tag = listing.find('a', class_='zReHs')
                url = a_tag.get('href', '').strip()

                info_dict = {
                    'name': name,
                    'url': url,
                }
                if url:
                    primary_info.append(info_dict)

        st.markdown("Start collecting contact infos...")
        lead_info = self._scrape_contact_info(primary_info)
        return lead_info


    def close(self):
        self.progress_bar.empty()
        self.driver.quit()


if __name__ == "__main__":
    scraper = LeadScraper(headless=True)
    results = scraper.scrape_leads(search_query='fitness coaches',
                                   platform_domains=[
                                       'facebook.com', 'linkedin.com', 'instagram.com'],
                                   max_results=50)
    print(results)
    scraper.close()

    df = pd.DataFrame(results)
    df.to_csv('lead_informations.csv', index=False)
    print("CSV file 'lead_informations.csv' created successfully.")
