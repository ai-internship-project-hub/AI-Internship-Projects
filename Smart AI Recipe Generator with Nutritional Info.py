!pip install streamlit openai requests

import random
from IPython.display import display, HTML

# Sample nutritional database
nutritional_database = {
    'egg': {'calories': 155, 'protein': 13, 'fat': 11},
    'milk': {'calories': 42, 'protein': 3.4, 'fat': 1},
    'rice': {'calories': 130, 'protein': 2.7, 'fat': 0.3},
    'chicken': {'calories': 239, 'protein': 27, 'fat': 14},
    'tomato': {'calories': 18, 'protein': 0.9, 'fat': 0.2},
    'onion': {'calories': 40, 'protein': 1.1, 'fat': 0.1},
    'potato': {'calories': 77, 'protein': 2, 'fat': 0.1},
    'spinach': {'calories': 23, 'protein': 2.9, 'fat': 0.4}
}

# Cooking steps pool
cooking_steps = [
    "Wash and chop the ingredients properly.",
    "Heat oil in a pan and sauté the onions until golden.",
    "Add the chopped tomatoes and cook till soft.",
    "Mix in the spices and stir well.",
    "Add the main ingredients and stir-fry for a few minutes.",
    "Pour in water or broth if needed and let it simmer.",
    "Cover the lid and cook on low flame for 10-15 minutes.",
    "Garnish with herbs and serve hot!"
]

def get_recipe(ingredients):
    random_steps = random.sample(cooking_steps, k=min(5, len(cooking_steps)))  # pick random steps
    recipe = "<ol>"
    for step in random_steps:
        recipe += f"<li>{step}</li>"
    recipe += "</ol>"
    return recipe

def calculate_nutrition(ingredients):
    total = {'calories': 0, 'protein': 0, 'fat': 0}
    missing = []
    for item in ingredients:
        if item.lower() in nutritional_database:
            data = nutritional_database[item.lower()]
            total['calories'] += data['calories']
            total['protein'] += data['protein']
            total['fat'] += data['fat']
        else:
            missing.append(item)
    return total, missing

# Input from user
user_input = input("Enter ingredients separated by commas (e.g. egg, milk, rice): ")
ingredients = [x.strip().lower() for x in user_input.split(',')]

# Generate output
recipe = get_recipe(ingredients)
nutrition, missing = calculate_nutrition(ingredients)

# Display with HTML
html_output = f"""
<div style="font-family: Arial; border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f9fff9;">
    <h2 style="color: #4CAF50;">🍳 Smart AI Recipe Generator</h2>
    <h3>👩‍🍳 Ingredients:</h3>
    <p>{', '.join(ingredients)}</p>
    <h3>📝 Recipe Steps:</h3>
    {recipe}
    <h3>📊 Nutritional Information:</h3>
    <ul>
        <li><b>Calories:</b> {nutrition['calories']} kcal</li>
        <li><b>Protein:</b> {nutrition['protein']} g</li>
        <li><b>Fat:</b> {nutrition['fat']} g</li>
    </ul>
"""

if missing:
    html_output += f"<p style='color: red;'>⚠️ <b>No nutritional data for:</b> {', '.join(missing)}</p>"

html_output += "</div>"

display(HTML(html_output))

