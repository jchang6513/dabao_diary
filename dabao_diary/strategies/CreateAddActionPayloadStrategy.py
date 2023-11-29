import json
from dabao_diary.model.UserAction import UserAction
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy
from dabao_diary.utils.CreateActionJob import CreateActionJob

class CreateAddActionPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    UserAction.setUserAction(self.user_id, CreateActionJob())

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": "請輸入動作",
        },
      ]
    })
