# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dabao_diary.utils.MessageApi import MessageApi

class WebhookView(APIView):
    def get(self, request, *args, **kwargs):
        # Perform any necessary processing for the incoming webhook data here

        # Example: Log the request data
        print("Webhook Data:", request.data)

        # Your webhook processing logic goes here...

        # Return a success response
        response_data = {"success": True}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Perform any necessary processing for the incoming webhook data here

        # Example: Log the request data
        print("Webhook Data:", request.data)

        reply_token = request.data['events'][0]['replyToken']
        msg_type = request.data['events'][0]['message']['type']

        response_data = {"success": True}
        messageApi = MessageApi()
        messageApi.replyMessage(reply_token, msg_type, request)

        return Response(response_data, status=status.HTTP_200_OK)
