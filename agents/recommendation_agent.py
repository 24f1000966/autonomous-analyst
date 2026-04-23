import os
from google import genai
import json

class RecommendationAgent:
    def __init__(self):
        self.name = "Recommendation Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            
    def execute(self, insights, alerts):
        print(f"[{self.name}] Generating recommendations...")
        if self.client:
            insights_str = json.dumps(insights)
            alerts_str = json.dumps(alerts)
            
            prompt = f"""Act as a Chief Operating Officer (COO) for a Tech SaaS Company. 
Based on these insights: {insights_str}
And these critical alerts: {alerts_str}

List 3 highly actionable, business-focused recommendations to improve ROI and mitigate the alerts.
If there is a high-severity alert, dedicate at least one recommendation to solving it (e.g. 'Reduce operational cost by X', 'Improve user retention via Y', 'Increase marketing budget in Z').

Return ONLY the recommendations as distinct bullet points without markdown bolding or extra introductory text.
"""
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                ai_recs = [r.strip().lstrip('*-• ') for r in response.text.split('\n') if r.strip() and len(r.strip()) > 5]
                return ai_recs[:3]
            except:
                pass
        
        fallback = ["Reduce operational cost anomalies associated with recent variance.", "Improve user retention strategies in underperforming cohorts."]
        if alerts:
            fallback.append(f"Mitigate risk: {alerts[0].get('msg', 'Review recent alerts.')}")
        return fallback
