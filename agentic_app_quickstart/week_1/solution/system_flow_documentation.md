# System flow documentation: how the csv analysis system works

## System architecture overview

the csv analysis system uses a multi-agent architecture with specialized agents that handle different types of requests:

```
user input -> coordinator agent -> specialized agent -> response
                |
        memory & context management
                |
        seamless agent handoffs & coordination
```

## Agent roles and responsibilities

### Coordinator agent
- main system coordinator and entry point
- **responsibilities**: 
  - understand user requests
  - route to appropriate specialized agents
  - maintain conversation flow
  - handle general questions
- **tools**: limited to basic dataset info tools only
- **handoffs**: can transfer to any specialized agent
- **strict rule**: never handles specialized tasks, only coordinates

### Data loader agent
- **primary role**: handle file operations and data preparation
- **responsibilities**:
  - load csv files
  - validate data integrity
  - provide dataset information
  - handle file-related errors
- **tools**: file loading, column info, basic dataset operations
- **handoffs**: can transfer to analytics or communication agents
- **strict rule**: redirects analysis and guidance requests to appropriate agents

### analytics agent
- **primary role**: perform data analysis and calculations
- **responsibilities**:
  - statistical calculations
  - pattern detection
  - correlation analysis
  - outlier detection
  - grouped analysis
- **tools**: all analytical tools (averages, correlations, outliers, grouping)
- **handoffs**: can transfer to data loader or communication agents
- **strict rule**: redirects file operations and guidance requests to appropriate agents

### communication agent
- **primary role**: user guidance and explanation
- **responsibilities**:
  - explain results in user friendly language
  - suggest follow up questions
  - provide guidance and help
  - translate technical findings
- **tools**: question suggestions, guidance tools
- **handoffs**: can transfer to other agents for deeper analysis
- **strict rule**: redirects file operations and analysis requests to appropriate agents

## question flow analysis

### simple questions flow

#### example: "what columns are in the dataset?"

```
1. user input: "what columns are in the dataset?"
2. coordinator agent receives input
3. coordinator identifies this as a data exploration question
4. coordinator uses get_column_names() tool directly
5. response: "columns: date, product, price, quantity, customer_state"
6. no agent handoff needed (coordinator handles directly)
```

**flow path**: user -> coordinator -> tool execution -> response

#### example: "what is the average price?"

```
1. user input: "what is the average price?"
2. coordinator agent receives input
3. coordinator identifies this as an analytics question
4. coordinator redirects: "for this, ask the analytics agent"
5. system: "handing over to AnalyticsAgent"
6. analytics agent processes the same question automatically
7. response: "average price: 354.49"
```

**flow path**: user -> coordinator -> handoff detection -> analytics agent -> tool execution → response

### medium complexity questions flow

#### example: "what is the average salary by department?"

```
1. user input: "what is the average salary by department?"
2. coordinator agent receives input
3. coordinator identifies this as a grouping/aggregation question
4. coordinator redirects: "for this, ask the analytics agent"
5. system: "handing over to AnalyticsAgent"
6. analytics agent processes the same question automatically
7. analytics agent uses group_by_column("department", "salary", "mean") tool
8. response: detailed breakdown by department
```

**flow path**: user -> coordinator -> handoff -> analytics agent -> advanced tool execution -> response

#### example: "are there any missing values in the dataset?"

```
1. user input: "are there any missing values in the dataset?"
2. coordinator agent receives input
3. coordinator identifies this as a data quality question
4. coordinator redirects: "for this, ask the data loader agent"
5. system: "handing over to DataLoaderAgent"
6. data loader agent processes the same question automatically
7. data loader agent uses get_column_info() for each column
8. response: comprehensive missing value report
```

**flow path**: user -> coordinator -> handoff -> data loader agent -> multiple tool calls -> analysis -> response

### complex questions flow

#### example: "what are the correlations between numeric columns?"

```
1. user input: "what are the correlations between numeric columns?"
2. coordinator agent receives input
3. coordinator identifies this as advanced statistical analysis
4. coordinator redirects: "for this, ask the analytics agent"
5. system: "handing over to AnalyticsAgent"
6. analytics agent processes the same question automatically
7. analytics agent uses find_correlations() tool
8. response: comprehensive correlation matrix with insights
```

**flow path**: user -> coordinator -> handoff -> analytics agent -> specialized tool -> enhanced response

#### example: "suggest some interesting questions i can ask about this data"

```
1. user input: "suggest some interesting questions i can ask about this data"
2. coordinator agent receives input
3. coordinator identifies this as guidance/communication question
4. coordinator redirects: "for this, ask the communication agent"
5. system: "handing over to CommunicationAgent"
6. communication agent processes the same question automatically
7. communication agent analyzes loaded dataset
8. communication agent uses suggest_questions() tool
9. response: contextual, intelligent suggestions
```

**flow path**: user -> coordinator -> handoff -> communication agent -> analysis + suggestions -> enhanced response

## memory and context management

### session based memory
- **persistence**: conversations are stored in sqlite database
- **context awareness**: agents remember previous questions and loaded datasets
- **follow-up support**: users can ask "what about the median?" after asking about averages

### context limitations
- **single dataset**: only one csv file can be loaded at a time
- **dataset switching**: users must explicitly load a new file to switch datasets
- **context preservation**: loaded dataset information persists across questions

## single-file limitation explanation

### why one file at a time?

the system is designed to work with one csv file at a time for several reasons:

1. **memory efficiency**: keeps system memory usage manageable
2. **context clarity**: prevents confusion about which dataset a question refers to
3. **tool simplicity**: function tools are designed for single dataset operations
4. **user experience**: clearer and more focused analysis

## improved agent handoff system

### seamless handoffs with automatic question forwarding

the system now implements intelligent agent handoffs that automatically forward user questions:

```
1. user: "i want to load employee_data"
   coordinator: "for this, ask the data loader agent"
   system: "handing over to DataLoaderAgent"
   dataloader: "the csv file 'employee_data.csv' has been successfully loaded..."

2. user: "what is the average salary?"
   system: "handing over to AnalyticsAgent"
   analytics: "the average salary is $73,466.67..."

3. user: "suggest some questions i can ask"
   system: "handing over to CommunicationAgent"
   communication: "here are some interesting questions you can ask..."
```

### handoff detection logic

the system detects handoff intent by parsing agent responses for keywords:

- **data loader keywords**: "data loader", "file", "load"
- **analytics keywords**: "analytics", "analysis", "calculation"
- **communication keywords**: "communication", "guidance", "help"
- **coordinator keywords**: "coordinator", "general"