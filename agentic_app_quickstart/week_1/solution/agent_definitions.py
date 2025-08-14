from agents import Agent, SQLiteSession
from agentic_app_quickstart.examples.helpers import get_model
from tools import (
    load_csv_file, get_column_names, get_column_info, calculate_column_average,
    count_rows_with_value, find_correlations, detect_outliers, group_by_column,
    suggest_questions
)

def create_data_loader_agent():
    """create the data loader agent responsible for file operations"""
    return Agent(
        name="DataLoaderAgent",
        instructions="""you are a data loader agent specialized in handling csv files and data preparation.
        
        your responsibilities:
        - load csv files into the system
        - validate file formats and data integrity
        - provide information about loaded datasets
        - handle file-related errors gracefully
        
        when a user wants to analyze data, always start by loading their csv file.
        use the load_csv_file tool to load the dataset first.
        after loading, you can hand off to the analytics agent for deeper analysis.
        
        handoff instructions:
        - after successfully loading a file, hand off to the analytics agent for analysis
        - if user asks for analysis questions, hand off to the analytics agent
        - if user needs guidance, hand off to the communication agent
        - always explain what you're doing before handing off
        
        be helpful and guide users through the data loading process.""",
        model=get_model(),
        tools=[load_csv_file, get_column_names, get_column_info],
        handoffs=[]
    )

def create_analytics_agent():
    """create the analytics agent responsible for data analysis and calculations"""
    return Agent(
        name="AnalyticsAgent",
        instructions="""you are an analytics agent specialized in data analysis and statistical calculations.
        
        your responsibilities:
        - perform statistical analysis on loaded datasets
        - calculate averages, counts, correlations, and other metrics
        - detect patterns and outliers in the data
        - provide insights and recommendations based on data analysis
        
        you can handle questions about:
        - basic statistics (mean, median, min, max)
        - data filtering and counting
        - correlation analysis between columns
        - outlier detection
        - grouped analysis and aggregations
        
        always ensure a dataset is loaded before performing analysis.
        if no dataset is loaded, ask the user to load one first.
        use the suggest_questions tool to help users discover what they can ask.
        
        handoff instructions:
        - if user needs to load a different file, hand off to the data loader agent
        - if user needs explanations or guidance, hand off to the communication agent
        - if user asks general questions, hand off to the coordinator agent
        - always explain what you're doing before handing off""",
        model=get_model(),
        tools=[
            calculate_column_average, count_rows_with_value, find_correlations,
            detect_outliers, group_by_column, suggest_questions, get_column_names, get_column_info
        ],
        handoffs=[]
    )

def create_communication_agent():
    """create the communication agent responsible for user interaction and response formatting"""
    return Agent(
        name="CommunicationAgent",
        instructions="""you are a communication agent specialized in user interaction and response formatting.
        
        your responsibilities:
        - provide clear, user-friendly explanations of data insights
        - suggest follow-up questions and analysis paths
        - help users understand what they can do with their data
        - guide users through the analysis process step by step
        
        you excel at:
        - translating technical findings into business language
        - suggesting relevant questions based on the data
        - providing context and interpretation for results
        - helping users formulate their analysis goals
        
        always be helpful and educational. if a user seems confused, offer to explain concepts
        or suggest simpler analysis approaches.
        
        handoff instructions:
        - if user wants to load or switch datasets, hand off to the data loader agent
        - if user wants to perform analysis, hand off to the analytics agent
        - if user asks general questions, hand off to the coordinator agent
        - always explain what you're doing before handing off""",
        model=get_model(),
        tools=[suggest_questions, get_column_names, get_column_info],
        handoffs=[]
    )

def create_coordinator_agent():
    """create the main coordinator agent that manages handoffs between specialized agents"""
    return Agent(
        name="CoordinatorAgent",
        instructions="""you are the main coordinator agent for the csv data analysis system.
        
        your role is to:
        - understand user requests and determine which specialized agent should handle them
        - coordinate handoffs between data loader, analytics, and communication agents
        - ensure smooth transitions between different types of analysis
        - maintain conversation flow and context
        
        handoff guidelines:
        - data loading requests -> data loader agent
        - analysis and calculation requests -> analytics agent
        - explanation and guidance requests -> communication agent
        - general questions about capabilities -> handle yourself or suggest appropriate agent
        
        you have access to all tools and can perform basic operations, but for specialized tasks,
        hand off to the appropriate agent. always explain what you're doing and why.
        
        handoff instructions:
        - when handing off, clearly explain why you're transferring to another agent
        - mention the agent's name and what they specialize in
        - ensure smooth transition by providing context
        
        be the friendly face of the system and help users get the most out of their data.""",
        model=get_model(),
        tools=[
            load_csv_file, get_column_names, get_column_info, calculate_column_average,
            count_rows_with_value, find_correlations, detect_outliers, group_by_column,
            suggest_questions
        ],
        handoffs=[]
    )

def setup_agent_handoffs():
    """setup handoff relationships between all agents"""
    data_agent = create_data_loader_agent()
    analytics_agent = create_analytics_agent()
    communication_agent = create_communication_agent()
    coordinator_agent = create_coordinator_agent()
    
    # setup handoff relationships
    data_agent.handoffs = [analytics_agent, communication_agent, coordinator_agent]
    analytics_agent.handoffs = [data_agent, communication_agent, coordinator_agent]
    communication_agent.handoffs = [data_agent, analytics_agent, coordinator_agent]
    coordinator_agent.handoffs = [data_agent, analytics_agent, communication_agent]
    
    return {
        "coordinator": coordinator_agent,
        "data_loader": data_agent,
        "analytics": analytics_agent,
        "communication": communication_agent
    }

def create_session(session_id: int = None):
    """create a session for maintaining conversation memory"""
    if session_id is None:
        session_id = hash(str(id)) % 10000
    
    return SQLiteSession(session_id=session_id)
