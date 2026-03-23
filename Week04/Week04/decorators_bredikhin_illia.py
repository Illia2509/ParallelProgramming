import time
import tracemalloc


def track_performance(func):
    """
    Decorator for measuring execution stats of a function.
    """

    stats = {
        "calls": 0,
        "time_sum": 0.0,
        "memory_sum": 0
    }

    def inner(*args, **kwargs):
        tracemalloc.start()

        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start

        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        stats["calls"] += 1
        stats["time_sum"] += duration
        stats["memory_sum"] += peak_memory

        return result

    inner.stats = stats  

    return inner
