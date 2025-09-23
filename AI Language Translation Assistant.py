!pip install googletrans==4.0.0-rc1

from googletrans import Translator, LANGUAGES
import ipywidgets as widgets
from IPython.display import display, HTML
translator = Translator()
display(HTML("""
    <div style="text-align:center; padding: 20px; background-color:#f2f2f2; border-radius: 10px;">
        <h1 style="color:#4CAF50;">🌍 AI Language Translation Assistant</h1>
        <p style="font-size:16px;">Type any sentence and translate it into your desired language instantly!</p>
    </div>
"""))
input_text = widgets.Textarea(
    placeholder='Type your text here...',
    description='Input:',
    layout=widgets.Layout(width='600px', height='100px')
)

language_dropdown = widgets.Dropdown(
    options=list(LANGUAGES.values()),
    description='Translate to:',
    layout=widgets.Layout(width='300px')
)

translate_button = widgets.Button(
    description='Translate',
    button_style='success',
    layout=widgets.Layout(width='200px')
)

output_area = widgets.Textarea(
    placeholder='Translated text will appear here...',
    description='Output:',
    disabled=True,
    layout=widgets.Layout(width='600px', height='100px')
)
def translate_text(b):
    target_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(language_dropdown.value)]
    result = translator.translate(input_text.value, dest=target_lang_code)
    output_area.value = result.text

translate_button.on_click(translate_text)
display(HTML("<br><hr style='border: 1px solid #ccc'><br>"))
display(input_text)
display(language_dropdown)
display(translate_button)
display(output_area)
