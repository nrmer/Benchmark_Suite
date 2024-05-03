import pytest
import os
import time
import numpy
from benchmark_suite.benchmark_timer import Benchmark_Timer


@pytest.mark.parametrize("repeats", [i for i in range(10)])
@pytest.mark.parametrize("duration", [(float(i) * 1e-5) for i in range(500)])
@pytest.mark.parametrize("atol", [1e-4, 1e-5])
def test_basic(repeats, duration, atol):
    timer = Benchmark_Timer()
    timer.create_timing_stream()
    timer.start_timer()
    time.sleep(duration)
    timed = timer.stop_timer(ret=True)

    st = time.perf_counter_ns()
    time.sleep(duration)
    ed = time.perf_counter_ns()
    dif = (ed - st) / 1e9

    assert numpy.isclose(timed, dif, atol=atol, rtol=1e-12)



@pytest.mark.parametrize("repeats", [10])
@pytest.mark.parametrize("duration", [(float(i) * 1e-5) for i in range(100)])
@pytest.mark.parametrize("atol", [1e-4, 1e-5])
def test_basic(repeats, duration, atol):
    timer = Benchmark_Timer()
    timer.create_timing_stream()
    timer.start_timer()
    for i in range(repeats):
        timer.interval()
        time.sleep(duration)
    timer.stop_timer()
    test = timer.return_dict(intervals=True)
    print(test)

    reference = []
    reference.append(time.perf_counter_ns())
    for i in range(repeats):
        reference.append(time.perf_counter_ns())
        time.sleep(duration)
    reference.append(time.perf_counter_ns())
    temp = reference
    for i in range(len(temp)-1, 0, -1):
        temp[i] = (temp[i] - temp[i - 1]) * 1e-9
    temp[0] = 0
    print(temp)

    for i in range(2, len(temp), 1):
        assert numpy.isclose(temp[i], test['standard'][i], atol=atol, rtol=1e-12)


@pytest.mark.xfail(reason='This test needs to be chacked manually.')
@pytest.mark.parametrize('file_path', [None, 'startstop_test'])
@pytest.mark.parametrize('file_name_decorator', [None, '_startstop_naming_test'])
@pytest.mark.parametrize('stream_names', [None, ['standard'], ['standard', 'second', 'third']])
@pytest.mark.parametrize('additional_data', [None, {'second': ['This', 'is', 'additional', 'data.']}])
def test_file_save(file_path, file_name_decorator, stream_names, additional_data):
    timer = Benchmark_Timer()
    timer.create_timing_stream()
    timer.create_timing_stream('second')
    timer.create_timing_stream('third')

    
    for i in range(10):
        timer.start_timer()
        time.sleep(0.01)
        timer.stop_timer()
    

    for i in range(10):
        timer.start_timer(stream_name='second')
        time.sleep(0.01)
        timer.stop_timer(stream_name='second')

    timer.times_to_files(stream_names=stream_names,
                         times_filename_decorator=file_name_decorator,
                         times_path=file_path,
                         additional_data=additional_data)

    print('Confirm the correctness of the generated file(s) now.')
    time.sleep(30)
