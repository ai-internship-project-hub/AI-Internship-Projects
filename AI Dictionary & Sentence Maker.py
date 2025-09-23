import nltk
from nltk.corpus import wordnet as wn
from IPython.display import display, HTML

# Check if WordNet is ready
try:
    wn.synsets("test")
    wordnet_ready = True
except:
    wordnet_ready = False

# Take input
word = input("📥 Enter any English word: ").strip().lower()

# Default sentence generator using logic
def generate_sentence(word, pos):
    pos = pos.lower()
    if pos.startswith('n'):  # noun
        return f"I saw a {word} at the park today."
    elif pos.startswith('v'):  # verb
        return f"I love to {word} every morning."
    elif pos.startswith('a'):  # adjective
        return f"The weather is very {word} today."
    elif pos.startswith('r'):  # adverb
        return f"She finished the work {word}."
    else:
        return f"This is a sentence using the word '{word}'."

# Build HTML
if not wordnet_ready:
    html = f"""
    <div style='background-color:#fff0f0; border:2px solid #e74c3c; border-radius:10px; padding:15px; max-width:600px; font-family:Arial; color:#e74c3c;'>
        <h3>⚠️ WordNet is not available.</h3>
        <p>Please run <code>nltk.download('wordnet')</code> once, if space allows.</p>
    </div>
    """
else:
    synsets = wn.synsets(word)
    if synsets:
        html = f"""
        <div style='background-color:#f9f9f9; border:2px solid #4CAF50; border-radius:12px; padding:20px; max-width:700px; font-family:Arial; color:#333; box-shadow:0 4px 8px rgba(0,0,0,0.1);'>
            <h2 style='color:#2c7be5;'>📚 AI Dictionary & Sentence Maker</h2>
            <h3 style='color:#4CAF50;'>🔤 Word: <span style='color:#111;'>{word}</span></h3>
        """

        for i, syn in enumerate(synsets[:1]):  # only first meaning
            definition = syn.definition()
            pos = syn.pos()
            sentence = generate_sentence(word, pos)

            html += f"""
                <p><b>📘 Meaning:</b> {definition}</p>
                <p><b>✍️ Sentence:</b> {sentence}</p>
            """
        html += "</div>"
    else:
        html = f"""
        <div style='background-color:#fff0f0; border:2px solid #e74c3c; border-radius:10px; padding:15px; max-width:600px; font-family:Arial; color:#e74c3c;'>
            <h3>❌ No definitions found for '<b>{word}</b>'.</h3>
        </div>
        """

# Display
display(HTML(html))
