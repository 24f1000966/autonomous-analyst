import os
from google import genai
import json

class InsightAgent:
    def __init__(self):
        self.name = "Insight Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            
    def execute(self, data, stats, forecasts, alerts):
        print(f"[{self.name}] Extracting insights...")
        if self.client:
            column_names = list(data.columns)
            
            cat_cols = data.select_dtypes(exclude=['number']).columns
            top_values = {}
            for col in cat_cols:
                try:
                    top_values[col] = data[col].value_counts().head(3).to_dict()
                except:
                    pass
                
            num_cols = list(data.select_dtypes(include=['number']).columns)
            correlations = {}
            if len(num_cols) > 1:
                try:
                    correlations = data[num_cols].corr().to_dict()
                except:
                    pass
             
            forecasts_ctx = json.dumps(forecasts.get("forecasts", {}))
            alerts_ctx = json.dumps(alerts)
                
            prompt = f"""You are a senior tech company business analyst.

Given the following dataset summary:
* Columns: {column_names}
* Key statistics: {stats}
* Top categories: {top_values}
* Correlations: {correlations}
* Forecast Projections: {forecasts_ctx}
* System Alerts: {alerts_ctx}

Generate specific, non-generic business insights with CAUSE-EFFECT logic.

Rules:
* Detail WHY things are happening by cross-referencing correlations or forecasts.
* If there is an Alert (e.g. Revenue dropping), explain what might be causing it based on the data.
* Do not give generic statements. Use the exact numbers and column names provided.

Examples:
* "Revenue dropped 15% due to a massive decline in Region West active users, despite stable engagement elsewhere."
* "User churn is trending upwards (+5%) because the average support ticket resolution time correlates perfectly (0.85) with cancellations."

Generate exactly 5 highly analytical insights as bullet points.
"""
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                ai_insights = [i.strip() for i in response.text.split('\n') if i.strip() and len(i.strip()) > 5]
               
                ai_insights = [i.lstrip('*-• ') for i in ai_insights]
                return {"insights": ai_insights[:5]} 
            except Exception as e:
                print(f"[{self.name}] Error: {str(e)}")
        
        sim_insights = ["Simulated Insight: Consistent numeric distributions.", "Simulated Insight: No extreme outliers detected."]
        if alerts:
            sim_insights.append(f"Simulated Insight: Alert Triggered - {alerts[0].get('msg', 'Risk detected.')}")
        return {"insights": sim_insights}
