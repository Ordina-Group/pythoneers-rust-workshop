import time

import pytest

from palindrome import buildPalindrome, start_palindrome, start_palindrome_with_rust


# from palindrome_rust import start_palindrome

@pytest.fixture()
def simpel_Case():
    input_string = """bac
    bac
    abc
    def
    jdfh
    fds"""

@pytest.fixture()
def few_seconds_Case():
    input_string = """htwqxzraskdjfoqbvjasdfpavsoidubalskjdiubas;plkfnpocvansdflkavpudabsdlfkjasbckjnapoxicnalsikebflaksjcnpaosebflskajdncaposeibfvlkacjnd
sdjcklfsfjapoewrnalkvmzcbpweiucrskdjfwein
pokdsfnvzlksdjfnowpeorijskdfpoesjdfowenf
sdkjfnweoskdjcnwpeorksmclkfnweoskdfnwpoe
weporifskdjcnwpeofjnaskdjfnpwejrofnskdjf
"""
    expected = ""
    return input_string, expected



def test_palindrome_simple_case():
    expected_output = ['aba', '-1', 'dfhfd']
    input_string = """bac
bac
abc
def
jdfh
fds"""

    start_time_python = time.time()
    found_palindromes = start_palindrome(input_string)
    end_time_python =time.time()
    print(f"\npython finished {round(end_time_python - start_time_python,2)} sec")
    start_time_rust = time.time()
    found_palindromes_2 = start_palindrome_with_rust(input_string)
    end_time_rust = time.time()
    print(f"rust finished {round(end_time_rust - start_time_rust,2)} sec")
    print(f"rust is {round((start_time_python-end_time_python)/(start_time_rust-end_time_rust) *100,2) }% faster")

    assert found_palindromes_2 ==expected_output
    assert found_palindromes ==expected_output

def test_palindrome_normal_case():
    expected_output = ['jdidj', 'kdsfsdk', 'cndnc']
    input_string = """htwqxzraskdjfoqbvjasdfpavsoidubalskjdiubas
sdjcklfsfjapoewrnalkvmzcbpweiucrskdjfwein
pokdsfnvzlksdjfnowpeorijskdfpoesjdfowenf
sdkjfnweoskdjcnwpeorksmclkfnweoskdfnwpoe
weporifskdjcnwpeofjnaskdjfnpwejrofnskdjf
plkfnpocvansdflkavpudabsdlfkjasbckjnapoxicnalsikebflaksjcnpaosebflskajdncaposeibfvlkacjnd
"""
    start_time_python = time.time()
    found_palindromes = start_palindrome(input_string)
    end_time_python =time.time()
    print(f"\npython finished {round(end_time_python - start_time_python,2)} sec")
    start_time_rust = time.time()
    found_palindromes_2 = start_palindrome_with_rust(input_string)
    end_time_rust = time.time()
    print(f"rust finished {round(end_time_rust - start_time_rust,2)} sec")
    print(f"rust is {round((start_time_python-end_time_python)/(start_time_rust-end_time_rust) *100,2) }% faster")

    assert found_palindromes_2 ==expected_output
    assert found_palindromes ==expected_output

def test_palindrome_havey_case():
    expected_output = ['eioie', 'djfjd', 'euiue', 'eirie', 'eurue', '-1']
    input_string = """asdjfpoqwenralskdjfpweiorlaksjdfpweoiralksjdfpoiausdfmnalskdfjpoaieurals
skdjnfowpneiralskdjfpoweiralskdjfpoaiwefnalskdfjpoaiwueralskdjfnvwpieuropalskdfjpoaiwuer
qpwoeirfalskdjfpoaiwueralskdjfpoaieurolaksjdfpoweirnalksjdfpoaiweuralskdjfpoweiruopalskiwe
alskdjfpowieuralksjdfpoaiwerulsdkjfpoaisudfmnalskdfjpoawieuralskdjfnweoirnpalskdjfpoawin
qwoeuiralskdjfpoaiweuralskdjfpoawueralskdfjpoaiwueralksdjfnpoiwueralskdjfpoawieuralskdjr
aklsdjfpoiwueralksdjfpoawieuralskdjfpoawierunalksdjfpoiwueralksdjfpoaiwerulsdkjfpoaiweudjf
pwoeiralksjdfpoaiwueralskdjfpoaiwueralksdjfpoiwueralksdjfpoaiweuralskdjfpoaiweuralskdjfral
sdjfpoaiweuralskdjfpoawieuralskdjfpoaiwerulsdkjfpoaisudfmnalskdfjpoaiwueralksdjfpoiwuer
fpoaiwueralskdjfpoawierunalksdjfpoiwueralksdjfpoaiweuralskdjfpoawierunalskdjfpoaiweuraloa
lkdfjpoaiweuralskdjfpoaiwueralksdjfpoiwueralskdjfpoaiweuralskdjfpoaiweuralskdjfpoaiwuerp
woeiralksjdfpoaiwueralskdjfpoaiwueralksdjfpoiwueralksdjfpoaiweuralskdjfpoaiweuralskdjfpal
"""

    start_time_python = time.time()
    found_palindromes = start_palindrome(input_string)
    end_time_python =time.time()
    print(f"\npython finished {round(end_time_python - start_time_python,2)} sec")
    start_time_rust = time.time()
    found_palindromes_2 = start_palindrome_with_rust(input_string)
    end_time_rust = time.time()
    print(f"rust finished {round(end_time_rust - start_time_rust,2)} sec")
    print(f"rust is {round((start_time_python-end_time_python)/(start_time_rust-end_time_rust) *100,2) }% faster")

    assert found_palindromes_2 ==expected_output
    assert found_palindromes ==expected_output