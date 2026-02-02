from config.fileControl import update, read
import json

def test_update_and_read(tmp_path):
    """ Testa as funções de leitura e atualização do arquivo json """
    test_data = {
        "temperature": {
            "code": "T",
            "intervals": 200,
            "levels":{
                "max": 30,
                "min": 10
            },
            "actions":{
                "get_value": ""
            }
        }
    }
    file_path = tmp_path / 'test_moduleConfig.json'

    update(file_path, test_data)
    data = read(file_path)

    assert file_path.exists()
    assert data == test_data
