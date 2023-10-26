import asyncio
from typing import Any, Callable


def run_async_function(function: Callable, *args: Any) -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.create_task(function(*args))
    else:
        asyncio.run(function(*args))
