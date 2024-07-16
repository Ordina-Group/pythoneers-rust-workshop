import time

import numpy as np
from quicksort_py import quick_sort as quick_sort_py

from quicksort_rs import quick_sort as quick_sort_rs

rng = np.random.default_rng()
array = list(rng.integers(2**10, size=10000))

start_time = time.monotonic()
rs_result = quick_sort_rs(array)
rs_duration = time.monotonic() - start_time

start_time = time.monotonic()
py_result = quick_sort_py(array)
py_duration = time.monotonic() - start_time

print(f"Rust: {rs_duration:.6f} seconds"), print(f"Python: {py_duration:.6f} seconds")
print(f"Rust/Python: {py_duration/rs_duration:.2f} times faster")

assert rs_result == py_result
