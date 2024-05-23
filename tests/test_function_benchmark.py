import pytest
import time
from benchmark_suite.function_benchmark import Function_Benchmark
from typing import Optional

def wait_function(delay: Optional[int] = 2):
    time.sleep(delay)


def test_no_call():
    timer = Function_Benchmark()
    timer.define_func_to_benchmark(wait_function)


def test_no_args():
    timer = Function_Benchmark()
    # def wait_function(delay: Optional[int] = 2):
    #     time.sleep(delay)
    timer.define_func_to_benchmark(wait_function)
    wait_function()
    print(timer.return_dict(times=True))


def test_with_args():
    timer = Function_Benchmark()
    # def wait_function(delay: Optional[int] = 2):
    #     time.sleep(delay)
    timer.define_func_to_benchmark(wait_function)
    wait_function(delay=5)
    print(timer.return_dict(times=True))
