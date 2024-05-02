import pytest
import time
import os
import numpy
from benchmark_suite.benchmark_timer import Benchmark_Timer


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


@pytest.mark.parametrize('file_path', [None, 'interval_test'])
@pytest.mark.parametrize('file_name', [None, 'interval_naming_test'])
@pytest.mark.parametrize('stream_names', [None, ['standard'], ['standard', 'second', 'third']])
@pytest.mark.parametrize('additional_data', [None, {'second': ['test1', 'test2']}])
def test_file_save(file_path, file_name, stream_names, additional_data):
    timer = Benchmark_Timer()
    timer.create_timing_stream()
    timer.create_timing_stream('second')
    timer.create_timing_stream('third')

    timer.start_timer()
    for i in range(10):
        timer.interval()
        time.sleep(0.01)
    timer.stop_timer()

    timer.start_timer(stream_name='second')
    for i in range(10):
        timer.interval(stream_name='second')
        time.sleep(0.01)
    timer.stop_timer(stream_name='second')

    timer.intervals_to_file(stream_names=stream_names, intervals_filename=file_name, intervals_path=file_path, additional_data=additional_data)

    if file_path is None:
        if file_name is None:
            print('Confirm the correctness of the file "intervals.csv" now.')
            time.sleep(30)
            os.remove('intervals.csv')
        else:
            print('Confirm the correctness of the file "' + file_name + '.csv" now.')
            time.sleep(30)
            os.remove(file_name + '.csv')
    else:
        if file_name is None:
            print('Confirm the correctness of the file "' + file_path + '/intervals.csv" now.')
            time.sleep(30)
            os.remove(file_path + '/intervals.csv')
        else:
            print('Confirm the correctness of the file "' + file_path + '/' + file_name + '.csv" now.')
            time.sleep(30)
            os.remove(file_path + '/' + file_name + '.csv')

