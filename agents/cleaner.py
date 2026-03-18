import pandas as pd

class DataCleanerAgent:
    def __init__(self):
        self.name = "Data Cleaner"
        
    def execute(self, dataframe):
        # Implementation of data cleaning
        print(f"Cleaning data with shape: {dataframe.shape}")
        
        # Real cleaning behavior
        df = dataframe.copy()
        
        # Drop entirely empty rows
        df = df.dropna(how='all')
        
        # Impute missing numeric values with median
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            df[col] = df[col].fillna(df[col].median())
        
        # Fill categorical/string columns with "Unknown"
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        df[cat_cols] = df[cat_cols].fillna("Unknown")
        
        # Removing duplicates
        df = df.drop_duplicates()
        
        print(f"Cleaned data shape: {df.shape}")
        return df
