
from prettytable import PrettyTable, HRuleStyle
from Interface.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo

class User_GitHub:
    languages = []
    repos_user = []
    max_judgement = 0
    judgement_rName = ""
    main_repo = None
    def __init__(self, name, followers, following, hireable, private_repos, public_repos,
                 updated_at, created_at, plan, blog, repos, company, org, publicOrPrivate):
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
        self.publicOrPrivate = publicOrPrivate
        self.org = [org_.login for org_ in org]
        prbar.updatePd()
        for repo in self.repos:
            if self.publicOrPrivate == "public":
                repo_user = User_repo(repo.name, repo.language, repo.forks, repo.stargazers_count,
                                      repo.get_contributors().totalCount,
                                      repo.created_at,
                                      repo.updated_at, repo.get_commits().totalCount, "-")
            else:
                repo_user = User_repo(repo.name, repo.language, repo.forks, repo.stargazers_count,
                                      repo.get_contributors().totalCount,
                                      repo.created_at,
                                      repo.updated_at, repo.get_commits().totalCount, repo.get_views_traffic()['count'])
            self.repos_user.append(repo_user)
            judgement = repo_user.tournament(repo_user)
            if judgement > self.max_judgement:
                self.max_judgement = judgement
                self.judgement_rName = repo_user.name
            prbar.updatePd()
            if repo.language not in self.languages and repo.language is not None:
                self.languages.append(repo.language)
        prbar.closePd()
        self.main_repo = User_repo.serch_repo(self.repos, self.judgement_rName)


    def Print_user_information(self):
        tables = []
        x = PrettyTable(hrules=HRuleStyle.ALL)
        x.field_names = ["Field name", "Significance"]
        x.add_row(["Доступ к профилю", self.publicOrPrivate])
        x.add_row(["Имя пользователя",self.name ])
        x.add_row(["Количество подписчиков", self.followers])
        x.add_row(["Количество подписок", self.following])
        x.add_row(["Доступность для найма", self.hireable])
        x.add_row(["Количество приватных репозиториев", self.private_repos])
        x.add_row(["Количество публичных репозиториев", self.public_repos])
        x.add_row(["Дата создания аккаунта", self.created_at])
        x.add_row(["Дата последнего изменения", self.updated_at])
        x.add_row(["Подписка", self.plan])
        x.add_row(["Ссылка на блог", self.blog])
        x.add_row(["Компания", self.company])
        x.add_row(["Организации", ' '.join(map(str, self.org))])
        x.add_row(["Языки программирования", ' '.join(map(str, self.languages))])
        x.align["Field name"] = "l"  # Выравнивание текста в столбце
        x.align["Significance"] = "r"  # Выравнивание текста в столбце
        x.border = True  # Отображать границы таблицы
        x.header = True  # Отображать заголовок таблицы
        x.padding_width = 1  # Отступ между ячейками
        tables.append(x)
        for i in range (len(self.repos_user)):
            x_r = PrettyTable(hrules=HRuleStyle.ALL)
            x_r.field_names = ["Field name", "Significance"]
            x_r.add_row(["Название репозитория", self.repos_user[i].name])
            x_r.add_row(["Язык программирования", self.repos_user[i].language])
            x_r.add_row(["Количество веток", self.repos_user[i].forks])
            x_r.add_row(["Количество звезд", self.repos_user[i].stargazers_count])
            x_r.add_row(["Количество контрибьютеров", self.repos_user[i].contributors_count])
            x_r.add_row(["Дата создания репозитория", self.repos_user[i].created_at])
            x_r.add_row(["Дата последнего изменения репозитория", self.repos_user[i].last_date])
            x_r.add_row(["Количество коммитов внутри репозитория", self.repos_user[i].commits])
            x_r.add_row(["Количество просмотров репозитория", self.repos_user[i].count_views])
            x_r.align["Field name"] = "l"  # Выравнивание текста в столбце
            x_r.align["Significance"] = "r"  # Выравнивание текста в столбце
            x_r.border = True  # Отображать границы таблицы
            x_r.header = True  # Отображать заголовок таблицы
            x_r.padding_width = 1  # Отступ между ячейками
            tables.append(x_r)
        return tables