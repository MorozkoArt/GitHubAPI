from github import Github
from github import Auth

def login_auth (my_token, login_user):
    login = Github(my_token)
    user = login.get_user(login_user)
    return user

def login_password(login, password):
    auth = Auth.Login(login, password)
    login = Github(auth=auth)
    user = login.get_user()
    return user

def login_token(access_token):
    auth = Auth.Token(access_token)
    login = Github(auth=auth)
    user = login.get_user()
    return user