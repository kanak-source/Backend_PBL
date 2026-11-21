from fastapi import FastAPI
import psutil
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import tracemalloc
import statistics

app = FastAPI(
    title="Performance Profiling Dashboard",
    description="A practical project for identifying CPU and memory bottlenecks",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

import time
import cProfile
import pstats
import io

def memory_heavy_task():
    # Intentionally creates a large list in memory
    data = [i * i for i in range(2_000_000)]

    total = sum(data)

    return total


@app.get("/profile/memory")
def profile_memory():

    tracemalloc.start()

    start_time = time.perf_counter()

    result = memory_heavy_task()

    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "test": "Memory Profiling",
        "execution_time_seconds": round(end_time - start_time, 4),
        "peak_memory_mb": round(peak / (1024 * 1024), 2),
        "bottleneck": "Large list stores all calculated values in memory",
        "result": result
    }

def slow_cpu_task():
    total = 0

    for i in range(5_000_000):
        # Inefficient:
        # the same multiplication is performed repeatedly
        if (i * i) % 2 == 0:
            total += i * i
        else:
            total -= i * i

    return total


def optimized_cpu_task():
    total = 0

    for i in range(5_000_000):
        # Optimized:
        # calculate the square once and reuse it
        square = i * i

        if square % 2 == 0:
            total += square
        else:
            total -= square

    return total

@app.get("/profile/cpu")
def profile_cpu():

    profiler = cProfile.Profile()

    start_time = time.perf_counter()

    profiler.enable()
    result = slow_cpu_task()
    profiler.disable()

    end_time = time.perf_counter()

    stream = io.StringIO()

    stats = pstats.Stats(
        profiler,
        stream=stream
    ).sort_stats("cumulative")

    stats.print_stats(10)

    return {
        "test": "CPU Profiling",
        "execution_time_seconds": round(end_time - start_time, 4),
        "result": result,
        "bottleneck": "slow_cpu_task",
        "profile": stream.getvalue()
    }

@app.get("/profile/cpu/optimized")
def profile_cpu_optimized():

    profiler = cProfile.Profile()

    start_time = time.perf_counter()

    profiler.enable()
    result = optimized_cpu_task()
    profiler.disable()

    end_time = time.perf_counter()

    stream = io.StringIO()

    stats = pstats.Stats(
        profiler,
        stream=stream
    ).sort_stats("cumulative")

    stats.print_stats(10)

    return {
        "test": "Optimized CPU Profiling",
        "execution_time_seconds": round(end_time - start_time, 4),
        "result": result,
        "status": "optimized",
        "profile": stream.getvalue()
    }

def memory_optimized_task():
    # Generator: values are produced one at a time
    # instead of storing 2,000,000 values in a list
    total = sum(i * i for i in range(2_000_000))
    return total


@app.get("/profile/memory/optimized")
def profile_memory_optimized():

    tracemalloc.start()

    start_time = time.perf_counter()

    result = memory_optimized_task()

    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "test": "Optimized Memory Profiling",
        "execution_time_seconds": round(end_time - start_time, 4),
        "peak_memory_mb": round(peak / (1024 * 1024), 2),
        "optimization": "Generator processes values without storing the complete list",
        "result": result
    }

@app.get("/profile/cpu/compare")
def compare_cpu():

    runs = 5
    slow_times = []
    optimized_times = []

    slow_result = None
    optimized_result = None

    for _ in range(runs):
        start = time.perf_counter()
        slow_result = slow_cpu_task()
        slow_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        optimized_result = optimized_cpu_task()
        optimized_times.append(time.perf_counter() - start)

    slow_average = statistics.mean(slow_times)
    optimized_average = statistics.mean(optimized_times)

    improvement = (
        (slow_average - optimized_average)
        / slow_average
        * 100
    )

    return {
        "test": "CPU Performance Comparison",
        "runs": runs,
        "same_result": slow_result == optimized_result,
        "slow_average_seconds": round(slow_average, 4),
        "optimized_average_seconds": round(optimized_average, 4),
        "improvement_percent": round(improvement, 2)
    }