import requests
import json
from django.conf import settings

url = "https://api.line.me/v2/bot/message/reply"

class MessageApi():
  def replyMessage(self, replyToken, msg_type, request):
    if msg_type == 'text':
      message = request.data['events'][0]['message']['text']
      payload = self.getTextMsgPayload(replyToken, message)
    elif msg_type == 'sticker':
      payload = self.getStickerMsgPayload(replyToken)
    else:
      # Handle other message types or set a default payload
      payload = self.getDefaultPayload(replyToken)

    headers = {
      'Authorization': 'Bearer ' + settings.ACCESS_TOKEN,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

  def getTextMsgPayload(self, replyToken, message):
    return json.dumps({
      "replyToken": replyToken,
      "messages": [
        {
          "type": "text",
          "text": "[測試]大寶日記"
        },
        {
          "type": "text",
          "text": "你輸入的是: " + message
        }
      ]
    })

  def getStickerMsgPayload(self, replyToken):
    return json.dumps({
      "replyToken": replyToken,
      "messages": [
        {
          "type": "text",
          "text": "[測試]大寶日記"
        },
        {
          "type": "text",
          "text": "我看不懂貼圖ＱＱ"
        }
      ]
    })

  def getDefaultPayload(self, replyToken):
    return json.dumps({
      "replyToken": replyToken,
      "messages": [
        {
          "type": "text",
          "text": "[測試]大寶日記"
        },
        {
          "type": "text",
          "text": "你傳什麼啊？"
        }
      ]
    })
