# Autonomous Business Analyst (Agentic AI System)

A complete, production-ready multi-agent AI system that automatically cleans, analyzes, visualizes, and reports on business datasets.

## Features & AI Agents
- **Data Cleaning Agent:** Cleans missing values and duplicates via pandas.
- **Analysis Agent:** Extracts statistical trends.
- **Visualization Agent:** Generates intelligent data-driven charts (Trend lines, Bar charts, Histograms) via seaborn.
- **Forecast Agent:** Predicts future trends (growth & direction) on time-series records.
- **Alert Agent:** Actively flags operational risks and anomalies based on statistical projections.
- **Insight Agent:** Uses LLMs to generate high-value, cause-and-effect reasoning based on forecasts and alerts.
- **Recommendation Agent:** Provides actionable business suggestions to management to mitigate risks flagged by the Alerter.
- **Report Agent:** Consolidates everything into a clean report dashboard.
- **Chat Agent:** Dedicated conversational AI memory that answers questions specifically concerning past reports.

## System Workflow Pipeline
The multi-agent system uses a strict execution pipeline to prevent AI hallucinations:
1. **Data Phase:** `File Upload -> Cleaning Agent -> Analysis Agent`
2. **Projection Phase:** `Forecast Agent (Predicts) -> Alert Agent (Flags Risks)`
3. **Reasoning Phase:** `Insight Agent (Why) -> Recommendation Agent (Actionables)`
4. **Compilation Phase:** `Visualization Agent (Aesthetics) -> Report Agent (Aggregation)`
5. **UI & Memory:** `Persisted to Database -> Displayed on Dashboard -> Available to Chat Agent`

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
- Open `http://127.0.0.1:5002`
- Register an account.
- Upload an Excel or CSV file.
- View the generated Autonomous Analysis Report.
