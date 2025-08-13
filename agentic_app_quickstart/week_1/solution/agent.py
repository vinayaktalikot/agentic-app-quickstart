"""
Hybrid Professional CSV Data Analysis Agent

This agent combines the best of both approaches:
- SQLiteSession for professional memory management (like instructor examples)
- Direct OpenAI API calls to bypass the openai-agents Union bug
- Professional architecture and session management
- Scalable, production-ready design

This gives us the reliability of sessions without the framework bugs.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from agents import SQLiteSession
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()


class CSVAgent:
    """
    CSV analysis agent with SQLiteSession memory management.
    
    Features:
    - SQLiteSession for persistent conversation memory
    - Direct OpenAI API for reliable responses
    - Professional architecture and error handling
    """
    
    def __init__(self, session_id: str = "default_csv_session"):
        """
        Initialize the CSV agent.
        
        Args:
            session_id: Unique identifier for the conversation session
        """
        self.session_id = session_id
        self.data_path = Path(__file__).parent / "data"
        self._data_cache = {}
        
        # Memory management using SQLiteSession
        self.session = SQLiteSession(
            session_id=session_id,
            db_path="csv_conversations.db"
        )
        
        # Direct OpenAI client for reliable API calls
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_ENDPOINT")
        )
        self.model = "gpt-4o-mini"
        
        # Initialize session memory
        self._initialize_session_memory()
    
    def _initialize_session_memory(self):
        """Initialize the session with conversation memory."""
        try:
            # Store initial session info
            asyncio.create_task(self.session.add_items([
                {"role": "system", "content": "CSV Data Analysis Session initialized"}
            ]))
        except Exception as e:
            print(f"Warning: Could not initialize session memory: {e}")
    
    def _add_to_session_memory(self, role: str, content: str):
        """Add message to session memory."""
        try:
            asyncio.create_task(self.session.add_items([
                {"role": role, "content": content}
            ]))
        except Exception as e:
            print(f"Warning: Could not add to session memory: {e}")
    
    async def _get_conversation_context(self) -> str:
        """Get conversation context from session for OpenAI API."""
        try:
            # Get recent messages from session
            messages = await self.session.get_items()
            if not messages:
                return ""
            
            # Format recent context (last 5 messages)
            recent_messages = messages[-5:] if len(messages) > 5 else messages
            context = "Recent conversation context:\n"
            
            for msg in recent_messages:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')[:200]  # Truncate long messages
                context += f"{role}: {content}\n"
            
            return context
        except Exception as e:
            print(f"Warning: Could not retrieve conversation context: {e}")
            return ""
    
    def _load_csv_safely(self, filename: str) -> pd.DataFrame:
        """Load CSV file with comprehensive error handling."""
        file_path = self.data_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset '{filename}' not found")
        
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError(f"Dataset '{filename}' contains no data")
            return df
        except pd.errors.EmptyDataError:
            raise ValueError(f"Dataset '{filename}' contains no data")
        except pd.errors.ParserError:
            raise ValueError(f"Dataset '{filename}' has invalid CSV format")
        except Exception as e:
            raise ValueError(f"Error loading '{filename}': {str(e)}")
    
    def _get_cached_data(self, filename: str) -> pd.DataFrame:
        """Get data from cache or load if not cached."""
        if filename not in self._data_cache:
            self._data_cache[filename] = self._load_csv_safely(filename)
        return self._data_cache[filename].copy()
    
    def get_available_datasets(self) -> Dict[str, str]:
        """Get list of available CSV datasets."""
        datasets = {
            "sample_sales.csv": "E-commerce sales data with product, price, quantity, and customer state",
            "employee_data.csv": "HR dataset with employee names, departments, salaries, and performance scores",
            "weather_data.csv": "Weather measurements with temperature, humidity, precipitation, and city data"
        }
        return datasets
    
    def get_dataset_info(self, filename: str) -> Dict[str, Any]:
        """Get comprehensive information about a specific dataset."""
        try:
            df = self._get_cached_data(filename)
            
            info = {
                "filename": filename,
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "sample_data": df.head(3).to_dict('records')
            }
            return info
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_column_statistics(self, filename: str, column_name: str) -> Dict[str, Any]:
        """Calculate statistical measures for a numeric column."""
        try:
            df = self._get_cached_data(filename)
            
            if column_name not in df.columns:
                return {"error": f"Column '{column_name}' not found"}
            
            if not pd.api.types.is_numeric_dtype(df[column_name]):
                return {"error": f"Column '{column_name}' is not numeric"}
            
            stats = {
                "column": column_name,
                "count": int(df[column_name].count()),
                "mean": float(df[column_name].mean()),
                "median": float(df[column_name].median()),
                "std": float(df[column_name].std()),
                "min": float(df[column_name].min()),
                "max": float(df[column_name].max()),
                "quartiles": df[column_name].quantile([0.25, 0.5, 0.75]).to_dict()
            }
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def get_column_names(self, filename: str) -> Dict[str, Any]:
        """Get all column names from a dataset with their data types."""
        try:
            df = self._get_cached_data(filename)
            
            columns_info = {
                "filename": filename,
                "total_columns": len(df.columns),
                "columns": [
                    {
                        "name": col,
                        "type": str(df[col].dtype),
                        "non_null_count": int(df[col].count()),
                        "null_count": int(df[col].isnull().sum())
                    }
                    for col in df.columns
                ]
            }
            return columns_info
        except Exception as e:
            return {"error": str(e)}
    
    def perform_data_aggregation(self, filename: str, group_by_column: str, operation: str, target_column: str) -> Dict[str, Any]:
        """Perform aggregation operations on grouped data."""
        try:
            df = self._get_cached_data(filename)
            
            if group_by_column not in df.columns:
                return {"error": f"Group column '{group_by_column}' not found"}
            
            if target_column not in df.columns:
                return {"error": f"Target column '{target_column}' not found"}
            
            if not pd.api.types.is_numeric_dtype(df[target_column]):
                return {"error": f"Target column '{target_column}' is not numeric"}
            
            # Perform aggregation
            if operation.lower() == "mean":
                result = df.groupby(group_by_column)[target_column].mean()
            elif operation.lower() == "sum":
                result = df.groupby(group_by_column)[target_column].sum()
            elif operation.lower() == "count":
                result = df.groupby(group_by_column)[target_column].count()
            elif operation.lower() == "max":
                result = df.groupby(group_by_column)[target_column].max()
            elif operation.lower() == "min":
                result = df.groupby(group_by_column)[target_column].min()
            else:
                return {"error": f"Unsupported operation '{operation}'"}
            
            aggregation_result = [
                {
                    "group_value": str(key),
                    "result": round(float(value), 2) if isinstance(value, (int, float)) else value,
                }
                for key, value in result.items()
            ]
            
            return {
                "aggregation": {
                    "operation": operation,
                    "group_by": group_by_column,
                    "target_column": target_column,
                    "results": aggregation_result
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def detect_correlations(self, filename: str, columns: List[str]) -> Dict[str, Any]:
        """Calculate correlation coefficients between numeric columns."""
        try:
            df = self._get_cached_data(filename)
            
            # Validate columns exist and are numeric
            for col in columns:
                if col not in df.columns:
                    return {"error": f"Column '{col}' not found"}
                if not pd.api.types.is_numeric_dtype(df[col]):
                    return {"error": f"Column '{col}' is not numeric"}
            
            # Calculate correlations
            correlation_matrix = df[columns].corr()
            
            # Extract correlation pairs
            correlations = []
            for i in range(len(columns)):
                for j in range(i + 1, len(columns)):
                    col1, col2 = columns[i], columns[j]
                    corr_value = correlation_matrix.loc[col1, col2]
                    
                    if not pd.isna(corr_value):
                        correlations.append({
                            "column1": col1,
                            "column2": col2,
                            "correlation": round(float(corr_value), 4),
                            "strength": self._interpret_correlation(corr_value)
                        })
            
            return {
                "correlations": correlations,
                "total_pairs": len(correlations)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def find_outliers(self, filename: str, column_name: str, method: str = "iqr") -> Dict[str, Any]:
        """Detect outliers in a numeric column using statistical methods."""
        try:
            df = self._get_cached_data(filename)
            
            if column_name not in df.columns:
                return {"error": f"Column '{column_name}' not found"}
            
            if not pd.api.types.is_numeric_dtype(df[column_name]):
                return {"error": f"Column '{column_name}' is not numeric"}
            
            # Remove null values for analysis
            clean_data = df[column_name].dropna()
            
            if method.lower() == "iqr":
                Q1 = clean_data.quantile(0.25)
                Q3 = clean_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)]
                
                outlier_info = {
                    "method": "IQR",
                    "lower_bound": round(float(lower_bound), 4),
                    "upper_bound": round(float(upper_bound), 4),
                    "outlier_count": len(outliers),
                    "total_values": len(clean_data),
                    "outlier_percentage": round(len(outliers) / len(clean_data) * 100, 2),
                    "outlier_values": [round(float(x), 4) for x in outliers.head(10).tolist()]
                }
            else:
                return {"error": f"Unsupported method '{method}'"}
            
            return {"outlier_analysis": outlier_info}
        except Exception as e:
            return {"error": str(e)}
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """Interpret correlation strength."""
        abs_corr = abs(corr_value)
        if abs_corr >= 0.8:
            return "very strong"
        elif abs_corr >= 0.6:
            return "strong"
        elif abs_corr >= 0.4:
            return "moderate"
        elif abs_corr >= 0.2:
            return "weak"
        else:
            return "very weak"
    
    async def analyze_request(self, user_input: str) -> str:
        """
        Analyze user request using actual data analysis functions.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            str: The agent's response
        """
        try:
            # Add user input to session memory
            self._add_to_session_memory("user", user_input)
            
            # Get conversation context for better responses
            context = await self._get_conversation_context()
            
            # First, check if this is a simple data request
            if "available" in user_input.lower() or "datasets" in user_input.lower():
                datasets = self.get_available_datasets()
                response_content = f"""Available Datasets:

