class MessageEntity():
  def __init__(self, message):
    self.message = message

  def getType(self):
    return self.message['type']

  def getMessage(self):
    return self.message['text']
