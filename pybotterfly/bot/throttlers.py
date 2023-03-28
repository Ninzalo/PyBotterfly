import functools
import asyncio
from typing import Coroutine, Literal


def throttler_decorator(
    delay: float,
    measure: Literal["end_to_start", "start_to_start"] = "start_to_start",
):
    delay = delay + 0.0001

    def decorator(actual_func: Coroutine) -> Coroutine:
        queue = None

        async def _single_query(future, args, kwargs):
            try:
                result = await actual_func(*args, **kwargs)
            except Exception as err:
                future.set_exception(err)
            else:
                future.set_result(result)

        async def _work_loop():
            nonlocal queue
            while True:
                try:
                    future, args, kwargs = await asyncio.wait_for(
                        queue.get(), delay
                    )
                except asyncio.TimeoutError:
                    queue = None
                    return
                task = _single_query(future, args, kwargs)
                if measure == "start_to_start":
                    asyncio.create_task(task)
                else:
                    await task
                queue.task_done()
                await asyncio.sleep(delay)

        @functools.wraps(actual_func)
        async def query(*args, **kwargs):
            nonlocal queue
            future = asyncio.Future()
            if queue is None:
                queue = asyncio.Queue()
                asyncio.create_task(_work_loop())
            await queue.put((future, args, kwargs))
            return await future

        return query

    return decorator


class ThrottledResource:
    """
    A class for throttling the usage of a resource.

    This class can be used to limit the rate at which a coroutine that
    consumes a resource is executed.

    :param delay: The minimum amount of time (in seconds) that should pass
        between executions of the throttled coroutine.
    :type delay: float

    :param func_to_throttle: The coroutine function that needs to be throttled.
    :type func_to_throttle: Coroutine

    :ivar _delay: The delay between executions of the coroutine.
    :ivar _func: The coroutine function to throttle.
    :ivar _queue: A queue that stores the parameters for the throttled coroutine.
    :ivar _task: The asyncio task that runs the throttled coroutine.

    :returns: None
    :rtype: NoneType

    Methods:
        __init__(self, delay: float, func_to_throttle: Coroutine): Instantiates
            a new ThrottledResource object.
        start(self): Starts the work loop task.
        stop(self): Stops the work loop task.
        query(self, params): Adds a new request to the queue and returns
            the result.
        _single_response(self, params, future): Processes a single response
            received from the queue.
        _work_loop(self): Executes a loop that waits for incoming requests
            from the queue and passes them to _single_response().
    """

    def __init__(self, delay: float, func_to_throttle: Coroutine):
        """
        Initialises a ThrottledResource instance.

        :param delay: The time delay (in seconds) between queries.
        :type delay: float

        :param func_to_throttle: The coroutine function to be throttled.
        :type func_to_throttle: Coroutine

        :returns: None
        :rtype: NoneType
        """
        self._delay = delay + 0.0001
        self._func = func_to_throttle
        self._queue = asyncio.Queue()
        self._task = None

    def start(self):
        """
        Starts the work loop task.
        """
        self._task = asyncio.create_task(self._work_loop())

    def stop(self):
        """
        Stops the work loop task.
        """
        self._task.cancel()
        self._task = None

    async def query(self, params):
        """
        Queries the throttled resource with the given parameters.

        :param params: The parameters to pass to the throttled function.
        :type params: Any

        :returns: The result of the throttled function.
        :rtype: Any
        """
        future = asyncio.Future()
        await self._queue.put((future, params))
        result = await future
        return result

    async def _single_response(self, params, future):
        """
        Processes a single response received from the queue.

        Args:
            params: The parameters to pass to the throttled function.
            future: The future object to set with the result of the throttled
                function call.
        """
        try:
            result = await self._func(params)
        except Exception as err:
            future.set_exception(err)
        else:
            future.set_result(result)

    async def _work_loop(self):
        """
        Executes a loop that waits for incoming requests from the queue
        and passes them to _single_response().
        """
        while True:
            future, params = await self._queue.get()
            asyncio.create_task(self._single_response(params, future))
            self._queue.task_done()
            await asyncio.sleep(self._delay)