{chr(10).join([f"• {name}: {desc}" for name, desc in datasets.items()])}

Ask me to analyze any of these datasets!"""
            
            elif "info about" in user_input.lower() and ".csv" in user_input.lower():
                # Extract filename from request
                filename = user_input.lower().split("info about")[1].strip().replace(".", "").replace("csv", ".csv")
                info = self.get_dataset_info(filename)
                if "error" in info:
                    response_content = f"Error getting info for {filename}: {info['error']}"
                else:
                    response_content = f"""Information for {filename}:
Total Rows: {info['total_rows']}
Total Columns: {info['total_columns']}
Columns: {', '.join(info['columns'])}
Sample Data: {info['sample_data']}"""
            
            elif "highest" in user_input.lower() and "temperature" in user_input.lower():
                # Analyze weather data for highest temperature
                try:
                    df = self._get_cached_data("weather_data.csv")
                    max_temp_row = df.loc[df['temperature'].idxmax()]
                    response_content = f"""Highest Temperature Analysis:

Based on the actual weather_data.csv dataset:
• **Highest Temperature**: {max_temp_row['temperature']}°C
• **City**: {max_temp_row['city']}
• **Date**: {max_temp_row['date']}
• **Humidity**: {max_temp_row['humidity']}%
• **Precipitation**: {max_temp_row['precipitation']}mm

