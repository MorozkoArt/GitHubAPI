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
    def __init__(self, name, followers, following, hireable, private_repos, public_repos,
                 updated_at, created_at, plan, blog, repos, company, org):
        total = (repos.totalCount+1)
        prbar = ProgressBar(total)
        self.name = name
        self.followers = followers
        self.following = following
        self.hireable = hireable
        self.private_repos = private_repos
        self.public_repos = public_repos
        self.updated_at = updated_at
        self.created_at = created_at
        self.plan = plan
        self.blog = blog
        self.repos = repos
        self.company = company
        self.org = [org_.login for org_ in org]
        prbar.updatePd()
        for repo in self.repos:
            repo_user = User_repo(repo.name, repo.language, repo.forks, repo.stargazers_count, repo.get_contributors().totalCount,
                                  repo.created_at,
                                  repo.updated_at, repo.get_commits().totalCount)
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
              f"Дата последнего изменения: {self.updated_at} \n"
              f"Подписка: {self.plan} \n"
              f"Ссылка на блог: {self.blog} \n"
              f"Компания: {self.company} \n"
              f"Организации: " + ' '.join(map(str, self.org)) + "\n"
              f"Языки программирования: " + ' '.join(map(str, self.languages)))
        print("########################################################################################")
        for i in range (len(self.repos_user)):
            print(f"Название репозитория {self.repos_user[i].name} \n"
                  f"Язык программированния {self.repos_user[i].language} \n"
                  f"Количество веток: {self.repos_user[i].forks} \n"
                  f"Колличество звезд: {self.repos_user[i].stargazers_count} \n"
                  f"Колличество контрибьютеров: {self.repos_user[i].contributors_count} \n"
                  f"Дата создания репозитория: {self.repos_user[i].created_at} \n"
                  f"Дата последнего изменения репозитория: {self.repos_user[i].last_date} \n"
                  f"Колличество коммитов внутри репозитория: {self.repos_user[i].commits}")
            print("/////////////////////////////////////////////////////////////////////////////////////////")



# Класс который хранит основные поля репозитория
class User_repo:
    def __init__(self, name, language, forks, stargazers_count, contributors_count, created_at, last_date, commits):
        self.name = name
        self.language = language
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

class ProfileAssessment:
    #Коэффициенты для оценки профиля
    coefficient_followers = 1.5
    coefficient_following = 0.5
    coefficient_hireable = 0.6
    coefficient_private_repos = 2.5
    coefficient_public_repos = 2.3
    coefficient_created_update = 0.6
    coefficient_plan = 5.0
    coefficient_blog = 0.3
    coefficient_company = 10.0
    coefficient_org = 1.4
    coefficient_languages = 4.1
    #Коэффициенты для оценки репозиториев
    coefficient_forks = 1.7
    coefficient_stargazers_count = 1.5
    coefficient_contributors_count = 0.9
    coefficient_created_update_r = 0.6
    coefficient_commits = 0.2
    def __init__(self, user):
        self.user = user
    def assessment_profile(self):
        assessment = (self.coefficient_followers*int(self.user.followers)
                      + self.coefficient_following*int(self.user.following)
                      + self.coefficient_private_repos* int(self.user.private_repos)
                      + self.coefficient_public_repos*int(self.user.public_repos)
                      + self.coefficient_org* len(self.user.org)
                      + self.coefficient_languages * len(self.user.languages))
        if self.user.hireable is not None:
            assessment += 1 *  self.coefficient_hireable
        if self.user.plan is not None:
            if self.user.plan.name != "free":
                assessment += 1 * self.coefficient_plan
        if self.user.company is not None:
            assessment += 1 * self.coefficient_company


        return assessment




def take_data (user):
    user_git = User_GitHub(user.login, user.followers, user.following, user.hireable, user.owned_private_repos, user.public_repos,
                           user.updated_at, user.created_at, user.plan, user.blog, user.get_repos(), user.company, user.get_orgs())
    user_git.Print_user_information()
    return user_git



def evaluate_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Для иследования проанализируй код и поставь ему оценку от 1 до 100, выводи только число, вот код: {code}"}],
        # Add any other necessary parameters
    )
    file.close()
    print(response.choices[0].message.content)


#######################  Main
file_path = r"C:\Users\Артём Морозов\source\repos\ClimbingTheHill\ClimbingTheHill\Program.cs"
#evaluate_code(file_path)

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
        class_user = take_data(user)
        assessment = ProfileAssessment(class_user)
        print(assessment.assessment_profile())
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





