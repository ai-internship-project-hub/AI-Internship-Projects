!pip install flask sumy

from flask import Flask, request, render_template_string
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Visual Note Generator</title>
    <style>
        body { font-family: Arial; margin: 40px; background-color: #f0f4f8; }
        textarea { width: 100%; height: 150px; padding: 10px; font-size: 16px; }
        .container { max-width: 800px; margin: auto; }
        .output-box { background: #fff; padding: 20px; margin-top: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
<div class="container">
    <h1>📚 AI Visual Note Generator</h1>
    <form method="POST">
        <label><strong>Enter Your Lecture Notes/Text:</strong></label><br>
        <textarea name="text">{{ request.form.get('text', '') }}</textarea><br><br>
        <button type="submit">Generate Notes</button>
    </form>

    {% if summary %}
    <div class="output-box">
        <h2>📝 Summarized Notes:</h2>
        <p>{{ summary }}</p>
    </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        input_text = request.form['text']
        parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 3)
        summary = ' '.join(str(sentence) for sentence in summary_sentences)

    return render_template_string(TEMPLATE, summary=summary)

if __name__ == '__main__':
    app.run(debug=False)
