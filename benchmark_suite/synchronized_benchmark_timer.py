from benchmark_suite.benchmark_timer import Benchmark_Timer
import time
from typing import Optional, Callable

class Synchronized_Benchmark_Timer(Benchmark_Timer):

    def __init__(self,
                 synchronization_func: Callable,
                 timer_func: Optional[Callable] = time.perf_counter_ns,
                 output_unit_conversion: Optional[int] = 1e-9,
                 output_unit: Optional[str] = 'seconds'
                 ):
        self._synchronization_func = synchronization_func
        super().__init__(timer_func=timer_func, output_unit_conversion=output_unit_conversion, output_unit=output_unit)

    def start_timer(self,
                    stream_name: Optional[str] = 'standard'
                    ):
        self._synchronization_func()
        super().start_timer(stream_name=stream_name)

    def stop_timer(self,
                   stream_name: Optional[str] = 'standard',
                   ouput: Optional[bool] = False,
                   ret: Optional[bool] = False
                   ):
        self._synchronization_func()
        return super().stop_timer(stream_name=stream_name, ouput=ouput, ret=ret)
    
    def interval(self,
                 stream_name: Optional[str] = 'standard'
                 ):
        self._synchronization_func()
        super().interval(stream_name=stream_name)