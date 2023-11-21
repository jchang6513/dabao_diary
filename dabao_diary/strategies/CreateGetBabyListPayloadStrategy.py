import json
from dabao_diary.model.BabyList import BabyList
from dabao_diary.strategies.CreatePayloadStrategy import CreatePayloadStrategy

class CreateGetBabyListPayloadStrategy(CreatePayloadStrategy):
  def generate_payload(self):
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
