from agents import Agent, SQLiteSession
from helpers import get_model
from tools import (
    load_csv_file,
    get_column_names,
    get_column_info,
    calculate_column_average,
    count_rows_with_value,
    find_correlations,
    detect_outliers,
    group_by_column,
    suggest_questions,
)


def create_data_loader_agent():
    """create the data loader agent responsible for file operations"""
    return Agent(
        name="DataLoaderAgent",
        instructions="""you are the data loader agent. you handle csv file operations.

        you can load csv files, show column information, and provide dataset overview.
        if someone asks for analysis or guidance, redirect them to the appropriate agent.""",
        model=get_model(),
        tools=[load_csv_file, get_column_names, get_column_info],
        handoffs=[],
    )


def create_analytics_agent():
    """create the analytics agent responsible for data analysis and calculations"""
    return Agent(
        name="AnalyticsAgent",
        instructions="""you are the analytics agent. you handle data analysis and calculations.

        you can calculate averages, correlations, detect outliers, and perform statistical analysis.
        if someone needs to load files or get guidance, redirect them to the appropriate agent.""",
        model=get_model(),
        tools=[
            calculate_column_average,
            count_rows_with_value,
            find_correlations,
            detect_outliers,
            group_by_column,
            get_column_names,
            get_column_info,
        ],
        handoffs=[],
    )


def create_communication_agent():
    """create the communication agent responsible for user interaction and response formatting"""
    return Agent(
        name="CommunicationAgent",
        instructions="""you are the communication agent. you provide guidance and suggestions.

        you can suggest questions, provide guidance, and explain data concepts.
        if someone needs to load files or perform analysis, redirect them to the appropriate agent.""",
        model=get_model(),
        tools=[suggest_questions, get_column_names, get_column_info],
        handoffs=[],
    )


def create_coordinator_agent():
    """create the main coordinator agent that manages handoffs between specialized agents"""
    return Agent(
        name="CoordinatorAgent",
        instructions="""you are the coordinator agent. you coordinate between specialized agents.

        redirect users to appropriate agents:
        - file operations -> "ask the data loader agent"
        - data analysis -> "ask the analytics agent"
        - guidance and help -> "ask the communication agent"

        you can only explain system capabilities and direct users to agents.
        never handle specialized tasks yourself.""",
        model=get_model(),
        tools=[get_column_names, get_column_info],
        handoffs=[],
    )


def setup_agent_handoffs():
    """setup handoff relationships between all agents"""
    data_agent = create_data_loader_agent()
    analytics_agent = create_analytics_agent()
    communication_agent = create_communication_agent()
    coordinator_agent = create_coordinator_agent()

    data_agent.handoffs = [analytics_agent, communication_agent, coordinator_agent]
    analytics_agent.handoffs = [data_agent, communication_agent, coordinator_agent]
    communication_agent.handoffs = [data_agent, analytics_agent, coordinator_agent]
    coordinator_agent.handoffs = [data_agent, analytics_agent, communication_agent]

    return {
        "coordinator": coordinator_agent,
        "data_loader": data_agent,
        "analytics": analytics_agent,
        "communication": communication_agent,
    }


def create_session(session_id: int = None):
    """create a session for maintaining conversation memory"""
    if session_id is None:
        session_id = hash(str(id)) % 10000

    return SQLiteSession(session_id=session_id)
