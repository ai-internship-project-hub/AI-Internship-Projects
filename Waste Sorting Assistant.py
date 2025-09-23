!pip install pyttsx3 speechrecognition

# Waste Sorting Assistant: Enhanced Version 🌍

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from IPython.display import display, HTML
import pyttsx3
import speech_recognition as sr

# 🖼️ Stylish title
display(HTML("""
<h1 style="text-align:center; color:darkgreen; font-family:Arial;">♻️ AI WASTE SORTING ASSISTANT 🧠</h1>
<h3 style="text-align:center; color:#555;">Know where your waste belongs!</h3>
<hr style="border-top: 3px solid #aaa;">
"""))

# 🎯 Training dataset
items = [
    ("banana peel", "Organic"),
    ("apple core", "Organic"),
    ("plastic bottle", "Recyclable"),
    ("newspaper", "Recyclable"),
    ("cardboard box", "Recyclable"),
    ("egg shell", "Organic"),
    ("glass jar", "Recyclable"),
    ("tea bags", "Organic"),
    ("toilet paper", "Organic"),
    ("aluminum foil", "Recyclable"),
    ("leaves", "Organic"),
    ("pen", "Recyclable"),
    ("cotton pads", "Organic"),
    ("detergent packet", "Recyclable"),
    ("vegetable scraps", "Organic"),
    ("paper cup", "Recyclable"),
]

X = [x[0] for x in items]
y = [x[1] for x in items]

# 🧠 Model
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)
model = MultinomialNB()
model.fit(X_vec, y)

# 🔊 Voice engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# 🎤 Voice input (optional)
def listen_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now:")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("⚠️ Voice service error.")
        return ""

# 🧠 Prediction + Styling
def predict_waste(item_name):
    vec = vectorizer.transform([item_name])
    result = model.predict(vec)[0]

    if result == "Recyclable":
        display(HTML(f"""
        <div style="padding:10px; background-color:#e0f7fa; border-left:6px solid green;">
        <b>🔍 Item:</b> {item_name.title()} <br>
        <b>✅ Type:</b> <span style='color:green;'>Recyclable ♻️</span>
        </div><br>
        """))
        engine.say(f"{item_name} is Recyclable")
    elif result == "Organic":
        display(HTML(f"""
        <div style="padding:10px; background-color:#fff3e0; border-left:6px solid brown;">
        <b>🔍 Item:</b> {item_name.title()} <br>
        <b>🌱 Type:</b> <span style='color:brown;'>Organic Waste 🍃</span>
        </div><br>
        """))
        engine.say(f"{item_name} is Organic")
    engine.runAndWait()

# 🚀 User interaction
while True:
    print("\n📝 Enter a waste item (or 'exit' to quit):")
    user_input = input("👉 Your input: ").strip().lower()

    if user_input == "exit":
        print("👋 Thank you for using Waste Sorting Assistant!")
        engine.say("Thank you for using Waste Sorting Assistant")
        engine.runAndWait()
        break
    elif user_input == "voice":
        item_spoken = listen_input().lower()
        if item_spoken:
            predict_waste(item_spoken)
    elif user_input:
        predict_waste(user_input)
