from __future__ import unicode_literals

from hashids_cffi._hashids import lib, ffi

try:
    UnicodeType = unicode
    StrType = basestring
except NameError:
    StrType = UnicodeType = str


def _is_str(candidate):
    """Returns whether a value is a string."""
    return isinstance(candidate, StrType)


def _is_uint(number):
    """Returns whether a value is an unsigned integer."""
    try:
        return number == int(number) and number >= 0
    except ValueError:
        return False


def _convert_buffer_to_string(buffer):
    result = str(ffi.string(buffer).decode('ascii'))

    lib.free(buffer)

    return result


class Hashids(object):
    def __init__(self, salt=u'', min_length=0, alphabet=None):
        min_length = max(int(min_length), 0)

        if not min_length and alphabet is None:
            self._handle = ffi.gc(lib.hashids_init(UnicodeType(salt)), lib.hashids_free)
        elif min_length > 0 and alphabet is None:
            self._handle = ffi.gc(lib.hashids_init2(UnicodeType(salt), min_length), lib.hashids_free)
        else:
            self._handle = ffi.gc(
                lib.hashids_init3(UnicodeType(salt), min_length, UnicodeType(alphabet)),
                lib.hashids_free)

        if lib.hashids_errno == -2:
            raise ValueError('Alphabet must contain at least 16 '
                             'unique characters.')
        if lib.hashids_errno == -3:
            raise ValueError('Alphabet must not contain spaces.')

        if self._handle == ffi.NULL:
            raise ValueError('Unknown error occurred.')

    def encode(self, *values):
        if not (values and all(_is_uint(x) for x in values)):
            return ''

        numbers_count = len(values)
        if numbers_count == 1:
            return _convert_buffer_to_string(lib.encode_one(self._handle, values[0]))

        return _convert_buffer_to_string(lib.encode(self._handle, numbers_count, values))

    def encode_hex(self, hex_str):
        hex_str = UnicodeType(hex_str)
        if hex_str == '':
            return ''

        numbers = (int('1' + hex_str[i:i + 12], 16)
                   for i in range(0, len(hex_str), 12))

        try:
            return self.encode(*numbers)
        except ValueError:
            return ''

    def decode(self, hashid):
        if not hashid or not _is_str(hashid):
            return ()
        hashid = UnicodeType(hashid)

        numbers_count = ffi.new('unsigned int *')
        numbers = lib.decode(self._handle, hashid, numbers_count)
        if numbers == ffi.NULL:
            return ()

        result = tuple(numbers[i] for i in range(numbers_count[0]))
        lib.free(numbers)

        if self.encode(*result) != hashid:
            return ()

        return result

    def decode_hex(self, hashid):
        if hashid == '':
            return ''

        return ''.join(('%x' % x)[1:] for x in self.decode(hashid))


__all__ = ['Hashids']
