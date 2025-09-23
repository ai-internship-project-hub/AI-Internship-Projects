# Install necessary packages
!pip install pillow ipywidgets --quiet

# Imports
import random
from PIL import Image, ImageDraw, ImageFont
import ipywidgets as widgets
from IPython.display import display, HTML

# Meme caption templates (Funnier!)
CAPTION_TEMPLATES = [
    "Me pretending to work while actually Googling '{}'",
    "That moment when {} hits you like a truck",
    "When you say '{}' and immediately regret it",
    "If stress burned calories, I'd be a supermodel by now — thanks to '{}'",
    "'{}' — because why not ruin your day?",
    "When you realize '{}'\nwas a terrible idea but it's too late now",
    "POV: You're dealing with '{}'",
    "Nobody:\nLiterally nobody:\nMe: '{}'",
    "Trying to act cool about '{}', but dying inside",
    "I came. I saw. I {}'d.",
    "When life gives you '{}', throw it back",
    "404 Motivation not found — blamed on '{}'",
    "'{}' is the reason I need therapy (and coffee)"
]

# Generate caption
def make_caption(topic):
    tpl = random.choice(CAPTION_TEMPLATES)
    return tpl.format(topic)

# Create template image if missing
TEMPLATE_PATH = "meme_template.jpg"
try:
    Image.open(TEMPLATE_PATH)
except FileNotFoundError:
    img = Image.new("RGB", (600, 400), color=(40, 40, 40))
    draw = ImageDraw.Draw(img)
#     draw.text((180,180), "", fill=(200,200,200))
    img.save(TEMPLATE_PATH)

# Render meme image
def render_meme(caption):
    img = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Try loading a TTF font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Auto wrap caption
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            w, _ = draw.textsize(test_line, font=font)
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    # Prepare caption lines
    lines = wrap_text(caption, font, img.width - 40)

    # Calculate vertical position to center text
    total_height = sum([draw.textsize(line, font=font)[1] for line in lines]) + (len(lines)-1)*5
    y = (img.height - total_height) // 2

    # Draw each line centered
    for line in lines:
        w, h = draw.textsize(line, font=font)
        x = (img.width - w) // 2
        draw.text((x, y), line, font=font, fill="white")
        y += h + 5

    return img

# Widgets
topic_in = widgets.Text(
    placeholder="e.g. Monday meetings",
    description="Topic:",
    layout=widgets.Layout(width="80%")
)
button = widgets.Button(description="🎉 Generate Funny Meme", button_style="success")
out = widgets.Output()

def on_click(b):
    with out:
        out.clear_output()
        topic = topic_in.value.strip()
        if not topic:
            display(HTML("<p style='color:red;'>⚠️ Please enter a meme topic!</p>"))
            return
        caption = make_caption(topic)
        meme_img = render_meme(caption)
        display(HTML(f"<h4>🤣 Caption:</h4><p>{caption}</p>"))
        display(meme_img)

button.on_click(on_click)

# Display UI
display(HTML("<h2 style='color:teal;'>😂 AI‑Lite Funny Meme Generator (Offline)</h2>"))
display(HTML("<p>Enter a topic below and click the button to generate a meme! No internet or OpenAI required!</p>"))
display(topic_in, button, out)
