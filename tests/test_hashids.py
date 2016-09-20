from hashids_cffi import Hashids
import pytest


class TestConstructor(object):
    def test_small_alphabet(self):
        pytest.raises(ValueError, Hashids, alphabet='abcabc')


class TestEncoding(object):
    def test_empty_call(self):
        assert Hashids().encode() == ''

    def test_default_salt(self):
        assert Hashids().encode(1, 2, 3) == 'o2fXhV'

    @pytest.mark.parametrize('number,hashid', [[12345, 'j0gW'],
                                               [1, 'jR'],
                                               [22, 'Lw'],
                                               [333, 'Z0E'],
                                               [9999, 'w0rR']])
    def test_single_number(self, number, hashid):
        h = Hashids()
        assert h.encode(number) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(683, 94108, 123, 5), 'vJvi7On9cXGtD'],
                                                [(1, 2, 3), 'o2fXhV'],
                                                [(2, 4, 6), 'xGhmsW'],
                                                [(99, 25), '3lKfD']])
    def test_multiple_numbers(self, numbers, hashid):
        h = Hashids()
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(683, 94108, 123, 5), 'QWyf8yboH7KT2'],
                                                [(1, 2, 3), 'neHrCa'],
                                                [(2, 4, 6), 'LRCgf2'],
                                                [(99, 25), 'JOMh1']])
    def test_salt(self, numbers, hashid):
        h = Hashids(salt='Arbitrary string')
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(2839, 12, 32, 5), '_nJUNTVU3'],
                                                [(1, 2, 3), '7xfYh2'],
                                                [(23832,), 'Z6R>'],
                                                [(99, 25), 'AYyIB']])
    def test_alphabet(self, numbers, hashid):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'pO3K69b86jzc6krI416enr2B5'],
                                                [(1, 2, 3), 'gyOwl4B97bo2fXhVaDR0Znjrq'],
                                                [(6097,), 'Nz7x3VXyMYerRmWeOBQn6LlRG'],
                                                [(99, 25), 'k91nqP3RBe3lKfDaLJrvy8XjV']])
    def test_min_length(self, numbers, hashid):
        h = Hashids(min_length=25)
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'wygqxeunkatjgkrw'],
                                                [(1, 2, 3), 'pnovxlaxuriowydb'],
                                                [(60125,), 'jkbgxljrjxmlaonp'],
                                                [(99, 25), 'erdjpwrgouoxlvbx']])
    def test_all_parameters(self, numbers, hashid):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'X50Yg6VPoAO4'],
                                                [(1, 2, 3), 'GAbDdR'],
                                                [(60125,), '5NMPD'],
                                                [(99, 25), 'yGya5']])
    def test_alphabet_without_standard_separators(self, numbers, hashid):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890')
        assert h.encode(*numbers) == hashid

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'GJNNmKYzbPBw'],
                                                [(1, 2, 3), 'DQCXa4'],
                                                [(60125,), '38V1D'],
                                                [(99, 25), '373az']])
    def test_alphabet_with_two_standard_separators(self, numbers, hashid):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890uC')
        assert h.encode(*numbers) == hashid

    def test_negative_call(self):
        assert Hashids().encode(1, -2, 3) == ''

    def test_float_call(self):
        assert Hashids().encode(1, 2.5, 3) == ''

    def test_encode_hex(self):
        assert Hashids().encode_hex('507f1f77bcf86cd799439011') == 'y42LW46J9luq3Xq9XMly'
        assert len(Hashids(min_length=1000).encode_hex('507f1f77bcf86cd799439011')) >= 1000
        assert Hashids().encode_hex(
            'f000000000000000000000000000000000000000000000000000000000000000000000000000000000000f') == \
               'WxMLpERDrmh25Lp4L3xEfM6WovWYO3IjkRMKR2ogCMVzn4zQlqt1WK8jKq7OsEpy2qyw1Vi2p'

    def test_illegal_hex(self):
        assert Hashids().encode_hex('') == ''
        assert Hashids().encode_hex('1234SGT8') == ''


