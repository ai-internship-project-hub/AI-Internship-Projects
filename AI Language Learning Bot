from IPython.display import display, HTML

# HTML + CSS for the interface
html_code = """
<div style="font-family: Arial; text-align:center; background: linear-gradient(135deg, #74ABE2, #5563DE); padding:20px; color:white; border-radius:10px;">
    <h1>🌍 Language Learning Bot</h1>
    <p>Type the word or phrase number to learn translations in multiple languages!</p>
</div>
"""
display(HTML(html_code))

# Expanded translations data
translations = {
    "Hello": {
        "French": "Bonjour", "Spanish": "Hola", "German": "Hallo", "Italian": "Ciao",
        "Hindi": "नमस्ते", "Telugu": "హలో", "Japanese": "こんにちは", "Chinese": "你好"
    },
    "Thank you": {
        "French": "Merci", "Spanish": "Gracias", "German": "Danke", "Italian": "Grazie",
        "Hindi": "धन्यवाद", "Telugu": "ధన్యవాదాలు", "Japanese": "ありがとう", "Chinese": "谢谢"
    },
    "Goodbye": {
        "French": "Au revoir", "Spanish": "Adiós", "German": "Tschüss", "Italian": "Arrivederci",
        "Hindi": "अलविदा", "Telugu": "వీడ్కోలు", "Japanese": "さようなら", "Chinese": "再见"
    },
    "Yes": {
        "French": "Oui", "Spanish": "Sí", "German": "Ja", "Italian": "Sì",
        "Hindi": "हाँ", "Telugu": "అవును", "Japanese": "はい", "Chinese": "是"
    },
    "No": {
        "French": "Non", "Spanish": "No", "German": "Nein", "Italian": "No",
        "Hindi": "नहीं", "Telugu": "కాదు", "Japanese": "いいえ", "Chinese": "不是"
    },
    "Please": {
        "French": "S'il vous plaît", "Spanish": "Por favor", "German": "Bitte", "Italian": "Per favore",
        "Hindi": "कृपया", "Telugu": "దయచేసి", "Japanese": "お願いします", "Chinese": "请"
    },
    "Excuse me": {
        "French": "Excusez-moi", "Spanish": "Perdón", "German": "Entschuldigung", "Italian": "Mi scusi",
        "Hindi": "माफ़ कीजिये", "Telugu": "క్షమించండి", "Japanese": "すみません", "Chinese": "对不起"
    },
    "How are you?": {
        "French": "Comment ça va?", "Spanish": "¿Cómo estás?", "German": "Wie geht es dir?", "Italian": "Come stai?",
        "Hindi": "आप कैसे हैं?", "Telugu": "మీరు ఎలా ఉన్నారు?", "Japanese": "お元気ですか？", "Chinese": "你好吗？"
    },
    "Good night": {
        "French": "Bonne nuit", "Spanish": "Buenas noches", "German": "Gute Nacht", "Italian": "Buona notte",
        "Hindi": "शुभ रात्रि", "Telugu": "శుభ రాత్రి", "Japanese": "おやすみなさい", "Chinese": "晚安"
    },
    "I love you": {
        "French": "Je t'aime", "Spanish": "Te amo", "German": "Ich liebe dich", "Italian": "Ti amo",
        "Hindi": "मैं तुमसे प्यार करता हूँ", "Telugu": "నేను నిన్ను ప్రేమిస్తున్నాను", "Japanese": "愛してる", "Chinese": "我爱你"
    }
}

# Show available phrases
print("\nAvailable phrases:")
for idx, phrase in enumerate(translations.keys(), 1):
    print(f"{idx}. {phrase}")

# Interactive loop
while True:
    choice = input("\nEnter the phrase number (or 'exit' to quit): ").strip()
    if choice.lower() == "exit":
        print("👋 Goodbye! Keep learning!")
        break
    if choice.isdigit() and 1 <= int(choice) <= len(translations):
        phrase = list(translations.keys())[int(choice)-1]
        print(f"\nTranslations for '{phrase}':")
        for lang, trans in translations[phrase].items():
            print(f"  {lang}: {trans}")
    else:
        print("❌ Invalid choice. Try again.")
