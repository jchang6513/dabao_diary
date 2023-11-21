import requests
from dabao_diary.constants import HEADERS, URL


class CreateBabyJob():
  name = ''
  value = ''

  def setName(self, name):
    self.value = name

class MessageApi():
  def replyMessage(self, payload: str):
    response = requests.request("POST", URL, headers=HEADERS, data=payload)
    print(response.text)
