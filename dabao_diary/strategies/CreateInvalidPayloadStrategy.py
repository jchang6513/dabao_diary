import json
from dabao_diary.enums.Command import Command
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateInvalidPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": f"請輸入有效指令，可輸入'{Command.COMMAND_LIST.value}'已取得指令列表"
        }
      ]
    })
