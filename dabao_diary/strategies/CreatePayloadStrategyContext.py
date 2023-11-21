from setuptools import Command
from dabao_diary.entity.MessageEntity import MessageEntity
from dabao_diary.model.UserAction import UserAction
from dabao_diary.strategies.CreateAddBabyPayloadStrategy import CreateAddBabyPayloadStrategy
from dabao_diary.strategies.CreateCreateBabyJobPayloadStrategy import CreateCreateBabyJobPayloadStrategy
from dabao_diary.strategies.CreateCommandListPayloadStrategy import CreateCommandListPayloadStrategy
from dabao_diary.strategies.CreateGetBabyListPayloadStrategy import CreateGetBabyListPayloadStrategy
from dabao_diary.strategies.CreateInvalidPayloadStrategy import CreateInvalidPayloadStrategy

from dabao_diary.entity.MessageEntity import MessageEntity
from dabao_diary.enums.Command import Command
from dabao_diary.model.UserAction import UserAction
from dabao_diary.utils.MessageApi import CreateBabyJob

class CreatePayloadStrategyContext():
  strategy = None

  def __init__(self, user_id: str, reply_token: str, msg_entity: MessageEntity):
    self.user_id = user_id
    self.reply_token = reply_token
    self.msg_entity = msg_entity

  def execute_strategy(self):
    msg_type = self.msg_entity.getType()

    if msg_type == 'text':
      self.getTextMsgStrategy()
    else:
      self.strategy = CreateInvalidPayloadStrategy

    return self.strategy(self.user_id, self.reply_token, self.msg_entity).generate_payload()

  def getTextMsgStrategy(self):
    message = self.msg_entity.getMessage()

    if UserAction.isUserActionExist(self.user_id):
      if isinstance(UserAction.getUserAction(self.user_id), CreateBabyJob):
        self.strategy = CreateCreateBabyJobPayloadStrategy

    # without job
    elif message == Command.COMMAND_LIST.value:
      self.strategy = CreateCommandListPayloadStrategy

    elif message == Command.ADD_BABY.value:
      self.strategy = CreateAddBabyPayloadStrategy

    elif message == Command.BABY_LIST.value:
      self.strategy = CreateGetBabyListPayloadStrategy

    else:
      self.strategy = CreateInvalidPayloadStrategy
