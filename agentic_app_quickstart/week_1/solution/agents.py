import asyncio
from typing import List, Dict, Any, Optional
from agents import Agent, Runner, set_tracing_disabled, SQLiteSession
from agentic_app_quickstart.examples.helpers import get_model
from .tools import (
    get_available_datasets,
    get_dataset_info,
    get_column_names,
    calculate_column_statistics,
    count_rows_with_value,
    perform_data_aggregation,
    detect_correlations,
    find_outliers
)

set_tracing_disabled(True)


class AgentOrchestrator:
    """Coordinates multiple specialized agents for complex data analysis tasks."""
    
    def __init__(self):
        self.agents = self._create_agents()
        self._setup_handoffs()
        self.session = SQLiteSession(session_id="csv_analysis_session")
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create and configure all specialized agents."""
        
        data_loader_agent = Agent(
            name="DataLoaderAgent",
            instructions="""You are a specialized data loading and validation agent.
            
            Your responsibilities:
            - Load and validate CSV datasets
            - Provide dataset metadata and structure information
            - Handle file-related errors gracefully
            - Guide users to available datasets
            
            Always start by mentioning you are the Data Loader Agent.
            Be helpful and informative about what data is available.""",
            model=get_model(),
            tools=[get_available_datasets, get_dataset_info, get_column_names]
        )
        
        analytics_agent = Agent(
            name="AnalyticsAgent",
            instructions="""You are a specialized statistical analysis agent.
            
            Your responsibilities:
            - Perform statistical calculations on numeric columns
            - Calculate means, medians, standard deviations, quartiles
            - Count and analyze categorical data
            - Perform data aggregation and grouping operations
            
            Always start by mentioning you are the Analytics Agent.
            Provide clear, professional statistical analysis with business insights.
            Use the data to tell a story about what the numbers mean.""",
            model=get_model(),
            tools=[
                calculate_column_statistics,
                count_rows_with_value,
                perform_data_aggregation
            ]
        )
        
        insight_agent = Agent(
            name="InsightAgent",
            instructions="""You are a specialized pattern detection and business intelligence agent.
            
            Your responsibilities:
            - Detect correlations between variables
            - Identify outliers and unusual patterns
            - Generate business insights from data
            - Suggest relevant follow-up analyses
            
            Always start by mentioning you are the Insight Agent.
            Focus on actionable insights and business value.
            Explain why patterns matter and what they suggest.""",
            model=get_model(),
            tools=[detect_correlations, find_outliers]
        )
        
        communication_agent = Agent(
            name="CommunicationAgent",
            instructions="""You are a specialized communication and user experience agent.
            
            Your responsibilities:
            - Format and present analysis results clearly
            - Handle user queries and route to appropriate specialists
            - Provide helpful error messages and suggestions
            - Maintain conversation context and flow
            
            Always start by mentioning you are the Communication Agent.
            Be conversational, helpful, and professional.
            Use emojis and formatting to make responses engaging.""",
            model=get_model(),
            tools=[get_available_datasets, get_dataset_info]
        )
        
        return {
            "data_loader": data_loader_agent,
            "analytics": analytics_agent,
            "insight": insight_agent,
            "communication": communication_agent
        }
    
    def _setup_handoffs(self):
        """Configure agent handoff capabilities."""
        for agent in self.agents.values():
            agent.handoffs = list(self.agents.values())
    
    async def route_request(self, user_input: str, context: Dict[str, Any]) -> str:
        """Intelligently route user requests to appropriate agents."""
        
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['load', 'file', 'dataset', 'available', 'columns']):
            agent = self.agents["data_loader"]
            agent_name = "Data Loader"
        elif any(word in user_input_lower for word in ['average', 'mean', 'median', 'count', 'sum', 'statistics']):
            agent = self.agents["analytics"]
            agent_name = "Analytics"
        elif any(word in user_input_lower for word in ['correlation', 'outlier', 'pattern', 'insight', 'relationship']):
            agent = self.agents["insight"]
            agent_name = "Insight"
        else:
            agent = self.agents["communication"]
            agent_name = "Communication"
        
        context["current_agent"] = agent_name
        context["agent_switch_count"] = context.get("agent_switch_count", 0) + 1
        
        result = await Runner.run(
            starting_agent=agent,
            input=user_input,
            session=self.session
        )
        
        return result.final_output
    
    async def process_complex_request(self, user_input: str) -> str:
        """Handle complex requests that require multiple agents."""
        
        context = {"request_type": "complex", "agents_used": []}
        
        if "compare" in user_input.lower() or "across" in user_input.lower():
            return await self._handle_comparison_request(user_input, context)
        elif "trend" in user_input.lower() or "pattern" in user_input.lower():
            return await self._handle_pattern_request(user_input, context)
        else:
            return await self.route_request(user_input, context)
    
    async def _handle_comparison_request(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle requests for comparing data across different dimensions."""
        
        context["agents_used"].append("analytics")
        context["agents_used"].append("insight")
        
        analytics_result = await Runner.run(
            starting_agent=self.agents["analytics"],
            input=user_input,
            session=self.session
        )
        
        insight_result = await Runner.run(
            starting_agent=self.agents["insight"],
            input=f"Based on this analysis: {analytics_result.final_output}, provide additional insights and patterns",
            session=self.session
        )
        
        return f"""🔄 Multi-Agent Analysis Complete!

📊 Analytics Agent Results:
{analytics_result.final_output}

💡 Insight Agent Analysis:
{insight_result.final_output}

🎯 This coordinated analysis provides comprehensive insights across multiple dimensions."""
    
    async def _handle_pattern_request(self, user_input: str, context: Dict[str, Any]) -> str:
        """Handle requests for pattern detection and trend analysis."""
        
        context["agents_used"].extend(["analytics", "insight"])
        
        analytics_result = await Runner.run(
            starting_agent=self.agents["analytics"],
            input=user_input,
            session=self.session
        )
        
        insight_result = await Runner.run(
            starting_agent=self.agents["insight"],
            input=f"Analyze this data for patterns: {analytics_result.final_output}",
            session=self.session
        )
        
        return f"""🔍 Pattern Analysis Complete!

📈 Analytics Foundation:
{analytics_result.final_output}

🧠 Pattern Detection:
{insight_result.final_output}

✨ Combined insights reveal the underlying patterns in your data."""
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents."""
        return {
            "total_agents": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "session_active": True,
            "handoffs_configured": True
        }


class CSVAnalysisAgent:
    """Main agent that orchestrates the entire CSV analysis system."""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.session = self.orchestrator.session
        
        self.main_agent = Agent(
            name="CSVAnalysisAgent",
            instructions="""You are the main CSV Data Analysis Agent, a sophisticated AI system that coordinates multiple specialized agents.
            
            Your role:
            - Understand user requests and route them appropriately
            - Coordinate between specialized agents for complex analyses
            - Provide clear, professional responses with business insights
            - Maintain conversation context and suggest follow-up questions
            
            Available specialized agents:
            - Data Loader Agent: Handles file operations and dataset information
            - Analytics Agent: Performs statistical calculations and aggregations
            - Insight Agent: Detects patterns, correlations, and outliers
            - Communication Agent: Formats responses and handles user interaction
            
            Always be helpful, professional, and insightful. Use the specialized agents to provide comprehensive analysis.""",
            model=get_model(),
            tools=[
                get_available_datasets,
                get_dataset_info,
                get_column_names,
                calculate_column_statistics,
                count_rows_with_value,
                perform_data_aggregation,
                detect_correlations,
                find_outliers
            ]
        )
    
    async def analyze_request(self, user_input: str) -> str:
        """Analyze user request and provide comprehensive response."""
        
        try:
            if self._is_complex_request(user_input):
                return await self.orchestrator.process_complex_request(user_input)
            else:
                return await self.orchestrator.route_request(user_input, {})
                
        except Exception as e:
            return f"""❌ Analysis Error

I encountered an issue while processing your request: {str(e)}

🔧 Troubleshooting:
- Check if the dataset name is correct
- Ensure column names match exactly
- Verify the data format is valid

💡 Try asking:
- "What datasets are available?"
- "Show me the columns in [dataset_name]"
- "What's the average [column_name] in [dataset_name]?" """
    
    def _is_complex_request(self, user_input: str) -> bool:
        """Determine if a request requires multiple agents."""
        complex_keywords = [
            'compare', 'across', 'trend', 'pattern', 'relationship',
            'correlation', 'outlier', 'insight', 'analysis'
        ]
        return any(keyword in user_input.lower() for keyword in complex_keywords)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        agent_status = self.orchestrator.get_agent_status()
        
        return {
            "system": "CSV Data Analysis Multi-Agent System",
            "status": "operational",
            "agents": agent_status,
            "session_id": str(self.session.session_id),
            "available_tools": len(self.main_agent.tools),
            "architecture": "multi-agent orchestration"
        }


def create_analysis_system() -> CSVAnalysisAgent:
    """Factory function to create the complete analysis system."""
    return CSVAnalysisAgent()
