import json
from channels.generic.websocket import AsyncWebsocketConsumer
 
class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = 'stock_%s' % self.room_name

        # Join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type" : "stock_update",
                "message" : message
            }
        )
    
    # Celery sends results to the group where all users are connected
    # unique objects are created for each user
    # this function(stock_update) is called from the object  
    # this function then filters the stocks requested and sends it to the user
    async def stock_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                "message": message
            }
        ))