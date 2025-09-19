!pip install flask

import time
import random
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from threading import Thread

# Sentence bank categorized by difficulty
sentences = {
    "Easy": [
        "Typing is fun.",
        "I love Python.",
        "This is simple.",
        "Practice makes perfect."
    ],
    "Medium": [
        "Typing fast helps in coding efficiently.",
        "Accuracy is just as important as speed.",
        "Python is widely used in AI projects."
    ],
    "Hard": [
        "Artificial Intelligence enhances human capability in unprecedented ways.",
        "Precision and consistency are crucial for high-speed typing accuracy.",
        "Machine learning models require both data quality and quantity."
    ]
}

# Widgets
difficulty_selector = widgets.Dropdown(
    options=["Easy", "Medium", "Hard"],
    value="Easy",
    description="Difficulty:"
)

start_button = widgets.Button(description="Start Test", button_style='success')
restart_button = widgets.Button(description="Restart", button_style='warning')
text_input = widgets.Textarea(placeholder='Type here...', layout=widgets.Layout(width='100%', height='120px'))
submit_button = widgets.Button(description="Submit", button_style='info')
timer_display = widgets.HTML()
progress_display = widgets.HTML()
live_word_count = widgets.HTML(value="<b>Word Count:</b> 0")
output = widgets.Output()

# Display base UI
ui_box = widgets.VBox([difficulty_selector, start_button, progress_display, timer_display, text_input, live_word_count, submit_button, restart_button, output])
display(ui_box)

# Globals
prompt_sentence = ""
start_time = [None]
test_running = [False]
max_time = 30

# Countdown function
def countdown():
    for t in range(max_time, -1, -1):
        if not test_running[0]:
            break
        timer_display.value = f"<h3 style='color:green;'>Time Left: <span style='color:red;'>{t}</span> seconds</h3>"
        progress_display.value = f"""
        <progress value="{max_time - t}" max="{max_time}" style="width: 100%; height: 20px;"></progress>
        """
        time.sleep(1)
    if test_running[0]:
        on_submit(None)  # Auto-submit when timer ends

# Word count live update
def update_word_count(change):
    words = len(text_input.value.strip().split())
    live_word_count.value = f"<b>Word Count:</b> {words}"

text_input.observe(update_word_count, names='value')

# Start test
def start_test(_):
    global prompt_sentence
    level = difficulty_selector.value
    prompt_sentence = random.choice(sentences[level])
    text_input.value = ""
    text_input.disabled = False
    submit_button.disabled = False
    test_running[0] = True
    start_time[0] = time.time()
    with output:
        clear_output()
        display(HTML(f"""
        <div style="background:#f8f9fa;border-left:5px solid #17a2b8;padding:10px;font-size:18px;">
            <b>📝 Type this sentence:</b><br><br>
            <span style="color:#007bff;">{prompt_sentence}</span>
        </div>
        """))
    # Start timer in a separate thread
    Thread(target=countdown).start()

# Submit test
def on_submit(_):
    if not test_running[0]:
        return
    test_running[0] = False
    text_input.disabled = True
    submit_button.disabled = True

    end_time = time.time()
    user_input = text_input.value.strip()
    time_taken = end_time - start_time[0]
    words = len(user_input.split())
    wpm = round(words / (time_taken / 60), 2)
    correct_chars = sum(1 for a, b in zip(user_input, prompt_sentence) if a == b)
    accuracy = round((correct_chars / len(prompt_sentence)) * 100, 2)

    with output:
        display(HTML(f"""
        <div style="background:#e8f5e9;padding:15px;border-radius:10px;margin-top:10px;">
            <h4 style="color:#28a745;">✅ Your Results:</h4>
            <ul style="font-size:16px;">
                <li>⏱️ <b>Time Taken:</b> {round(time_taken, 2)} seconds</li>
                <li>⌨️ <b>Words Per Minute (WPM):</b> {wpm}</li>
                <li>🎯 <b>Accuracy:</b> {accuracy}%</li>
            </ul>
            <p style="font-style:italic;color:#555;">
                {"🎉 Excellent job!" if accuracy >= 90 else "Keep practicing to improve speed and accuracy!"}
            </p>
        </div>
        """))

# Restart test
def restart_test(_):
    text_input.value = ""
    text_input.disabled = True
    submit_button.disabled = True
    timer_display.value = ""
    progress_display.value = ""
    live_word_count.value = "<b>Word Count:</b> 0"
    output.clear_output()
    test_running[0] = False

# Bind buttons
start_button.on_click(start_test)
submit_button.on_click(on_submit)
restart_button.on_click(restart_test)

# Initially disable inputs
text_input.disabled = True
submit_button.disabled = True
