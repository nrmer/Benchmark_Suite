from benchmark_suite.benchmark_timer import Benchmark_Timer
from benchmark_suite.synchronized_benchmark_timer import Synchronized_Benchmark_Timer
import time
from types import FunctionType
from typing import Optional, Callable

class Function_Benchmark(Benchmark_Timer):
    def __init__(self,
                 timer_func: Optional[Callable] = time.perf_counter_ns,
                 output_unit_conversion: Optional[int] = 1e-9,
                 output_unit: Optional[str] = 'seconds'
                 ):
        super().__init__(timer_func=timer_func,
                         output_unit_conversion=output_unit_conversion,
                         output_unit=output_unit)
        
    def _new_func(self, func_to_benchmark: Callable, *args, **kwargs):
        name = str(func_to_benchmark)
        print(name)
        if not name in self._time:
            self.create_timing_stream(stream_name=name)
        self.start_timer(stream_name=name)
        func_to_benchmark(*args, **kwargs)
        self.stop_timer(stream_name=name)
        print(self._time())

    def _wrapper_function(self, func_to_benchmark: Callable):
        print('hi')
        def wrapper(*args, **kwargs):
            return self._new_func(func_to_benchmark, *args, **kwargs)
        return wrapper

    def define_func_to_benchmark(self, func_to_benchmark: Callable):
        if isinstance(func_to_benchmark, FunctionType):
            return self._wrapper_function(func_to_benchmark)
        else:
            for attr_name, attr_value in func_to_benchmark.__class__.__dict__.items():
                if callable(attr_value):
                    setattr(func_to_benchmark.__class__, attr_name, self._wrapper_function(attr_value))



class Synchronized_Function_Benchmark(Synchronized_Benchmark_Timer):
    def __init__(self,
                 synchronization_func: Callable,
                 timer_func: Optional[Callable] = time.perf_counter_ns,
                 output_unit_conversion: Optional[int] = 1e-9,
                 output_unit: Optional[str] = 'seconds'
                 ):
        super().__init__(synchronization_func=synchronization_func,
                         timer_func=timer_func,
                         output_unit_conversion=output_unit_conversion,
                         output_unit=output_unit)
        
    def _new_func(self,
                  func_to_benchmark: Callable):
        name = str(func_to_benchmark)
        if not name in self._time:
            self.create_timing_stream(stream_name=name)
        self.start_timer(stream_name=name)
        func_to_benchmark()
        self.stop_timer(stream_name=name)

    def define_func_to_benchmark(self,
                                 func_to_benchmark: Callable):
        orig_func_to_benchmark = func_to_benchmark
        func_to_benchmark = self._new_func(func_to_benchmark=orig_func_to_benchmark)
