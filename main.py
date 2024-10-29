import requests
from github import Github
from pprint import pprint
from github import Auth

def take_data (user, var_aut):
    user_data = []
    user_data.append(user.login)
    user_data.append(user.public_repos)
    if var_aut != 1:
        user_data.append(user.owned_private_repos)
    user_data.append(user.followers)
    user_data.append(user.hireable)

    for i in range(0, len(user_data), +1):
        print(user_data[i])
    print(user.location)

    my_repos = user.get_repos()

    for repository in my_repos:
        name = repository.name
        private, public = repository.private, not (repository.private)
        created_date = repository.created_at
        language = repository.language
        comit = repository.forks
        rrr = repository.stargazers_count
        owner = repository.get_contributors()

        print(name, private, public, created_date, language, comit, rrr, *owner)

print("Каким способом вы желаете авторизоваться? \n" 
      " 1 - Авторизация через логин \n"
      " 2 - Авторизация через логин и пароль \n"
      " 3 - Авторизация через токен доступа")
var_aut  = input(" Введите номер варианта авторизации (от 1-цы до 3-ех) или полность навзвание варианта: ")

#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

if var_aut == "1":
    login = input(" Введите логин пользователя: ")
    g = Github()
    user = g.get_user(login)
    take_data(user, var_aut)

elif var_aut == "2":
    login= input(" Введите логин пользователя: ")
    password = input(" Введите пароль: " )
    auth = Auth.Login(login, password)
    g = Github(auth = auth)
    user = g.get_user()

    take_data(user, var_aut)

elif var_aut == "3":
    access_token = input(" Введите токен доступа пользователя: ")
    auth = Auth.Token(access_token)

    login = Github(auth = auth)
    user = login.get_user()

    take_data(user, var_aut)





