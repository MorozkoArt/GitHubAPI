import requests
import base64
import os
import tqdm
from github import Github
from pprint import pprint
from github import Auth
from g4f.client import Client



# Класс, который хранит основые поля пользователя
class User_GitHub:
    languages = []
    repos_user = []
    def __init__(self, name, followers, following, hireable, private_repos, public_repos, last_modified, created_at, plan, blog, repos ):
        total = (repos.totalCount+1)
        prbar = ProgressBar(total)
        self.name = name
        self.followers = followers
        self.following = following
        self.hireable = hireable
        self.private_repos = private_repos
        self.public_repos = public_repos
        self.last_modified = last_modified
        self.created_at = created_at
        self.plan = plan
        self.blog = blog
        self.repos = repos
        prbar.updatePd()
        for repo in self.repos:
            repo_user = User_repo(repo.name, repo.forks, repo.stargazers_count, repo.get_contributors().totalCount,
                                  repo.created_at,
                                  repo.last_modified_datetime, repo.get_commits().totalCount)
            self.repos_user.append(repo_user)
            prbar.updatePd()
            if repo.language not in self.languages:
                self.languages.append(repo.language)
        prbar.closePd()
    def Print_user_information(self):
        print("########################################################################################")
        print(f"Имя пользователя: {self.name} \n"
              f"Колличество подписчиков: {self.followers} \n"
              f"Колличество подписок: {self.following} \n"
              f"Доступность для найма: {self.hireable} \n"
              f"Колличество приватных репозиториев: {self.private_repos} \n"
              f"Колличество публичных репозиториев: {self.public_repos} \n"
              f"Дата создание аккаунта: {self.created_at}\n"
              f"Дата последнего изменения: {self.last_modified} \n"
              f"Подписка: {self.plan} \n"
              f"Ссылка на блог: {self.blog} \n"
              f"Языки программирования: " + ' '.join(map(str, self.languages)))
        print("########################################################################################")
        for i in range (len(self.repos_user)):
            print(f"Название репозитория {self.repos_user[i].name} \n"
                  f"Количество веток: {self.repos_user[i].forks} \n"
                  f"Колличество звезд: {self.repos_user[i].stargazers_count} \n"
                  f"Колличество контрибьютеров: {self.repos_user[i].contributors_count} \n"
                  f"Дата создания репозитория: {self.repos_user[i].created_at} \n"
                  f"Дата последнего изменения репозитория: {self.repos_user[i].last_date} \n"
                  f"Колличество коммитов внутри репозитория: {self.repos_user[i].commits}")
            print("/////////////////////////////////////////////////////////////////////////////////////////")



# Класс который хранит основные поля репозитория
class User_repo:
    def __init__(self, name, forks, stargazers_count, contributors_count, created_at, last_date, commits):
        self.name = name
        self.forks = forks
        self.stargazers_count = stargazers_count
        self.contributors_count = contributors_count
        self.created_at = created_at
        self.last_date = last_date
        self.commits = commits
        #self.content = content

# Класс, который выводит progressbar в консоль
class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.pd = tqdm.tqdm(
            desc="Загрузка данных о пользователе: ",
            total=self.total,
            miniters=1,
            ncols=100,
            unit='итерация',
            unit_scale=True,
            unit_divisor=1024,
        )
    def updatePd(self):
        self.pd.update(1)
    def closePd(self):
        self.pd.close()


def take_data (user):
    user_git = User_GitHub(user.login, user.followers, user.following, user.hireable, user.owned_private_repos, user.public_repos,
                           user.last_modified_datetime, user.created_at, user.plan, user.blog, user.get_repos())
    user_git.Print_user_information()

def evaluate_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"what is the future of the British monarchy"}],
        # Add any other necessary parameters
    )
    file.close()
    print(response.choices[0].message.content)


#######################  Main
file_path = r"C:\Users\Артём Морозов\source\repos\ClimbingTheHill\ClimbingTheHill\Program.cs"
evaluate_code(file_path)

print("Каким способом вы желаете авторизоваться? \n" 
      " 1 - Авторизация через логин \n"
      " 2 - Авторизация через логин и пароль \n"
      " 3 - Авторизация через токен доступа")
var_aut  = input(" Введите номер варианта авторизации (от 1-цы до 3-ех) или полность навзвание варианта: ")

#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

MyToken = "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"
if var_aut == "1":
    login = input(" Введите логин пользователя: ")
    try:
        g = Github(MyToken)
        user = g.get_user(login)
        take_data(user)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

elif var_aut == "2":
    login= input(" Введите логин пользователя: ")
    password = input(" Введите пароль: " )
    try:
        auth = Auth.Login(login, password)
        g = Github(auth=auth)
        user = g.get_user()
        take_data(user)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

elif var_aut == "3":
    access_token = input(" Введите токен доступа пользователя: ")
    try:
        auth = Auth.Token(access_token)
        login = Github(auth=auth)
        user = login.get_user()
        take_data(user)
    except Exception as e:
        print(f"Произошла ошибка: {e}")





