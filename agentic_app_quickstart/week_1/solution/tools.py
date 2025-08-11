import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional, Any
from pathlib import Path
import json
from datetime import datetime
from agents import function_tool


class DataManager:
    """Manages csv data loading, caching & validation"""
    
    def __init__(self):
        self._data_cache = {}
        self._metadata_cache = {}
        self._data_path = Path(__file__).parent / "data"
    
    def _load_csv_safely(self, filename: str) -> pd.DataFrame:
        """
        load CSV file with error handling & validation
        """
        file_path = self._data_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset '{filename}' not found")
        
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError(f"Dataset '{filename}' is empty")
            return df
        except pd.errors.EmptyDataError:
            raise ValueError(f"Dataset '{filename}' contains no data")
        except pd.errors.ParserError:
            raise ValueError(f"Dataset '{filename}' has invalid CSV format")
    
    def _get_cached_data(self, filename: str) -> pd.DataFrame:
        """
        retrieve data from cache or load if not cached
        """
        if filename not in self._data_cache:
            self._data_cache[filename] = self._load_csv_safely(filename)
        return self._data_cache[filename].copy()
    
    def _validate_column_exists(self, df: pd.DataFrame, column_name: str) -> None:
        """
        validate that a column exists in the dataset
        """
        if column_name not in df.columns:
            available_columns = ", ".join(df.columns)
            raise ValueError(f"Column '{column_name}' not found. Available columns: {available_columns}")
    
    def _validate_numeric_column(self, df: pd.DataFrame, column_name: str) -> None:
        """
        validate that a column contains numeric data
        """
        self._validate_column_exists(df, column_name)
        
        if not pd.api.types.is_numeric_dtype(df[column_name]):
            raise ValueError(f"Column '{column_name}' is not numeric. Data type: {df[column_name].dtype}")


_data_manager = DataManager()


@function_tool
def get_available_datasets() -> Dict[str, str]:
    """
    get list of available CSV datasets with descriptions.
    
    Returns:
        dict mapping dataset names to descriptions
    """
    datasets = {
        "sample_sales.csv": "E-commerce sales data with product, price, quantity, and customer state",
        "employee_data.csv": "HR dataset with employee names, departments, salaries, and performance scores",
        "weather_data.csv": "Weather measurements with temperature, humidity, precipitation, and city data"
    }
    return datasets


@function_tool
def get_dataset_info(filename: str) -> Dict[str, Any]:
    """
    get comprehensive information about a specific dataset
    
    Args:
        filename: Name of the CSV file to analyze
        
    Returns:
        dict containing dataset metadata and statistics
    """
    try:
        df = _data_manager._get_cached_data(filename)
        
        info = {
            "filename": filename,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(3).to_dict('records')
        }
        
        return info
        
    except Exception as e:
        return {"error": str(e), "filename": filename}


@function_tool
def calculate_column_statistics(filename: str, column_name: str) -> Dict[str, Any]:
    """
    calculate comprehensive statistics for a numeric column.
    
    Args:
        filename: Name of the CSV file
        column_name: Name of the column to analyze
        
    Returns:
        dict containing statistical measures
    """
    try:
        df = _data_manager._get_cached_data(filename)
        _data_manager._validate_numeric_column(df, column_name)
        
        column_data = df[column_name].dropna()
        
        if len(column_data) == 0:
            return {"error": f"No valid numeric data found in column '{column_name}'"}
        
        stats = {
            "column_name": column_name,
            "dataset": filename,
            "count": len(column_data),
            "mean": round(float(column_data.mean()), 2),
            "median": round(float(column_data.median()), 2),
            "std": round(float(column_data.std()), 2),
            "min": float(column_data.min()),
            "max": float(column_data.max()),
            "q25": round(float(column_data.quantile(0.25)), 2),
            "q75": round(float(column_data.quantile(0.75)), 2),
            "missing_values": int(df[column_name].isnull().sum())
        }
        
        return stats
        
    except Exception as e:
        return {"error": str(e), "column_name": column_name, "dataset": filename}


