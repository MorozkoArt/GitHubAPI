import requests
import base64
import os
from github import Github
from pprint import pprint
from github import Auth

class User_GitHub:
    languages = []
    repos_user = []


    def __init__(self, name, followers, following, hireable, private_repos, public_repos, last_modified, created_at, plan, blog, repos ):
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
        for repo in self.repos:
            #for content in repo.get_contents(""):
              #  if content.path.endswith(".py"):
                    # save the file
                 #   filename = os.path.join("python-files", f"{repo.full_name.replace('/', '-')}-{content.path}")
                 #   with open(filename, "wb") as f:
                 #       f.write(content.decoded_content)
            repo_user = User_repo(repo.name, repo.forks, repo.stargazers_count, repo.get_contributors().totalCount, repo.created_at,
                                  repo.last_modified_datetime, repo.get_commits().totalCount)
            self.repos_user.append(repo_user)
            if self.languages.count(repo.language) == 0:
                self.languages.append(repo.language)


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



def take_data (user):

    user_git = User_GitHub(user.login, user.followers, user.following, user.hireable, user.owned_private_repos, user.public_repos,
                           user.last_modified_datetime, user.created_at, user.plan, user.blog, user.get_repos())
    print(user_git.Get_Name())

if not os.path.exists("python-files"):
    os.mkdir("python-files")

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
    take_data(user)

elif var_aut == "2":
    login= input(" Введите логин пользователя: ")
    password = input(" Введите пароль: " )
    auth = Auth.Login(login, password)
    g = Github(auth = auth)
    user = g.get_user()

    take_data(user)

elif var_aut == "3":
    access_token = input(" Введите токен доступа пользователя: ")
    auth = Auth.Token(access_token)

    login = Github(auth = auth)
    user = login.get_user()

    take_data(user)





