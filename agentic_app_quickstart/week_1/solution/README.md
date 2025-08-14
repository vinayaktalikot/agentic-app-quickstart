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
- **seamless agent handoffs with automatic question forwarding**
- persistent conversation memory

## improved agent handoff system

### seamless handoffs
the system now implements intelligent agent handoffs that automatically forward user questions:

```
user: "load employee_data"
coordinator: "for this, ask the data loader agent"
handing over to DataLoaderAgent
dataloader: "the csv file 'employee_data.csv' has been successfully loaded..."
```

### key improvements
1. **automatic question forwarding**: after a handoff, your question is automatically processed by the new agent
2. **clean handoff messages**: simple "handing over to [AgentName]" without verbose explanations
3. **seamless user experience**: users don't need to repeat their questions after handoffs
4. **intelligent routing**: agents automatically redirect specialized requests to appropriate agents
5. **natural conversation flow**: handoffs happen invisibly in the background

### handoff detection
the system automatically detects when an agent wants to hand off by parsing responses for keywords:
- **data loader**: "data loader", "file", "load"
- **analytics**: "analytics", "analysis", "calculation"
- **communication**: "communication", "guidance", "help"

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
   uv run python main.py
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

#### seamless handoff examples
```
user: load employee_data
coordinator: for this, ask the data loader agent
handing over to DataLoaderAgent
dataloader: the csv file 'employee_data.csv' has been successfully loaded...

user: what is the average salary?
dataloader: for this type of request, you should ask the analytics agent
handing over to AnalyticsAgent
analytics: the average salary is $73,466.67...
```

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
- **intelligent handoffs**: agents automatically redirect specialized requests to appropriate agents
- **automatic question forwarding**: user questions are seamlessly forwarded after handoffs
- **coordinator management**: coordinator agent manages overall system flow
- **specialized expertise**: each agent focuses on their domain for optimal results
- **seamless transitions**: handoffs maintain conversation context without interruption

### memory management
- sqlite-based session storage
- persistent conversation history
- context-aware responses
- dataset memory across interactions

## testing and quality assurance

### test suite
the system includes a comprehensive test suite:
- **basic functionality tests**: verify file loading, data analysis, and system initialization
- **makefile integration**: professional development workflow with linting, formatting, and testing
- **quality checks**: automated code quality, formatting, and testing pipeline

### development tools
```bash
make test          # run all tests
make lint          # check code quality
make format        # format code with black
make quality       # run all quality checks
make dev           # complete development cycle
```

## sample datasets

the system includes three sample datasets for testing:

- **sample_sales.csv**: e-commerce sales data with date, product, price, quantity, customer_state
- **employee_data.csv**: hr dataset with name, department, salary, hire_date, performance_score
- **weather_data.csv**: weather measurements with date, temperature, humidity, precipitation, city

## challenges overcome

1. **version compatibility**: resolved openai sdk version conflicts by updating to 1.99.5+
2. **agent coordination**: implemented seamless handoffs with automatic question forwarding
3. **memory persistence**: integrated session-based memory for context continuity
4. **error handling**: robust error handling with user-friendly messages
5. **data validation**: comprehensive csv validation and data type detection
6. **user experience**: eliminated need for users to repeat questions after handoffs

## learning outcomes

this implementation demonstrates:
- practical multi-agent system design
- function calling and tool integration
- session-based memory management
- **intelligent agent handoffs with automatic routing**
- advanced data analysis capabilities
- user experience design for non-technical users
- professional testing and development practices

the system successfully achieves all assignment requirements while providing a professional, scalable architecture with seamless agent handoffs that ensure users always get expert help from the right specialized agent.