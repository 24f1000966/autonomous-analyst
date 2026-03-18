class ReportAgent:
    def __init__(self):
        self.name = "Report Agent"
        
    def execute(self, stats, insights, recommendations, charts):
        print(f"[{self.name}] Compiling report...")
        report = []
        report.append("### Automated Business Analysis Report\n")
        report.append(f"**Insights Found:**\n{insights.get('insights', [])}\n")
        report.append(f"**Strategic Recommendations:**\n{recommendations}\n")
        
        return "\n".join(report)
