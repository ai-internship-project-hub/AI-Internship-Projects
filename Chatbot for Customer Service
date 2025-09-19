# ---------------- Customer Service Chatbot (single Jupyter cell) ----------------
import re, math, os, datetime, json, random
from collections import Counter, defaultdict
from IPython.display import display, HTML, clear_output

# try ipywidgets for UI; fallback to CLI if not available
try:
    import ipywidgets as widgets
    HAS_WIDGETS = True
except Exception:
    HAS_WIDGETS = False

# ----------------------
# 1) Small FAQ knowledge base
# ----------------------
FAQ = [
    {"q":"What are your shipping times?", "a":"Standard shipping takes 3-7 business days. Expedited options are available at checkout."},
    {"q":"How do I track my order?", "a":"You can track your order using the tracking number sent to your email after shipment. Provide your order number and I can check the status."},
    {"q":"What is the return policy?", "a":"We accept returns within 30 days of delivery for most items in original condition. Some items are final sale."},
    {"q":"How do I request a refund?", "a":"Open a return request from your Orders page. Once we receive the returned item, refund is processed to the original payment method."},
    {"q":"How can I change my shipping address?", "a":"If your order hasn't shipped, you can update the shipping address from the Orders page or reply with your order number and new address."},
    {"q":"How do I reset my password?", "a":"Click 'Forgot password' on the login page and follow instructions. You will receive a reset link by email."},
    {"q":"Which payment methods do you accept?", "a":"We accept credit/debit cards, PayPal, and major buy-now-pay-later services where available."},
    {"q":"How can I cancel my order?", "a":"Orders can be cancelled if they haven't shipped. Provide your order number and we'll check eligibility."},
    {"q":"Do you ship internationally?", "a":"Yes — we ship to many countries. International shipping costs and duties may apply."},
    {"q":"What warranty do your products have?", "a":"Most products include a 1-year limited warranty. Check the product page for specifics."},
    {"q":"My app is crashing or showing an error - what should I do?", "a":"Try clearing the app cache, restarting the device, and ensuring the app is updated. If problem persists, provide the error message."},
    {"q":"How do I get an invoice for my purchase?", "a":"Invoices are available in your account under Orders → Invoice. You can download or request one via support."},
    {"q":"Do you offer student discounts?", "a":"We offer occasional student promotions. Subscribe to our newsletter for announcements or ask support for current deals."},
    {"q":"How do I contact a human agent?", "a":"You can reply 'escalate' or click the 'Escalate to human' button. Provide order number and a short summary for faster assistance."}
]

# Build a question corpus for retrieval
FAQ_QUESTIONS = [f["q"] for f in FAQ]

# ----------------------
# 2) Small utilities: preprocess, vectorize, similarity
# ----------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s#@]", " ", text)  # keep numbers, # (for order numbers), @ (for emails)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text):
    return text.split()

def term_freq_vector(tokens, vocab):
    vec = [0]*len(vocab)
    counts = Counter(tokens)
    for i, w in enumerate(vocab):
        vec[i] = counts.get(w, 0)
    return vec

def dot(u, v): 
    return sum(ux*vx for ux,vx in zip(u,v))

def norm(u): 
    return math.sqrt(dot(u,u))

def cosine_sim(u, v):
    nu, nv = norm(u), norm(v)
    if nu==0 or nv==0: 
        return 0.0
    return dot(u,v)/(nu*nv)

def best_faq_match(user_text, threshold=0.35):
    # build vocabulary from FAQ questions + user tokens
    pre_user = preprocess(user_text)
    user_tokens = tokenize(pre_user)
    all_tokens = set(user_tokens)
    for q in FAQ_QUESTIONS:
        all_tokens |= set(tokenize(preprocess(q)))
    vocab = sorted(list(all_tokens))
    # vectors
    uvec = term_freq_vector(user_tokens, vocab)
    best_score = 0.0
    best_idx = -1
    for i,q in enumerate(FAQ_QUESTIONS):
        qtokens = tokenize(preprocess(q))
        qvec = term_freq_vector(qtokens, vocab)
        s = cosine_sim(uvec, qvec)
        if s>best_score:
            best_score = s; best_idx = i
    if best_score >= threshold:
        return best_idx, best_score
    return None, best_score

# ----------------------
# 3) Intent heuristics & handlers
# ----------------------
ORDER_PAT = re.compile(r"(?:order|#order|order#|ord)\s*[:#]?\s*(\d{5,12})|#(\d{5,12})|(\d{6,12})")
EMAIL_PAT = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_PAT = re.compile(r"\b\d{6,15}\b")

