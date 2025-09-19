import spacy
import fitz  # PyMuPDF
import docx
import webbrowser
import os

# ================================
# 🤖 AI RESUME ANALYZER
# ================================

print("="*60)
print("🤖 AI RESUME ANALYZER".center(60))
print("="*60)

nlp = spacy.load("en_core_web_sm")

# 📌 Extract text from PDF
def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# 📌 Extract text from DOCX
def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

# 📌 Extract based on file type
def get_resume_text(path):
    if path.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.endswith(".docx"):
        return extract_text_from_docx(path)
    else:
        raise ValueError("❌ Unsupported file format! Use PDF or DOCX.")

# 📌 Extract skills
def extract_skills(text, skills_db):
    text_lower = text.lower()
    return [skill for skill in skills_db if skill.lower() in text_lower]

# 📌 Analyze
def analyze_resume(resume_text, job_text, skills_list):
    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_text, skills_list)
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))
    return resume_skills, matched, missing

# 📌 Generate HTML report
def generate_html(resume_skills, matched, missing):
    html_content = f"""
    <html>
    <head>
        <title>AI Resume Analyzer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #e3f2fd, #fffde7);
                padding: 30px;
            }}
            h1 {{
                background-color: #1e88e5;
                color: white;
                text-align: center;
                padding: 15px;
                border-radius: 10px;
            }}
            .section {{
                margin-top: 30px;
                padding: 20px;
                border-radius: 10px;
                background-color: #f0f0f0;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .matched {{
                background-color: #c8e6c9;
            }}
            .missing {{
                background-color: #ffcdd2;
            }}
            ul {{
                list-style: square;
                padding-left: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>🤖 AI Resume Analyzer</h1>

        <div class="section">
            <h2>📄 Skills Found in Resume:</h2>
            <ul>{"".join(f"<li>{skill}</li>" for skill in resume_skills) if resume_skills else "<p>None found.</p>"}</ul>
        </div>

        <div class="section matched">
            <h2>✅ Matched Skills with Job Description:</h2>
            <ul>{"".join(f"<li>{skill}</li>" for skill in matched) if matched else "<p>No matched skills.</p>"}</ul>
        </div>

        <div class="section missing">
            <h2>❌ Missing Skills (Expected but not in Resume):</h2>
            <ul>{"".join(f"<li>{skill}</li>" for skill in missing) if missing else "<p>Perfect Match!</p>"}</ul>
        </div>
    </body>
    </html>
    """

    html_path = "resume_analysis.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Open in browser
    webbrowser.open('file://' + os.path.realpath(html_path))

# ================================
# 🧑‍💻 Inputs
# ================================

resume_path = r"C:\Users\tejas\OneDrive\Desktop\Tejaswini Madduluri.docx"

job_description = """
We are looking for a Python full stack developer with experience in Django, React, MySQL, HTML, CSS, and Git.
Familiarity with REST APIs and deployment tools is a plus.
"""

skills_list = [
    "Python", "Java", "C++", "Django", "Flask", "React",
    "HTML", "CSS", "JavaScript", "MySQL", "MongoDB",
    "Git", "GitHub", "REST API", "Deployment", "AWS", "Azure"
]

# ================================
# 🚀 Run
# ================================

try:
    resume_text = get_resume_text(resume_path)
    resume_skills, matched_skills, missing_skills = analyze_resume(resume_text, job_description, skills_list)
    generate_html(resume_skills, matched_skills, missing_skills)

except Exception as e:
    print(f"\n⚠️ Error: {e}")
