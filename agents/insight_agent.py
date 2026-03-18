import os
import google.generativeai as genai

class InsightAgent:
    def __init__(self):
        self.name = "Insight Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            
    def execute(self, data, stats):
        print(f"[{self.name}] Extracting insights...")
        if self.model:
            column_names = list(data.columns)
            
            # Calculate top categories
            cat_cols = data.select_dtypes(exclude=['number']).columns
            top_values = {}
            for col in cat_cols:
                top_values[col] = data[col].value_counts().head(3).to_dict()
                
            # Calculate simple correlations
            num_cols = list(data.select_dtypes(include=['number']).columns)
            correlations = {}
            if len(num_cols) > 1:
                correlations = data[num_cols].corr().to_dict()
                
            prompt = f"""You are a professional business analyst.

Given the following dataset summary:
* Columns: {column_names}
* Key statistics: {stats}
* Top categories: {top_values}
* Trends: See statistics.
* Correlations: {correlations}

Generate specific, non-generic business insights.

Rules:
* DO NOT give generic statements like "data is consistent"
* Each insight must reference actual columns or values
* Explain what is happening and why it matters

Examples:
* "Region West contributes 45% of total revenue, making it the dominant market"
* "Product A has the highest sales but also the highest return rate"

Generate at least 5 meaningful insights.
"""
            try:
                response = self.model.generate_content(prompt)
                ai_insights = [i.strip() for i in response.text.split('\n') if i.strip() and len(i.strip()) > 5]
                return {"insights": ai_insights}
            except Exception as e:
                print(f"[{self.name}] Error: {str(e)}")
        return {"insights": ["Simulated Insight: Consistent numeric distributions.", "Simulated Insight: No extreme outliers detected."]}
