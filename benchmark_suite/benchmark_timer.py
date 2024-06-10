import time
import os
from typing import Optional, Callable


class Benchmark_Timer():
    
    def __init__(self,
                 timer_func: Optional[Callable] = time.perf_counter_ns,
                 output_unit_conversion: Optional[int] = 1e-9,
                 output_unit: Optional[str] = 'seconds'
                 ):
        self._timer_func = timer_func
        self._time = {}
        self._interval = {}
        self._running = {}
        self._special_streams = {}
        self._aggregate_streams = {}
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


    def create_aggregate_stream(self,
                             stream_name: Optional[str] = 'standard'
                             ):
        if stream_name in self._aggregate_streams:
            raise Exception(f'The aggregate_streams {stream_name} already exists. Please choose a different name.')
        self._aggregate_streams[stream_name] = []


    def create_special_stream(self,
                             stream_name: Optional[str] = 'standard'
                             ):
        if stream_name in self._special_streams:
            raise Exception(f'The special_stream {stream_name} already exists. Please choose a different name.')
        self._special_streams[stream_name] = []

    def reset_times(self,
                    exceptions: Optional[list] = None
                    ):
        for stream in self._time:
            if exceptions == None or not stream in exceptions:
                self._time[stream] = []
                self._interval[stream] = []
                self._running[stream] = 0


    def delete_aggregate_streams(self,
                    exceptions: Optional[list] = None
                    ):
        reset_list = []
        for stream in self._aggregate_streams:
            if exceptions == None or not stream in exceptions:
                reset_list.append(stream)
        for stream in reset_list:
            del self._aggregate_streams[stream]

    def delete_streams(self,
                      exceptions: Optional[list] = None
                      ):
        reset_list = []
        for stream in self._time:
            if exceptions == None or not stream in exceptions:
                reset_list.append(stream)
        for stream in reset_list:
            del self._time[stream]
            del self._interval[stream]
            del self._running[stream]


    def reset_special_streams(self,
                    exceptions: Optional[list] = None
                    ):
        for stream in self._special_streams:
            if exceptions == None or not stream in exceptions:
                self._special_streams[stream] = []


    def reset_aggregate_streams(self,
                    exceptions: Optional[list] = None
                    ):
        for stream in self._aggregate_streams:
            if exceptions == None or not stream in exceptions:
                self._aggregate_streams[stream] = []

    def delete_special_streams(self,
                      exceptions: Optional[list] = None
                      ):
        reset_list = []
        for stream in self._special_streams:
            if exceptions == None or not stream in exceptions:
                reset_list.append(stream)
        for stream in reset_list:
            del self._special_streams[stream]

    def start_timer(self,
                    stream_name: Optional[str] = 'standard'
                    ):
        if self._running[stream_name] == 1:
            raise Exception(f'The timing_stream {stream_name} is already running. It needs to be stopped before it can start again.')
        self._running[stream_name] = 1
        self._time[stream_name].append(self._timer_func())

    def stop_timer(self,
                   stream_name: Optional[str] = 'standard',
                   output: Optional[bool] = False,
                   ret: Optional[bool] = False
                   ):
        timing = self._timer_func()
        self._time[stream_name].append(timing)
        if self._running[stream_name] == 0:
            raise Exception(f'The timing_stream {stream_name} was not running. It needs to be started before it can stop.')
        self._running[stream_name] = 0
        if output:
            print(f'The measured time was {(self._time[stream_name][-1] - self._time[stream_name][-2]) * self._scaling_factor} {self._scaling_unit}.')
        if ret:
            return (self._time[stream_name][-1] - self._time[stream_name][-2]) * self._scaling_factor
        


    def special_stream_add(self,
                      stream_name: Optional[str] = 'standard',
                      input: Optional[list] = None
                      ):
        for element in input:
            self._special_streams[stream_name].append(element)



    def interval(self,
                 stream_name: Optional[str] = 'standard'
                 ):
        self._interval[stream_name].append(self._timer_func())


    def add_to_aggregate_streams(self,
                 aggregate_stream_name: Optional[str] = 'standard',
                 timing_stream_name: Optional[str] = 'standard',
                 additional_data: Optional[list] = None,
                 delimiter: Optional[str] = ','

                 ):
        sum = 0.0
        count = 0
        for i in range(0, len(self._time[timing_stream_name]), 2):
            sum += self._time[timing_stream_name][i+1] - self._time[timing_stream_name][i]
            count += 1
        if count == 0:
            raise Exception(f'The timing_stream {timing_stream_name} is empty. Please choose a non-empty stream to aggregate.')
        result_string = str((sum / float(count)) * self._scaling_factor)
        additional_data_string = ''
        if additional_data is not None:
            for i in additional_data:
                additional_data_string += delimiter + str(i)
        self._aggregate_streams[aggregate_stream_name].append(result_string + additional_data_string)


    def aggregate_stream_to_file(self,
                 aggregate_stream_name: Optional[str] = 'standard',
                 aggregate_filename: Optional[str] = None,
                 aggregate_path: Optional[str] = None):
        if aggregate_filename is None:
            aggregate_filename = 'aggregate'
        if aggregate_path is not None:
            self._create_path(aggregate_path)
            with open(aggregate_path + '/' + aggregate_filename + '.csv', 'a') as fp:
                for data in self._aggregate_streams[aggregate_stream_name]:
                    fp.write(data + '\n')
        else:
            with open(aggregate_filename + '.csv', 'a') as fp:
                for data in self._aggregate_streams[aggregate_stream_name]:
                    fp.write(data + '\n')


    def _create_intervals(self,
                          stream_name
                          ):
        temp = self._interval[stream_name]
        if len(temp) > 0:
            for i in range(len(temp)-1, 0, -1):
                temp[i] = (temp[i] - temp[i - 1]) * self._scaling_factor
        return temp[1:]
    

    def _create_path(self, path):
        os.makedirs(path, exist_ok=True)



    def intervals_to_file(self,
                    stream_names: Optional[list] = None,
                    intervals_path: Optional[str] = None,
                    intervals_filename: Optional[str] = None,
                    additional_data: Optional[dict] = None,
                    special_streams: Optional[list] = None,
                    delimiter: Optional[str] = ','
                    ):
        if intervals_filename is None:
            intervals_filename = 'intervals'
        if stream_names is None:
            stream_names = []
            for stream in self._time:
                stream_names.append(stream)
        if intervals_path is not None:
            self._create_path(intervals_path)
            with open(intervals_path + '/' + intervals_filename + '.csv', 'a') as fp:
                for stream in stream_names:
                    if additional_data is not None and stream in additional_data:
                        for i in additional_data[stream]:
                            fp.write(str(i) + delimiter)
                    fp.write(str(stream) + delimiter)
                    if len(self._interval[stream]) != 0:
                        interval = self._create_intervals(stream_name=stream)
                        for i in range(0, len(interval), 1):
                            fp.write(str(interval[i]))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][i]))
                            fp.write('\n')
        else:
            with open(intervals_filename + '.csv', 'a') as fp:
                for stream in stream_names:
                    if additional_data is not None and stream in additional_data:
                        for i in additional_data[stream]:
                            fp.write(str(i) + delimiter)
                    fp.write(str(stream) + delimiter)
                    if len(self._interval[stream]) != 0:
                        interval = self._create_intervals(stream_name=stream)
                        for i in range(0, len(interval), 1):
                            fp.write(str(interval[i]))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][i]))
                            fp.write('\n')


    

    def times_to_files(self,
                    stream_names: Optional[list] = None,
                    times_path: Optional[str] = None,
                    times_filename_decorator: Optional[str] = '',
                    additional_data: Optional[dict] = None,
                    special_streams: Optional[list] = None,
                    delimiter: Optional[str] = ','
                    ):
        if stream_names is None:
            stream_names = []
            for stream in self._time:
                stream_names.append(stream)
        if times_path is not None:
            self._create_path(times_path)
            for stream in stream_names:
                if self._running[stream] == 1:
                    raise Exception(f'The {stream} timer is still running. Stop the timer before saving the results to the file')
                if times_filename_decorator is not None:
                    with open(times_path + '/' + stream + '_' + times_filename_decorator + '.csv', 'a') as fp:
                        if additional_data is not None and stream in additional_data:
                            for i in additional_data[stream][0:-1]:
                                fp.write(str(i) + delimiter)
                            fp.write(str(additional_data[stream][-1]) + '\n')
                        for i in range(0, len(self._time[stream]), 2):
                            fp.write(str(self._time[stream][i]) + delimiter + str(self._time[stream][i + 1]) + delimiter +
                                    str((self._time[stream][i + 1] - self._time[stream][i]) * self._scaling_factor))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][int(i / 2)]))
                            fp.write('\n')
                else:
                    with open(times_path + '/' + stream + '.csv', 'a') as fp:
                        if additional_data is not None and stream in additional_data:
                            for i in additional_data[stream][0:-1]:
                                fp.write(str(i) + delimiter)
                            fp.write(str(additional_data[stream][-1]) + '\n')
                        for i in range(0, len(self._time[stream]), 2):
                            fp.write(str(self._time[stream][i]) + delimiter + str(self._time[stream][i + 1]) + delimiter +
                                    str((self._time[stream][i + 1] - self._time[stream][i]) * self._scaling_factor))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][int(i / 2)]))
                            fp.write('\n')
        else:
            for stream in stream_names:
                if self._running[stream] == 1:
                    raise Exception(f'The {stream} timer is still running. Stop the timer before saving the results to the file')
                if times_filename_decorator is not None:
                    with open(stream + '_' + times_filename_decorator + '.csv', 'a') as fp:
                        if additional_data is not None and stream in additional_data:
                            for i in additional_data[stream][0:-1]:
                                fp.write(str(i) + delimiter)
                            fp.write(str(additional_data[stream][-1]) + '\n')
                        for i in range(0, len(self._time[stream]), 2):
                            fp.write(str(self._time[stream][i]) + delimiter + str(self._time[stream][i + 1]) + delimiter +
                                    str((self._time[stream][i + 1] - self._time[stream][i]) * self._scaling_factor))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][int(i / 2)]))
                            fp.write('\n')
                else:
                    with open(stream + '.csv', 'a') as fp:
                        if additional_data is not None and stream in additional_data:
                            for i in additional_data[stream][0:-1]:
                                fp.write(str(i) + delimiter)
                            fp.write(str(additional_data[stream][-1]) + '\n')
                        for i in range(0, len(self._time[stream]), 2):
                            fp.write(str(self._time[stream][i]) + delimiter + str(self._time[stream][i + 1]) + delimiter +
                                    str((self._time[stream][i + 1] - self._time[stream][i]) * self._scaling_factor))
                            if special_streams is not None:
                                for special_stream in special_streams:
                                    fp.write(delimiter + str(self._special_streams[special_stream][int(i / 2)]))
                            fp.write('\n')
                

    def special_streams_to_files(self,
                    stream_names: Optional[list] = None,
                    special_streams_path: Optional[str] = None,
                    special_streams_filename: Optional[str] = None,
                    additional_data: Optional[dict] = None,
                    delimiter: Optional[str] = ','
                    ):
        if special_streams_filename is None:
            special_streams_filename = 'special_streams'
        if stream_names is None:
            stream_names = []
            for stream in self._special_streams:
                stream_names.append(stream)
        if special_streams_path is not None:
            self._create_path(special_streams_path)
            with open(special_streams_path + '/' + special_streams_filename + '.csv', 'a') as fp:
                for stream in stream_names:
                    if additional_data is not None and stream in additional_data:
                        for i in additional_data[stream]:
                            fp.write(str(i) + delimiter)
                    fp.write(str(stream) + delimiter)
                    if len(self._special_streams[stream]) != 0:
                        for i in self._special_streams[stream][0:-1]:
                            fp.write(str(i) + delimiter)
                        fp.write(str(self._special_streams[stream][-1]) + '\n')
        else:
            with open(special_streams_filename + '.csv', 'a') as fp:
                for stream in stream_names:
                    if additional_data is not None and stream in additional_data:
                        for i in additional_data[stream]:
                            fp.write(str(i) + delimiter)
                    fp.write(str(stream) + delimiter)
                    if len(self._special_streams[stream]) != 0:
                        for i in self._special_streams[stream][0:-1]:
                            fp.write(str(i) + delimiter)
                        fp.write(str(self._special_streams[stream][-1]) + '\n')




    def return_dict(self,
                    times: Optional[bool] = False,
                    intervals: Optional[bool] = False,
                    special_streams: Optional[bool] = False
                    ):
        interval_output = {}
        for stream in self._interval:
            interval_output[stream] = self._create_intervals(stream)
        if times and intervals and special_streams:
            return self._time, interval_output, self._special_streams
        if times and intervals:
            return self._time, interval_output
        if times and special_streams:
            return self._time, self._special_streams
        if intervals and special_streams:
            return interval_output, self._special_streams
        if times:
            return self._time
        if intervals:
            return interval_output
        if special_streams:
            return self._special_streams
        raise Exception('You need to choose at least one dictionary to output.')