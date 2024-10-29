import requests
from github import Github
from pprint import pprint

print("Каким способом вы желаете авторизоваться? \n" 
      " 1 - Авторизация через логин \n"
      " 2 - Авторизация через логин и пароль \n"
      " 3 - Авторизация через токен доступа")
print(" Введите номер варианта авторизации (от 1-цы до 3-ех) или полность навзвание варианта")

var_aut = input()
access_token = "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"


login  = Github(access_token)


user  = login.get_user()

user_data = []
user_data.append(user.login)
user_data.append(user.public_repos)
user_data.append(user.owned_private_repos)
user_data.append(user.followers)
user_data.append(user.hireable)
for i in range (0, len(user_data), +1):
    print(user_data[i])

my_repos = user.get_repos()

for repository  in my_repos:
    name =  repository.name
    private,public = repository.private, not(repository.private)
    created_date = repository.created_at
    language = repository.language
    comit = repository.forks
    rrr = repository.stargazers_count
    print(name, private, public, created_date, language, comit, rrr)



