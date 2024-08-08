# pythoneers-rust-workshop

## Installing Rust (using rustc)

[linux](https://doc.rust-lang.org/book/ch01-01-installation.html#installing-rustup-on-linux-or-macos) / [windows](https://doc.rust-lang.org/book/ch01-01-installation.html#installing-rustup-on-windows)

## Working through some Rustlings examples

Rather than reinventing the wheel, we will use some community maintained examples from [Rustlings](https://github.com/rust-lang/rustlings).

`cargo install rustlings`

`rustlings init`

`cd rustlings`

`rustlings`

navigate with `l`, `c`, `q`

OR `cargo run --bin intro1`

Exercises to work through:

1. intro2 (printing)
2. variables1 (initialisation)
3. variables4 (mutability)
4. variables5 (shadowing)
5. functions4 (signature)
6. functions5 (return), there is no return!
7. if1 (conditional)
8. primitive_types3 (array)
9. move_semantics2 (ownership)
10. move_semantics5 (references)
11. structs2 (struct)
12. hashmaps1 (python dict)

## Rust Resources
Reading:
- [The Rust Book](https://doc.rust-lang.org/book/)

Excercises:
- [Rustlings](https://github.com/rust-lang/rustlings)
- [Rust by example](https://doc.rust-lang.org/rust-by-example/)

## PyO3
To combine the speed of Rust with the readability of Python, we use the PyO3 package. 
Keep difficult logic in Python and put easy but compute-heavy tasks in Rust. To use PyO3, follow these basic steps:
to use PyO3 we need to have `maturin` in the python environment, you can install it with: `pip install maturin`.

Create a new Rust library in the root of your project:
`cargo new intro_py_rs --lib`.
This will give you a Rust lib structured as follows:
```
intro_py_rs
    src
        lib.rs
    Cargo.toml
```
In lib.rs, we will create our Rust module for Python. But first, we need to add the PyO3 dependency in Cargo.toml:

```
[dependencies]
pyo3 = { version = "0.22.1", features = ["extension-module"] }
```
When you go to the folder `cd intro_py_rs`, you can compile and build the Rust library for Python with:
`maturin develop` 
instead of the usual `cargo build`. `maturin develop` builds the Rust library and inserts it into the Python environment.

### Exercise 1 
First, let's check if everything is up and running with a simple "Hello, World!" example. 
We need to import the PyO3 library in our Rust code:
`use pyo3::prelude::*;` 
#### Setup
We can start building our function with: 

```
#[pyfunction]
fn hello_world(name: String) -> PyResult<String> {
    // here your function
}
```
The `#[pyfunction]` macro indicates to PyO3 that this is a Python function. 
Before we can use it in Python, we need to add it to our module, which we will import in Python.

To add it to the module, it needs to be wrapped into a function, as follows:
```
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
}
```
This function needs to have the same name as the name in `Cargo.toml`, 
so Rust knows where our entry point is when building the package.
#### Exercise 1.1
Fill in the function `hello_world` that will return a string :`hello ... from rust`.

#### Compile to python
When the function is complete enough to be tested in Python, you can compile it to the Python environment.

Go to the folder `cd intro_py_rs` and compile with: `maturin develop`. 
When the compiler finishes (if an error appears, you need to fix the error 😃), 
start a Python console within your environment. With the following, you can test the code:
```
>> from intro_py_rs import hello_world
>> hello_world("Name")
```
Due to the difference in error handling from python and rust, PyO3 has special errors to communicate to Python.
For example `ValueError` for Python in Rust, for our `hello_world`, we can use:
`use pyo3::exceptions::PyValueError;` PyO3 has big list of conversions for python objects.
[exceptions Pyo3](https://pyo3.rs/v0.11.0/exception)

#### Exercise 1.2
Add an exception to the hello_world function when we give it an empty string. (you can use the `.trim().is_empty()`)

<details>
<summary>Solution Exercise 1</summary>

```rust
#[pyfunction]
fn hello_world(name: String) -> PyResult<String> {
    if name.trim().is_empty() {
        Err(PyValueError::new_err("Please provide a valid string!"))
    } else {
        Ok(format!("hello {} from rust", name))
    }
}
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    Ok(())
}
```
</details>

### Exercise 2
Let's make a `fibonacci` function as a demo for the speed of Rust while using Python. 
With the given Python function, it will take some time to finish with higher numbers:

```python
def fibonacci_python(n):
    """pythonic fibonacci function"""
    if n == 0: return 0
    if n == 1: return 1
    return fibonacci_python(n-1) + fibonacci_python(n-2)
```

Let's make the same function in Rust, and call it from Python to see the speed difference. 
After compiling, we should be able to call the Fibonacci function from Rust like:

```python
from intro_py_rs import fibonacci
n= 40
print(fibonacci(n))
```
Don't forget to compile/build with `maturin develop` after you update the Rust package.

<details>
<summary>Solution</summary>

```rust
#[pyfunction]
fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?; // < our new function
    Ok(())
}
```
</details>

### Exercise 3
To better understand data transfer between Rust and Python, we can make a mapping tool to map two lists to a dictionary.
Let's say we have a list of keys and values, and we want to collect and put them in a dictionary. 
In Rust, a dictionary is a HashMap. [conversions in Pyo3](https://pyo3.rs/v0.11.0/conversions) lists the possible conversions. 
The goal is to call the dictionary mapping function from Python like this:

```python
from intro_py_rs import create_dict

keys = ['a', 'b', 'c','a','c','b','c']
values = [1, 2, 3,4,5,6,7]
print(f"we got our dict from rust :) :{create_dict(keys, values)}")
```

<details>
<summary>Solution</summary>

```rust
#[pyfunction]
pub fn create_dict(keys: Vec<String>, values: Vec<i32>) -> PyResult<HashMap<String, Vec<i32>>> {
    if keys.len() != values.len() {
        return Err(PyValueError::new_err("Lengths of keys and values must match"));
    }

    let mut map = HashMap::new();
    for (key, value) in keys.into_iter().zip(values.into_iter()) {
        map.entry(key).or_insert(Vec::new()).push(value);
    }

    Ok(map)
}
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(create_dict, m)?)?; // < our new function
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    Ok(())
}

```

</details>

### Exercise 4 
Classes in Rust differ significantly, but we can still create a similar structure. 
Let's build a class-like object (struct) in Rust that holds a value. 
We should be able to increment the value by 1 with an `increment()` function. 
The goal is to do something like this in Python:
```python
from intro_py_rs import RustStruct

rust_struct = RustStruct(10)
print(f"Initial value: {rust_struct.get_value()}")
rust_struct.increment()
print(f"Value after increment: {rust_struct.get_value()}")
```

<details>
<summary>Solution</summary>

```rust
#[pyclass]
struct CustomStruct {
    value: i32,
}

#[pymethods]
impl CustomStruct {
    #[new]
    fn new(value: i32) -> Self {
        CustomStruct { value }
    }

    fn increment(&mut self) {
        self.value += 1;
    }

    fn get_value(&self) -> i32 {
        self.value
    }
}
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(create_dict, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    m.add_class::<CustomStruct>()?; // < our new class
    Ok(())
}
```

</details>


### Exercise 5.1 (Bonus)
Parallel processing using multiple threads can help process items faster. First, let's use Rust's standard library:
`use std::thread;` [docs thread](https://doc.rust-lang.org/std/thread/)
The goal of this assignment is to receive a list of strings from Python. 
For each string, we create a separate thread to count the number of words in the sentence and return the total count.
Example input of the function: `["this is some sentence","this is a second sentence","is this maybe also a sentance?"]`
Expected return of the function: `[4,5,6]` We will keep the process simple to demonstrate the threads, 
but in a real-world scenario, the process would likely be more resource-intensive.

<details>
<summary>Solution exersize 5.1</summary>

```rust
use pyo3::prelude::*;
use std::collections::HashMap;
use std::thread;

fn count_words(sentence: &str) -> usize {
    sentence.split_whitespace().count()
}


#[pyfunction]
fn find_words(strings: Vec<String>) -> PyResult<Vec<usize>> {
    let mut handles = vec![];

    for s in strings {
        let handle = thread::spawn(move || {
            count_words(&s)
        });
        handles.push(handle);
    }

    let mut results = vec![];
    for handle in handles {
        results.push(handle.join().unwrap());
    }

    Ok(results)
}

#[pymodule]
fn rust_python_threads(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_words, m)?)?;
    Ok(())
}
```
</details>

### Exercise 5.2 (Bonus, Bonus)

you can try out adding A good community lib for parallel processing instead of the standard library:
`use rayon::prelude::*;` [docs rayon](https://docs.rs/rayon/latest/rayon/index.html)