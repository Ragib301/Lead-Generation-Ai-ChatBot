# Lead-Generation-AI-Tool

An AI-powered Python tool that automates **Lead Generation** by combining conversational AI with web scraping. It features a clean **Streamlit UI**, query parsing with **Gemini API**, dynamic scraping with **Selenium**, and structured export with **Pandas**. Ideal for businesses, marketers, and students aiming to streamline contact discovery.

---
## 🚀 Features

* Conversational AI chatbot interface (Streamlit)
* Collects search queries, online platforms, and number of results
* Google-powered search queries with site filters
* Automated web scraping via Selenium
* AI-assisted data cleanup (Gemini)
* Extracts contact info: Emails, Phone numbers, Websites, Source URL
* Clean CSV export of lead infos
* Persistent chat history in UI

---
## 🧪 How It Works

1. User interacts with chatbot in Streamlit UI.
2. Gemini API parses natural-language prompts into structured parameters (search query, platforms, result count).
3. Google search is automated with `site:instagram.com` / `site:linkedin.com` queries, filtered by email domains.
4. Selenium navigates result pages and scrapes data.
5. Regex extracts emails, phone numbers, and URLs.
6. Gemini cleanups collected data, if any corrupted data in included.
7. Data is compiled with Pandas and exported as a CSV file.

---
## 📸 Screenshots
<img width="1366" height="768" alt="Screenshot (111)" src="https://github.com/user-attachments/assets/77f95c17-377e-4d94-a1a8-379380a58d25" />
<img width="1366" height="768" alt="Screenshot (114)" src="https://github.com/user-attachments/assets/cc55e311-e0eb-41f1-baa6-0a490ad7e273" />
<img width="1366" height="768" alt="Screenshot (115)" src="https://github.com/user-attachments/assets/0cb9d805-3b20-43f3-b713-3d0ca4e31ebf" />
<img width="1366" height="768" alt="Screenshot (117)" src="https://github.com/user-attachments/assets/331030ad-186c-4a02-be5b-3d88596b9fdc" />

---
## ⚙️ Technologies Used
* **Python**: Core backend
* **Streamlit**: Chatbot-style UI
* **Selenium**: Web automation & scraping
* **BeautifulSoup4**: Parsing HTML content
* **Gemini API**: Query parsing & intent extraction
* **Regex**: Lead info extraction
* **Pandas**: CSV creation & export

---
## 🖥️ Code Snippets & Highlights
*   `Gemini API Call & ChatBot` — Extracts structured JSON (query, platforms, number of results)

```python
def chatbot(user_input):
  prompt = f"""
  You are a lead scraping Ai ChatBot. You will interact like a human being 
  to the user. Don't be rude. Behave like a well-behaved human with the user.
  Based on the chats your task is to extract the following 3 things as JSON.
  1. search_query
  2. platform_domains (eg: facebook.com, instagram.com, linkedin.com, x.com)
  3. max_results (integer, default 10)

  Only return the JSON like this:
  {{
    "search_query": "fitness coaches",
    "platform_domains": ["facebook.com", "instagram.com"],
    "max_results": 15
  }}
  Note that, after giving the output JSON, don't say stuffs like "How else I can 
  help you?" or anything like that. Just say "Now I am starting my Ultimate Lead 
  Generation Task" or anything like this.
  Also if the user wants any kind of example from you, only give an example prompt,
  never give the JSON file.

  User Prompt: {user_input}
  """

  payload = {
      "contents": [{"role": "user", "parts": [{"text": prompt}]}]
  }
  headers = {"Content-Type": "application/json"}
  response = requests.post(GEMINI_URL, headers=headers, json=payload)
  try:
      return str(response.json()["candidates"][0]["content"]["parts"][0]["text"])

  except Exception as e:
      return f"Sorry, I couldn't process that: {e}"
```

* `scrape_leads()` — Main Lead Scraping function
```python
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
```

* **`Contact Info` Extraction Regex Patterns**
```python
email_pattern = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', re.IGNORECASE)
phone_pattern = re.compile(r'(?:(?:\+?\d{1,3}[-.\s]*)?(?:\(?\d{2,4}\)?[-.\s]*)?\d{3,4}[-.\s]?\d{4})')
website_pattern = re.compile(r'(https?://(?:www\.)?[^\s/$.?#].[^\s]*)', re.IGNORECASE)
```
---

## 📦 Installation
```bash
git clone https://github.com/yourusername/Lead-Generation-AI-Tool.git
cd Lead-Generation-AI-Tool
pip install -r requirements.txt
streamlit run main.py
```
---

## 📁 Folder Structure
```
📦 Lead-Generation-AI-Tool
├── main.py               # Streamlit chatbot app
├── lead_gen.py           # LeadScraper class with Selenium scraping
├── gemini_chatbot.py     # Gemini ChatBot function
├── requirements.txt      # Dependencies
├── bg.jpg                # Streamlit Background Image
└── README.md             # Documentation
```
---

## 📜 License
MIT License — feel free to fork, modify, and build on it.
---

## 📬 Feedback & Contributions
> Built as a prototype to merge conversational AI with business automation. Contributions are welcome! 🚀
