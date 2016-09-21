from __future__ import print_function

import string

import pytest
from hashids import Hashids
from hashids_cffi import Hashids as HashidsCFFI
from hypothesis import assume, given
from hypothesis.strategies import text, integers, tuples, lists, sampled_from, characters

valid_characters = list(string.ascii_letters + string.digits + string.punctuation)
MAX_ULONGLONG = 2 ** 64 - 1


@given(lists(characters(min_codepoint=128), average_size=64).map(''.join).filter(lambda s: bool(s) and not s.isspace()),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32))
def test_unicode_salt(salt, alphabet, min_length):
    with pytest.raises(UnicodeEncodeError):
        HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)


@given(text(alphabet=valid_characters, average_size=64),
       lists(characters(min_codepoint=128), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32))
def test_unicode_alphabet(salt, alphabet, min_length):
    alphabet = alphabet
    salt = salt

    with pytest.raises(UnicodeEncodeError):
        HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)


@given(text(alphabet=valid_characters, average_size=64),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), tuples(integers(min_value=0, max_value=MAX_ULONGLONG)))
def test_encode(salt, alphabet, min_length, numbers):
    alphabet = str(alphabet)
    salt = str(salt)

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    hashids_cffi_encoded_hash = hashids_cffi.encode(*numbers)
    assert hashids.encode(*numbers) == hashids_cffi_encoded_hash

    assert len(hashids_cffi_encoded_hash) >= min_length


@given(text(alphabet=valid_characters, average_size=64),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), text(alphabet=valid_characters, max_size=128))
def test_decode(salt, alphabet, min_length, hashid):
    alphabet = str(alphabet)
    salt = str(salt)
    hashid = str(hashid)

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    hashid_decoded_numbers = hashids.decode(hashid)
    # TODO: Add overflow checks the to C library
    # These cases causes integer overflow
    assume(all((number <= MAX_ULONGLONG for number in hashid_decoded_numbers)) or (hashid_decoded_numbers == ()))

    assert hashid_decoded_numbers == hashids_cffi.decode(hashid)
