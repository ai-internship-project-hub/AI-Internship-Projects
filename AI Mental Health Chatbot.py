# AI Mental Health Chatbot - single Jupyter cell
# No external APIs required. Uses ipywidgets for UI (fall back to CLI).
import re, datetime, json, os
from IPython.display import display, HTML, clear_output

# Try import widgets
try:
    import ipywidgets as widgets
    HAS_WIDGETS = True
except Exception:
    HAS_WIDGETS = False

# --- Simple lexicons (expand as you like) ---
POS_WORDS = {"calm","good","happy","okay","well","better","fine","relieved","hopeful","relief","great","content","peace"}
NEG_WORDS = {"sad","depressed","anxious","anxiety","stressed","stress","lonely","angry","hurt","upset","overwhelmed","tired","hopeless","down"}
CRISIS_KEYWORDS = {
    "suicide","kill myself","want to die","end my life","hurt myself","self-harm","die by suicide",
    "cant go on","can't go on","i'll kill myself","i will kill myself","i want to die"
}
THEME_KEYWORDS = {
    "work":["work","job","boss","office","colleague"],
    "relationship":["relationship","partner","breakup","divorce","boyfriend","girlfriend","wife","husband"],
    "study":["exam","study","assignment","exam stress","grades","school","college","university"],
    "health":["sleep","insomnia","sick","ill","health","pain"],
}

# --- Utilities ---
def clean_words(text):
    return re.findall(r"\b[a-z']+\b", text.lower())

def sentiment_score(text):
    words = clean_words(text)
    if not words:
        return 0.0
    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    score = (pos - neg) / max(1, len(words))
    return round(score, 3)

def detect_crisis(text):
    t = text.lower()
    for kw in CRISIS_KEYWORDS:
        if kw in t:
            return True
    return False

def detect_themes(text):
    t = text.lower()
    hits = []
    for theme, kws in THEME_KEYWORDS.items():
        for k in kws:
            if k in t:
                hits.append(theme)
                break
    return hits

# --- Response generator ---
def generate_response(user_text):
    # immediate crisis check
    if detect_crisis(user_text):
        resp = (
            "I'm really sorry you're feeling this way. If you're in immediate danger, "
            "please call your local emergency number or contact a crisis hotline right now. "
            "If you can, please reach out to a trusted person and tell them how you feel. "
            "I can also share coping steps and resources — would you like that?"
        )
        flagged = True
        return resp, flagged

    # sentiment & theme
    s = sentiment_score(user_text)
    themes = detect_themes(user_text)

    # Empathetic reflection
    if s <= -0.03:
        empath = "I’m sorry you’re going through a hard time — that sounds really difficult."
    elif s >= 0.03:
        empath = "It’s good to hear some positive things — thank you for sharing that."
    else:
        empath = "Thanks for sharing. I hear you."

    # Theme-specific follow-up
    if themes:
        theme = themes[0]
        if theme == "work":
            follow = "Is it mainly work-related stress? Would you like tips for setting boundaries or short breaks you can try?"
        elif theme == "relationship":
            follow = "Relationships can be heavy. Do you want to talk about what happened or get coping strategies for handling strong emotions?"
        elif theme == "study":
            follow = "Exam/study stress is common. Would you like a quick study-break plan or a short breathing exercise?"
        elif theme == "health":
            follow = "Health issues can affect mood a lot. Would you like some simple sleep hygiene or relaxation tips?"
        else:
            follow = "Would you like to share more about that?"
    else:
        follow = "Would you like some coping suggestions, a breathing exercise, or to just keep talking?"

    # Suggestion seeds
    if s <= -0.15:
        suggestions = "You might try: (1) grounding — name 5 things you can see/hear/touch; (2) breathing: 4 in, 4 hold, 6 out for 2 minutes; (3) text/call a trusted friend. If thoughts are intense, please seek immediate help."
    elif s <= -0.03:
        suggestions = "Some small steps: take a five-minute walk, drink water, write one line about how you feel, or try a short breathing exercise."
    elif s > 0.03:
        suggestions = "Nice — if you'd like to build on this, try noting what helped you feel better and do more of it."

    bot_text = f"{empath} {follow}\n\nIf you'd like, press the 'Coping Tips' button for concrete steps or 'Breathing Exercise' for a short guided practice."
    flagged = False
    return bot_text, flagged

