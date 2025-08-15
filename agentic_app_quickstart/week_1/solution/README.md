# CSV data analysis agent system

## Quick Access Documentation

- [Question Examples](question_examples.md) - example questions to test the system
- [System Flow Documentation](system_flow_documentation.md) - detailed architecture and handoff logic
- [Screenshots Documentation](docs/screenshots_documentation.md) - visual proof of system functionality

---

## Architecture overview

This system implements a multi-agent architecture for intelligent csv data analysis, achieving all three bonus levels from the assignment requirements.

### multi-agent system

the system consists of four specialized agents:

- **coordinator agent** -- main system coordinator that manages handoffs and coordinates other agents
- **data loader agent** -- handles csv file operations, validation, and data preparation
- **analytics agent** -- performs statistical analysis, calculations, and pattern detection
- **communication agent** -- provides user guidance, explanations, and suggests analysis approaches

### Memory system

- **session-based memory** - uses sqlitesession to maintain conversation context across interactions
- **context awareness** - agents remember loaded datasets and previous questions
- **follow-up support** - users can ask follow-up questions like "what about the median?" after asking about averages

### Advanced analytics 

- **smart data insights** - automatic pattern detection and correlation analysis
- **outlier detection** - statistical outlier detection using z-score method
- **grouped analysis** -  flexible grouping and aggregation capabilities
- **intelligent suggestions** - ai-powered question suggestions based on data characteristics

## Features

### Core functionality
- csv file loading and validation
- column information and data type detection
- basic statistical calculations (mean, median, min, max, std dev)
- data filtering and counting
- error handling

### Advanced capabilities
- correlation analysis between numeric columns
- statistical outlier detection
- grouped analysis with multiple aggregation functions
- intelligent question suggestions
- multi-file support and dataset management

### user experience
- natural language CLI interface
- helpful error messages 
- command shortcuts (load, help, agents, quit)
- **seamless agent handoffs with automatic question forwarding**
- persistent conversation memory
- clean visual interface with text emoticons and message separators

## Improved agent handoff system

### seamless handoffs
the system now implements intelligent agent handoffs that automatically forward user questions:

```
user: "load employee_data"
handing over to DataLoaderAgent
dataloader: "the csv file 'employee_data.csv' has been successfully loaded..."
```

### handoff detection
the system automatically detects when an agent wants to hand off by parsing responses for keywords:
- **data loader**: "data loader", "file", "load"
- **analytics**: "analytics", "analysis", "calculation"
- **communication**: "communication", "guidance", "help"

## How to run ?

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

## Technical implementation

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

### Test suite
The system includes a test suite:
- Verify file loading, data analysis, and system initialization
- Development workflow with linting, formatting, and testing
- Automated code quality, formatting, and testing pipeline

### Development tools
```bash
make test          # run all tests
make lint          # check code quality
make format        # format code with black
make quality       # run all quality checks
make dev           # complete development cycle
```
