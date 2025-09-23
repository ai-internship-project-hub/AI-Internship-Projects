import tkinter as tk
import math
import re

# -------- Core parsing & safe evaluation --------
def safe_eval(expression: str):
    """Safely evaluate a math expression with friendly syntax:
       - ^ as power
       - sin/cos/tan take DEGREES
       - log() is base-10, ln() is natural log
       - sqrt(), pow(), pi, e supported
    """
    expr = expression.strip().lower()

    # common friendly replacements
    expr = expr.replace('^', '**')            # 2^5 -> 2**5
    expr = expr.replace('√', 'sqrt')          # √9 -> sqrt9 or sqrt(9)
    expr = re.sub(r'sqrt(\d+)', r'sqrt(\1)', expr)  # sqrt9 -> sqrt(9)
    expr = expr.replace('×', '*').replace('÷', '/')

    # allow percent-of syntax: "25% of 480"
    # convert "a% of b" -> "(a/100)*b"
    expr = re.sub(r'(\d+(\.\d+)?)\s*%\s*of\s*(\d+(\.\d+)?)',
                  r'(\1/100)*(\3)', expr)

    # Allowed functions/constants (no builtins)
    def sin_deg(x): return math.sin(math.radians(x))
    def cos_deg(x): return math.cos(math.radians(x))
    def tan_deg(x): return math.tan(math.radians(x))
    def log10(x):   return math.log10(x)
    def ln(x):      return math.log(x)

    allowed = {
        'sqrt': math.sqrt,
        'pow': math.pow,
        'abs': abs,
        'round': round,
        'sin': sin_deg,
        'cos': cos_deg,
        'tan': tan_deg,
        'log': log10,   # base-10
        'ln': ln,       # natural log
        'pi': math.pi,
        'e': math.e
    }

    try:
        return eval(expr, {"__builtins__": {}}, allowed)
    except Exception as e:
        return f"Invalid input ({e.__class__.__name__})"

def ai_parse(query: str):
    """Handle simple natural-language requests, then fall back to safe_eval."""
    q = query.strip().lower()

    # add / plus
    if re.search(r'\b(add|plus)\b', q):
        nums = list(map(float, re.findall(r'-?\d+\.?\d*', q)))
        if nums:
            return sum(nums)

    # subtract / minus
    if re.search(r'\b(subtract|minus)\b', q):
        nums = list(map(float, re.findall(r'-?\d+\.?\d*', q)))
        if len(nums) >= 2:
            return nums[0] - nums[1]

    # multiply / times
    if re.search(r'\b(multiply|times)\b', q):
        nums = list(map(float, re.findall(r'-?\d+\.?\d*', q)))
        if len(nums) >= 2:
            prod = 1
            for n in nums:
                prod *= n
            return prod

    # divide
    if 'divide' in q or 'divided by' in q:
        nums = list(map(float, re.findall(r'-?\d+\.?\d*', q)))
        if len(nums) >= 2:
            return nums[0] / nums[1]

    # square root
    m = re.search(r'square\s*root\s*of\s*(-?\d+\.?\d*)', q)
    if m:
        return math.sqrt(float(m.group(1)))

    # percentage like "what is 25% of 480"
    m = re.search(r'(\d+(\.\d+)?)\s*%\s*of\s*(\d+(\.\d+)?)', q)
    if m:
        a = float(m.group(1))
        b = float(m.group(3))
        return (a/100.0) * b

    # power like "raise 2 to 5" / "2 to the power of 5"
    m = re.search(r'(-?\d+\.?\d*)\s*(to the power of|power|raised to|raise to)\s*(-?\d+\.?\d*)', q)
    if m:
        a = float(m.group(1)); b = float(m.group(3))
        return math.pow(a, b)

    # fallback to expression evaluator
    return safe_eval(query)

# -------- Tkinter UI --------
def calculate():
    query = entry.get()
    result = ai_parse(query)
    output_var.set(f"Result: {result}")

# UI setup
root = tk.Tk()
root.title("AI Calculator")
root.geometry("460x360")
root.configure(bg="#f7f7fb")

title = tk.Label(
    root, text="🤖 AI Calculator",
    font=("Segoe UI", 18, "bold"),
    bg="#f7f7fb", fg="#333"
)
title.pack(pady=10)

tips = tk.Label(
    root,
    text="Tips: use ^ for power (2^5), log(x)=log₁₀, ln(x)=natural log,\n"
         "sin/cos/tan expect DEGREES, sqrt( ), pi & e supported.\n"
         "Examples: sqrt(25), log(100), pi*5^2, sin(30), 25% of 480",
    font=("Segoe UI", 9),
    bg="#f7f7fb", fg="#666", justify="center"
)
tips.pack(pady=4)

entry = tk.Entry(root, font=("Segoe UI", 14), width=30, relief="solid", bd=1)
entry.pack(pady=10)
entry.focus()

btn = tk.Button(
    root, text="Calculate", font=("Segoe UI", 12, "bold"),
    command=calculate, bg="#4CAF50", fg="white", padx=16, pady=6
)
btn.pack(pady=8)

output_var = tk.StringVar(value="Result: ")
output = tk.Label(root, textvariable=output_var, font=("Segoe UI", 14), bg="#f7f7fb", fg="#1a73e8")
output.pack(pady=16)

# Quick test buttons (optional)
frame = tk.Frame(root, bg="#f7f7fb")
frame.pack(pady=6)
examples = ["sqrt(25)", "2^5", "log(100)", "ln(100)", "sin(30)", "cos(60)", "tan(45)", "pi*5^2", "25% of 480"]
def fill(e):
    entry.delete(0, tk.END)
    entry.insert(0, e)
for ex in examples:
    tk.Button(frame, text=ex, command=lambda ex=ex: fill(ex), padx=8, pady=4).pack(side="left", padx=3)

root.mainloop()
