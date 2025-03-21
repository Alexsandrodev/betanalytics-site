import json
from channels.generic.websocket import AsyncWebsocketConsumer




class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceita a conexão com o WebSocket
        await self.accept()


    async def disconnect(self, close_code):
        # Chamado quando a conexão é fechada
        pass

    
    async def receive(self, text_data):
        # Chamado quando uma mensagem é recebida
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Aqui você processa a mensagem recebida da API WebSocket
        # Exemplo: Imprimir no console
        print(f"Mensagem recebida: {message}")

        # Se precisar enviar uma resposta de volta:
        await self.send(text_data=json.dumps({
            'message': f'Mensagem recebida pelo servidor: {message}'
        }))