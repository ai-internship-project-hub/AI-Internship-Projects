import webbrowser

# Simple sentiment keywords
positive_words = ["good", "excellent", "great", "amazing", "helpful", "nice", "awesome", "fantastic", "love"]
negative_words = ["bad", "poor", "worst", "boring", "unhelpful", "hate", "terrible"]

# Store feedback data
feedback_list = []

print("=== Student Feedback Review System ===")
while True:
    name = input("Enter Student Name (or 'done' to finish): ")
    if name.lower() == "done":
        break
    feedback = input("Enter Feedback: ")

    # Simple sentiment analysis
    feedback_lower = feedback.lower()
    sentiment = "Neutral"
    for word in positive_words:
        if word in feedback_lower:
            sentiment = "Positive"
            break
    for word in negative_words:
        if word in feedback_lower:
            sentiment = "Negative"
            break

    feedback_list.append((name, feedback, sentiment))

# Create HTML output
html_content = """
<!DOCTYPE html>
<html>
<head>
<title>Student Feedback Review</title>
<style>
    body { font-family: Arial; margin: 20px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid black; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    .Positive { color: green; font-weight: bold; }
    .Negative { color: red; font-weight: bold; }
    .Neutral { color: gray; font-weight: bold; }
</style>
</head>
<body>
<h2>Student Feedback Review</h2>
<table>
<tr>
<th>Student Name</th>
<th>Feedback</th>
<th>Sentiment</th>
</tr>
"""

for name, feedback, sentiment in feedback_list:
    html_content += f"<tr><td>{name}</td><td>{feedback}</td><td class='{sentiment}'>{sentiment}</td></tr>"

html_content += """
</table>
</body>
</html>
"""

# Save HTML file
file_path = "student_feedback.html"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"\nFeedback saved to {file_path}")
print("Opening in browser...")
webbrowser.open(file_path)
