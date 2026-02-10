from unittest.mock import Mock, MagicMock, patch
from schedules.schedule import Schedule, Job
from pytest import fixture

@fixture
def fake_schedule():
    fake_checker = Mock()
    fake_checker.run.return_value = None
    return Schedule(fake_checker)

class TestSchedule:
    def test_contructor(self):
        """ Testa o contrutor da classe """
        fake_checker = Mock()
        schedule = Schedule(fake_checker)

        assert schedule.checker == fake_checker
        assert schedule.jobs == {}
        assert schedule.tasks == {}

    def test_new_job(self, fake_schedule):
        """ Testa se a função está criando, guardando e iniciado novos trabalhos """
        fake_schedule._start_new_task = Mock()
        fake_schedule.new_job('B', ['1', '0'], [100, 50])

        assert fake_schedule.jobs.get('B') != None
        fake_schedule._start_new_task.assert_called_once()

    def test_start_new_task(self, fake_schedule):
        """ Testa se está criando uma nova tarefa """
        # auxiliares para engolir a corotina quando 
        # chamada pelo create_task
        fake_task = MagicMock()
        def fake_task(coro):
            coro.close()
            return fake_task

        with patch("asyncio.create_task", side_effect=fake_task) as mock_create_task:
            # adiciona um novo trabalho ao mesmo tempo que cria uma task
            fake_schedule._start_new_task(
                Job(
                    module_code='B',
                    commands=['1', '0'],
                    intervals=[100, 50])
                )

            # verifica se as funções para criar a task foi chamada
            mock_create_task.assert_called_once()

            # verifica se a task foi guardada
            assert fake_schedule.tasks.get('B') != None
            assert fake_schedule.tasks.get('B') == fake_task

    def test_update_job_interval(self, fake_schedule):
        """ Testa se está atualizando o intervalo e se está atualizando a task """
        # iniciando dados fake
        task = Mock()
        job = Job(module_code='T', commands=[''], intervals=[100])

        fake_schedule.jobs['T'] = job
        fake_schedule.tasks['T'] = task
        fake_schedule._start_new_task = Mock()

        # atualizando intervalo para 50
        status_code = fake_schedule.update_job_interval('T', [50])
        assert status_code == True

        # verificando se alterou o intervalo e se atualizou a task
        assert job.intervals[0] == 50
        task.cancel.assert_called_once()
        fake_schedule._start_new_task.assert_called_once()

        # pendente: teste do loop de verificação