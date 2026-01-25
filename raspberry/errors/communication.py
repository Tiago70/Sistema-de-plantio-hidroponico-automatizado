from errors.base import HydroponicsException

class ArduinoCommunicationException(HydroponicsException):
    """ Para erros genéricos de comunicação com o arduino """
    pass

class NoResponseException(ArduinoCommunicationException):
    """ Para erros de comunicação sem resposta do arduino """
    pass

class TimeoutException(ArduinoCommunicationException):
    """ Para erros de comunicação onde a mensagem não está completa """
    pass