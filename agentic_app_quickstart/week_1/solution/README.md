# csv data analysis agent system

## architecture overview

this system implements a multi-agent architecture for intelligent csv data analysis, achieving all three bonus levels from the assignment requirements.

### multi-agent system (bronze level)

the system consists of four specialized agents:

- **coordinator agent**: main system coordinator that manages handoffs and coordinates other agents
- **data loader agent**: handles csv file operations, validation, and data preparation
- **analytics agent**: performs statistical analysis, calculations, and pattern detection
- **communication agent**: provides user guidance, explanations, and suggests analysis approaches

### memory system (silver level)

- **session-based memory**: uses sqlitesession to maintain conversation context across interactions
- **context awareness**: agents remember loaded datasets and previous questions
- **follow-up support**: users can ask follow-up questions like "what about the median?" after asking about averages

### advanced analytics (gold level)

- **smart data insights**: automatic pattern detection and correlation analysis
- **outlier detection**: statistical outlier detection using z-score method
- **grouped analysis**: flexible grouping and aggregation capabilities
- **intelligent suggestions**: ai-powered question suggestions based on data characteristics

## features

### core functionality
- csv file loading and validation
- column information and data type detection
- basic statistical calculations (mean, median, min, max, std dev)
- data filtering and counting
- error handling and graceful degradation

### advanced capabilities
- correlation analysis between numeric columns
- statistical outlier detection
- grouped analysis with multiple aggregation functions
- intelligent question suggestions
- multi-file support and dataset management

### user experience
- natural language interface
- helpful error messages and guidance
- command shortcuts (load, help, agents, quit)
- seamless agent handoffs
- persistent conversation memory

## how to run

### prerequisites
- python 3.11 or higher
- required packages: openai, openai-agents, pandas, numpy

### setup
1. ensure you have the required environment variables:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_API_ENDPOINT=your_endpoint_here
   ```

2. install dependencies:
   ```bash
   uv sync
   ```

3. run the system:
   ```bash
   cd week_1/solution
   python -m main
   ```

### usage examples

#### basic commands
- `help` - show help information
- `agents` - list available agents
- `load sample_sales.csv` - load a dataset
- `quit` or `exit` - end the session

#### example questions
- "what columns are in the dataset?"
- "what is the average price?"
- "how many customers are from california?"
- "are there any outliers in the salary column?"
- "what are the correlations between numeric columns?"
- "suggest some questions i can ask"

#### follow-up conversations
```
user: what is the average price?
agent: average price: 299.99

user: what about the median?
agent: median price: 159.99
```

## technical implementation

### tools and functions
the system provides 10 function tools:
1. `load_csv_file` - load and validate csv files
2. `get_column_names` - list available columns
3. `get_column_info` - detailed column information
4. `calculate_column_average` - basic statistics
5. `count_rows_with_value` - data filtering
6. `find_correlations` - correlation analysis
7. `detect_outliers` - outlier detection
8. `group_by_column` - grouped analysis
9. `suggest_questions` - intelligent suggestions

### agent coordination
- agents can hand off to each other based on user needs
- coordinator agent manages overall system flow
- specialized agents focus on their domains
- seamless transitions maintain conversation context

### memory management
- sqlite-based session storage
- persistent conversation history
- context-aware responses
- dataset memory across interactions

## sample datasets

the system includes three sample datasets for testing:

- **sample_sales.csv**: e-commerce sales data with date, product, price, quantity, customer_state
- **employee_data.csv**: hr dataset with name, department, salary, hire_date, performance_score
- **weather_data.csv**: weather measurements with date, temperature, humidity, precipitation, city

## challenges overcome

1. **version compatibility**: resolved openai sdk version conflicts by updating to 1.100.0+
2. **agent coordination**: implemented seamless handoffs between specialized agents
3. **memory persistence**: integrated session-based memory for context continuity
4. **error handling**: robust error handling with user-friendly messages
5. **data validation**: comprehensive csv validation and data type detection

## learning outcomes

this implementation demonstrates:
- practical multi-agent system design
- function calling and tool integration
- session-based memory management
- agent handoffs and coordination
- advanced data analysis capabilities
- user experience design for non-technical users

the system successfully achieves all assignment requirements while providing a professional, scalable architecture that can be extended with additional agents and capabilities.