@function_tool
def count_rows_with_value(filename: str, column_name: str, value: Union[str, int, float]) -> Dict[str, Any]:
    """
    count rows where a specific column contains a given value.
    
    Args:
        filename: Name of the CSV file
        column_name: Name of the column to search
        value: Value to search for
        
    Returns:
        dictionary containing count and percentage information
    """
    try:
        df = _data_manager._get_cached_data(filename)
        _data_manager._validate_column_exists(df, column_name)
        
        total_rows = len(df)
        matching_rows = len(df[df[column_name] == value])
        percentage = round((matching_rows / total_rows) * 100, 2) if total_rows > 0 else 0
        
        result = {
            "dataset": filename,
            "column_name": column_name,
            "search_value": value,
            "total_rows": total_rows,
            "matching_rows": matching_rows,
            "percentage": percentage,
            "non_matching_rows": total_rows - matching_rows
        }
        
        return result
        
    except Exception as e:
        return {"error": str(e), "column_name": column_name, "dataset": filename}


@function_tool
def get_column_names(filename: str) -> Dict[str, Any]:
    """
    get all column names from a dataset with their data types.
    
    Args:
        filename: Name of the CSV file
        
    Returns:
        Dict containing column information
    """
    try:
        df = _data_manager._get_cached_data(filename)
        
        columns_info = []
        for col in df.columns:
            col_info = {
                "name": col,
                "data_type": str(df[col].dtype),
                "is_numeric": pd.api.types.is_numeric_dtype(df[col]),
                "unique_values": int(df[col].nunique()),
                "missing_values": int(df[col].isnull().sum())
            }
            columns_info.append(col_info)
        
        return {
            "dataset": filename,
            "total_columns": len(columns_info),
            "columns": columns_info
        }
        
    except Exception as e:
        return {"error": str(e), "dataset": filename}


@function_tool
def perform_data_aggregation(filename: str, group_by_column: str, operation: str, target_column: str) -> Dict[str, Any]:
    """
    perform aggregation operations on grouped data.
    
    Args:
        filename: Name of the CSV file
        group_by_column: Column to group by
        operation: Aggregation operation (sum, mean, count, min, max)
        target_column: Column to perform operation on
        
    Returns:
        dictionary containing aggregated results
    """
    try:
        df = _data_manager._get_cached_data(filename)
        _data_manager._validate_column_exists(df, group_by_column)
        _data_manager._validate_column_exists(df, target_column)
        
        if operation not in ['sum', 'mean', 'count', 'min', 'max', 'median']:
            return {"error": f"Unsupported operation '{operation}'. Supported: sum, mean, count, min, max, median"}
        
        if operation != 'count':
            _data_manager._validate_numeric_column(df, target_column)
        
        grouped = df.groupby(group_by_column)
        
        if operation == 'count':
            result = grouped.size().to_dict()
        else:
            result = grouped[target_column].agg(operation).to_dict()
        
        aggregated_data = [
            {
                "group_value": str(key),
                "result": round(float(value), 2) if isinstance(value, (int, float)) else value
            }
            for key, value in result.items()
        ]
        
        return {
            "dataset": filename,
            "group_by_column": group_by_column,
            "operation": operation,
            "target_column": target_column,
            "total_groups": len(aggregated_data),
            "results": aggregated_data
        }
        
    except Exception as e:
        return {"error": str(e), "dataset": filename}


