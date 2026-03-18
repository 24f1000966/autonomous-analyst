import os
import google.generativeai as genai

class ChatAgent:
    def __init__(self):
        self.name = "Chat Agent"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None

    def execute(self, question, context):
        print(f"[{self.name}] Answering question: {question}")
        if self.model:
            prompt = f"""
            You are an AI Business Analyst Assistant. 
            Answer the user's question based on the following report context.
            
            REPORT CONTEXT:
            {context}
            
            QUESTION: {question}
            
            Provide a helpful, concise, and strategic answer. Format your answer elegantly.
            """
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"[{self.name}] Error: {str(e)}")
                return "Sorry, I am having trouble connecting to my brain right now."
        return f"Simulated Response: Based on your report, I recommend further investigating the variances regarding: {question}"
