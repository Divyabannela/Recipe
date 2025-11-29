# 🍽️ AI Recipe Generator using LangChain

This project generates recipes based on the ingredients entered by the user.  
It uses **LangChain**, **Prompt Engineering**, **Flask**, and **HTML/CSS**.

## 🚀 Features
- Enter any ingredients
- Get 3 suggested recipe names
- Select a recipe to get:
  - Ingredients list
  - Step-by-step instructions
  - Cooking time
  - Difficulty level
  - Calorie estimate
- Clean HTML + CSS UI
- LangChain SequentialChains
- Deployable on Render

## 🏗️ Tech Stack
- Python + Flask
- LangChain + LLMs
- HTML5 + CSS3
- Render (deployment)

## 📂 Project Structure
recipe-generator/
│
├── app.py  
├── templates/
│     └── index.html
├── static/
│     └── style.css
├── requirements.txt
└── README.md

## ▶️ Run Locally
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=yourkey
python app.py
