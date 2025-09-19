import re
import traceback
from io import StringIO
from contextlib import redirect_stdout
from IPython.display import display, HTML
import ipywidgets as widgets

# ------------------------------
# Function to detect and fix issues
# ------------------------------
def debug_and_fix_code(code):
    fixed_code = code

    # Try running the code to catch errors
    try:
        f = StringIO()
        with redirect_stdout(f):
            exec(code, {})
        output = f.getvalue()
        return "✅ No errors found.\nOutput:\n" + output, code

    except Exception as e:
        error_msg = traceback.format_exc()

        # Try common fixes
        # 1. Add missing colons
        fixed_code = re.sub(r"(if|elif|else|for|while|def|class)\s*\(?.*[^:]\n", lambda m: m.group(0).rstrip() + ":\n", fixed_code)

        # 2. Add missing imports for common libraries
        common_libs = {
            "math": r"\bmath\.",
            "re": r"\bre\.",
            "random": r"\brandom\.",
        }
        for lib, pattern in common_libs.items():
            if re.search(pattern, fixed_code) and f"import {lib}" not in fixed_code:
                fixed_code = f"import {lib}\n" + fixed_code

        # 3. Replace print without parentheses (Python 2 style) → Python 3
        fixed_code = re.sub(r"print\s+(['\"].*['\"])", r"print(\1)", fixed_code)

        return f"⚠ Errors detected:\n{error_msg}\n\nSuggested Fixes Applied.", fixed_code

# ------------------------------
# HTML & Widgets
# ------------------------------
code_input = widgets.Textarea(
    value='''# Example faulty code
for i in range(5)
    print i
''',
    placeholder='Paste your Python code here...',
    description='Your Code:',
    layout=widgets.Layout(width='100%', height='200px')
)

button = widgets.Button(description="🔍 Debug & Fix", button_style='success')
output_box = widgets.Output()

def on_button_click(b):
    with output_box:
        output_box.clear_output()
        result, fixed = debug_and_fix_code(code_input.value)

        html_result = f"""
        <div style='border:2px solid #333; padding:20px; border-radius:10px; background:#f8f9fa; font-family:Arial;'>
            <h3>🛠 Debugging Result</h3>
            <pre>{result}</pre>
            <h3>💡 Fixed Code</h3>
            <pre>{fixed}</pre>
        </div>
        """
        display(HTML(html_result))

button.on_click(on_button_click)

display(code_input, button, output_box)
