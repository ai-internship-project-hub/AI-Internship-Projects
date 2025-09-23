!pip install flask nest_asyncio textblob --quiet

import nest_asyncio
nest_asyncio.apply()

from flask import Flask, request, render_template_string, session
from textblob import TextBlob
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to use session

# Interview Questions
questions = {
    "Software Engineer": [
        "Tell me about yourself.",
        "What programming languages are you comfortable with?",
        "Describe a challenging coding problem you faced.",
        "Why do you want to work at our company?",
        "Where do you see yourself in 5 years?"
    ],
    "Data Analyst": [
        "What are the key steps in data cleaning?",
        "Which tools do you use for data visualization?",
        "How do you handle missing data?",
        "Describe a data project you've worked on."
    ],
    "AI Intern": [
        "What is your understanding of AI and its applications?",
        "How would you explain machine learning to a non-technical person?",
        "Tell us about a mini project you’ve built in AI.",
        "What are ethical concerns in using AI?"
    ],
    "Web Developer": [
        "What tech stack are you comfortable with?",
        "How do you optimize website performance?",
        "Explain how you manage responsive design.",
        "What is the difference between REST and GraphQL?"
    ]
}

# Appreciation messages
appreciations = [
    "🎉 Well done! You gave a thoughtful answer.",
    "👏 Great effort! Your response was meaningful.",
    "👍 Good job! You’re on the right track.",
    "🔥 Impressive! Keep up the confidence.",
    "💡 Nice explanation! Shows your clarity."
]

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Virtual Job Interview Coach</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef1f5;
            text-align: center;
            padding: 40px;
        }
        h1 {
            color: #222;
        }
        form {
            background: #fff;
            padding: 30px;
            margin-top: 20px;
            border-radius: 10px;
            display: inline-block;
            width: 500px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        }
        select, textarea {
            width: 100%;
            padding: 10px;
            margin-top: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 20px;
            background: #3498db;
            border: none;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .feedback {
            margin-top: 20px;
            font-size: 17px;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>🤖 AI Virtual Job Interview Coach</h1>
    <form method="POST">
        <label>Select a Role:</label>
        <select name="role" required onchange="this.form.submit()">
            <option value="">-- Choose a Role --</option>
            {% for r in roles %}
                <option value="{{ r }}" {% if r == selected_role %}selected{% endif %}>{{ r }}</option>
            {% endfor %}
        </select>

        {% if question %}
            <p><strong>Question:</strong> {{ question }}</p>
            <textarea name="answer" placeholder="Type your answer here..." rows="5" required></textarea>
            <br><button type="submit">Submit Answer</button>
        {% endif %}
    </form>

    {% if feedback %}
        <div class="feedback">
            <p><strong>Feedback:</strong> {{ feedback }}</p>
            <p>{{ appreciation }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    appreciation = ""
    role = ""
    question = ""

    if request.method == "POST":
        role = request.form.get("role", "")
        answer = request.form.get("answer", "")

        if answer:  # If answer submitted
            question = session.get("question", "")
            analysis = TextBlob(answer).sentiment
            if analysis.polarity > 0.5:
                feedback = "✅ Great! You sound confident and positive."
            elif analysis.polarity < 0:
                feedback = "⚠️ Try to use more positive language."
            else:
                feedback = "🟡 Neutral response. Try adding more enthusiasm or detail."
            feedback += f" (Polarity: {analysis.polarity:.2f}, Subjectivity: {analysis.subjectivity:.2f})"
            appreciation = random.choice(appreciations)
            session.pop("question", None)  # Reset question after feedback
        else:  # Role selected or re-selected
            question = random.choice(questions.get(role, []))
            session["question"] = question

    elif request.method == "GET":
        session.pop("question", None)

    question = session.get("question", question)
    return render_template_string(html_template, roles=questions.keys(), selected_role=role, question=question, feedback=feedback, appreciation=appreciation)

# Run Flask App in Notebook
from threading import Thread
def run():
    app.run(port=5000)
Thread(target=run).start()