class TestDecoding(object):
    def test_empty_string(self):
        assert Hashids().decode('') == ()

    def test_non_string(self):
        assert Hashids().decode(object()) == ()

    def test_default_salt(self):
        assert Hashids().decode('o2fXhV') == (1, 2, 3)

    def test_empty_call(self):
        assert Hashids().decode('') == ()

    @pytest.mark.parametrize('numbers,hashid', [[(12345,), 'j0gW'],
                                                [(1,), 'jR'],
                                                [(22,), 'Lw'],
                                                [(333,), 'Z0E'],
                                                [(9999,), 'w0rR']])
    def test_single_number(self, numbers, hashid):
        h = Hashids()
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(683, 94108, 123, 5), 'vJvi7On9cXGtD'],
                                                [(1, 2, 3), 'o2fXhV'],
                                                [(2, 4, 6), 'xGhmsW'],
                                                [(99, 25), '3lKfD']])
    def test_multiple_numbers(self, numbers, hashid):
        h = Hashids()
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(683, 94108, 123, 5), 'QWyf8yboH7KT2'],
                                                [(1, 2, 3), 'neHrCa'],
                                                [(2, 4, 6), 'LRCgf2'],
                                                [(99, 25), 'JOMh1']])
    def test_salt(self, numbers, hashid):
        h = Hashids(salt='Arbitrary string')
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(2839, 12, 32, 5), '_nJUNTVU3'],
                                                [(1, 2, 3), '7xfYh2'],
                                                [(23832,), 'Z6R>'],
                                                [(99, 25), 'AYyIB']])
    def test_alphabet(self, numbers, hashid):
        h = Hashids(alphabet='!"#%&\',-/0123456789:;<=>ABCDEFGHIJKLMNOPQRSTUVWXYZ_`abcdefghijklmnopqrstuvwxyz~')
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'pO3K69b86jzc6krI416enr2B5'],
                                                [(1, 2, 3), 'gyOwl4B97bo2fXhVaDR0Znjrq'],
                                                [(6097,), 'Nz7x3VXyMYerRmWeOBQn6LlRG'],
                                                [(99, 25), 'k91nqP3RBe3lKfDaLJrvy8XjV']])
    def test_min_length(self, numbers, hashid):
        h = Hashids(min_length=25)
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'wygqxeunkatjgkrw'],
                                                [(1, 2, 3), 'pnovxlaxuriowydb'],
                                                [(60125,), 'jkbgxljrjxmlaonp'],
                                                [(99, 25), 'erdjpwrgouoxlvbx']])
    def test_all_parameters(self, numbers, hashid):
        h = Hashids('arbitrary salt', 16, 'abcdefghijklmnopqrstuvwxyz')
        assert h.decode(hashid) == numbers

    def test_invalid_hash(self):
        assert Hashids(alphabet='abcdefghijklmnop').decode('qrstuvwxyz') == ()

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'X50Yg6VPoAO4'],
                                                [(1, 2, 3), 'GAbDdR'],
                                                [(60125,), '5NMPD'],
                                                [(99, 25), 'yGya5']])
    def test_alphabet_without_standard_separators(self, numbers, hashid):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890')
        assert h.decode(hashid) == numbers

    @pytest.mark.parametrize('numbers,hashid', [[(7452, 2967, 21401), 'GJNNmKYzbPBw'],
                                                [(1, 2, 3), 'DQCXa4'],
                                                [(60125,), '38V1D'],
                                                [(99, 25), '373az']])
    def test_alphabet_with_two_standard_separators(self, numbers, hashid):
        h = Hashids(alphabet='abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890uC')
        assert h.decode(hashid) == numbers

    def test_only_one_valid(self):
        h = Hashids(min_length=6)
        assert h.decode(h.encode(1)[:-1] + '0') == ()

    def test_decode_hex(self):
        hex_str = '507f1f77bcf86cd799439011'
        assert Hashids().decode_hex('y42LW46J9luq3Xq9XMly') == hex_str
        h = Hashids(min_length=1000)
        assert h.decode_hex(h.encode_hex(hex_str)) == hex_str
        assert Hashids().decode_hex('WxMLpERDrmh25Lp4L3xEfM6WovWYO3IjkRMKR2ogCMVzn4zQlqt1WK8jKq7OsEpy2qyw1Vi2p') == \
               'f000000000000000000000000000000000000000000000000000000000000000000000000000000000000f'

    def test_illegal_decode_hex(self):
        assert Hashids().decode_hex('') == ''
        assert Hashids().decode_hex('WxMLpERDrmh25Lp4L3xEfM6WovWYO3IjkRMKR2ogCMVlqt1WK8jKq7OsEp1Vi2p') == ''
