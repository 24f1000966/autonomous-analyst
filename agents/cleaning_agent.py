import pandas as pd

class DataCleaningAgent:
    def __init__(self):
        self.name = "Data Cleaning Agent"
        
    def execute(self, dataframe):
        print(f"[{self.name}] Cleaning data. Original shape: {dataframe.shape}")
        df = dataframe.copy()
        df = df.dropna(how='all')
        
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
            
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        df[cat_cols] = df[cat_cols].fillna("Unknown")
        
        df = df.drop_duplicates()
        print(f"[{self.name}] Cleaned data shape: {df.shape}")
        return df
