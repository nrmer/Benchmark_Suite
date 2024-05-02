import pytest
import time
import torch
from benchmark_suite.benchmark_timer import Benchmark_Timer
from benchmark_suite.synchronized_benchmark_timer import Synchronized_Benchmark_Timer

def test_init_basic():
    timer = Benchmark_Timer()

def test_init_input():
    timer = Benchmark_Timer(timer_func=time.time())
    timer = Benchmark_Timer(output_unit_conversion=10)
    timer = Benchmark_Timer(output_unit='minutes')
    timer = Benchmark_Timer(timer_func=time.time(), output_unit_conversion=10, output_unit='minutes')

def test_init_basic_sync():
    timer = Synchronized_Benchmark_Timer(torch.cuda.synchronize())

@pytest.mark.xfail(reason='This test is expected to fail. The synchronized function needs an argument')
def test_init_basic_sync_false():
    timer = Synchronized_Benchmark_Timer()

def test_init_input_sync():
    timer = Synchronized_Benchmark_Timer(torch.cuda.synchronize(),timer_func=time.time())
    timer = Synchronized_Benchmark_Timer(torch.cuda.synchronize(),output_unit_conversion=10)
    timer = Synchronized_Benchmark_Timer(torch.cuda.synchronize(),output_unit='minutes')
    timer = Synchronized_Benchmark_Timer(torch.cuda.synchronize(),timer_func=time.time(), output_unit_conversion=10, output_unit='minutes')