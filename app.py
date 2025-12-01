import os
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ----------------------------
# Helper function to call Groq
# ----------------------------
def groq_chat(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # FREE MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------
# 1️⃣ RECIPE SUGGESTION
# ---------------------------------------------------------
def suggest_recipes(ingredients):
    prompt = f"""
You are an expert chef. Based on the following ingredients:
{ingredients}

Suggest exactly 3 possible recipes.

Output only in this format:
1. Recipe name
2. Recipe name
3. Recipe name
"""
    return groq_chat(prompt)


# ---------------------------------------------------------
# 2️⃣ RECIPE DETAILS
# ---------------------------------------------------------
def recipe_details(recipe_name):
    prompt = f"""
Write a complete recipe for: {recipe_name}

Output EXACTLY in this format:

### Ingredients
- item1
- item2

### Instructions
1. step
2. step
3. step

### Cooking Time
X minutes

### Difficulty
Easy / Medium / Hard

### END
"""
    return groq_chat(prompt)


# ---------------------------------------------------------
# 3️⃣ CALORIE ESTIMATOR
# ---------------------------------------------------------
def recipe_calories(recipe_name):
    prompt = f"""
Estimate the total calories for the recipe "{recipe_name}".
Just return one number + the word "calories".

Example:
350 calories
"""
    return groq_chat(prompt)


# ---------------------------------------------------------
# FLASK ROUTES
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    recipes = ""
    details = ""
    calories = ""

    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        selected_recipe = request.form.get("selected_recipe")

        if selected_recipe:
            details = recipe_details(selected_recipe)
            calories = recipe_calories(selected_recipe)
        else:
            recipes = suggest_recipes(ingredients)

    return render_template("index.html", recipes=recipes, details=details, calories=calories)


# ---------------------------------------------------------
# Run on Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
