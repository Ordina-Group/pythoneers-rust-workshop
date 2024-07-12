#!/bin/python3
import time

from palindrome_rs import build_palindrome_rs

def is_palindrome(string_to_test):
    return string_to_test == string_to_test[::-1]


def yield_substrings(string):
    l = len(string) + 1
    for i in range(0, l):
        for j in range(0, l):
            if string[i:j]:
                yield string[i:j]


def buildPalindrome(a, b):
    found_strings = []
    for str_a in yield_substrings(a):
        for str_b in yield_substrings(b):
            combined = str_a + str_b
            if is_palindrome(combined):
                found_strings.append(combined)

    if found_strings:
        res = sorted(found_strings, key=lambda word: (-len(word), word))
        return res[0]
    return "-1"

def start_palindrome(input_string:str)-> list[str]:
    iterator = iter(input_string.split("\n"))
    found_palindromes = []
    try:
        while True:
            element1 = next(iterator)
            element2 = next(iterator)
            found_palindromes.append(buildPalindrome(element1, element2))

    except StopIteration:
        pass
    return found_palindromes

def start_palindrome_with_rust(input_string: str) -> list[str]:
    iterator = iter(input_string.split("\n"))
    found_palindromes = []
    try:
        while True:
            element1 = next(iterator)
            element2 = next(iterator)
            start_time_python = time.time()
            found_palindromes.append(build_palindrome_rs(element1, element2))
            end_time_python = time.time()
            print(f"\nrust call finished {round(end_time_python - start_time_python, 2)} sec")

    except StopIteration:
        pass

    return found_palindromes