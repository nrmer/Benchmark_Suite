import time
import os
from typing import Optional, Callable


class Benchmark_Timer():
    
    def __init__(self,
                 timer_func: Optional[Callable] = time.perf_counter_ns,
                 output_unit_conversion: Optional[int] = 1e9,
                 output_unit: Optional[str] = 'seconds'
                 ):
        self._timer_func = timer_func
        self._time = {}
        self._interval = {}
        self._running = {}
        self._scaling_factor = output_unit_conversion
        self._scaling_unit = output_unit

    def create_timing_stream(self,
                             stream_name: Optional[str] = 'standard'
                             ):
        if stream_name in self._time:
            raise Exception(f'The timing_stream {stream_name} already exists. Please choose a different name.')
        self._time[stream_name] = []
        self._interval[stream_name] = []
        self._running[stream_name] = 0

    def reset_times(self,
                    exceptions: Optional[list] = None
                    ):
        for stream in self._time:
            if not stream in exceptions:
                self._time[stream] = []
                self._interval[stream] = []
                self._running[stream] = 0

    def reset_streams(self,
                      exceptions: Optional[list] = None
                      ):
        for stream in self._time:
            if not stream in exceptions:
                del self._time[stream]
                del self._interval[stream]
                del self._running[stream]

    def start_timer(self,
                    stream_name: Optional[str] = 'standard'
                    ):
        if self._running[stream_name] == 1:
            raise Exception(f'The timing_stream {stream_name} is already running. It needs to be stopped before it can start again.')
        measurement = self._timer_func()
        self._time[stream_name].append(measurement)
        self._interval[stream_name].append(measurement)

    def stop_timer(self,
                   stream_name: Optional[str] = 'standard',
                   ouput: Optional[bool] = False,
                   ret: Optional[bool] = False
                   ):
        measurement = self._timer_func()
        self._time[stream_name].append(measurement)
        self._interval[stream_name].append(measurement)
        self._running[stream_name] = 0
        if ouput:
            print(f'The measured time was {(self._time[stream_name][-1] - self._time[stream_name][-2]) / self._scaling_factor} {self._scaling_unit}.')
        if ret:
            return (self._time[stream_name][-1] - self._time[stream_name][-2]) / self._scaling_factor
        
    def interval(self,
                 stream_name: Optional[str] = 'standard'
                 ):
        self.interval[stream_name].append(self._timer_func())

    def _create_intervals(self,
                          stream_name
                          ):
        temp = self._interval[stream_name]
        for i in range(len(temp)-1, 0, -1):
            temp[i] = temp[i] - temp[i - 1]
        return temp

    def _create_path(path):
        os.makedirs("path", exist_ok=True)


    def intervals_to_file(self,
                    stream_names: Optional[list] = None,
                    intervals_path: Optional[str] = "",
                    intervals_filename: Optional[str] = 'intervals',
                    additional_data: Optional[dict] = None
                    ):
        if stream_names is None:
            stream_names = []
            for stream in self._time:
                stream_names.append(stream)
        self._create_path(intervals_path)
        with open(intervals_path + '/' + intervals_filename + '.csv', 'a') as fp:
            for stream in stream_names:
                if additional_data is not None and stream in additional_data:
                    for i in additional_data[stream]:
                        fp.write(str(i) + ',')
                fp.write(str(stream))
                for i in self._interval[stream][1:-1]:
                    fp.write(str(i) + ',')
                fp.write(str(self.interval[stream][-1]) + '\n')


    

    def times_to_files(self,
                    stream_name: Optional[list] = None,
                    times_path: Optional[str] = None,
                    times_filename_decorator: Optional[str] = '',
                    ):
        if stream_names is None:
            stream_names = []
            for stream in self._time:
                stream_names.append(stream)
        self._create_path(times_path)
        for stream in stream_names:
            if self._running[stream] == 1:
                raise Exception(f'The {stream} timer is still running. Stop the timer before saving the results to the file')
            with open(times_path + '/' + stream + times_filename_decorator + '.csv', 'a') as fp:
                for i in range(0, len(self._time[stream]), 2):
                    fp.write(str(self._time[stream]) + ',' + str(self._time[stream + 1]) + ',' +
                              str(self._time[stream + 1] - self._time[stream]) + '\n')
                


    def return_dict(self,
                    times: Optional[bool] = False,
                    intervals: Optional[bool] = False
                    ):
        interval_output = {}
        for stream in self._interval:
            interval_output[stream] = self._create_intervals(stream)
        if times and intervals:
            return self._time, interval_output
        if times:
            return self._time
        if intervals:
            return interval_output
        raise Exception('You need to choose at least one dictionary to output.')