from dataclasses import dataclass
from typing import Coroutine


@dataclass()
class ScheduledJob:
    """
    A data class representing a scheduled job, containing a `payload` attribute
    that represents the parameters for the job and a `dst` attribute that is
    the coroutine that will be scheduled for execution.

    :param payload: A dictionary containing parameters for the job.
    :type payload: str
    :param dst: A coroutine that will be scheduled for execution.
    :type dst: Coroutine
    """

    payload: str
    dst: Coroutine
