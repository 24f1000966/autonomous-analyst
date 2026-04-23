from .cleaning_agent import DataCleaningAgent
from .analysis_agent import AnalysisAgent
from .visualization_agent import VisualizationAgent
from .forecast_agent import ForecastAgent
from .alert_agent import AlertAgent
from .insight_agent import InsightAgent
from .recommendation_agent import RecommendationAgent
from .report_agent import ReportAgent

class NexusWorkflow:
    def __init__(self):
        self.cleaner = DataCleaningAgent()
        self.analyst = AnalysisAgent()
        self.visualizer = VisualizationAgent()
        self.forecaster = ForecastAgent()
        self.alerter = AlertAgent()
        self.insighter = InsightAgent()
        self.recommender = RecommendationAgent()
        self.reporter = ReportAgent()
        
    def run_workflow(self, dataframe):
        cleaned_data = self.cleaner.execute(dataframe)
        stats = self.analyst.execute(cleaned_data)
        charts = self.visualizer.execute(cleaned_data, stats)
    
        forecasts = self.forecaster.execute(cleaned_data, stats)
        alerts = self.alerter.execute(stats, forecasts, cleaned_data)
        
        insights = self.insighter.execute(cleaned_data, stats, forecasts, alerts)
        recommendations = self.recommender.execute(insights, alerts)
        
        report_summary = self.reporter.execute(stats, insights, recommendations, charts, forecasts, alerts)
        
        return {
            "insights": insights,
            "charts": charts,
            "forecasts": forecasts,
            "alerts": alerts,
            "recommendations": recommendations,
            "report_summary": report_summary
        }
