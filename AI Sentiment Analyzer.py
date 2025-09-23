!pip install textblob
!pip install ipython

from textblob import TextBlob
from IPython.display import display, HTML

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)

    # Set sentiment message and colors
    if polarity > 0:
        sentiment = "Positive"
        response = "That's wonderful to hear! Keep up the positive vibes and stay motivated!"
        bg_color = "#2F855A"  # green
    elif polarity < 0:
        sentiment = "Negative"
        response = "It sounds like you're feeling low. Take a deep breath and remember that things will get better."
        bg_color = "#C53030"  # red
    else:
        sentiment = "Neutral"
        response = "Your message seems neutral. If you ever want to talk or reflect more, I'm here to listen."
        bg_color = "#B7791F"  # amber

    #  HTML Output
    html_content = f"""
    <div style="font-family:Arial; background-color:#1A202C; color:#E2E8F0; max-width:800px; margin:20px auto; padding:30px; border-radius:10px; box-shadow:0 0 15px rgba(0,0,0,0.5);">
        <h1 style="text-align:center; color:#63B3ED;"> Sentiment Analyzer</h1>
        
        <div style="margin-top:25px; padding:20px; background-color:#2D3748; border-radius:8px;">
            <p style="font-size:16px;"><strong>Your Message:</strong></p>
            <p style="font-style:italic; color:#CBD5E0;">{text}</p>
        </div>

        <div style="margin-top:25px; padding:20px; background-color:{bg_color}; border-radius:8px;">
            <h3 style="margin:0 0 10px 0;">Detected Sentiment: <span style="color:white;">{sentiment}</span></h3>
            <p style="color:white; font-size:15px;">{response}</p>
        </div>
    </div>
    """
    display(HTML(html_content))

# User Input
user_input = input(" Enter your message to analyze: ")
analyze_sentiment(user_input)
