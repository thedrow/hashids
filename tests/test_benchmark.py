import pytest
from hashids import Hashids
from hashids_cffi import Hashids as HashidsCFFI


@pytest.mark.benchmark(group='encode', warmup=True, min_rounds=10, warmup_iterations=1000000)
@pytest.mark.parametrize("min_length", (0, 4, 8, 12, 24, 48, 120))
def test_encode_cffi(benchmark, min_length):
    @benchmark
    def bench():
        h = HashidsCFFI(min_length=min_length)
        h.encode(1)


@pytest.mark.benchmark(group='encode', warmup=True, min_rounds=10, warmup_iterations=1000000)
@pytest.mark.parametrize("min_length", (0, 4, 8, 12, 24, 48, 120))
def test_encode(benchmark, min_length):
    @benchmark
    def bench():
        h = Hashids(min_length=min_length)
        h.encode(1)


@pytest.mark.benchmark(group='decode', warmup=True, min_rounds=10, warmup_iterations=1000000)
@pytest.mark.parametrize("min_length", (0, 4, 8, 12, 24, 48, 120))
@pytest.mark.parametrize("hashid", ('jR', 'ejRe', 'olejRejN', '2VolejRejNmG', 'L39J4q2VolejRejNmGQBW71g',
                                    'KAyZnxO60XzkL39J4q2VolejRejNmGQBW71gPv58RYDMrpwE',
                                    'W9jOVvKy2G7qgRLGgV6QYRoBlrkyXZ5A43v2KAyZnxO60XzkL39J4q2VolejRejNmGQBW71gPv58RYDMrpwEO8z9jD0MEmNJqK7nw1xWPpBxkm5A4nYzXoMZ'))
def test_decode_cffi(benchmark, min_length, hashid):
    @benchmark
    def bench():
        h = HashidsCFFI(min_length=min_length)
        h.decode(hashid)


@pytest.mark.benchmark(group='decode', warmup=True, min_rounds=10, warmup_iterations=1000000)
@pytest.mark.parametrize("min_length", (0, 4, 8, 12, 24, 48, 120))
@pytest.mark.parametrize("hashid", ('jR', 'ejRe', 'olejRejN', '2VolejRejNmG', 'L39J4q2VolejRejNmGQBW71g',
                                    'KAyZnxO60XzkL39J4q2VolejRejNmGQBW71gPv58RYDMrpwE',
                                    'W9jOVvKy2G7qgRLGgV6QYRoBlrkyXZ5A43v2KAyZnxO60XzkL39J4q2VolejRejNmGQBW71gPv58RYDMrpwEO8z9jD0MEmNJqK7nw1xWPpBxkm5A4nYzXoMZ'))
def test_decode(benchmark, min_length, hashid):
    @benchmark
    def bench():
        h = Hashids(min_length=min_length)
        h.decode(hashid)