# --- Coping content helpers ---
def coping_tips_html():
    tips = [
        ("Grounding", "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste."),
        ("Breathing", "4 seconds in, hold 4, 6 seconds out. Repeat for 2–3 minutes."),
        ("Movement", "Stand up and stretch gently or walk for 5 minutes."),
        ("Write it down", "Write one paragraph about what's bothering you — don't edit, just write."),
        ("Reach out", "Message or call one person you trust and tell them you're having a tough moment.")
    ]
    html = "<ul>"
    for t, desc in tips:
        html += f"<li><b>{t}:</b> {desc}</li>"
    html += "</ul>"
    return html

def breathing_html():
    html = """
    <div style='font-family:Arial; max-width:600px;'>
      <p style='font-weight:600;'>Guided breath (box/4-4-6):</p>
      <ol>
        <li>Inhale slowly for <b>4 seconds</b>.</li>
        <li>Hold the breath for <b>4 seconds</b>.</li>
        <li>Exhale slowly for <b>6 seconds</b>.</li>
      </ol>
      <p>Repeat this cycle 6 times. Try to sit comfortably and focus on your breathing.</p>
    </div>
    """
    return html

# --- Chat handling ---
chat_log = []  # list of dicts: {'who':'user'/'bot','text':..., 'ts':...,'sent':score}
mood_history = []  # list of numeric mood scores (0-10)

def mood_from_sentiment(s):
    # s is in approx range [-0.5,0.5], map to 0-10
    val = int(round((s + 0.5) * 10))
    return max(0, min(10, val))

def render_chat_html():
    # build chat bubbles
    html = """
    <style>
      .chat-card { max-width:760px; font-family:Arial; margin:6px; }
      .bubble { padding:10px 14px; border-radius:14px; margin:8px 0; display:inline-block; max-width:78%; }
      .user { background:#daf1ff; float:right; text-align:right; }
      .bot { background:#fff7da; float:left; text-align:left; }
      .meta { font-size:11px; color:#666; margin-top:4px; }
      .clear { clear:both; }
      .header { background:linear-gradient(90deg,#6078ff,#00c6ff); color:white; padding:12px; border-radius:10px; margin-bottom:8px; }
      .small { font-size:13px; color:#333; }
    </style>
    <div class='chat-card'>
      <div class='header'><b>AI Mental Wellness Assistant</b> — supportive, non-clinical help</div>
    """
    for item in chat_log[-30:]:
        ts = item['ts'].strftime("%H:%M")
        if item['who']=='user':
            html += f"<div class='bubble user'><div class='small'>{item['text']}</div><div class='meta'>{ts} • You</div></div><div class='clear'></div>"
        else:
            html += f"<div class='bubble bot'><div class='small'>{item['text']}</div><div class='meta'>{ts} • Assistant</div></div><div class='clear'></div>"
    # mood summary
    if mood_history:
        avg_mood = round(sum(mood_history)/len(mood_history),1)
        html += f"<div style='margin-top:10px; padding:10px; border-radius:8px; background:#f0f4f8;'><b>Mood summary</b>: last={mood_history[-1]}, avg={avg_mood} (0 low — 10 high)</div>"
    else:
        html += f"<div style='margin-top:10px; padding:10px; border-radius:8px; background:#f0f4f8;'><b>Mood summary</b>: no entries yet</div>"
    html += "</div>"
    return html

# --- Save transcript ---
def save_transcript():
    if not chat_log:
        return None
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"mental_chat_{ts}.txt"
    path = os.path.join(os.getcwd(), fname)
    with open(path, "w", encoding="utf-8") as f:
        for item in chat_log:
            who = "You" if item['who']=='user' else "Assistant"
            f.write(f"[{item['ts'].isoformat()}] {who}: {item['text']}\n")
    return path

