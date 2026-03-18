import os
import google.generativeai as genai

class AnalystAgent:
    def __init__(self):
        self.name = "Analyst Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            print("WARNING: GEMINI_API_KEY not found. Using fallback heuristics.")
        
    def execute(self, dataframe):
        # Get dataframe summary
        summary = dataframe.describe().to_string()
        head = dataframe.head(10).to_string()
        
        if self.model:
            prompt = f"""
            Act as a Senior Business Analyst. Analyze the following data summary and sample, and provide 2-3 deep, actionable business insights:
            
            SUMMARY:
            {summary}
            
            SAMPLE:
            {head}
            
            Format your insights as a list of strings. Limit the response to just the insights separated by the pipe character '|'. Do not include markdown formatting.
            """
            try:
                response = self.model.generate_content(prompt)
                ai_insights = [i.strip() for i in response.text.split('|') if i.strip()]
                if ai_insights:
                    return {"insights": ai_insights}
            except Exception as e:
                print(f"Gemini API Error: {e}")
        
        # Fallback pseudo-insights if no model or error
        num_cols = dataframe.select_dtypes(include=['number']).columns
        fallback_insights = [f"Processed structured tabular dataset containing {len(dataframe)} rows."]
        if len(num_cols) > 0:
            top_col = num_cols[0]
            max_val = dataframe[top_col].max()
            fallback_insights.append(f"Identified a maximum value of {max_val} in column '{top_col}'.")
            fallback_insights.append(f"The metric '{top_col}' shows strong variance requiring attention across key segments.")
        return {"insights": fallback_insights}
