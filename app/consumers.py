# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class StockDataConsumer(WebsocketConsumer):
    def connect(self):
        self.symbol_name = self.scope['url_route']['kwargs']['symbol_name']
        self.symbol_group_name = 'data_%s' % self.symbol_name
        print("Group name: ", self.symbol_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.symbol_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.symbol_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json['data']
        print("Sending message: ", data)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.symbol_group_name,
            {
                'type': 'ohlc_data',
                'message': data
            }
        )

    # Receive message from room group
    def ohlc_data(self, event):
        data = event['data']
        # print("Sending data here: ", data)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data': data
        }))
