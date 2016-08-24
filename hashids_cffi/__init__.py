from hashids_cffi._hashids import lib, ffi

try:
    StrType = basestring
except NameError:
    StrType = str


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
    result = ffi.string(buffer)

    lib.free(buffer)

    return result


class Hashids(object):
    def __init__(self, salt='', min_length=0, alphabet=None):
        min_length = max(int(min_length), 0)

        if not min_length and alphabet is None:
            self._handle = ffi.gc(lib.hashids_init(salt), lib.hashids_free)
        elif min_length > 0 and alphabet is None:
            self._handle = ffi.gc(lib.hashids_init2(salt, min_length), lib.hashids_free)
        else:
            self._handle = ffi.gc(lib.hashids_init3(salt, min_length, alphabet), lib.hashids_free)

        if lib.hashids_errno == -2:
            raise ValueError('Alphabet must contain at least 16 '
                             'unique characters.')

    def encode(self, *values):
        if not (values and all(_is_uint(x) for x in values)):
            return ''

        numbers_count = len(values)
        if numbers_count == 1:
            return _convert_buffer_to_string(lib.encode_one(self._handle, values[0]))

        return _convert_buffer_to_string(lib.encode(self._handle, numbers_count, values))

    def encode_hex(self, hex_str):
        if hex_str == '':
            return ''

        result = lib.encode_hex(self._handle, hex_str)
        if result == ffi.NULL:
            return ''

        return _convert_buffer_to_string(result)

    def decode(self, hashid):
        if not hashid or not _is_str(hashid):
            return ()

        numbers_count = ffi.new('unsigned int *')
        numbers = lib.decode(self._handle, hashid, numbers_count)
        if numbers == ffi.NULL:
            return ()

        result = tuple(numbers[i] for i in range(numbers_count[0]))
        lib.free(numbers)

        return result

    def decode_hex(self, hashid):
        if hashid == '':
            return ''

        output = ffi.new('char[18]')
        if lib.hashids_decode_hex(self._handle, hashid, ffi.addressof(output)) == 0:
            return ''

        return ffi.string(output)


__all__ = ['Hashids']