This is the real data from your dataset, not estimated values."""
                except Exception as e:
                    response_content = f"Error analyzing temperature data: {str(e)}"
            
            elif "lowest" in user_input.lower() and "temperature" in user_input.lower():
                # Analyze weather data for lowest temperature
                try:
                    df = self._get_cached_data("weather_data.csv")
                    min_temp_row = df.loc[df['temperature'].idxmin()]
                    response_content = f"""Lowest Temperature Analysis:

Based on the actual weather_data.csv dataset:
• **Lowest Temperature**: {min_temp_row['temperature']}°C
• **City**: {min_temp_row['city']}
• **Date**: {min_temp_row['date']}
• **Humidity**: {min_temp_row['humidity']}%
• **Precipitation**: {min_temp_row['precipitation']}mm

This is the real data from your dataset."""
                except Exception as e:
                    response_content = f"Error analyzing temperature data: {str(e)}"
            
            elif "average" in user_input.lower() and "temperature" in user_input.lower():
                # Calculate average temperature
                try:
                    df = self._get_cached_data("weather_data.csv")
                    avg_temp = df['temperature'].mean()
                    response_content = f"""Average Temperature Analysis:

Based on the actual weather_data.csv dataset:
• **Average Temperature**: {avg_temp:.1f}°C
• **Total Records**: {len(df)} weather measurements
• **Date Range**: {df['date'].min()} to {df['date'].max()}
• **Cities**: {', '.join(df['city'].unique())}

