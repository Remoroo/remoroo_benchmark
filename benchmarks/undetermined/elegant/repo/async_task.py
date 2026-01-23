import asyncio
import functools
import time
from typing import Any, Callable, Coroutine, Protocol, TypeVar, runtime_checkable

# Generic type variables for type safety
T = TypeVar("T")
R = TypeVar("R")

@runtime_checkable
class TaskProtocol(Protocol):
    """Defines the structural contract for any processable task."""
    async def execute(self, data: Any) -> Any: ...

def trace_execution(func: Callable[..., Coroutine[Any, Any, R]]) -> Callable[..., Coroutine[Any, Any, R]]:
    """Decorator to measure execution latency using high-precision timers."""
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> R:
        start_ts = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_ts = time.perf_counter()
            print(f"[{func.__name__}] Latency: {end_ts - start_ts:.6f}s")
    return wrapper

class Registry(type):
    """Metaclass to automatically register specialized processing units."""
    _processors: dict[str, type] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "BaseProcessor":
            mcs._processors[name.lower()] = cls
        return cls

class BaseProcessor(metaclass=Registry):
    """Abstract base utilizing the Registry metaclass for auto-discovery."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

class ComputeNode(BaseProcessor):
    @trace_execution
    async def execute(self, val: int) -> int:
        # Simulating a non-blocking I/O bound compute
        await asyncio.sleep(0.5)
        return sum(i**2 for i in range(val))

class Orchestrator:
    """Manages the lifecycle and concurrent execution of registered nodes."""
    def __init__(self, inputs: list[int]):
        self.inputs = inputs
        self.results: list[Any] = []

    async def run_pipeline(self):
        # Dynamically instantiate nodes from the Registry
        nodes = [Registry._processors['computenode']() for _ in range(len(self.inputs))]
        
        # Dispatch tasks concurrently using a list comprehension over zip
        tasks = [node.execute(val) for node, val in zip(nodes, self.inputs)]
        
        print(f"Dispatching {len(tasks)} concurrent tasks...")
        self.results = await asyncio.gather(*tasks)
        return self.results

if __name__ == "__main__":
    data_stream = [100, 500, 1000]
    orchestrator = Orchestrator(data_stream)
    
    final_output = asyncio.run(orchestrator.run_pipeline())
    print(f"Pipeline Result: {final_output}")