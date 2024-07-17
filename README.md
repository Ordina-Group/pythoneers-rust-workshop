# pythoneers-rust-workshop


## PyO3
Using rust in python is like having only positives.
keep difficult logic in python and put easy but compute heavy resources in rust.
to use PyO3 there are some basic steps.
type in the root of your project:
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
there are more options but this one is not optional.

when you go to the folder `cd intro_py_rs`, you can compile and build the rust to python with:
`maturin develop`
That's all

### Exercise 1 
as first let's check if all is up and running with a simple hello world
`use pyo3::prelude::*;` this import is used to have the rust functions to convert to python. 

we can start building our function with 

```
#[pyfunction]
pub fn hello_world(name: String) -> PyResult<String> {
    // here your function
}
```
the `#[pyfunction]` is a macro to let PyO3 know that it is a python function.
To let make a module from this function and give it to python we need to wrap it in the module and make it public. 

```
#[pymodule]
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
}
```
this we do to "hang" the function that we wrote on the module

to test 
in the folder `intro_py_rs` `maturin develop` and starts compiling. 
When compiler finishes (when error you need to fix your error ;) start a python console within your environment. 
```
>> from intro_py_rs import hello_world
>> hellow_world("Name")
```
but what happens when we want to tell python that's somthing went wrong 
`use pyo3::exceptions::PyValueError;` PyO3 has big list of conversions for python objects.
[conversions/exceptions Pyo3](https://pyo3.rs/v0.11.0/exception)
<details>
<summary>Solution</summary>

```rust
#[pyfunction]
pub fn hello_world(name: String) -> PyResult<String> {
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
A frequently used function 'fibonnacci' is a good demo for the speed of rust while using Python
so given python function
```python
def fibonacci_python(n):
    """pythonic fibonacci function"""
    if n == 0: return 0
    if n == 1: return 1
    return fibonacci_python(n-1) + fibonacci_python(n-2)
```

let's make the same function in rust, and call it from Python to see the speed difference:
you can call you're function like a normal python package (after compiling)
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
in Rust a dict is a HashMap
an example in python how we use our rust is:
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
Classes! what is python without class. in Rust class is pretty different but we can still make sort of the same structure
so let's build a class in rust that we initiate in python
let's build a simple class (struct) in rust that holds a value. 
We can increment the value by 1
in the end in python we will have this working
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

