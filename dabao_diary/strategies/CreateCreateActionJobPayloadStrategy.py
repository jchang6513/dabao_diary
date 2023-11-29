import json
from dabao_diary.enums.ConfirmOption import Confirm
from dabao_diary.model.ActionList import ActionList
from dabao_diary.model.UserAction import UserAction
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateCreateActionJobPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    message = self.msg_entity.getMessage()

    if (not UserAction.getUserAction(self.user_id).value):
      UserAction.getUserAction(self.user_id).setValue(message)
      return self.getConfirmBabyJobPayload(message)

    if (message == Confirm.NO.value):
      return self.getResubmitPayload()

    action = UserAction.getUserAction(self.user_id).value
    UserAction.removeUserAction(self.user_id)

    if (action in ActionList.getList()):
      return self.getBabyAlreadyExistPayload(action)
    else:
      ActionList.createAction(action)
      return self.getCreateBabyJobSuccessPayload(action)

  def getConfirmBabyJobPayload(self, action):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
            "type": "template",
            "altText": "this is a confirm template",
            "template": {
                "type": "confirm",
                "text": f"你是要新增'{action}'嗎?",
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

  def getBabyAlreadyExistPayload(self, action):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"'{action}'已存在"
        }
      ]
    })

  def getCreateBabyJobSuccessPayload(self, action):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"已新增動作: {action}"
        }
      ]
    })


  def getResubmitPayload(self):
    UserAction.getUserAction(self.user_id).setValue(None)

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": "請重新輸入動作",
        },
      ]
    })
