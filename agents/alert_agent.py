class AlertAgent:
    def __init__(self):
        self.name = "Alert Agent"
        
    def execute(self, stats, forecasts, data):
        print(f"[{self.name}] Scanning for anomalies and risks...")
        alerts = []
        
        for col, fcast in forecasts.get('forecasts', {}).items():
            if 'rev' in col.lower() or 'sales' in col.lower():
                if fcast['trend_direction'] == 'Down':
                    alerts.append({"level": "high", "msg": f"CRITICAL: Revenue ({col}) is trending down by {abs(fcast['growth_rate_pct'])}%. Urgent intervention required."})
            if 'user' in col.lower() or 'active' in col.lower():
                if fcast['trend_direction'] == 'Down':
                    alerts.append({"level": "medium", "msg": f"WARNING: Active user base ({col}) is shrinking by {abs(fcast['growth_rate_pct'])}%. Potential churn risk."})
            if 'cost' in col.lower() or 'exp' in col.lower():
                if fcast['trend_direction'] == 'Up' and fcast['growth_rate_pct'] > 10:
                    alerts.append({"level": "medium", "msg": f"ATTENTION: Costs ({col}) are rising sharply by {fcast['growth_rate_pct']}%."})
        
        cols = [c.lower() for c in data.columns]
        rev_col = next((c for c in data.columns if 'rev' in c.lower() or 'sales' in c.lower()), None)
        exp_col = next((c for c in data.columns if 'exp' in c.lower() or 'cost' in c.lower()), None)
        
        if rev_col and exp_col:
            try:
                total_rev = data[rev_col].sum()
                total_exp = data[exp_col].sum()
                if total_exp > total_rev and total_rev > 0:
                    alerts.append({"level": "high", "msg": f"CRITICAL: Total expenses ({total_exp}) have exceeded total revenue ({total_rev}). Serious profitability risk."})
            except Exception:
                pass
                
        return alerts
