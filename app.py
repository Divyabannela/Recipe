import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

app = Flask(__name__)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------------------------
# 1️⃣ RECIPE SUGGESTION PROMPT
# ---------------------------------------------------------
suggest_prompt = PromptTemplate(
    input_variables=["ingredients"],
    template="""
You are an expert chef. Based on these ingredients:
{ingredients}

Suggest EXACTLY 3 possible recipes.

Format:
1. Recipe name
2. Recipe name
3. Recipe name
"""
)

# ---------------------------------------------------------
# 2️⃣ RECIPE DETAILS PROMPT
# ---------------------------------------------------------
details_prompt = PromptTemplate(
    input_variables=["recipe_name"],
    template="""
Write a complete recipe for: {recipe_name}

Output exactly in this format:

### Ingredients
- item1
- item2

### Instructions
1. step
2. step

### Cooking Time
X minutes

### Difficulty
Easy / Medium / Hard

### END
"""
)

# ---------------------------------------------------------
# 3️⃣ CALORIE ESTIMATOR PROMPT
# ---------------------------------------------------------
calorie_prompt = PromptTemplate(
    input_variables=["recipe_name"],
    template="""
Estimate the total calories for "{recipe_name}".
Return only:
123 calories
"""
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

        # If user selected recipe → generate details + calories
        if selected_recipe:
            final_prompt = details_prompt.format(recipe_name=selected_recipe)
            details = llm.invoke(final_prompt).content

            calorie_prompt_text = calorie_prompt.format(recipe_name=selected_recipe)
            calories = llm.invoke(calorie_prompt_text).content

        # If user first entered ingredients → show recipe suggestions
        else:
            suggest_prompt_text = suggest_prompt.format(ingredients=ingredients)
            recipes = llm.invoke(suggest_prompt_text).content

    return render_template("index.html", recipes=recipes, details=details, calories=calories)

# ---------------------------------------------------------
# Run on Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
