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
            
            # --- Break-Even Analysis Logic ---
            rev_cols = [c for c in num_cols if 'rev' in c.lower() or 'sales' in c.lower()]
            cost_cols = [c for c in num_cols if 'cost' in c.lower() or 'exp' in c.lower()]
            
            if rev_cols and cost_cols:
                try:
                    total_rev = dataframe[rev_cols[0]].sum()
                    total_cost = dataframe[cost_cols[0]].sum()
                    
                    # Look for explicit fixed cost, otherwise assume 30% of total costs
                    fixed_cols = [c for c in num_cols if 'fixed' in c.lower()]
                    if fixed_cols:
                        fc = dataframe[fixed_cols[0]].sum()
                        vc = total_cost - fc
                    else:
                        fc = total_cost * 0.3
                        vc = total_cost * 0.7
                        
                    contribution_margin = total_rev - vc
                    if contribution_margin > 0:
                        break_even_revenue = fc / (contribution_margin / total_rev)
                        stats['break_even_analysis'] = {
                            'estimated_breakeven_revenue': round(break_even_revenue, 2),
                            'actual_total_revenue': round(total_rev, 2),
                            'status': 'Profitable (Above Break-Even)' if total_rev > break_even_revenue else 'Loss-Making (Below Break-Even)'
                        }
                except:
                    pass
        
        return stats
