# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dabao_diary.entity.MessageEntity import MessageEntity
from dabao_diary.strategies.CreatePayloadStrategyContext import CreatePayloadStrategyContext
from dabao_diary.utils.MessageApi import MessageApi

class WebhookView(APIView):
    def get(self, request, *args, **kwargs):
        response_data = {"success": True}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data['events'][0]['source']['userId']
        reply_token = request.data['events'][0]['replyToken']
        msg_entity = MessageEntity(request.data['events'][0]['message'])

        response_data = {"success": True}
        context = CreatePayloadStrategyContext(user_id, reply_token, msg_entity)
        payload = context.execute_strategy()
        MessageApi().replyMessage(payload)

        return Response(response_data, status=status.HTTP_200_OK)
