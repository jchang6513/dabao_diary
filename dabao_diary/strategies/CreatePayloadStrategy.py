from dabao_diary.entity.MessageEntity import MessageEntity

class CreatePayloadStrategy():
  def __init__(self, user_id: str, reply_token: str, msg_entity: MessageEntity):
    self.user_id = user_id
    self.reply_token = reply_token
    self.msg_entity = msg_entity

  def generate_payload(self):
    pass