This is calculated from your real data, not estimated."""
                except Exception as e:
                    response_content = f"Error analyzing temperature data: {str(e)}"
            
            elif "statistics" in user_input.lower() or "stats" in user_input.lower():
                # Provide general statistics
                try:
                    df = self._get_cached_data("weather_data.csv")
                    stats = df['temperature'].describe()
                    response_content = f"""Temperature Statistics (Real Data):

Based on weather_data.csv:
• **Count**: {stats['count']} measurements
• **Mean**: {stats['mean']:.1f}°C
• **Std**: {stats['std']:.1f}°C
• **Min**: {stats['min']:.1f}°C
• **25%**: {stats['25%']:.1f}°C
• **50%**: {stats['50%']:.1f}°C
• **75%**: {stats['75%']:.1f}°C
• **Max**: {stats['max']:.1f}°C

All values are calculated from your actual dataset."""
                except Exception as e:
                    response_content = f"Error calculating statistics: {str(e)}"
            
            else:
                # For other requests, use OpenAI to help interpret but with real data context
                try:
                    # Get some real data samples to provide context
                    weather_df = self._get_cached_data("weather_data.csv")
                    weather_sample = weather_df.head(3).to_dict('records')
                    
                    system_prompt = f"""You are a CSV data analysis assistant. You have access to REAL data from these datasets:

1. **weather_data.csv** - {len(weather_df)} weather records from {weather_df['date'].min()} to {weather_df['date'].max()}
   Sample data: {weather_sample}

2. **sample_sales.csv** - E-commerce sales data
3. **employee_data.csv** - HR dataset

IMPORTANT: Only provide analysis based on the actual data available. If asked about specific values (temperatures, dates, cities), refer to the real data samples provided. Do NOT make up or estimate values.

{context}

Analyze the user's request using the real data context provided."""
                    
                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        max_tokens=600,
                        temperature=0.1
                    )
                    
                    response_content = response.choices[0].message.content
                except Exception as e:
                    response_content = f"Error processing request: {str(e)}"
            
            # Add response to session memory
            self._add_to_session_memory("assistant", response_content)
            
            return response_content
            
        except Exception as e:
            error_response = f"""Analysis Error

I encountered an issue while processing your request: {str(e)}

Please try:
- Checking if the dataset name is correct
- Ensuring column names match exactly
- Verifying the data format is valid

For help, ask: "What datasets are available?" or "Show me the columns in [dataset_name]" """
            
            # Add error to session memory
            self._add_to_session_memory("assistant", error_response)
            
            return error_response
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current session."""
        return {
            "session_id": self.session_id,
            "database_path": "csv_conversations.db",
            "framework": "hybrid (SQLiteSession + OpenAI API)",
            "memory_enabled": True,
            "session_type": "SQLiteSession"
        }


def create_csv_analysis_system(session_id: str = "default_csv_session") -> CSVAgent:
    """
    Factory function to create a CSV analysis system.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        CSVAgent: Configured agent instance
    """
    return CSVAgent(session_id=session_id) 