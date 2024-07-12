use pyo3::prelude::*;
use std::cmp::Ordering;

fn is_palindrome(string_to_test: &str) -> bool {
    let bytes = string_to_test.as_bytes();
    let mut left = 0;
    let mut right = bytes.len() - 1;
    while left < right {
        if bytes[left] != bytes[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }
    true
}

#[pyfunction]
fn build_palindrome_rs(a: &str, b: &str) -> String {
    let mut longest_palindrome = String::new();
    let len_a = a.len();
    let len_b = b.len();

    for i in 0..len_a {
        for j in i + 1..=len_a {
            let substring_a = &a[i..j];
            for k in 0..len_b {
                for l in k + 1..=len_b {
                    let substring_b = &b[k..l];
                    let combined = format!("{}{}", substring_a, substring_b);
                    if is_palindrome(&combined) {
                        match combined.len().cmp(&longest_palindrome.len()) {
                            Ordering::Greater => longest_palindrome = combined.clone(),
                            Ordering::Equal => if combined < longest_palindrome {
                                longest_palindrome = combined.clone();
                            },
                            Ordering::Less => {}
                        }
                    }
                }
            }
        }
    }

    if longest_palindrome.is_empty() {
        "-1".to_string()
    } else {
        longest_palindrome
    }
}

#[pymodule]
fn palindrome_rs(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(build_palindrome_rs, m)?)?;
    Ok(())
}
