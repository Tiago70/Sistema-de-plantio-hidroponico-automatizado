"""
Código responsável por realizar as medições e
regagens de forma periódica com base nos intervalos
definidos pelo arquivo de configurações

Deve se atualizar imediatamente após ocorrer alguma
alteração nos intervalos dos sensores
"""

from dataclasses import dataclass, field
from schedules.checker import Checker
import time
import asyncio

@dataclass
class Job:
    module_code: str
    commands: list[str]
    intervals: list[int]
    last_run: float = field(default_factory=time.monotonic)

class Schedule:
    def __init__(self, checker: Checker) -> None:
        self.checker = checker
        self.jobs: dict[str, Job] = {}
        self.tasks: dict[str, asyncio.Task] = {}

    async def _job_loop(self, job: Job, special_break: int = 0):
        try:
            current_command = 0
            current_interval = 0

            if special_break != 0:
                await asyncio.sleep(special_break)

            while True:
                await asyncio.to_thread(
                    self.checker.run,
                    job.module_code,
                    job.commands[current_command]
                )
                job.last_run = time.monotonic()

                current_command = (current_command + 1) % len(job.commands)

                await asyncio.sleep(job.intervals[current_interval])
                current_interval = (current_interval + 1) % len(job.intervals)

        except asyncio.CancelledError:
            # erro esperado durante a alteração do intervalo
            pass

    def _start_new_task(self, job: Job, special_break: int = 0):
        self.tasks[job.module_code] = asyncio.create_task(self._job_loop(job, special_break))

    def new_job(self, module_code: str, commands: list[str], intervals: list[int]):
        # possivel veriricacão em commands e intervals para 
        # garantir que eles não venham vazios e acabar
        # desencadeando um erro de divisao por 0
        self.jobs[module_code] = Job(module_code, commands, intervals)
        self._start_new_task(self.jobs[module_code])

    def update_job_interval(self, module_code: str, intervals: list[int]) -> bool:
        task = self.tasks.get(module_code)
        job = self.jobs.get(module_code)

        if task is None or job is None:
            return False

        task.cancel()

        job.intervals = intervals
        diff = job.last_run + job.intervals[0] - time.monotonic()
        if diff < 0:
            diff = 0
        self._start_new_task(job, diff)

        return True