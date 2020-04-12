import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WizardConsumer(WebsocketConsumer):

    def connect(self):
        self.name = self.scope['url_route']['kwargs']['name']
        self.group_name = 'wizard_%s' % self.name

        print(self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    def game_message(self, event):
        message = event['message']
        print(self.group_name, "->", message)

        self.send(text_data=json.dumps({
            'message': message
        }))