def handle_user_message(msg, history):
    text = preprocess(msg)
    # greetings
    if re.search(r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b", text):
        return random.choice([
            "Hello! 👋 How can I help you today?",
            "Hi there! How may I assist you with your order or account?"
        ])
    # thanks/bye
    if re.search(r"\b(thank|thanks|thx|bye|goodbye|see ya)\b", text):
        return random.choice(["You're welcome! If you need anything else, I'm here.", "Happy to help — have a great day!"])
    # order tracking
    if re.search(r"\b(track|tracking|where.*order|status.*order)\b", text) or "track my order" in text:
        m = ORDER_PAT.search(msg)
        if m:
            order_num = next(g for g in m.groups() if g)
            return f"I found order **#{order_num}**. Current status: *In transit*. Estimated delivery: 2 business days. Would you like the tracking link?"
        else:
            return "Could you please provide your order number (e.g., `#12345678`)? I can check the shipping status for you."
    # refund/return
    if re.search(r"\b(return|refund|exchange|replace)\b", text):
        m = ORDER_PAT.search(msg)
        if m:
            order_num = next(g for g in m.groups() if g)
            return (f"Thanks — for order **#{order_num}**, you can start a return from Orders → Return. "
                    "Return window is 30 days. Would you like me to open a return request for you?")
        else:
            return ("You can return items within 30 days in most cases. Please share your order number if you'd like me to start a return.")
    # account/password
    if re.search(r"\b(password|forgot|reset|login|sign in|account)\b", text):
        if "forgot" in text or "reset" in text:
            return "To reset your password, use 'Forgot password' on the login page — we'll email a reset link. Did you want me to resend a link?"
        return "For account help, could you tell me if you're unable to login or want to change account details?"
    # pricing/plans
    if re.search(r"\b(price|cost|plan|subscription|pricing)\b", text):
        return ("Our plans: Basic (free) — limited features; Pro — $9.99/mo; Business — $29.99/mo with priority support. "
                "Would you like a comparison table?")
    # troubleshooting / technical
    if re.search(r"\b(crash|error|not working|bug|issue|slow|lag)\b", text):
        # ask for app/platform and error text
        if "app" in text or "mobile" in text or "desktop" in text:
            return ("Try restarting the app, clearing cache, and ensuring the app is updated. "
                    "If you see an error code, please share it (e.g., `Error 500`). Would you like steps tailored to Android or iOS?")
        return ("Sorry you're seeing issues. Can you describe what you tried and any error messages you see?")
    # invoice/billing
    if re.search(r"\b(invoice|receipt|bill|billing)\b", text):
        return "Invoices are available in your account under Orders → Invoice. I can email it to you if you provide the order number or your registered email."
    # contact human
    if re.search(r"\b(agent|human|representative|support)\b", text):
        return "I can connect you to a support agent — please provide a short summary and your order number (if relevant)."

    # fallback: try FAQ match
    idx, score = best_faq_match(msg, threshold=0.35)
    if idx is not None:
        fa = FAQ[idx]["a"]
        return f"{fa} (confidence {score:.2f})"
    # low-confidence fallback
    # ask clarifying question or offer human agent
    return ("I didn't fully understand — do you mean one of the following?\n"
            "- Track an order\n- Start a return\n- Reset account password\nOr reply 'escalate' to contact a human agent.")

# ----------------------
# 4) Chat UI render helpers
# ----------------------
def render_bot_bubble(text):
    safe = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
    html = f"""
    <div style="display:flex; margin:8px 0; align-items:flex-start;">
      <div style="width:40px;height:40px;border-radius:50%;background:#2b7cff;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;margin-right:8px">CS</div>
      <div style="background:#f1f5ff;padding:10px 12px;border-radius:12px;max-width:78%;box-shadow:0 2px 6px rgba(43,124,255,0.08);">
        <div style="font-size:14px;color:#0b2546;">{safe}</div>
      </div>
    </div>
    """
    return html

def render_user_bubble(text):
    safe = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
    html = f"""
    <div style="display:flex; margin:8px 0; justify-content:flex-end;">
      <div style="background:#dfeeff;padding:10px 12px;border-radius:12px;max-width:78%;box-shadow:0 2px 6px rgba(0,0,0,0.03);">
        <div style="font-size:14px;color:#022a5a;">{safe}</div>
      </div>
    </div>
    """
    return html

def render_chat(history):
    chat_html = "<div style='font-family:Arial, sans-serif; max-width:880px;'>"
    chat_html += "<div style='padding:8px 0;color:#333;margin-bottom:8px'><b>Customer Service Chat</b></div>"
    for turn in history:
        if turn["role"] == "user":
            chat_html += render_user_bubble(turn["text"])
        else:
            chat_html += render_bot_bubble(turn["text"])
    chat_html += "</div>"
    return chat_html

# ----------------------
# 5) Main UI (ipywidgets) and handlers
# ----------------------
def run_widget_chatbot():
    # conversation history
    history = []
    output = widgets.Output(layout={'border':'1px solid #ddd','width':'920px','height':'420px','overflow':'auto','padding':'8px'})

    input_box = widgets.Textarea(placeholder="Type your message here...", layout=widgets.Layout(width='680px', height='80px'))
    send_btn = widgets.Button(description="Send", button_style='primary', layout=widgets.Layout(width='80px'))
    escalate_btn = widgets.Button(description="Escalate to human", button_style='warning', layout=widgets.Layout(width='150px'))
    save_btn = widgets.Button(description="Save transcript", layout=widgets.Layout(width='130px'))
    reset_btn = widgets.Button(description="Reset chat", layout=widgets.Layout(width='100px'))

    def append_and_render(role, text):
        history.append({"role":role,"text":text,"ts":datetime.datetime.now().isoformat()})
        with output:
            clear_output(wait=True)
            display(HTML(render_chat(history)))

    def on_send(b):
        user_text = input_box.value.strip()
        if not user_text:
            return
        append_and_render("user", user_text)
        input_box.value = ""
        # bot processing
        bot_reply = handle_user_message(user_text, history)
        append_and_render("bot", bot_reply)

    def on_escalate(b):
        append_and_render("user", "Please escalate to human agent.")
        agent_msg = ("I've escalated your request to a human agent. Please provide your order number and a one-line summary — an agent will contact you at the registered email within 24 hours.")
        append_and_render("bot", agent_msg)

    def on_save(b):
        if not history:
            with output:
                print("No conversation yet to save.")
            return
        fname = f"chat_transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html = "<html><body style='font-family:Arial;font-size:14px;'>"
        html += render_chat(history)
        html += "</body></html>"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        with output:
            display(HTML(f"<div style='background:#e8f5e9;padding:8px;border-radius:6px;'>Saved transcript: <b>{os.path.abspath(fname)}</b></div>"))

    def on_reset(b):
        history.clear()
        with output:
            clear_output(wait=True)
            display(HTML("<div style='color:#666'>Chat cleared. Start a new conversation.</div>"))

    send_btn.on_click(on_send)
    escalate_btn.on_click(on_escalate)
    save_btn.on_click(on_save)
    reset_btn.on_click(on_reset)

    header = HTML("<h3 style='font-family:Arial;color:#1f4ea3;margin:4px 0'>Customer Service Chatbot</h3><div style='color:#444;margin-bottom:6px'>Ask about orders, returns, billing, or app issues. Click 'Escalate to human' to simulate handover.</div>")
    controls = widgets.HBox([input_box, widgets.VBox([send_btn, escalate_btn, save_btn, reset_btn])])
    display(header, controls, output)

    # initial greeting
    append_and_render("bot", "Hi — I'm your virtual assistant. How can I help you today?")

# ----------------------
# 6) CLI fallback
# ----------------------
def run_cli_chatbot():
    print("Customer Service Chatbot (CLI mode). Type 'exit' to quit, 'save' to save transcript, 'escalate' to request human agent.")
    history = []
    def append(role, text):
        history.append({"role":role,"text":text,"ts":datetime.datetime.now().isoformat()})
        if role == "bot":
            print("Bot:", text)
        else:
            print("You:", text)
    append("bot", "Hi — I'm your virtual assistant. How can I help you today?")
    while True:
        msg = input("You: ").strip()
        if not msg:
            continue
        if msg.lower() in ("exit","quit"):
            print("Goodbye.")
            break
        if msg.lower() == "save":
            fname = f"chat_transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            html = "<html><body style='font-family:Arial,font-size:14px;'>"
            for h in history:
                if h["role"]=="user":
                    html += f"<div style='text-align:right'><b>You:</b> {h['text']}</div>"
                else:
                    html += f"<div style='text-align:left'><b>Bot:</b> {h['text']}</div>"
            html += "</body></html>"
            with open(fname,"w",encoding="utf-8") as f:
                f.write(html)
            print("Saved to", os.path.abspath(fname))
            continue
        if msg.lower() == "escalate":
            append("user", msg)
            append("bot", "Escalation requested. A human agent will contact you within 24 hours.")
            continue
        append("user", msg)
        reply = handle_user_message(msg, history)
        append("bot", reply)

# ----------------------
# 7) Run appropriate interface
# ----------------------
if HAS_WIDGETS:
    run_widget_chatbot()
else:
    run_cli_chatbot()
# ------------------------------------
