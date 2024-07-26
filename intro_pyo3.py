import time
from intro_py_rs import fibonacci,hello_world,create_dict,RustStruct

# Exercise 1 Hello World from rust in Python PyO3 install
print(hello_world("Pythoneer"))
# Exercise 1.5 Exception handling
try:
    print(hello_world(""))
except ValueError:
    print("print wow we got python exceptions from rust")

# Exercise 2 use the mapping ans Hasmaps to dict in PyO3
keys = ['a', 'b', 'c','a','c','b','c']
values = [1, 2, 3,4,5,6,7]
print(f"we got our dict from rust :) :{create_dict(keys, values)}")

# Exercise 3, Show the speed of Rust, recursion.
n = 12

start_time = time.monotonic()
print(fibonacci(n))
rust_duration = time.monotonic() - start_time
print('Rust Fibonacci duration: {:.2f} seconds'.format(rust_duration))

def fibonacci_python(n):
    """pythonic fibonacci function"""
    if n == 0: return 0
    if n == 1: return 1
    return fibonacci_python(n-1) + fibonacci_python(n-2)

start_time = time.monotonic()
print(fibonacci_python(n))
python_duration = time.monotonic() - start_time
print('Python Fibonacci duration: {:.2f} seconds'.format(python_duration))
try:
    speedup = python_duration / rust_duration
except ZeroDivisionError:
    speedup = 0
if speedup == 0:
    print("it's a draw")
else:
    print('Rust Fibonacci is {:.2f} % faster than Python'.format(speedup*100))

rust_struct = RustStruct(10)
print(f"Initial value: {rust_struct.get_value()}")
rust_struct.increment()
print(f"Value after increment: {rust_struct.get_value()}")