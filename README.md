# Autonomous Business Analyst (Agentic AI System)

A complete, production-ready multi-agent AI system that automatically cleans, analyzes, visualizes, and reports on business datasets.

## Features
- **Data Cleaning Agent:** Cleans missing values and duplicates via pandas.
- **Analysis Agent:** Extracts statistical trends.
- **Visualization Agent:** Generates data-driven charts via matplotlib and seaborn.
- **Insight Agent:** Uses LLMs to generate high-value insights.
- **Recommendation Agent:** Provide business suggestions to management based on the insights.
- **Report Agent:** Consolidates everything into a clean report dashboard.

## Tech Stack
- Backend: Python (Flask)
- Frontend: HTML, CSS, JS
- AI/Agents: Google Gemini LLM API
- Database: SQLite (via SQLAlchemy)

## Setup Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Configure `.env` file with `GEMINI_API_KEY=your_key`
3. Run the application: `python app.py`

## Usage
- Open `http://127.0.0.1:5000`
- Register an account.
- Upload an Excel or CSV file.
- View the generated Autonomous Analysis Report.
