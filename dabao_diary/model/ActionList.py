ACTION_LIST = []

class ActionList():
  def getList():
    return ACTION_LIST

  def createAction(action: str):
    ACTION_LIST.append(action)
