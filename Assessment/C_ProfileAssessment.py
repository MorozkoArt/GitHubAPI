from copy import deepcopy
from prettytable import PrettyTable, HRuleStyle
from User_and_Repo.C_UserRepo import User_repo
from Assessment.C_GPT import GPT
import textwrap

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
    coefficient_stargazers_count = 5.0
    coefficient_contributors_count = 3.4
    coefficient_created_update_r = 0.4
    coefficient_commits = 0.2
    coefficient_count_views = 0.1

    assessmen_profile_list = []
    assessmen_repos_list = []
    assessment_kod_list = []
    score_profile = 0
    average_score_repos = 0
    score_kod = 0
    def __init__(self, user):
        self.user = user
    def assessment_profile(self):
        self.assessmen_profile_list.append(self.coefficient_followers*int(self.user.followers))
        self.assessmen_profile_list.append(self.coefficient_following*int(self.user.following))
        self.assessmen_profile_list.append(1 * self.coefficient_hireable if self.user.hireable is not None else 0)
        self.assessmen_profile_list.append(int(self.user.private_repos) * self.coefficient_private_repos if self.user.private_repos is not None else 0)
        self.assessmen_profile_list.append(int(self.user.public_repos) * self.coefficient_public_repos if self.user.public_repos is not None else 0)
        if self.user.updated_at is not None and self.user.created_at is not None:
            years_diff = self.user.updated_at.year - self.user.created_at.year
            months_diff = self.user.updated_at.month - self.user.created_at.month
            total_months = years_diff * 12 + months_diff
            if self.user.updated_at.day < self.user.created_at.day:
                total_months -= 1
            self.assessmen_profile_list.append(total_months * self.coefficient_created_update)
        else:
            self.assessmen_profile_list.append(0)
        self.assessmen_profile_list.append(1 * self.coefficient_plan if self.user.plan is not None and self.user.plan.name != "free" else 0)
        self.assessmen_profile_list.append(1 * self.coefficient_blog if self.user.blog not in (None, "") else 0)
        self.assessmen_profile_list.append(1 * self.coefficient_company if self.user.company is not None else 0)
        self.assessmen_profile_list.append(self.coefficient_org* len(self.user.org))
        self.assessmen_profile_list.append(self.coefficient_languages * len(self.user.languages))

        self.score_profile = sum(self.assessmen_profile_list)
        return self.score_profile

    def assessment_repos(self):
        assessment_repo = []
        overall_assessment = 0
        average_score = 0
        for i in range (len(self.user.repos_user)):
            assessment_repo.append(int(self.user.repos_user[i].forks) * self.coefficient_forks)
            assessment_repo.append(int(self.user.repos_user[i].stargazers_count) * self.coefficient_stargazers_count)
            assessment_repo.append(int(self.user.repos_user[i].contributors_count) * self.coefficient_contributors_count)
            total_days = (int((self.user.repos_user[i].last_date - self.user.repos_user[i].created_at).days))
            assessment_repo.append(total_days * self.coefficient_created_update_r)
            assessment_repo.append(int(self.user.repos_user[i].commits) * self.coefficient_commits)
            if self.user.publicOrPrivate == "public":
                assessment_repo.append(0)
            else:
                assessment_repo.append(int(self.user.repos_user[i].count_views) * self.coefficient_count_views)
            copy_assessment_repo = deepcopy(assessment_repo)
            self.assessmen_repos_list.append(copy_assessment_repo)
            for j in range (len(assessment_repo)):
                overall_assessment += assessment_repo[j]
            assessment_repo.clear()
        self.average_score_repos = overall_assessment / len(self.user.repos_user)
        return self.average_score_repos

    def assessment_kod(self, full_or_three):
        list_of_path = User_repo.dounloud_mainRepo(self.user.main_repo)
        chat_gpt = GPT(list_of_path)
        self.assessment_kod_list = chat_gpt.evaluate_codeS(full_or_three)
        for i in range (len(self.assessment_kod_list)):
            text, marks, file_name = self.assessment_kod_list[i]
            self.score_kod+=marks
        self.score_kod = (self.score_kod/len(self.assessment_kod_list))*5
        return self.score_kod
    def print_assessment(self):
        tables = []

        #Данные об оценке профиля
        x = PrettyTable(hrules=HRuleStyle.ALL)
        x.field_names = ["Field name", "Assessment"]
        x.add_row(["Количество подписчиков", self.assessmen_profile_list[0]])
        x.add_row(["Количество подписок", self.assessmen_profile_list[1]])
        x.add_row(["Доступность для найма", self.assessmen_profile_list[2]])
        x.add_row(["Количество приватных репозиториев", self.assessmen_profile_list[3]])
        x.add_row(["Количество публичных репозиториев", self.assessmen_profile_list[4]])
        x.add_row(["Продолжительность пользования", self.assessmen_profile_list[5]])
        x.add_row(["Подписка", self.assessmen_profile_list[6]])
        x.add_row(["Блог", self.assessmen_profile_list[7]])
        x.add_row(["Компания", self.assessmen_profile_list[8]])
        x.add_row(["Организации", self.assessmen_profile_list[9]])
        x.add_row(["Языки программирования", self.assessmen_profile_list[10]])
        x.align["Field name"] = "l"  # Выравнивание текста в столбце
        x.align["Assessment"] = "r"  # Выравнивание текста в столбце
        x.border = True  # Отображать границы таблицы
        x.header = True  # Отображать заголовок таблицы
        x.padding_width = 1  # Отступ между ячейками
        tables.append(x)

        #Данные об оценке репозиториев
        for i in range (len(self.assessmen_repos_list)):
            x_r = PrettyTable(hrules=HRuleStyle.ALL)
            x_r.field_names = ["Field name", "Assessment"]
            x_r.add_row(["Количество веток", self.assessmen_repos_list[i][0]])
            x_r.add_row(["Количество звезд", self.assessmen_repos_list[i][1]])
            x_r.add_row(["Количество контрибьютеров", self.assessmen_repos_list[i][2]])
            x_r.add_row(["Продолжительность работы", self.assessmen_repos_list[i][3]])
            x_r.add_row(["Количество коммитов внутри репозитория", self.assessmen_repos_list[i][4]])
            x_r.add_row(["Количество просмотров репозитория", self.assessmen_repos_list[i][5]])
            x_r.align["Field name"] = "l"  # Выравнивание текста в столбце
            x_r.align["Assessment"] = "r"  # Выравнивание текста в столбце
            x_r.border = True  # Отображать границы таблицы
            x_r.header = True  # Отображать заголовок таблицы
            x_r.padding_width = 1  # Отступ между ячейками
            tables.append(x_r)

        #Данные об оценке кода
        x_y_r = PrettyTable(hrules=HRuleStyle.ALL)
        x_y_r.field_names = ["Field name", "Assessment", "Explanation"]
        for j in range (len(self.assessment_kod_list)):
            text, marks, file_name = self.assessment_kod_list[j]
            x_y_r.add_row([file_name, marks, textwrap.fill(text, width=50)])
        x_y_r.align["Field name"] = "l"  # Выравнивание текста в столбце
        x_y_r.align["Assessment"] = "l"  # Выравнивание текста в столбце
        x_y_r.align["Explanation"] = "l"  # Выравнивание текста в столбце
        x_y_r.border = True  # Отображать границы таблицы
        x_y_r.header = True  # Отображать заголовок таблицы
        x_y_r.padding_width = 1  # Отступ между ячейками
        tables.append(x_y_r)
        return tables
