# comprehensive question guide for csv data analysis agent

## getting started questions

### basic system commands
- `help` - show help information
- `agents` - list available ai agents
- `load sample_sales.csv` - load a dataset
- `quit` or `exit` - end the session

### dataset overview questions
- "what columns are in the dataset?"
- "how many rows and columns does this dataset have?"
- "what types of data are in each column?"
- "are there any missing values in the dataset?"
- "what does this dataset contain?"

## simple analysis questions (bronze level)

### basic statistics
- "what is the average price?"
- "what is the highest salary in the dataset?"
- "what is the lowest temperature recorded?"
- "how many total rows are there?"
- "what is the median performance score?"

### data exploration
- "how many unique products are there?"
- "what are the different customer states?"
- "how many departments are in the company?"
- "what cities are included in the weather data?"
- "what is the date range in this dataset?"

### simple counting
- "how many employees are in the engineering department?"
- "how many sales were made in california?"
- "how many days had precipitation above 0?"
- "how many laptops were sold?"
- "how many employees have a performance score above 4.0?"

## intermediate analysis questions (silver level)

### data filtering and grouping
- "what is the average salary by department?"
- "how many sales per customer state?"
- "what is the total quantity sold by product?"
- "what is the average temperature by city?"
- "how many employees were hired each year?"

### pattern detection
- "are there any missing values in the dataset?"
- "what is the distribution of prices?"
- "how do salaries vary across departments?"
- "what is the range of performance scores?"
- "are there any unusual values in the data?"

### comparative analysis
- "which department has the highest average salary?"
- "which product has the highest total sales?"
- "which city has the most temperature variation?"
- "which month had the most sales?"
- "which employee has the best performance score?"

## advanced analysis questions (gold level)

### statistical insights
- "are there any outliers in the salary column?"
- "what are the correlations between numeric columns?"
- "what is the standard deviation of prices?"
- "are there any statistical patterns in the data?"
- "what is the data quality like?"

### complex aggregations
- "what is the average price by product and customer state?"
- "show me the total revenue by month and product"
- "what is the performance score distribution by department and hire year?"
- "how do temperature and humidity correlate by city?"
- "what is the sales trend over time?"

### intelligent insights
- "suggest some interesting questions i can ask about this data"
- "what patterns do you notice in this dataset?"
- "what insights would be most valuable for a business owner?"
- "are there any data quality issues i should be aware of?"
- "what additional analysis would be helpful?"

## dataset-specific questions

### for sample_sales.csv (e-commerce data)
- "what is the total revenue from all sales?"
- "which product generates the most revenue?"
- "how do sales vary by customer state?"
- "what is the average order value?"
- "are there any seasonal patterns in sales?"

### for employee_data.csv (hr data)
- "what is the salary distribution across departments?"
- "how does performance correlate with salary?"
- "which department has the most employees?"
- "what is the average tenure of employees?"
- "are there any gender pay gaps in the data?"

### for weather_data.csv (weather data)
- "what is the temperature range for each city?"
- "how does humidity vary with temperature?"
- "which city has the most precipitation?"
- "are there any extreme weather events?"
- "what is the weather pattern over time?"

## seamless agent handoff examples

### file operations (automatic handoff to data loader)
```
user: "load employee_data"
coordinator: "for this, ask the data loader agent"
handing over to DataLoaderAgent
dataloader: "the csv file 'employee_data.csv' has been successfully loaded..."
```

### data analysis (automatic handoff to analytics)
```
user: "what is the correlation between salary and performance?"
dataloader: "for this type of request, you should ask the analytics agent"
handing over to AnalyticsAgent
analytics: "the correlation between salary and performance is 0.67..."
```

### guidance and suggestions (automatic handoff to communication)
```
user: "what should i ask next about this data?"
analytics: "for guidance and suggestions, ask the communication agent"
handing over to CommunicationAgent
communication: "here are some interesting questions you can ask..."
```

### key benefits of the handoff system
1. **no question repetition**: your question is automatically forwarded to the right agent
2. **seamless experience**: handoffs happen invisibly in the background
3. **expert handling**: each agent specializes in their domain
4. **natural flow**: conversation continues smoothly without interruption
5. **intelligent routing**: system automatically knows which agent is best for each task

## follow-up questions (memory-enabled)

### building on previous answers
- "what about the median for the same column?"
- "can you show me the same analysis for a different column?"
- "how does this compare to the overall average?"
- "what if we group by a different column?"
- "can you break this down further?"

### deepening analysis
- "why do you think this pattern exists?"
- "what business implications does this have?"
- "how reliable is this analysis?"
- "what other factors might influence this?"
- "how could we improve this analysis?"

## troubleshooting questions

### when things go wrong
- "why did that calculation fail?"
- "what does this error message mean?"
- "how can i fix this issue?"
- "what should i check in my data?"
- "can you suggest an alternative approach?"

### getting help
- "what can this system do?"
- "how do i use this feature?"
- "what are the limitations?"
- "can you explain this concept?"
- "what should i try next?"

## pro tips for better results

1. **start simple**: begin with basic questions to understand your data
2. **use natural language**: ask questions as you would ask a human analyst
3. **build on answers**: use follow-up questions to dig deeper
4. **be specific**: mention column names and values you're interested in
5. **explore patterns**: ask about correlations, outliers, and trends
6. **get suggestions**: ask the agent to suggest interesting questions
7. **use memory**: the system remembers your conversation, so build on previous questions
8. **trust the handoffs**: let the system automatically route you to the right expert agent
9. **no need to repeat**: after a handoff, your question is automatically processed

## example conversation flow with seamless handoffs

```
user: load sample_sales.csv
coordinator: for this, ask the data loader agent
handing over to DataLoaderAgent
dataloader: the csv file 'sample_sales.csv' has been successfully loaded...

user: what columns are in the dataset?
dataloader: the dataset contains: date, product, price, quantity, customer_state

user: what is the average price?
dataloader: for this type of request, you should ask the analytics agent
handing over to AnalyticsAgent
analytics: the average price is $354.49

user: what about the median?
analytics: the median price is $299.99

user: are there any outliers in the price column?
analytics: yes, i found 3 outliers above $800...

user: what are the correlations between numeric columns?
analytics: the correlation between price and quantity is -0.23...

user: suggest some other interesting questions
analytics: for guidance and suggestions, ask the communication agent
handing over to CommunicationAgent
communication: here are some interesting questions you can ask...
```

## testing the handoff system

### questions that trigger handoffs
- **file operations**: "load", "file", "dataset" → data loader agent
- **analysis requests**: "calculate", "average", "correlation" → analytics agent
- **guidance needs**: "suggest", "help", "what should i ask" → communication agent
- **general questions**: "what can you do", "explain" → coordinator agent

### handoff verification
after each handoff, you'll see:
1. the current agent redirecting you to another agent
2. a clean "handing over to [AgentName]" message
3. the new agent immediately processing your original question
4. seamless continuation of the conversation

this comprehensive guide covers everything from basic data exploration to advanced statistical analysis, with seamless agent handoffs that ensure you always get expert help from the right specialized agent! 