import requests

TOKEN = '7769667614:AAGP7ei6UvquxrjiwBJZ0q7TpGn1aC7JaxI'
USERNAME = 'your_pythonanywhere_username'  # 🔁 Replace with your actual username
URL = f"https://{USERNAME}.pythonanywhere.com/{TOKEN}"

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
print(response.json())
