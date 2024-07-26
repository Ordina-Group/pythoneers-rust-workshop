use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use std::collections::HashMap;
use std::thread;

#[pyfunction]
pub fn hello_world(name: String) -> PyResult<String> {
    if name.trim().is_empty() {
        Err(PyValueError::new_err("Please provide a valid string!"))
    } else {
        Ok(format!("hello {} from rust", name))
    }
}

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

#[pyfunction]
pub fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

#[pyclass]
struct RustStruct {
    value: i32,
}

#[pymethods]
impl RustStruct {
    #[new]
    fn new(value: i32) -> Self {
        RustStruct { value }
    }

    fn increment(&mut self) {
        self.value += 1;
    }

    fn get_value(&self) -> i32 {
        self.value
    }
}

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
fn intro_py_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(create_dict, m)?)?;
    m.add_class::<RustStruct>()?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    m.add_function(wrap_pyfunction!(find_words, m)?)?;
    Ok(())
}
