from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import random

console = Console()

# Predefined project ideas
project_ideas = {
    "python": [
        "AI-Powered Resume Analyzer",
        "Chatbot for Student Queries",
        "Text Summarizer using NLP",
        "Weather Forecasting App"
    ],
    "machine learning": [
        "Stock Price Prediction",
        "Movie Recommendation System",
        "Credit Card Fraud Detection",
        "Handwritten Digit Recognition"
    ],
    "web development": [
        "Portfolio Website",
        "E-commerce Store",
        "Blogging Platform",
        "Online Learning System"
    ],
    "data science": [
        "Customer Segmentation Analysis",
        "Sales Forecasting",
        "Sentiment Analysis on Social Media",
        "Healthcare Data Insights"
    ],
    "nlp": [
        "Spam Email Classifier",
        "AI Language Translation Assistant",
        "Speech Emotion Recognition",
        "Text-to-Speech Converter"
    ],
    "deep learning": [
        "Image Caption Generator",
        "Face Recognition System",
        "Self-Driving Car Simulation",
        "AI Music Composer"
    ]
}

def recommend_projects(user_skills):
    recommendations = []
    for skill in user_skills:
        skill = skill.lower().strip()
        if skill in project_ideas:
            recommendations.extend(project_ideas[skill])
    return recommendations

# --- Main Program ---
console.print(Panel.fit("🤖 AI PROJECT RECOMMENDER 🤖", style="bold cyan", title="Welcome", subtitle="Made with Python"))

skills_input = console.input("[bold yellow]👉 Enter your skills (comma separated): [/]")
user_skills = skills_input.split(",")

recommended_projects = recommend_projects(user_skills)

if recommended_projects:
    console.print("\n[bold green]✅ Based on your skills, here are some project ideas:[/]\n")
    
    table = Table(title="Project Recommendations", style="bold magenta")
    table.add_column("No.", style="cyan", justify="center")
    table.add_column("Project Idea", style="yellow")

    for i, project in enumerate(random.sample(recommended_projects, min(5, len(recommended_projects))), 1):
        table.add_row(str(i), project)

    console.print(table)
else:
    console.print(Panel.fit("⚠️ No matching projects found! Try adding skills like Python, ML, Web Development, etc.", style="bold red"))
