# import asyncio
# import ssl
# import aiomqtt

# user = {
#     'hostname': '950515519b5d4279b125f18156ed2554.s1.eu.hivemq.cloud',
#     'port': 8883,
#     'username': 'raspberry',
#     'password': 'Tiago123',
#     'tls_context': ssl.create_default_context()
# }

# async def main():
#     async with aiomqtt.Client(**user) as client:
#         print(client._hostname)
#         print(client._port)

#         await client.subscribe('teste') 
#         async for message in client.messages:
#             print('mensagem recebida')
#             print(message.payload.decode('utf-8'))

# asyncio.run(main())

import json

teste = '[1, 2]'

print(json.loads(teste))