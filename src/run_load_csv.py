import time
from pathlib import Path

from load_csv_py import load_csv as load_csv_py

from load_csv_rs import load_csv as load_csv_rs

ROOT_DIR = str(Path(__file__).parent.parent)
data_path = f"{ROOT_DIR}/data/full_dataset/goemotions_1.csv"

start_time = time.monotonic()
rs_result = load_csv_rs(data_path)
rs_duration = time.monotonic() - start_time

start_time = time.monotonic()
py_result = load_csv_py(data_path)
py_duration = time.monotonic() - start_time


print(f"Rust: {rs_duration:.6f} seconds"), print(f"Python: {py_duration:.6f} seconds")
print(f"Rust/Python: {py_duration/rs_duration:.2f} times faster")

print(py_result[1])
print(rs_result[1])

assert rs_result[1] == py_result[1]
