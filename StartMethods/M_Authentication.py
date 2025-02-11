from github import Github
from github import Auth

def Login (MyToken, loginUser):
    login = Github(MyToken)
    user = login.get_user(loginUser)
    return user

def LoginPassword(login, password):
    auth = Auth.Login(login, password)
    login = Github(auth=auth)
    user = login.get_user()
    return user

def LoginToken(access_token):
    auth = Auth.Token(access_token)
    login = Github(auth=auth)
    user = login.get_user()
    return user