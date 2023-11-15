import requests
import json
from django.conf import settings

from dabao_diary.entity.MessageEntity import MessageEntity

URL = "https://api.line.me/v2/bot/message/reply"

HEADERS = {
  'Authorization': 'Bearer ' + settings.ACCESS_TOKEN,
  'Content-Type': 'application/json'
}

class Command:
  BABY_LIST = '我的寶寶'
  ACTION_LIST = '動作列表'
  EVENT_QUERY = '事件查詢'
  ADD_BABY = '新增寶寶'
  ADD_ACTION = '新增動作'
  ADD_EVENT = '新增事件'
  COMMAND_LIST = '查詢指令'

COMMAND_LIST = f"""指令列表
- {Command.BABY_LIST}
- {Command.ACTION_LIST}
- {Command.EVENT_QUERY}
- {Command.ADD_BABY}
- {Command.ADD_ACTION}
- {Command.ADD_EVENT}
"""

BABY_LIST = []

class Action:
  CREATE_BABY = 'CREATE_BABY'
  CREATE_ACTION = 'CREATE_ACTION'

USER_ACTION = {}

class CreateBabyJob():
  name = ''

  def setName(self, name):
    self.name = name

class Confirm():
  yes = '是'
  no = '否'

class MessageApi():
  def __init__(self, user_id: str, reply_token: str, msg_entity: MessageEntity):
    self.user_id = user_id
    self.reply_token = reply_token
    self.msg_entity = msg_entity

  def replyMessage(self):
    payload = self.getPayload()
    response = requests.request("POST", URL, headers=HEADERS, data=payload)
    print(response.text)
    print(USER_ACTION)

  def getPayload(self):
    msg_type = self.msg_entity.getType()
    if msg_type == 'text':
      return self.getTextMsgPayload()
    else:
      return self.getInvalidPayload()

  def getTextMsgPayload(self):
    message = self.msg_entity.getMessage()

    if self.user_id in USER_ACTION:
      if isinstance(USER_ACTION[self.user_id], CreateBabyJob):
        return self.getCreateBabyJobPayload()

    # without job
    if message == Command.COMMAND_LIST:
      return self.getCommandListPayload()
    elif message == Command.ADD_BABY:
      return self.getAddBabyPayload()
    elif message == Command.BABY_LIST:
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
    USER_ACTION[self.user_id] = CreateBabyJob()

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
          "text": f"請輸入有效指令，可輸入'{Command.COMMAND_LIST}'已取得指令列表"
        }
      ]
    })

  def getCreateBabyJobPayload(self):
    message = self.msg_entity.getMessage()

    if (not USER_ACTION[self.user_id].name):
      USER_ACTION[self.user_id].setName(message)
      return self.getConfirmBabyJobPayload(message)

    if (message == Confirm.no):
      return self.getAddBabyPayload()

    name = USER_ACTION[self.user_id].name
    USER_ACTION.pop(self.user_id, None)

    if (name in BABY_LIST):
      return self.getBabyAlreadyExistPayload(name)
    else:
      BABY_LIST.append(name)
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
                        "label": Confirm.yes,
                        "text": Confirm.yes
                    },
                    {
                        "type": "message",
                        "label": Confirm.no,
                        "text": Confirm.no
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
    if not BABY_LIST:
      return json.dumps({
        "replyToken": self.reply_token,
        "messages": [
          {
            "type": "text",
            "text": "現在沒有寶寶",
          },
        ]
      })

    baby_string = "\n- ".join(BABY_LIST)
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
