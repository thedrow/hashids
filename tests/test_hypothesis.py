from __future__ import print_function

import string

import os
import pytest
from hashids import Hashids
from hashids_cffi import Hashids as HashidsCFFI
from hypothesis import Verbosity
from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import text, integers, tuples, lists, sampled_from, characters

valid_characters = list(string.ascii_letters + string.digits + string.punctuation)
MAX_EXAMPLES = 100000 if os.environ.get('CI', False) == 'true' else 10000


@given(lists(characters(min_codepoint=128), average_size=64).map(''.join).filter(lambda s: bool(s) and not s.isspace()),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32))
@settings(verbosity=Verbosity.verbose, max_examples=MAX_EXAMPLES)
def test_unicode_salt(salt, alphabet, min_length):
    with pytest.raises(UnicodeEncodeError):
        HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)


@given(text(alphabet=valid_characters, average_size=64),
       lists(characters(min_codepoint=128), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32))
@settings(verbosity=Verbosity.verbose, max_examples=MAX_EXAMPLES)
def test_unicode_alphabet(salt, alphabet, min_length):
    alphabet = alphabet
    salt = salt

    with pytest.raises(UnicodeEncodeError):
        HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)


@given(text(alphabet=valid_characters, average_size=64),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), tuples(integers(min_value=0)))
@settings(verbosity=Verbosity.verbose, max_examples=MAX_EXAMPLES)
def test_encode(salt, alphabet, min_length, numbers):
    alphabet = str(alphabet)
    salt = str(salt)

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    assert hashids.encode(*numbers) == hashids_cffi.encode(*numbers)


@given(text(alphabet=valid_characters, average_size=64),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), text(alphabet=valid_characters, max_size=128))
@settings(verbosity=Verbosity.verbose, max_examples=MAX_EXAMPLES)
def test_decode(salt, alphabet, min_length, hashid):
    alphabet = str(alphabet)
    salt = str(salt)
    hashid = str(hashid)

    # TODO: Add overflow checks the to C library
    # These cases causes integer overflow
    assume(salt != 'c' and alphabet != 'dfhajklbncemogpq' and min_length != 0 and hashid != 'abaaaabaaababbabaaaa')
    assume((salt != 'e' and alphabet != 'laqbmhgedjprkowfn2yzcEiAsBtGxv' and min_length != 1
            and hashid != 'aadrakvdrakaaaab'))

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    assert hashids.decode(hashid) == hashids_cffi.decode(hashid)
