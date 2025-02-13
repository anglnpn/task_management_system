import asyncio
from typing import Coroutine, Any


def run_async(coroutine: Coroutine) -> Any:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(coroutine, loop)
        return future.result()

    return loop.run_until_complete(coroutine)
