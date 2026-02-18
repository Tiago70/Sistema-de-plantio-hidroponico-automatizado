"""
Código responsável por realizar as medições e
regagens de forma periódica com base nos intervalos
definidos pelo arquivo de configurações

Deve se atualizar imediatamente após ocorrer alguma
alteração nos intervalos dos sensores
"""

from dataclasses import dataclass, field
from typing import Coroutine
from schemas.response import Response, Error
from schedules.checker import Checker
import time
import asyncio

@dataclass
class TaskControl:
    task: asyncio.Task | None = None

    def start(self, coro: Coroutine) -> None:
        if self.task and not self.task.done():
            raise RuntimeError("Task already running")

        self.task = asyncio.create_task(coro)

    async def stop(self) -> None:
        if self.task is None:
            return

        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass
        finally:
            self.task = None

@dataclass
class JobData:
    """ 
    armazena as informações necessárias para executar
    um trabalho em loop, além de funções utilitárias 
    """
    command: str
    intervals: list[int]
    is_linked: bool

    task: TaskControl | None = None
    last_run: float = field(default=0, init=False)
    current_interval_index: int = field(default=0, init=False)

    def get_next_interval(self) -> int:
        current_interval = self.intervals[self.current_interval_index]

        self.current_interval_index = (
            (self.current_interval_index + 1) % len(self.intervals)
        )
        return current_interval

    def update_interval(self, intervals: list[int]):
        self.current_interval_index = 0
        self.intervals = intervals

    def get_diff_interval(self) -> float:
        diff = self.last_run + self.intervals[self.current_interval_index] - time.monotonic()
        if diff < 0:
            diff = 0

        return diff
        
@dataclass
class Jobs:
    """
    encapsula todos os trabalhos relacionados à um
    módulo em um único lugar
    """
    related_jobs: list[JobData] = field(default_factory=list)

    def filter_jobs(self, linked: bool) -> list[JobData]:
        job_list: list[JobData] = []

        for job in self.related_jobs:
            if job.is_linked == linked:
                job_list.append(job)

        return job_list

class Schedule:
    def __init__(self, checker: Checker) -> None:
        self.checker = checker
        self.jobs: dict[str, Jobs] = {}

    async def _job_linked_loop(
        self,
        module_code,
        jobs: list[JobData],
        special_break: float = 0
    ) -> None:
        if special_break != 0:
            await asyncio.sleep(special_break)
        
        while True:
            for step in jobs:
                await self.checker.run(module_code, step.command)
                step.last_run = time.monotonic()

                await asyncio.sleep(step.get_next_interval())

    async def _job_loop(
        self,
        module_code: str,
        job_data: JobData,
        special_break: float = 0
    ) -> None:
        if special_break != 0:
            await asyncio.sleep(special_break)

        while True:
            await self.checker.run(module_code, job_data.command)
            job_data.last_run = time.monotonic()

            await asyncio.sleep(job_data.get_next_interval())

    def _start_task(self, module_code, job: JobData):
        task_control = TaskControl()
        task_control.start(self._job_loop(module_code, job))

        job.task = task_control

    def _start_linked_task(self, module_code, jobs: list[JobData]):
        task_control = TaskControl()
        task_control.start(self._job_linked_loop(module_code, jobs))
        
        for linked_job in jobs:
            linked_job.task = task_control
            
    def start_tasks(self):
        for module, jobs in self.jobs.items():
            linked_jobs_list: list[JobData] = []
            for job in jobs.related_jobs:
                if job.is_linked:
                    linked_jobs_list.append(job)
                    continue

                self._start_task(module, job)

            if not linked_jobs_list:
               continue

            self._start_linked_task(module, linked_jobs_list)

    def new_job(
        self,
        module_code: str,
        command: str,
        intervals: list[int],
        linked: bool = False
    ) -> None:
        job_dt = JobData(command, intervals, linked)
        jobs = self.jobs.get(module_code)

        if jobs is None:
            jobs = Jobs()
            self.jobs[module_code] = jobs
        
        jobs.related_jobs.append(job_dt)

    async def update_job_interval(self, module_code: str, command: str, intervals: list[int]) -> Response:
        module_jobs = self.jobs.get(module_code)

        if module_jobs is None:
            return Response(
                ok=False,
                payload='Module not found',
                error=Error(
                    err_type='Incorrect module',
                    cause='The specified module code was not found.'
                )
            )
        
        for job in module_jobs.related_jobs:
            if job.command == command:
                await job.task.stop()
                job.update_interval(intervals)

                if job.is_linked:
                    job.task.start(
                        self._job_linked_loop(
                            module_code,
                            module_jobs.filter_jobs(linked=True),
                            job.get_diff_interval()
                    )
                )
                else:
                    job.task.start(
                        self._job_loop(
                            module_code,
                            job,
                            job.get_diff_interval()
                        )
                    )

                return Response(
                    ok=True,
                    payload='OK'
                )

        return Response(
            ok=False,
            payload='Command not found',
            error=Error(
                err_type='Incorrect command',
                cause='The specified command was not found.'
            )
        )
                