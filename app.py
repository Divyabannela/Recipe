import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

# ---------------------------------------------------------
# 1️⃣ RECIPE SUGGESTION CHAIN
# ---------------------------------------------------------
suggest_prompt = PromptTemplate(
    input_variables=["ingredients"],
    template="""
You are an expert chef. Based on the following ingredients:
{ingredients}

Suggest exactly 3 possible recipes.

Output only in this format:
1. Recipe name
2. Recipe name
3. Recipe name
"""
)

suggest_chain = LLMChain(
    llm=llm,
    prompt=suggest_prompt,
    output_key="recipe_list",
)

# ---------------------------------------------------------
# 2️⃣ RECIPE DETAILS CHAIN
# ---------------------------------------------------------
details_prompt = PromptTemplate(
    input_variables=["recipe_name"],
    template="""
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
)

details_chain = LLMChain(
    llm=llm,
    prompt=details_prompt,
    output_key="recipe_details",
)

# ---------------------------------------------------------
# 3️⃣ CALORIE ESTIMATOR CHAIN
# ---------------------------------------------------------
calorie_prompt = PromptTemplate(
    input_variables=["recipe_name"],
    template="""
Estimate the total calories for the recipe "{recipe_name}".
Just return one number + the word "calories".

Example:
350 calories
"""
)

calorie_chain = LLMChain(
    llm=llm,
    prompt=calorie_prompt,
    output_key="calories",
)

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
            details = details_chain.run(recipe_name=selected_recipe)
            calories = calorie_chain.run(recipe_name=selected_recipe)

        else:
            recipes = suggest_chain.run(ingredients=ingredients)

    return render_template("index.html", recipes=recipes, details=details, calories=calories)

# ---------------------------------------------------------
# Run on Render (PORT fix)
# ---------------------------------------------------------
if __name__ == "__main__":
    from os import getenv
    app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)))


