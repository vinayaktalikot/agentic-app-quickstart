import pandas as pd
import numpy as np
from typing import Dict, Any
from agents import function_tool
import os


class CSVDataManager:
    def __init__(self):
        self.loaded_datasets = {}
        self.current_dataset = None

    def load_csv_file(self, file_path: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(file_path):
                return {"error": f"file not found: {file_path}"}

            df = pd.read_csv(file_path)
            dataset_info = {
                "file_path": file_path,
                "rows": len(df),
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "dataframe": df,
            }

            self.loaded_datasets[file_path] = dataset_info
            self.current_dataset = file_path

            return {
                "success": True,
                "message": f"loaded {len(df)} rows and {len(df.columns)} columns from {file_path}",
                "dataset_info": dataset_info,
            }
        except Exception as e:
            return {"error": f"failed to load csv: {str(e)}"}

    def get_column_names(self) -> Dict[str, Any]:
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]
        return {"columns": list(df.columns), "total_columns": len(df.columns)}

    def get_column_info(self, column_name: str) -> Dict[str, Any]:
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]

        if column_name not in df.columns:
            return {"error": f"column '{column_name}' not found"}

        col_data = df[column_name]
        info = {
            "column_name": column_name,
            "data_type": str(col_data.dtype),
            "total_values": len(col_data),
            "missing_values": col_data.isnull().sum(),
            "unique_values": col_data.nunique(),
        }

        if pd.api.types.is_numeric_dtype(col_data):
            info.update(
                {
                    "min_value": float(col_data.min()),
                    "max_value": float(col_data.max()),
                    "mean_value": float(col_data.mean()),
                    "median_value": float(col_data.median()),
                    "std_deviation": float(col_data.std()),
                }
            )
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            info.update({"date_range": {"start": str(col_data.min()), "end": str(col_data.max())}})
        else:
            info["sample_values"] = col_data.dropna().unique()[:5].tolist()

        return info

    def calculate_column_average(self, column_name: str) -> Dict[str, Any]:
        """calculate the average value of a numeric column"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]

        if column_name not in df.columns:
            return {"error": f"column '{column_name}' not found"}

        col_data = df[column_name]
        if not pd.api.types.is_numeric_dtype(col_data):
            return {"error": f"column '{column_name}' is not numeric"}

        avg_value = col_data.mean()
        return {
            "column_name": column_name,
            "average": float(avg_value),
            "total_values": len(col_data),
            "missing_values": col_data.isnull().sum(),
        }

    def count_rows_with_value(self, column_name: str, value: str) -> Dict[str, Any]:
        """count rows that contain a specific value in a column"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]

        if column_name not in df.columns:
            return {"error": f"column '{column_name}' not found"}

        count = (df[column_name] == value).sum()
        total_rows = len(df)

        return {
            "column_name": column_name,
            "search_value": value,
            "matching_rows": int(count),
            "total_rows": total_rows,
            "percentage": round((count / total_rows) * 100, 2),
        }

    def find_correlations(self) -> Dict[str, Any]:
        """find correlations between numeric columns"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return {"error": "need at least 2 numeric columns for correlation analysis"}

        corr_matrix = df[numeric_cols].corr()
        correlations = []

        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                col1, col2 = numeric_cols[i], numeric_cols[j]
                corr_value = corr_matrix.loc[col1, col2]
                correlations.append(
                    {"column1": col1, "column2": col2, "correlation": round(float(corr_value), 3)}
                )

        return {"numeric_columns": list(numeric_cols), "correlations": correlations}

    def detect_outliers(self, column_name: str, threshold: float = 2.0) -> Dict[str, Any]:
        """detect statistical outliers in a numeric column using z-score method"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]

        if column_name not in df.columns:
            return {"error": f"column '{column_name}' not found"}

        col_data = df[column_name]
        if not pd.api.types.is_numeric_dtype(col_data):
            return {"error": f"column '{column_name}' is not numeric"}

        z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
        outliers = z_scores > threshold

        outlier_indices = outliers[outliers].index.tolist()
        outlier_values = col_data[outliers].tolist()

        return {
            "column_name": column_name,
            "threshold": threshold,
            "outlier_count": len(outlier_indices),
            "outlier_indices": outlier_indices,
            "outlier_values": outlier_values,
            "total_values": len(col_data),
        }

    def group_by_column(
        self, group_column: str, agg_column: str, agg_function: str = "mean"
    ) -> Dict[str, Any]:
        """group data by a column and apply aggregation to another column"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]

        if group_column not in df.columns:
            return {"error": f"group column '{group_column}' not found"}
        if agg_column not in df.columns:
            return {"error": f"aggregation column '{agg_column}' not found"}

        if not pd.api.types.is_numeric_dtype(df[agg_column]):
            return {"error": f"aggregation column '{agg_column}' must be numeric"}

        valid_functions = ["mean", "sum", "count", "min", "max", "median"]
        if agg_function not in valid_functions:
            return {"error": f"invalid aggregation function. use one of: {valid_functions}"}

        grouped = df.groupby(group_column)[agg_column].agg(agg_function)

        return {
            "group_column": group_column,
            "aggregation_column": agg_column,
            "aggregation_function": agg_function,
            "results": grouped.to_dict(),
        }

    def suggest_questions(self) -> Dict[str, Any]:
        """suggest relevant questions based on the loaded dataset"""
        if not self.current_dataset:
            return {"error": "no dataset loaded"}

        df = self.loaded_datasets[self.current_dataset]["dataframe"]
        suggestions = []

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=["object"]).columns
        date_cols = df.select_dtypes(include=["datetime64"]).columns

        if len(numeric_cols) > 0:
            suggestions.extend(
                [
                    f"what is the average {numeric_cols[0]}?",
                    f"what is the highest {numeric_cols[0]}?",
                    f"are there any outliers in {numeric_cols[0]}?",
                ]
            )

        if len(categorical_cols) > 0:
            suggestions.extend(
                [
                    f"how many unique {categorical_cols[0]} values are there?",
                    f"what is the most common {categorical_cols[0]}?",
                    f"how many rows have {categorical_cols[0]} = 'specific_value'?",
                ]
            )

        if len(date_cols) > 0:
            suggestions.extend(
                [
                    f"what is the date range in {date_cols[0]}?",
                    f"are there any trends over time in {date_cols[0]}?",
                ]
            )

        if len(numeric_cols) >= 2:
            suggestions.append("what are the correlations between numeric columns?")

        return {"suggestions": suggestions[:8], "total_suggestions": len(suggestions)}


data_manager = CSVDataManager()


@function_tool
def load_csv_file(file_path: str) -> str:
    result = data_manager.load_csv_file(file_path)
    if "error" in result:
        return f"error: {result['error']}"
    return result["message"]


@function_tool
def get_column_names() -> str:
    result = data_manager.get_column_names()
    if "error" in result:
        return f"error: {result['error']}"
    return f"columns: {', '.join(result['columns'])}"


@function_tool
def get_column_info(column_name: str) -> str:
    result = data_manager.get_column_info(column_name)
    if "error" in result:
        return f"error: {result['error']}"

    info = result
    response = f"column '{column_name}' info:\n"
    response += f"- data type: {info['data_type']}\n"
    response += f"- total values: {info['total_values']}\n"
    response += f"- missing values: {info['missing_values']}\n"
    response += f"- unique values: {info['unique_values']}\n"

    if "mean_value" in info:
        response += f"- mean: {info['mean_value']:.2f}\n"
        response += f"- median: {info['median_value']:.2f}\n"
        response += f"- min: {info['min_value']:.2f}\n"
        response += f"- max: {info['max_value']:.2f}\n"

    return response


@function_tool
def calculate_column_average(column_name: str) -> str:
    result = data_manager.calculate_column_average(column_name)
    if "error" in result:
        return f"error: {result['error']}"
    return f"average {column_name}: {result['average']:.2f}"


@function_tool
def count_rows_with_value(column_name: str, value: str) -> str:
    result = data_manager.count_rows_with_value(column_name, value)
    if "error" in result:
        return f"error: {result['error']}"
    return f"found {result['matching_rows']} rows with {column_name} = '{value}' ({result['percentage']}%)"


@function_tool
def find_correlations() -> str:
    result = data_manager.find_correlations()
    if "error" in result:
        return f"error: {result['error']}"

    response = "correlations between numeric columns:\n"
    for corr in result["correlations"]:
        response += f"- {corr['column1']} vs {corr['column2']}: {corr['correlation']}\n"
    return response


@function_tool
def detect_outliers(column_name: str, threshold: float = 2.0) -> str:
    result = data_manager.detect_outliers(column_name, threshold)
    if "error" in result:
        return f"error: {result['error']}"

    if result["outlier_count"] == 0:
        return f"no outliers found in {column_name} (threshold: {threshold})"

    return f"found {result['outlier_count']} outliers in {column_name} (threshold: {threshold})"


@function_tool
def group_by_column(group_column: str, agg_column: str, agg_function: str = "mean") -> str:
    result = data_manager.group_by_column(group_column, agg_column, agg_function)
    if "error" in result:
        return f"error: {result['error']}"

    response = f"grouped by {group_column}, {agg_function} of {agg_column}:\n"
    for group, value in result["results"].items():
        if isinstance(value, float):
            response += f"- {group}: {value:.2f}\n"
        else:
            response += f"- {group}: {value}\n"
    return response


@function_tool
def suggest_questions() -> str:
    result = data_manager.suggest_questions()
    if "error" in result:
        return f"error: {result['error']}"

    response = "here are some questions you might want to ask:\n"
    for i, suggestion in enumerate(result["suggestions"], 1):
        response += f"{i}. {suggestion}\n"
    return response