@function_tool
def detect_correlations(filename: str, columns: List[str]) -> Dict[str, Any]:
    """
    calculate correlation coefficients between numeric columns
    
    Args:
        filename: Name of the CSV file
        columns: List of column names to analyze
        
    Returns:
        dictionary containing correlation matrix and insights
    """
    try:
        df = _data_manager._get_cached_data(filename)
        
        for col in columns:
            _data_manager._validate_column_exists(df, col)
            _data_manager._validate_numeric_column(df, col)
        
        if len(columns) < 2:
            return {"error": "At least 2 columns required for correlation analysis"}
        
        correlation_matrix = df[columns].corr()
        
        correlations = []
        for i, col1 in enumerate(columns):
            for j, col2 in enumerate(columns):
                if i < j:
                    corr_value = correlation_matrix.loc[col1, col2]
                    correlations.append({
                        "column1": col1,
                        "column2": col2,
                        "correlation": round(corr_value, 3),
                        "strength": _interpret_correlation_strength(corr_value)
                    })
        
        return {
            "dataset": filename,
            "columns_analyzed": columns,
            "correlations": correlations,
            "insights": _generate_correlation_insights(correlations)
        }
        
    except Exception as e:
        return {"error": str(e), "dataset": filename}


@function_tool
def find_outliers(filename: str, column_name: str, method: str = "iqr") -> Dict[str, Any]:
    """
    detect outliers in a numeric column using statistical methods
    
    Args:
        filename: Name of the CSV file
        column_name: Name of the column to analyze
        method: Detection method ('iqr' for Interquartile Range, 'zscore' for Z-Score)
        
    Returns:
        dict containing outlier info
    """
    try:
        df = _data_manager._get_cached_data(filename)
        _data_manager._validate_numeric_column(df, column_name)
        
        if method not in ['iqr', 'zscore']:
            return {"error": f"Unsupported method '{method}'. Supported: iqr, zscore"}
        
        column_data = df[column_name].dropna()
        
        if len(column_data) == 0:
            return {"error": f"No valid numeric data found in column '{column_name}'"}
        
        if method == 'iqr':
            outliers = _detect_outliers_iqr(column_data)
        else:
            outliers = _detect_outliers_zscore(column_data)
        
        outlier_values = column_data[outliers].tolist()
        
        return {
            "dataset": filename,
            "column_name": column_name,
            "method": method,
            "total_values": len(column_data),
            "outlier_count": len(outlier_values),
            "outlier_percentage": round((len(outlier_values) / len(column_data)) * 100, 2),
            "outlier_values": [round(x, 2) for x in outlier_values],
            "thresholds": _get_outlier_thresholds(column_data, method)
        }
        
    except Exception as e:
        return {"error": str(e), "column_name": column_name, "dataset": filename}


def _interpret_correlation_strength(corr_value: float) -> str:
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


def _generate_correlation_insights(correlations: List[Dict]) -> List[str]:
    insights = []
    
    for corr in correlations:
        if abs(corr['correlation']) >= 0.7:
            direction = "positive" if corr['correlation'] > 0 else "negative"
            insights.append(f"Strong {direction} correlation ({corr['correlation']}) between {corr['column1']} and {corr['column2']}")
        elif abs(corr['correlation']) >= 0.4:
            direction = "positive" if corr['correlation'] > 0 else "negative"
            insights.append(f"Moderate {direction} correlation ({corr['correlation']}) between {corr['column1']} and {corr['column2']}")
    
    return insights


def _detect_outliers_iqr(data: pd.Series) -> pd.Series:
    """
    detect outliers using interquartile-range-method
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (data < lower_bound) | (data > upper_bound)


def _detect_outliers_zscore(data: pd.Series) -> pd.Series:
    """
    detect outliers using z-score method
    """
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > 3


def _get_outlier_thresholds(data: pd.Series, method: str) -> Dict[str, float]:
    """
    get outlier detection thresholds
    """
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return {
            "lower_bound": round(float(Q1 - 1.5 * IQR), 2),
            "upper_bound": round(float(Q3 + 1.5 * IQR), 2)
        }
    else:
        mean = data.mean()
        std = data.std()
        return {
            "lower_bound": round(float(mean - 3 * std), 2),
            "upper_bound": round(float(mean + 3 * std), 2)
        }
