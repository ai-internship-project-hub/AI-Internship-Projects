# 📌 Step 1: Import required libraries
import pandas as pd
import random
from IPython.display import display, HTML
import ipywidgets as widgets

# 📌 Step 2: Define the dataset with more questions per level
data = {
    'Subject': [
        'Maths', 'Maths', 'Maths', 'Maths', 'Maths', 'Maths', 'Maths', 'Maths', 'Maths',
        'Physics', 'Physics', 'Physics', 'Physics', 'Physics', 'Physics', 'Physics', 'Physics', 'Physics',
        'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social', 'Social',
        'English', 'English', 'English', 'English', 'English', 'English', 'English', 'English', 'English',
        'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry', 'Chemistry'
    ],
    'Difficulty': [
        'easy', 'easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard',
        'easy', 'easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard',
        'easy', 'easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard',
        'easy', 'easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard',
        'easy', 'easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard'
    ],
    'Question': [
        # Maths
        'What is 5 + 3?', 'What is 9 - 4?', 'What is 6 × 2?',
        'Solve: 2x + 5 = 13', 'What is the area of a triangle?', 'What is the square root of 81?',
        'Prove Pythagoras theorem.', 'Derive the quadratic formula.', 'Integrate: ∫x^2 dx',

        # Physics
        'State Newton’s First Law.', 'What is speed?', 'What is force?',
        'Explain Ohm’s Law.', 'Define work, power, and energy.', 'State the laws of motion.',
        'Derive equations of motion.', 'Explain Lenz’s Law.', 'Describe the photoelectric effect.',

        # Social
        'Who was Mahatma Gandhi?', 'What is democracy?', 'Who wrote the Indian Constitution?',
        'Explain globalization.', 'What is the UN?', 'Describe the French Revolution.',
        'What caused World War II?', 'Explain Cold War.', 'Describe the role of UNO.',

        # English
        'Write the synonym of “happy”.', 'What is a noun?', 'Correct the sentence: He go to school.',
        'Explain metaphor with example.', 'What is a narrative essay?', 'Describe the main theme of "The Road Not Taken".',
        'Analyze a Shakespearean sonnet.', 'Explain irony in literature.', 'Critically evaluate "Animal Farm".',

        # Chemistry
        'What is H2O?', 'What is an element?', 'Define acid and base.',
        'Balance: H2 + O2 → H2O', 'State Mendeleev’s periodic law.', 'What are isotopes?',
        'Explain covalent bonding.', 'Describe electrolysis.', 'State Le Chatelier’s principle.'
    ]
}

df = pd.DataFrame(data)

# 📌 Step 3: Define the paper generator function
def generate_paper(subject, difficulty, num_questions=4):
    filtered = df[(df['Subject'].str.lower() == subject.lower()) &
                  (df['Difficulty'].str.lower() == difficulty.lower())]

    if filtered.empty:
        return "<p style='color:red;'>No questions found for the selected subject and difficulty level.</p>"

    selected = filtered.sample(min(num_questions, len(filtered)), random_state=random.randint(0, 9999))

    html_content = f"""
    <div style='
        border: 2px solid #2c3e50;
        padding: 20px;
        border-radius: 10px;
        background-color: #f4faff;
        font-family: Arial;
        max-width: 700px;
    '>
    <h2 style='color: #2980b9;'>📝 Generated Question Paper</h2>
    <p><b>Subject:</b> {subject.title()}</p>
    <p><b>Difficulty:</b> {difficulty.title()}</p>
    <ol>
    """

    for question in selected['Question']:
        html_content += f"<li>{question}</li>"

    html_content += "</ol></div>"
    return html_content

# 📌 Step 4: Build the interactive HTML interface
subject_input = widgets.Dropdown(
    options=['Maths', 'Physics', 'Social', 'English', 'Chemistry'],
    description='📚 Subject:',
    style={'description_width': 'initial'}
)
difficulty_input = widgets.Dropdown(
    options=['easy', 'medium', 'hard'],
    description='🎯 Difficulty:',
    style={'description_width': 'initial'}
)
button = widgets.Button(description='Generate Paper', button_style='success')
output_area = widgets.Output()

def on_button_click(b):
    with output_area:
        output_area.clear_output()
        subject = subject_input.value
        difficulty = difficulty_input.value
        result = generate_paper(subject, difficulty)
        display(HTML(result))

button.on_click(on_button_click)

# 📌 Step 5: Display the interface
display(subject_input, difficulty_input, button, output_area)
