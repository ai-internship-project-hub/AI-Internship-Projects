!pip install ipywidgets

import random
from IPython.display import display, HTML, Markdown
import ipywidgets as widgets

# Question Bank
question_bank = {
    "SDE": [
        "What is a linked list? How does it differ from an array?",
        "Explain polymorphism in OOP.",
        "What is a deadlock? How to avoid it?",
        "Explain time complexity with an example."
    ],
    "HR": [
        "What motivates you to work?",
        "Tell me about a conflict and how you resolved it.",
        "Why do you want to join our company?",
        "How do you handle pressure at work?"
    ],
    "Analyst": [
        "What tools do you use for data visualization?",
        "What is the difference between variance and standard deviation?",
        "Explain hypothesis testing.",
        "How would you clean a messy dataset?"
    ],
    "Marketing": [
        "What is a marketing funnel?",
        "How do you measure campaign success?",
        "What is customer segmentation?",
        "Explain AIDA model in marketing."
    ],
    "Finance": [
        "What is working capital?",
        "Explain ROI and how to calculate it.",
        "What is the difference between budgeting and forecasting?",
        "What are financial statements?"
    ],
    "Data Scientist": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain precision vs recall.",
        "How do you handle imbalanced datasets?",
        "What is feature selection?"
    ]
}

# UI Elements
role_dropdown = widgets.Dropdown(
    options=list(question_bank.keys()),
    description='Role:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='50%')
)

ask_button = widgets.Button(description="Generate Question", button_style='success')
answer_input = widgets.Textarea(placeholder="Type your answer here...", layout=widgets.Layout(width='100%', height='100px'))
rate_button = widgets.Button(description="Submit Answer", button_style='info')
output_box = widgets.Output()

# Display heading
display(HTML("<h2 style='text-align:center; color:darkblue;'>Interview Question Generator</h2>"))

# Show widgets
display(role_dropdown, ask_button, output_box)

# Show answer input and rating after question is asked
def rate_answer(btn):
    user_answer = answer_input.value
    length = len(user_answer.split())
    if length < 10:
        feedback = "❌ Too short. Try to elaborate more."
    elif length < 30:
        feedback = "✅ Decent. You could add more detail."
    else:
        feedback = "🌟 Excellent! Very detailed."
    
    with output_box:
        display(Markdown(f"**📝 Your Answer Feedback:** {feedback}"))

# Generate Question
def show_question(btn):
    role = role_dropdown.value
    question = random.choice(question_bank[role])
    
    output_box.clear_output()
    with output_box:
        display(Markdown(f"### ❓ Question for **{role}**:\n> {question}"))
        display(answer_input)
        display(rate_button)

# Link buttons
ask_button.on_click(show_question)
rate_button.on_click(rate_answer)

        show_question(user_role)
        rate_answer()
    else:
        print("Invalid role.")
