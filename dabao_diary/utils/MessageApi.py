import requests
import json
from dabao_diary.constants import COMMAND_LIST, HEADERS, URL

from dabao_diary.entity.MessageEntity import MessageEntity
from dabao_diary.enums.Command import Command
from dabao_diary.enums.ConfirmOption import Confirm
from dabao_diary.model.BabyList import BabyList
from dabao_diary.model.UserAction import UserAction

class CreateBabyJob():
  name = ''
  value = ''

  def setName(self, name):
    self.value = name

class MessageApi():
  def __init__(self, user_id: str, reply_token: str, msg_entity: MessageEntity):
    self.user_id = user_id
    self.reply_token = reply_token
    self.msg_entity = msg_entity

  def replyMessage(self):
    payload = self.getPayload()
    response = requests.request("POST", URL, headers=HEADERS, data=payload)
    print(response.text)

  def getPayload(self):
    msg_type = self.msg_entity.getType()
    if msg_type == 'text':
      return self.getTextMsgPayload()
    else:
      return self.getInvalidPayload()

  def getTextMsgPayload(self):
    message = self.msg_entity.getMessage()

    if UserAction.isUserActionExist(self.user_id):
      if isinstance(UserAction.getUserAction(self.user_id), CreateBabyJob):
        return self.getCreateBabyJobPayload()

    # without job
    if message == Command.COMMAND_LIST.value:
      return self.getCommandListPayload()
    elif message == Command.ADD_BABY.value:
      return self.getAddBabyPayload()
    elif message == Command.BABY_LIST.value:
      return self.getBabyListPayload()
    else:
      return self.getInvalidPayload()

  def getCommandListPayload(self):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": COMMAND_LIST,
        },
      ]
    })

  def getAddBabyPayload(self):
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

  def getInvalidPayload(self):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"請輸入有效指令，可輸入'{Command.COMMAND_LIST.value}'已取得指令列表"
        }
      ]
    })

  def getCreateBabyJobPayload(self):
    message = self.msg_entity.getMessage()

    if (not UserAction.getUserAction(self.user_id).value):
      UserAction.getUserAction(self.user_id).setName(message)
      return self.getConfirmBabyJobPayload(message)

    if (message == Confirm.NO.value):
      return self.getAddBabyPayload()

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

  def getBabyListPayload(self):
    if not BabyList.getList():
      return json.dumps({
        "replyToken": self.reply_token,
        "messages": [
          {
            "type": "text",
            "text": "現在沒有寶寶",
          },
        ]
      })

    baby_string = "\n- ".join(BabyList.getList())
    result_string = f"我的寶寶:\n- {baby_string}"

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": result_string,
        },
      ]
    })
