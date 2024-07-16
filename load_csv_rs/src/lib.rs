use csv::ReaderBuilder;
use pyo3::prelude::*;
use std::fs::File;

/// Reads a CSV file and returns a list of rows, each row is a list of strings.
#[pyfunction]
fn load_csv(path: String) -> PyResult<Vec<Vec<String>>> {
    let file = File::open(path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    let mut rdr = ReaderBuilder::new().has_headers(false).from_reader(file);
    let mut records = Vec::new();

    for result in rdr.records() {
        let record =
            result.map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
        records.push(record.iter().map(|s| s.to_string()).collect());
    }

    Ok(records)
}

/// A Python module implemented in Rust.
#[pymodule]
fn load_csv_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_csv, m)?)?;
    Ok(())
}
