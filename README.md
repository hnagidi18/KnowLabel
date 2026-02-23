KnowLabel – AI-Powered Ingredient Analyzer

📌 Overview
KnowLabel is an AI-driven application that helps users analyze cosmetic and skincare product ingredients. It identifies whether ingredients are beneficial, harmful, or unknown, provides detailed descriptions, and suggests safer alternatives. Unknown ingredients are explained using a local Llama 3.2 AI model, making the system both informative and interactive.

🚀 Problem Statement
Consumers often struggle to understand complex chemical names on product labels and may unknowingly use harmful or allergenic substances. Existing solutions lack real-time AI assistance for unknown ingredients and fail to provide alternative recommendations. KnowLabel solves this by combining a curated ingredient database with AI-powered insights.

💡 Key Features
1. Ingredient classification: Beneficial, Harmful, or Unknown.
2. AI explanations for ingredients not in the database using Llama 3.2.
3. Suggestions for safer or natural alternatives.
4. Interactive chatbot interface for user queries about ingredients.
5. Real-time parsing and analysis of multiple ingredients.

🛠️ Hardware Used
1. Personal computer or laptop for running the application.
2. (Optional) Mobile camera for OCR scanning of product labels.

💻 Software & Technologies
1. Python & Streamlit – Web interface and application framework.
2. CSV database – Curated ingredient dataset.
3. Ollama API + Llama 3.2 – Local AI model for unknown ingredient explanations.
4. Requests & JSON – API communication and data handling.

🧠 Working Principle
1. Users input ingredients manually or via OCR scanning.
2. Each ingredient is matched against the database for classification.
3. If an ingredient is not found, the system queries Llama 3.2 AI for details.

4.esults are displayed in the UI with classification, description, and alternative suggestions.
5.Users can interact with the chatbot to ask additional questions, receiving AI-driven insights.# KnowLabel
