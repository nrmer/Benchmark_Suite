import pytest
import time
import os
from numpy.testing import assert_allclose
from benchmark_suite.benchmark_timer import Benchmark_Timer



def test_basic():
    timer = Benchmark_Timer()
    timer.create_special_stream()

    reference = []
    for i in range(20):
        timer.special_stream_add(input=[i])
        reference.append(i)

    test = timer.return_dict(special_streams=True)['standard']

    assert_allclose(reference, test, atol=1e-3, rtol=1e-12)


def test_multiple():
    timer = Benchmark_Timer()
    timer.create_special_stream()

    reference = []
    for i in range(20):
        timer.special_stream_add(input=[i, i+1])
        reference.append(i)
        reference.append(i+1)

    test = timer.return_dict(special_streams=True)['standard']

    assert_allclose(reference, test, atol=1e-3, rtol=1e-12)


@pytest.mark.xfail(reason='This test needs to be chacked manually.')
@pytest.mark.parametrize('file_path', [None, 'special_streams_test'])
@pytest.mark.parametrize('file_name', [None, 'special_streams_naming_test'])
@pytest.mark.parametrize('stream_names', [None, ['standard'], ['standard', 'second', 'third']])
@pytest.mark.parametrize('additional_data', [None, {'second': ['test1', 'test2']}])
def test_file_save(file_path, file_name, stream_names, additional_data):
    timer = Benchmark_Timer()
    timer.create_special_stream()
    timer.create_special_stream('second')
    timer.create_special_stream('third')

    for i in range(10):
        timer.special_stream_add(input=[i])


    for i in range(10, 20):
        timer.special_stream_add(stream_name='second', input=[i, 'hi'])
 

    timer.special_streams_to_files(stream_names=stream_names,
                                   special_streams_filename=file_name,
                                   special_streams_path=file_path,
                                   additional_data=additional_data)

    if file_path is None:
        if file_name is None:
            print('Confirm the correctness of the file "special_streams.csv" now.')
            time.sleep(30)
            os.remove('special_streams.csv')
        else:
            print('Confirm the correctness of the file "' + file_name + '.csv" now.')
            time.sleep(30)
            os.remove(file_name + '.csv')
    else:
        if file_name is None:
            print('Confirm the correctness of the file "' + file_path + '/special_streams.csv" now.')
            time.sleep(30)
            os.remove(file_path + '/special_streams.csv')
        else:
            print('Confirm the correctness of the file "' + file_path + '/' + file_name + '.csv" now.')
            time.sleep(30)
            os.remove(file_path + '/' + file_name + '.csv')

# test_file_save(file_path=None,
#                file_name=None,
#                stream_names=None,
#                additional_data=None)