import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import uuid

class VisualizationAgent:
    def __init__(self, static_folder="static/charts"):
        self.name = "Visualization Agent"
        self.static_folder = static_folder
        os.makedirs(self.static_folder, exist_ok=True)
            
    def execute(self, data, stats):
        print(f"[{self.name}] Generating visualizations...")
        charts = []
        num_cols = data.select_dtypes(include=['number']).columns
        cat_cols = data.select_dtypes(include=['object', 'category']).columns
        
        plt.style.use('dark_background')
        
        if len(num_cols) >= 2:
            plt.figure(figsize=(8, 6))
            corr = data[num_cols].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Feature Correlations', color='white')
            filename = f"chart_{uuid.uuid4().hex[:8]}.png"
            plt.savefig(os.path.join(self.static_folder, filename), transparent=True)
            plt.close()
            charts.append(filename)
            
        return charts
