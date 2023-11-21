from django.conf import settings

from dabao_diary.entity.MessageEntity import MessageEntity
from dabao_diary.enums.Command import Command

URL = "https://api.line.me/v2/bot/message/reply"

HEADERS = {
  'Authorization': 'Bearer ' + settings.ACCESS_TOKEN,
  'Content-Type': 'application/json'
}

COMMAND_LIST = f"""指令列表
- {Command.BABY_LIST.value}
- {Command.ACTION_LIST.value}
- {Command.EVENT_QUERY.value}
- {Command.ADD_BABY.value}
- {Command.ADD_ACTION.value}
- {Command.ADD_EVENT.value}
"""
