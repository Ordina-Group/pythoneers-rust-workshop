use pyo3::prelude::*;

#[pyfunction]
fn quick_sort(nums: Vec<i32>) -> Vec<i32> {
    if nums.len() <= 1 {
        return nums;
    }
    let pivot = nums[nums.len() / 2];
    let less: Vec<i32> = nums.iter().filter(|&&x| x < pivot).cloned().collect();
    let greater: Vec<i32> = nums.iter().filter(|&&x| x > pivot).cloned().collect();
    let equal: Vec<i32> = nums.iter().filter(|&&x| x == pivot).cloned().collect();

    [
        quick_sort(less).as_slice(),
        equal.as_slice(),
        quick_sort(greater).as_slice(),
    ]
    .concat()
}

/// A Python module implemented in Rust.
#[pymodule]
fn quicksort_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(quick_sort, m)?)?;
    Ok(())
}
