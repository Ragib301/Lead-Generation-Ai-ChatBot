import requests

GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"


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
