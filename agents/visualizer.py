import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import uuid

class VisualizerAgent:
    def __init__(self, static_folder="static/charts"):
        self.name = "Visualizer Agent"
        self.static_folder = static_folder
        if not os.path.exists(self.static_folder):
            os.makedirs(self.static_folder, exist_ok=True)
            
    def execute(self, data, insights):
        # Implementation of generating actual charts based on data
        num_cols = data.select_dtypes(include=['number']).columns
        cat_cols = data.select_dtypes(include=['object', 'category']).columns
        
        charts = []
        plt.style.use('dark_background')
        
        if len(num_cols) >= 2:
            # Correlation Heatmap
            plt.figure(figsize=(8, 6))
            corr = data[num_cols].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f",
                        cbar_kws={'label': 'Correlation'})
            plt.title('Feature Correlation Matrix', color='white')
            chart_filename = f"chart_{uuid.uuid4().hex[:8]}.png"
            chart_path = os.path.join(self.static_folder, chart_filename)
            plt.savefig(chart_path, transparent=True)
            plt.close()
            charts.append(chart_filename)
            
        if len(cat_cols) > 0 and len(num_cols) > 0:
            # Bar chart of average value by category
            top_cat = cat_cols[0]
            top_num = num_cols[0]
            
            plt.figure(figsize=(10, 5))
            avg_data = data.groupby(top_cat)[top_num].mean().sort_values(ascending=False).head(10)
            sns.barplot(x=avg_data.index, y=avg_data.values, palette='viridis')
            plt.title(f'Average {top_num} by {top_cat}', color='white')
            plt.xticks(rotation=45, color='lightgray')
            plt.yticks(color='lightgray')
            plt.tight_layout()
            
            chart_filename = f"chart_{uuid.uuid4().hex[:8]}.png"
            chart_path = os.path.join(self.static_folder, chart_filename)
            plt.savefig(chart_path, transparent=True)
            plt.close()
            charts.append(chart_filename)
            
        return charts
