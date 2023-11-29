import json
from dabao_diary.model.ActionList import ActionList
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateGetActionListPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
    if not ActionList.getList():
      return json.dumps({
        "replyToken": self.reply_token,
        "messages": [
          {
            "type": "text",
            "text": "現在沒有建立任何動作",
          },
        ]
      })

    stringify_actions = "\n- ".join(ActionList.getList())
    result_string = f"已建立動作:\n- {stringify_actions}"

    return json.dumps({
      "replyToken": self.reply_token,
      "messages": [
        {
          "type": "text",
          "text": result_string,
        },
      ]
    })
