import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import pandas as pd

class VisualizationAgent:
    def __init__(self, static_folder="static/charts"):
        self.name = "Visualization Agent"
        self.static_folder = static_folder
        os.makedirs(self.static_folder, exist_ok=True)
            
    def execute(self, data, stats):
        print(f"[{self.name}] Generating Context-Aware Visualizations...")
        charts = []
        filename = f"chart_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.static_folder, filename)
        
        sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f8fafc", "figure.facecolor": "#ffffff", "grid.color": "#e2e8f0"})
        plt.figure(figsize=(9, 5))
        
        num_cols = list(data.select_dtypes(include=['number']).columns)
        cat_cols = list(data.select_dtypes(include=['object', 'category']).columns)
        datetime_cols = list(data.select_dtypes(include=['datetime']).columns)
        
        if not datetime_cols:
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    try:
                        data[col] = pd.to_datetime(data[col])
                        datetime_cols.append(col)
                        break
                    except:
                        pass
        
        chart_plotted = False
        
        if datetime_cols and num_cols:
            time_col = datetime_cols[0]
            val_col = num_cols[0]
            
            ts_data = data.sort_values(time_col).dropna(subset=[time_col, val_col])
            
            if len(ts_data) > 300:
                ts_data = ts_data.set_index(time_col).resample('ME')[val_col].mean().reset_index()
                
            sns.lineplot(data=ts_data, x=time_col, y=val_col, color="#2563eb", linewidth=2.5, marker="o")
            plt.title(f'{val_col} Trend Over Time', pad=15, fontweight='bold', fontsize=14, color="#1e293b")
            plt.xlabel(time_col, labelpad=10, fontweight='medium', color="#64748b")
            plt.ylabel(val_col, labelpad=10, fontweight='medium', color="#64748b")
            plt.xticks(rotation=45)
            chart_plotted = True

        elif cat_cols and len(data[cat_cols[0]].unique()) <= 15:
            cat_col = cat_cols[0]
            if num_cols:
                val_col = num_cols[0]
              
                agg_data = data.groupby(cat_col)[val_col].mean().reset_index().sort_values(by=val_col, ascending=False).head(10)
                sns.barplot(data=agg_data, x=val_col, y=cat_col, palette="Blues_r")
                plt.title(f'Average {val_col} by {cat_col}', pad=15, fontweight='bold', fontsize=14, color="#1e293b")
                plt.xlabel(f'Mean {val_col}', labelpad=10, fontweight='medium', color="#64748b")
                plt.ylabel(cat_col, labelpad=10, fontweight='medium', color="#64748b")
                chart_plotted = True
            else:
                
                sns.countplot(data=data, y=cat_col, order=data[cat_col].value_counts().index[:10], palette="Blues_r")
                plt.title(f'Top Counts in {cat_col}', pad=15, fontweight='bold', fontsize=14, color="#1e293b")
                plt.xlabel('Count', labelpad=10, fontweight='medium', color="#64748b")
                plt.ylabel(cat_col, labelpad=10, fontweight='medium', color="#64748b")
                chart_plotted = True
         
        elif num_cols:
            val_col = num_cols[0]
            sns.histplot(data=data, x=val_col, kde=True, color="#2563eb", bins=30)
            plt.title(f'Distribution of {val_col}', pad=15, fontweight='bold', fontsize=14, color="#1e293b")
            plt.xlabel(val_col, labelpad=10, fontweight='medium', color="#64748b")
            plt.ylabel('Frequency', labelpad=10, fontweight='medium', color="#64748b")
            chart_plotted = True
        
        else:
            if len(num_cols) >= 2:
                corr = data[num_cols].corr()
                sns.heatmap(corr, annot=True, cmap='Blues', fmt=".2f", cbar=False)
                plt.title('Feature Correlations', pad=15, fontweight='bold', fontsize=14, color="#1e293b")
                chart_plotted = True
                
        if chart_plotted:
            
            sns.despine()
            plt.tight_layout()
            plt.savefig(filepath, transparent=True, dpi=150)
            plt.close()
            charts.append(filename)
            
        return charts
