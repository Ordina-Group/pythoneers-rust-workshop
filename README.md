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

### solution:
```
#[pyfunction]
pub fn hello_world(name: String) -> PyResult<String> {
    if name.trim().is_empty() {
        Err(PyValueError::new_err("Please provide a valid string!"))
    } else {
        Ok(format!("hello {} from rust", name))
    }
}
```

