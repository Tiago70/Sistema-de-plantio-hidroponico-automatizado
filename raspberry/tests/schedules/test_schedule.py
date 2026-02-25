import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from schedules.schedule import TaskControl, JobData, Jobs, Schedule

@pytest.fixture
def schedule():
    checker = AsyncMock()
    schedule = Schedule(checker)

    return schedule

class TestTaskControl:
    @pytest.mark.asyncio
    async def test_constructor(self):
        task_control = TaskControl()
        assert task_control.task is None

    @pytest.mark.asyncio
    async def test_start_and_stop(self):
        task_control = TaskControl()

        async def fake_coro():
            await asyncio.sleep(0.01)

        task_control.start(fake_coro())

        assert task_control.task is not None
        assert not task_control.task.done()

        await task_control.stop()

        assert task_control.task is None

class TestJobData:
    def test_constructor(self):
        job = JobData("1", [1, 2, 3], False)

        assert job.command == "1"
        assert job.intervals == [1, 2, 3]
        assert job.is_linked is False
        assert job.task is None
        assert job.current_interval_index == 0
        assert job.last_run == 0

    def test_get_next_interval(self):
        job = JobData("1", [1, 2], False)

        assert job.get_next_interval() == 1
        assert job.current_interval_index == 1

        assert job.get_next_interval() == 2
        assert job.current_interval_index == 0  # loop circular

    def test_update_interval(self):
        job = JobData("1", [1, 2], False)
        job.current_interval_index = 1

        job.update_interval([5, 6])

        assert job.intervals == [5, 6]
        assert job.current_interval_index == 0

    def test_get_diff_interval(self):
        job = JobData("1", [10], False)

        job.last_run = 0
        diff = job.get_diff_interval()

        assert diff >= 0  # nunca negativo

class TestJobs:
    def test_constructor(self):
        jobs = Jobs()
        assert jobs.related_jobs == []

    def test_filter_jobs(self):
        j1 = JobData("A", [1], True)
        j2 = JobData("B", [1], False)
        j3 = JobData("C", [1], True)

        jobs = Jobs([j1, j2, j3])

        linked = jobs.filter_jobs(True)
        unlinked = jobs.filter_jobs(False)

        assert len(linked) == 2
        assert len(unlinked) == 1
        assert unlinked[0].command == "B"

class TestSchedule:
    def test_constructor(self):
        checker = Mock()
        schedule = Schedule(checker)

        assert schedule.checker == checker
        assert schedule.jobs == {}

    def test_new_job(self, schedule):
        schedule.new_job("B", "1", [1, 2], False)

        assert "B" in schedule.jobs
        assert len(schedule.jobs["B"].related_jobs) == 1

    @pytest.mark.asyncio
    async def test_update_job_interval_non_linked(self, schedule):
        schedule.new_job("T", "0", [1], False)
        job = schedule.jobs["T"].related_jobs[0]

        # mock task control
        job.task = TaskControl()
        job.task.start(asyncio.sleep(0.01))

        response = await schedule.update_job_interval(
            "T", "0", [5]
        )

        assert response.ok is True
        assert job.intervals == [5]

    @pytest.mark.asyncio
    async def test_update_job_not_found(self, schedule):
        response = await schedule.update_job_interval(
            "T", "", [5]
        )

        assert response.ok is False