from __future__ import print_function

import string

from hashids import Hashids
from hashids_cffi import Hashids as HashidsCFFI
from hypothesis import given
from hypothesis.strategies import text, integers, tuples, lists, sampled_from

valid_characters = list(string.ascii_letters + string.digits + string.punctuation)


@given(text(alphabet=valid_characters, average_size=54),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), tuples(integers(min_value=0)))
def test_encode(salt, alphabet, min_length, numbers):
    print('=' * 50)
    print("salt='%s'" % salt)
    print("alphabet='%s'" % alphabet)
    print("min_length=%s" % min_length)
    print("alphabet length=%s" % len(alphabet))
    print("numbers=%s" % list(numbers))

    alphabet = str(alphabet)
    salt = str(salt)

    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    assert hashids.encode(*numbers) == hashids_cffi.encode(*numbers)


@given(text(alphabet=valid_characters, average_size=64),
       lists(sampled_from(valid_characters), min_size=16, average_size=16, unique=True).map(''.join),
       integers(min_value=0, max_value=32), text(alphabet=valid_characters, max_size=128))
def test_decode(salt, alphabet, min_length, hashid):
    print('=' * 50)
    print("salt='%s'" % salt)
    print("alphabet='%s'" % bytes(alphabet))
    print("min_length=%s" % min_length)
    print("alphabet length=%s" % len(alphabet))
    print("hashid='%s'" % hashid)

    alphabet = str(alphabet)
    salt = str(salt)
    hashid = str(hashid)


    hashids = Hashids(salt=salt, alphabet=alphabet, min_length=min_length)
    hashids_cffi = HashidsCFFI(salt=salt, alphabet=alphabet, min_length=min_length)

    assert hashids.decode(hashid) == hashids_cffi.decode(hashid)
