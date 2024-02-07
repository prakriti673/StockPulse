from django.urls import re_path

from . import consumers
# Working of channels and websockets
# websocket connection consists of group and channel
# channel is specific to the user who wants to make a websocket connection with the server and each user is assigned unique channel id
# all users with different channel ids are added in the group 
# after retrieving data, celery sends result in the group 
websocket_urlpatterns = [
    re_path(r'ws/stock/(?P<room_name>\w+)/$', consumers.StockConsumer.as_asgi()),
]
# websocket_urlpatterns = [
#     re_path(r'ws/stock/(?P<room_name>\w+)/\?stockpicker=.+', consumers.StockConsumer.as_asgi()),
# ]
