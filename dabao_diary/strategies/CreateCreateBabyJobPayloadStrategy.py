import json
from dabao_diary.enums.Command import Command
from dabao_diary.enums.ConfirmOption import Confirm
from dabao_diary.model.BabyList import BabyList
from dabao_diary.model.UserAction import UserAction
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateCreateBabyJobPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    message = self.msg_entity.getMessage()

    if (not UserAction.getUserAction(self.user_id).value):
      UserAction.getUserAction(self.user_id).setName(message)
      return self.getConfirmBabyJobPayload(message)

    if (message == Confirm.NO.value):
      return self.getResubmitPayload()

    name = UserAction.getUserAction(self.user_id).value
    UserAction.removeUserAction(self.user_id)

    if (name in BabyList.getList()):
      return self.getBabyAlreadyExistPayload(name)
    else:
      BabyList.createBaby(name)
      return self.getCreateBabyJobSuccessPayload(name)

  def getConfirmBabyJobPayload(self, name):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
            "type": "template",
            "altText": "this is a confirm template",
            "template": {
                "type": "confirm",
                "text": f"你是要新增'{name}'嗎?",
                "actions": [
                    {
                        "type": "message",
                        "label": Confirm.YES.value,
                        "text": Confirm.YES.value
                    },
                    {
                        "type": "message",
                        "label": Confirm.NO.value,
                        "text": Confirm.NO.value
                    }
                ]
            }
        }
      ]
    })

  def getBabyAlreadyExistPayload(self, name):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"'{name}'已存在"
        }
      ]
    })

  def getCreateBabyJobSuccessPayload(self, name):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"已新增寶寶: {name}"
        }
      ]
    })


  def getResubmitPayload(self):
    UserAction.getUserAction(self.user_id).setName(None)

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": "請重新輸入寶寶的名字",
        },
      ]
    })
