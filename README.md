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

## Rust Resources
Reading:
- [The Rust Book](https://doc.rust-lang.org/book/)

Excercises:
- [Rustlings](https://github.com/rust-lang/rustlings)
- [Rust by example](https://doc.rust-lang.org/rust-by-example/)

## PyO3
To use the speed of Rust with the easy-to-read Python the PyO3 package is used.
keep difficult logic in python and put easy but compute heavy resources in rust.
to use PyO3 there are some basic steps.
create a new rust library in the root of your project:
`cargo new intro_py_rs --lib`.
this will give you a rust lib made with 
```
intro_py_rs
    src
        lib.rs
    Cargo.toml
```
in lib.rs we are going make our rust module for python.
But first we need to add in Cargo.toml PyO3 dependency

```
[dependencies]
pyo3 = { version = "0.22.1", features = ["extension-module"] }
```

when you go to the folder `cd intro_py_rs`, you can compile and build the rust to python with:
`maturin develop` instead of the usual `cargo build`
`maturin develop` is building the rust library and inserting it in the python env.

### Exercise 1 
First let's check if all is up and running with a simple hello world
first we need to import the PyO3 library in our rust
`use pyo3::prelude::*;` 
#### Setup
we can start building our function with 

```
#[pyfunction]
fn hello_world(name: String) -> PyResult<String> {
    // here your function
}
```
the `#[pyfunction]` is a macro to let PyO3 know that it is a python function.
before we can use it in python we need to add it to our module that we will import in python.

To add it to the module it needs to be wrapped into the public function.
this is done by:
```
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
}
```
This function needs to have the same name as the name in the `cargo.toml`, 
so Rust knows where our entry is when building the package
#### Exercise 1.1
fill in the function `hello_world`, with the given input `"hello ... from rust"`

#### Compile to python
When the function is complete enough to be testen in python you can compile it to the python env.

go to the folder `cd intro_py_rs` and compile: `maturin develop` and starts compiling. 
When compiler finishes (when error appears, you need to fix the error 😃) start a python console within your environment. 
with the following you can test the code.
```
>> from intro_py_rs import hello_world
>> hellow_world("Name")
```
PyO3 has alot of different conversion to be able to raise for example exceptions for python in rust.
for our `hello_world` we can use 
`use pyo3::exceptions::PyValueError;` PyO3 has big list of conversions for python objects.
[exceptions Pyo3](https://pyo3.rs/v0.11.0/exception)

#### Exercise 1.2
add the exception to the hello world when we give it an empty string.

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
Let's make a 'fibonnacci' as a demo for the speed of rust while using Python
with the given python function it will take some time to finish with higher numbers.
```python
def fibonacci_python(n):
    """pythonic fibonacci function"""
    if n == 0: return 0
    if n == 1: return 1
    return fibonacci_python(n-1) + fibonacci_python(n-2)
```
let's make the same function in rust, and call it from Python to see the speed difference.
After compiling we should be able to call the fibonacci from rust like:
```python
from intro_py_rs import fibonacci
n= 40
print(fibonacci(n))
```
Don't forget to compile / build with `maturin develop` after you update the rust package

<details>
<summary>Solution</summary>

```rust
#[pyfunction]
pub fn fibonacci(n: u32) -> u32 {
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
To have a more feeling about the datatransfer between the Rust and Python we can make a mapping tool to map 2 lists to a dict
so let's say we have a list of keys and values. and we want them to collect and put it in a dict.
in Rust a dict is a HashMap [conversions Pyo3](https://pyo3.rs/v0.11.0/conversions) to check the possible conversions. 
the goal is to be able to call the dict mapping function from python like this:
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
Classes! in Rust class is pretty different, but we can still make sort of the same structure
so let's build a class in rust that we initiate in python
let's build a simple class like object (struct) in rust that holds a value. 
We should be able to increment the value by 1 with a `increment()` function.
the goal is to be able to do somthing like this in python:
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


### Exercize 5.1 (Bonus)
parallel processing, multiple threads to be able to process items faster. 
at first lets use the standaard lib of rust:
`use std::thread;` [docs thread](https://doc.rust-lang.org/std/thread/)


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

### Excersize 5.2 (Bonus,Bonus)

now let's use some easy to use liberaries. ;)
`use rayon::prelude::*;` [docs rayon](https://docs.rs/rayon/latest/rayon/index.html)