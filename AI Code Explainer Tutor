from IPython.display import display, HTML

# Function to explain Python code line-by-line
def explain_code(code_input):
    explanation = ""
    lines = code_input.strip().split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        step = f"<b>Line {i+1}:</b> <code>{line}</code><br>"

        if line.startswith("print("):
            step += "📌 Prints something to the console.<br>"
        elif "=" in line and "==" not in line:
            var = line.split('=')[0].strip()
            step += f"📌 Assigns a value to variable <b>{var}</b>.<br>"
        elif line.startswith("def "):
            func = line.split("def ")[1].split("(")[0]
            step += f"📌 Defines a function named <b>{func}</b>.<br>"
        elif line.startswith("for "):
            step += "📌 Starts a loop to iterate over items.<br>"
        elif line.startswith("while "):
            step += "📌 Starts a while loop that runs until condition is false.<br>"
        elif line.startswith("if "):
            step += "📌 Conditional 'if' block checks a condition.<br>"
        elif line.startswith("elif "):
            step += "📌 'Else if' checks another condition.<br>"
        elif line.startswith("else"):
            step += "📌 Runs if none of the above conditions are true.<br>"
        elif line.startswith("return "):
            step += "📌 Returns a value from a function.<br>"
        elif line.startswith("#"):
            step += "📌 This is a comment (non-executable).<br>"
        else:
            step += "📌 Executes as part of program logic.<br>"

        explanation += step + "<br>"

    return HTML(explanation)

# ✅ User input via Jupyter
print("Enter your Python code below (type 'END' on a new line to finish):\n")
lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)

user_code = "\n".join(lines)

# Display explanation
display(HTML("<h2 style='color:darkblue;'>👨‍🏫 Code Explanation</h2>"))
display(explain_code(user_code))
