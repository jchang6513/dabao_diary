import json
from dabao_diary.constants import COMMAND_LIST
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateCommandListPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": COMMAND_LIST,
        },
      ]
    })
