import streamlit as st
import csv
import requests
import json


def ask_ollama(prompt, model="llama3.2"):
    """
    Sends a prompt to the local Ollama model (Llama 3.2) and returns its generated response.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": model, "prompt": prompt},
            timeout=120  
        )

        if response.status_code != 200:
            return f"⚠ API Error: {response.status_code} - {response.text}"

        text = ""
        for line in response.text.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                text += data.get("response", "")
            except json.JSONDecodeError:
                continue

        if not text.strip():
            return "⚠ No response from model (check memory or prompt length)."
        return text

    except requests.exceptions.ConnectionError:
        return "❌ Ollama server not running. Please run `ollama serve` first."
    except Exception as e:
        return f"⚠ Error: {e}"



@st.cache_data
def load_ingredients(file_path="combined_ingredient_dataset_appended.csv"):
    """
    Loads ingredient data from a CSV file.
    Columns: ingredient, beneficial, description, alternatives
    """
    ingredients = {}
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["ingredient"].strip().lower()
                beneficial = row["beneficial"].strip().lower() == "true"
                description = row["description"].strip()
                alternatives = [alt.strip() for alt in row["alternatives"].split(";") if alt.strip()] if row["alternatives"] else []
                ingredients[name] = {
                    "beneficial": beneficial,
                    "description": description,
                    "alternatives": alternatives,
                }
        st.success(f"✅ Loaded {len(ingredients)} ingredients from {file_path}")
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' not found.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading ingredients: {e}")
        st.stop()
    return ingredients



def analyze_ingredients(input_text, ingredients_db):
    """
    Parses and checks ingredients against the dataset.
    If not found, it will call Ollama automatically for details.
    """
    raw_ingredients = [item.strip() for item in input_text.replace("\n", ",").split(",") if item.strip()]
    results = {}

    for ingredient in raw_ingredients:
        key = ingredient.lower()
        if key in ingredients_db:
            results[ingredient] = ingredients_db[key]
        else:
            with st.spinner(f"🤖 Asking Llama 3.2 about '{ingredient}'..."):
                ai_info = ask_ollama(f"What can you tell me about the ingredient '{ingredient}' in cosmetics or skincare?")

            results[ingredient] = {
                "beneficial": None,
                "description": ai_info,
                "alternatives": [],
            }

    return results


def chatbot_answer(user_input, ingredients_db):
    user_input_lower = user_input.lower()
    found_ingredient = None
    for ing_key in ingredients_db.keys():
        if ing_key in user_input_lower:
            found_ingredient = ing_key
            break

    if found_ingredient:
        info = ingredients_db[found_ingredient]
        response = f"**{found_ingredient.title()}**\n\n"
        if info["beneficial"]:
            response += "✅ This ingredient is *beneficial*.\n"
        else:
            response += "⚠ This ingredient may be *harmful or controversial*.\n"
        response += f"**Description:** {info['description']}\n"
        if info["alternatives"]:
            response += f"**Alternatives:** {', '.join(info['alternatives'])}\n"
        return response
    else:
        ai_response = ask_ollama(f"{user_input}")
        return ai_response


def main():
    st.set_page_config(page_title="KnowLabel 🧴", page_icon="🧴", layout="centered")
    st.title("KnowLabel  – Ingredient Analyzer")

    st.write("""
    Enter your ingredients below to analyze if they're beneficial or harmful.
    Unknown ingredients will be automatically explained by the local Llama 3.2 model.
    """)

    ingredients_db = load_ingredients()

    st.header("🔍 Ingredient Analysis")
    user_input = st.text_area(
        "Enter Ingredients List:",
        height=150,
        placeholder="e.g. Water, Glycerin, Sodium Chloride, Parabens, Hyaluronic Acid",
        key="ingredients_input"
    )

    if st.button("Analyze Ingredients", key="analyze_button"):
        if not user_input.strip():
            st.warning("Please enter some ingredients.")
        else:
            with st.spinner("Analyzing..."):
                results = analyze_ingredients(user_input, ingredients_db)

            st.markdown("---")
            st.subheader("Results:")
            for ing, info in results.items():
                st.markdown(f"### {ing}")
                if info["beneficial"] is True:
                    st.success("✅ Beneficial")
                elif info["beneficial"] is False:
                    st.error("⚠ Harmful or Controversial")
                else:
                    st.info("🤖 Information fetched from Llama 3.2")
                st.write(info["description"])
                if info["alternatives"]:
                    st.info(f"Alternatives: {', '.join(info['alternatives'])}")
                st.markdown("---")

    st.header("💬 Chatbot")
    st.write("Ask about any ingredient — if it’s unknown, Llama 3.2 will answer!")

    chatbot_input = st.text_input("Ask your question:")
    if chatbot_input:
        with st.spinner("Llama 3.2 is thinking..."):
            response = chatbot_answer(chatbot_input, ingredients_db)
        st.markdown(response)


if __name__ == "__main__":
    main()
