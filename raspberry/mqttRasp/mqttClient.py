"""
Código resposável por manter uma conexão ativa com
o servidor mqtt, deve receber comandos e enviar
notificações do sistema
"""

from dataclasses import asdict
from mqttRasp.dispatcher import RequestDispatcher
import asyncio
import aiomqtt
import json
from schemas.response import (
    GetDataRequest,
    UpdateDataRequest,
    parse_request, 
    Response,
    Error
)

request = {
    'action': 'get',
    'targets': [
        'T',
        'C'
    ]
}

requests = {
    'action': 'set',
    'module': 'water_pump',
    'target': 'interval',
    'value': ''
}

class ClientRasp:
    def __init__(self, dispatcher: RequestDispatcher) -> None:
        self.dispatcher = dispatcher
        self.client = aiomqtt.Client()  # verificar de onde os dados virão

        # verficiar de onde os dados virão 
        self.requests_topic: str
        self.response_topic: str
        self.notification_topic: str

    async def execute(self, message: str):
        try:
            req = parse_request(json.loads(message))
            return await self.dispatcher.dispatch(req)

        except Exception as e:
            err_type = e.__class__.__name__
            message_err = e.__str__()

            response = Response(
                ok=False,
                payload='An error occurred while executing the command.',
                error=Error(err_type, message_err)
                )

            return response

    async def connect(self):
        while True:
            try:
                async with self.client as client:   
                    await client.subscribe(self.requests_topic)    # verirficar qual tópico se inscrever

                    # possível indicador de sucesso via led
                    async for mensage in client.messages:
                        response = await self.execute(mensage.payload.decode('utf-8'))
                        await self.client.publish(self.response_topic, payload=asdict(response))
            except:
                # possível indicador de erro via led
                await asyncio.sleep(5)  # se necessário, salvar o delay em arquivo

    async def notify(self, message: str):
        await self.client.publish(self.notification_topic, payload=message)