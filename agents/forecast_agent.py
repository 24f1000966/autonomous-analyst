import pandas as pd
import numpy as np

class ForecastAgent:
    def __init__(self):
        self.name = "Forecast Agent"
        
    def execute(self, data, stats):
        print(f"[{self.name}] Running predictive forecasting...")
        forecasts = {}
        num_cols = data.select_dtypes(include=['number']).columns
    
        for col in num_cols:
            if 'rev' in col.lower() or 'user' in col.lower() or 'sales' in col.lower() or 'cost' in col.lower():
            
                datetime_cols = list(data.select_dtypes(include=['datetime']).columns)
                ts_data = data.sort_values(datetime_cols[0]) if datetime_cols else data
                
                recent_avg = ts_data[col].tail(3).mean()
                historic_avg = ts_data[col].head(max(len(ts_data)//2, 1)).mean()
                
                if historic_avg != 0 and not pd.isna(recent_avg) and not pd.isna(historic_avg):
                    growth_rate = ((recent_avg - historic_avg) / historic_avg)
                else:
                    growth_rate = 0
                
                direction = "Up" if growth_rate > 0 else ("Down" if growth_rate < 0 else "Flat")
                
                forecasts[col] = {
                    "current_avg": round(recent_avg, 2) if not pd.isna(recent_avg) else 0,
                    "next_period_prediction": round(recent_avg * (1 + growth_rate), 2) if not pd.isna(recent_avg) else 0,
                    "trend_direction": direction,
                    "growth_rate_pct": round(growth_rate * 100, 2)
                }
        return {"forecasts": forecasts}
