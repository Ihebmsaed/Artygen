import google.generativeai as genai
import os

# Test avec la clé API du fichier .env
api_key = "AIzaSyDRys-PkwoyPksHIGM0AO8XMYhqrYcZIQI"

print(f"Testing API Key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Dis bonjour en une phrase")
    print("\n✅ SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    if "429" in str(e) or "RATE_LIMIT_EXCEEDED" in str(e):
        print("\n⚠️  Cette clé API a également un quota dépassé.")
        print("Vous devez obtenir une nouvelle clé API sur: https://aistudio.google.com/app/apikey")
