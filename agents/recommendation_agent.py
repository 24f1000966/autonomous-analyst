import os
import google.generativeai as genai

class RecommendationAgent:
    def __init__(self):
        self.name = "Recommendation Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            
    def execute(self, insights):
        print(f"[{self.name}] Generating recommendations...")
        if self.model:
            insights_str = str(insights)
            prompt = f"Act as a Business Consultant. Based on these insights: {insights_str}, list 2 actionable business recommendations to improve ROI."
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except:
                pass
        return "Recommendation: Investigate variances and increase marketing pipeline."
