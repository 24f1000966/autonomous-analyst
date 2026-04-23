class ReportAgent:
    def __init__(self):
        self.name = "Report Agent"
        
    def execute(self, stats, insights, recommendations, charts, forecasts, alerts):
        print(f"[{self.name}] Compiling advanced report...")
        report = []
        
        report.append("🌟 Executive Summary")
        report.append("========================\n")
        
        # Format Alerts if any
        if alerts:
            report.append("🚨 Critical Business Alerts:")
            for a in alerts:
                severity = a.get('level', 'LOW').upper()
                report.append(f"  [{severity}] {a.get('msg')}")
            report.append("\n")
            
        # Format Forecasts
        if forecasts and forecasts.get("forecasts"):
            report.append("📈 Predictive Forecast (Next Period):")
            for col, f in forecasts["forecasts"].items():
                trend = f.get('trend_direction', 'Flat')
                nxt = f.get('next_period_prediction', 0)
                report.append(f"  • {col}: Projected -> {nxt} (Trend: {trend})")
            report.append("\n")
            
        # Format Break-Even Analysis
        if stats and 'break_even_analysis' in stats:
            be = stats['break_even_analysis']
            report.append("⚖️ Break-Even Analysis:")
            report.append(f"  • Status: {be['status']}")
            report.append(f"  • Current Revenue: ${be['actual_total_revenue']}")
            report.append(f"  • Break-Even Revenue Target: ${be['estimated_breakeven_revenue']}")
            report.append("\n")
        
        # Format Insights nicely
        report.append("🔍 Key Insights Discovered:")
        for idx, insight in enumerate(insights.get('insights', []), 1):
            report.append(f"  • {insight}")
        report.append("\n")
            
        # Format Recommendations nicely
        if recommendations:
            report.append("💡 Strategic Recommendations:")
            if isinstance(recommendations, list):
                for rec in recommendations:
                    report.append(f"  • {rec}")
            else:
                report.append(f"  • {recommendations.replace('Recommendation: ', '')}")
        else:
            report.append("💡 Strategic Recommendations:")
            report.append("  • No specific recommendations generated for this dataset.")
            
        return "\n".join(report)
