import requests

url = "https://chatbot-faq.onrender.com/chat"  # mets bien TON URL
question = {"question": "Quels documents dois-je fournir ?"}
response = requests.post(url, json=question)
print(response.json())
