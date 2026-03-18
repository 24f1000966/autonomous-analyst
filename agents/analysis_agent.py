class AnalysisAgent:
    def __init__(self):
        self.name = "Analysis Agent"
        
    def execute(self, dataframe):
        print(f"[{self.name}] Analyzing statistics...")
        num_cols = dataframe.select_dtypes(include=['number']).columns
        stats = {}
        
        if len(num_cols) > 0:
            stats['summary'] = dataframe[num_cols].describe().to_dict()
            stats['columns'] = list(num_cols)
        
        return stats
