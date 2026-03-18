from .cleaning_agent import DataCleaningAgent
from .analysis_agent import AnalysisAgent
from .visualization_agent import VisualizationAgent
from .insight_agent import InsightAgent
from .recommendation_agent import RecommendationAgent
from .report_agent import ReportAgent

class NexusWorkflow:
    def __init__(self):
        self.cleaner = DataCleaningAgent()
        self.analyst = AnalysisAgent()
        self.visualizer = VisualizationAgent()
        self.insighter = InsightAgent()
        self.recommender = RecommendationAgent()
        self.reporter = ReportAgent()
        
    def run_workflow(self, dataframe):
        cleaned_data = self.cleaner.execute(dataframe)
        stats = self.analyst.execute(cleaned_data)
        charts = self.visualizer.execute(cleaned_data, stats)
        insights = self.insighter.execute(cleaned_data, stats)
        recommendations = self.recommender.execute(insights)
        report = self.reporter.execute(stats, insights, recommendations, charts)
        
        return {
            "insights": insights,
            "charts": charts,
            "recommendations": recommendations,
            "report_summary": report
        }