# --- UI (widgets) ---
if HAS_WIDGETS:
    message_box = widgets.Textarea(placeholder="Type how you're feeling, e.g. 'I'm feeling very anxious about exams'...", layout=widgets.Layout(width='720px', height='90px'))
    send_btn = widgets.Button(description="Send", button_style='primary', layout=widgets.Layout(width='120px'))
    tips_btn = widgets.Button(description="Coping Tips", layout=widgets.Layout(width='120px'))
    breath_btn = widgets.Button(description="Breathing Exercise", layout=widgets.Layout(width='160px'))
    save_btn = widgets.Button(description="Save Chat", layout=widgets.Layout(width='120px'))
    output = widgets.Output(layout={'border':'1px solid #ddd', 'width':'760px', 'height':'420px', 'overflow':'auto'})

    # initial assistant greeting
    init_text = ("Hi — I'm a supportive assistant. You can share how you're feeling. "
                 "I can suggest coping steps, a short breathing practice, or help you plan next small steps. "
                 "If you're in immediate danger, please contact local emergency services.")
    chat_log.append({'who':'bot','text':init_text,'ts':datetime.datetime.now(),'sent':0.0})

    def refresh():
        with output:
            output.clear_output()
            display(HTML(render_chat_html()))

    def on_send(b):
        user_text = message_box.value.strip()
        if not user_text:
            return
        # append user
        ts = datetime.datetime.now()
        s = sentiment_score(user_text)
        chat_log.append({'who':'user','text':user_text,'ts':ts,'sent':s})
        # generate bot response
        bot_text, flagged = generate_response(user_text)
        chat_log.append({'who':'bot','text':bot_text,'ts':datetime.datetime.now(),'sent':0.0})
        # update mood
        mood_history.append(mood_from_sentiment(s))
        message_box.value = ""
        refresh()
        # if crisis flagged, also show immediate advice block below
        if flagged:
            with output:
                display(HTML("<div style='padding:10px; margin-top:8px; border-radius:8px; background:#fff0f0;'><b>Important:</b> If you are in immediate danger or planning to harm yourself, please contact local emergency services right now and reach out to someone you trust.</div>"))

    def on_tips(b):
        chat_log.append({'who':'bot','text':"Here are some practical coping tips:",'ts':datetime.datetime.now(),'sent':0.0})
        refresh()
        with output:
            display(HTML(coping_tips_html()))

    def on_breath(b):
        chat_log.append({'who':'bot','text':"Let's try a short breathing exercise:",'ts':datetime.datetime.now(),'sent':0.0})
        refresh()
        with output:
            display(HTML(breathing_html()))

    def on_save(b):
        path = save_transcript()
        with output:
            if path:
                display(HTML(f"<div style='padding:8px; background:#e8f5e9; border-radius:6px;'>Saved chat to <b>{path}</b></div>"))
            else:
                display(HTML("<div style='padding:8px; background:#fff3cd; border-radius:6px;'>No chat to save yet.</div>"))

    send_btn.on_click(on_send)
    tips_btn.on_click(on_tips)
    breath_btn.on_click(on_breath)
    save_btn.on_click(on_save)

    # layout
    controls_top = widgets.HBox([message_box])
    controls_bot = widgets.HBox([send_btn, tips_btn, breath_btn, save_btn])
    display(widgets.VBox([widgets.HTML("<h2 style='font-family:Arial;color:#2c3e50;'>🤝 AI Mental Wellness Assistant</h2><div style='color:#555; font-family:Arial;'>Supportive and non-clinical. If you're in immediate danger call local emergency services.</div>"), controls_top, controls_bot, output]))
    refresh()

else:
    # CLI fallback
    print("Running in simple CLI mode (ipywidgets not available). Type 'exit' to quit.")
    print("Note: This is not a substitute for professional help.")
    print(init_text)
    while True:
        user_text = input("\nYou: ").strip()
        if not user_text:
            continue
        if user_text.lower() in {"exit","quit"}:
            print("Session ended.")
            break
        ts = datetime.datetime.now()
        s = sentiment_score(user_text)
        chat_log.append({'who':'user','text':user_text,'ts':ts,'sent':s})
        bot_text, flagged = generate_response(user_text)
        print("\nAssistant:", bot_text)
        chat_log.append({'who':'bot','text':bot_text,'ts':datetime.datetime.now(),'sent':0.0})
        mood_history.append(mood_from_sentiment(s))
        if flagged:
            print("\n!!! If you are in immediate danger, contact local emergency services right now and reach out to someone you trust.")
        # quick options
        print("\nType 'tips' for coping tips, 'breath' for a breathing exercise, 'save' to save transcript, or continue chatting.")
        cmd = input("Next (or press Enter to continue): ").strip().lower()
        if cmd == "tips":
            print("\nCoping Tips:\n", coping_tips_html().replace("<ul>","").replace("</ul>","").replace("<li>","- ").replace("</li>",""))
        elif cmd == "breath":
            print("\nBreathing Exercise: 4 in, 4 hold, 6 out. Repeat 6 times.")
        elif cmd == "save":
            path = save_transcript()
            if path:
                print("Saved to", path)
            else:
                print("Nothing to save.")
