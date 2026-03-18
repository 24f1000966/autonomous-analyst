import os
import google.generativeai as genai

class ReportGeneratorAgent:
    def __init__(self):
        self.name = "Report Generator"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None

    def execute(self, insights, charts):
        insights_str = "\n".join([f"- {i}" for i in insights.get('insights', [])])
        
        if self.model:
            prompt = f"""
            Act as an Executive Business Strategist. Write a short, highly professional summary report based on the following AI-discovered insights. Provide strategic business decisions that management should take. 
            Keep it strictly 3 short paragraphs.
            
            INSIGHTS:
            {insights_str}
            """
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini API Error: {e}")
                
        # Fallback
        return f"Executive Summary: The analyzed dataset yields {len(insights.get('insights', []))} key findings regarding the distribution of major performance metrics. Based on the insights found:\n {insights_str} \n\nStrategic Recommendation: Investigate the variances observed in the leading indicators to optimize quarterly outcomes."
