from pytest import fixture
from config.schemaControl import SchemaControl

@fixture
def fake_schemacontrol(fake_dataclass):
    return SchemaControl(fake_dataclass)

class TestSchemaControl:
    def test_set_max_value(self, fake_schemacontrol):
        fake_schemacontrol.set_max_value('T', 100)
        assert fake_schemacontrol.dataclass.temperature.get('levels').get('max') == 100

        fake_schemacontrol.set_max_value('C', 100)
        assert fake_schemacontrol.dataclass.conductivity.get('levels').get('max') == 100

    def test_set_min_value(self, fake_schemacontrol):
        fake_schemacontrol.set_min_value('T', 50)
        assert fake_schemacontrol.dataclass.temperature.get('levels').get('min') == 50

        fake_schemacontrol.set_min_value('C', 50)
        assert fake_schemacontrol.dataclass.conductivity.get('levels').get('min') == 50

    def test_set_interval(self, fake_schemacontrol):
        fake_schemacontrol.set_interval('T', 1000)
        assert fake_schemacontrol.dataclass.temperature.get('intervals') == 1000

        fake_schemacontrol.set_interval('C', 500)
        assert fake_schemacontrol.dataclass.conductivity.get('intervals') == 500

        fake_schemacontrol.set_interval('B', 250)
        assert fake_schemacontrol.dataclass.water_pump.get('intervals') == 250