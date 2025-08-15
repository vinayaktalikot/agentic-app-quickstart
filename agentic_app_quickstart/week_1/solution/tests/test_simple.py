import unittest
import os
import pandas as pd


class TestBasicFunctionality(unittest.TestCase):
    def test_data_files_exist(self):
        """test that sample data files exist"""
        data_dir = "data"
        self.assertTrue(os.path.exists(data_dir), f"data directory {data_dir} not found")

        csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
        self.assertGreater(len(csv_files), 0, "no csv files found in data directory")

        expected_files = ["employee_data.csv", "sample_sales.csv", "weather_data.csv"]
        for file in expected_files:
            self.assertIn(file, csv_files, f"expected file {file} not found")

    def test_csv_loading(self):
        data_dir = "data"
        employee_file = os.path.join(data_dir, "employee_data.csv")

        if os.path.exists(employee_file):
            df = pd.read_csv(employee_file)
            self.assertEqual(df.shape[0], 15)
            self.assertEqual(df.shape[1], 5)

            expected_columns = ["name", "department", "salary", "hire_date", "performance_score"]
            actual_columns = list(df.columns)
            self.assertEqual(set(expected_columns), set(actual_columns))

    def test_basic_analysis(self):
        """test basic data analysis operations"""
        data_dir = "data"
        employee_file = os.path.join(data_dir, "employee_data.csv")

        if os.path.exists(employee_file):
            df = pd.read_csv(employee_file)

            avg_salary = df["salary"].mean()
            self.assertGreater(avg_salary, 0)

            dept_counts = df["department"].value_counts()
            self.assertGreater(len(dept_counts), 0)

    def test_python_files_exist(self):
        required_files = ["main.py", "tools.py", "agent_definitions.py"]

        for file in required_files:
            self.assertTrue(os.path.exists(file), f"required file {file} not found")

    def test_file_sizes(self):
        files_to_check = ["main.py", "tools.py", "agent_definitions.py"]

        for file in files_to_check:
            if os.path.exists(file):
                size = os.path.getsize(file)
                self.assertGreater(size, 100, f"{file} seems too small ({size} bytes)")


if __name__ == "__main__":
    unittest.main()
