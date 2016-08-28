import gc
import pytest
from hashids import Hashids
from hashids_cffi import Hashids as HashidsCFFI


@pytest.mark.benchmark(group='encode', warmup=True, min_rounds=10, warmup_iterations=1000000)
def test_encode_cffi(benchmark):
    gc.collect()

    @benchmark
    def bench():
        h = HashidsCFFI()
        h.encode(1)


@pytest.mark.benchmark(group='encode', warmup=True, min_rounds=10, warmup_iterations=1000000)
def test_encode(benchmark):
    gc.collect()

    @benchmark
    def bench():
        h = Hashids()
        h.encode(1)


@pytest.mark.benchmark(group='decode', warmup=True, min_rounds=10, warmup_iterations=1000000)
def test_decode_cffi(benchmark):
    gc.collect()

    @benchmark
    def bench():
        h = HashidsCFFI()
        h.decode(u'gLNBk')


@pytest.mark.benchmark(group='decode', warmup=True, min_rounds=10, warmup_iterations=1000000)
def test_decode(benchmark):
    gc.collect()

    @benchmark
    def bench():
        h = Hashids()
        h.decode(u'gLNBk')
