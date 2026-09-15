"""
Unit tests for backend.core.hashing.

These don't touch the database or the network -- they're the fastest,
cheapest tests in the suite, which is exactly what pure functions like
"hash this string" deserve. When you add a new pure helper function
somewhere in backend/core, this is the kind of test file to copy.
"""

from backend.core.hashing import hash_password, verify_password


def test_hash_password_does_not_return_the_plaintext():
    hashed = hash_password("super-secret")

    assert hashed != "super-secret"


def test_hash_password_is_salted_and_therefore_not_deterministic():
    # Two hashes of the same password should differ because a random salt
    # is mixed in -- if this ever starts failing, something switched the
    # hashing scheme to an unsalted one, which is a security regression.
    first = hash_password("same-password")
    second = hash_password("same-password")

    assert first != second


def test_verify_password_accepts_the_correct_password():
    hashed = hash_password("correct-horse-battery-staple")

    assert verify_password("correct-horse-battery-staple", hashed) is True


def test_verify_password_rejects_an_incorrect_password():
    hashed = hash_password("correct-horse-battery-staple")

    assert verify_password("wrong-password", hashed) is False


def test_verify_password_is_case_sensitive():
    hashed = hash_password("CaseSensitive123")

    assert verify_password("casesensitive123", hashed) is False
