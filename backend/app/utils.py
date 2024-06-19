import asyncio
from concurrent.futures import ThreadPoolExecutor

# decorator that turns sync func into async
def async_wrapper(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        ret = await loop.run_in_executor(None, func, *args, **kwargs)
        return ret
    return wrapper