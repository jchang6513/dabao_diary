USER_ACTION = {}

class UserAction():
  def isUserActionExist(user_id: str):
    return user_id in USER_ACTION

  def getUserAction(user_id: str):
    return USER_ACTION[user_id]

  def setUserAction(user_id: str, action):
    USER_ACTION[user_id] = action

  def removeUserAction(user_id: str):
    return USER_ACTION.pop(user_id, None)
