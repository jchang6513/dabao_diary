import json
from dabao_diary.model.UserAction import UserAction
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy
from dabao_diary.utils.MessageApi import CreateBabyJob

class CreateAddBabyPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    UserAction.setUserAction(self.user_id, CreateBabyJob())

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": "請輸入寶寶的名字",
        },
      ]
    })
