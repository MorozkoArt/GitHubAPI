from prettytable import PrettyTable, HRuleStyle
import textwrap

def print_assessment(user, assessment, var_kod):
    tables = []
    assessmen_profile_dict = assessment.assessmen_profile_dict
    assessmen_repos_list = assessment.assessmen_repos_list
    assessmen_repoMain_dict = assessment.assessmen_repoMain_dict
    assessment_kod_list = assessment.assessment_kod_list

    x = PrettyTable(hrules=HRuleStyle.ALL)
    x.field_names = ["Field name", "Significance", "Assessment"]
    x.add_row(["Имя пользователя", user.name, " "])
    x.add_row(["Доступ к профилю", user.publicOrPrivate, " "])
    x.add_row(["Количество подписчиков", user.followers, round(assessmen_profile_dict.get("followers"),2)])
    x.add_row(["Количество подписок", user.following, round(assessmen_profile_dict.get("following"),2)])
    x.add_row(["Доступность для найма", user.hireable, round(assessmen_profile_dict.get("hireable"),2)])
    x.add_row(["Количество приватных репозиториев\nКоличество публичных репозиториев",
               f"{user.private_repos}\n{user.public_repos}", round(assessmen_profile_dict.get("repositories"),2)])
    x.add_row(["Дата создания аккаунта", user.created_at, " "])
    x.add_row(["Дата последнего изменения", user.updated_at, " "])
    x.add_row(["Продолжительность пользования", str(user.month_usege) + " Месяц(ев/а)", round(assessmen_profile_dict.get("month_usege"),2)])
    if len(user.repos_user)!=0:
        x.add_row(["Среднее число коммитов в репозиториях", round(user.countCommits,2), round(assessmen_profile_dict.get("countCommits"),2)])
        x.add_row(["Средняя частота коммитов (раз в сколько дней) в репозиториях", round(user.frequencyCommits,2), round(assessmen_profile_dict.get("frequencyCommits"),2)])
        x.add_row(["Среднее число коммитов в день в репозиториях", round(user.inDayCommits,2), round(assessmen_profile_dict.get("inDayCommits"),2)])
    x.add_row(["Подписка", user.plan, round(assessmen_profile_dict.get("plan"),2)])
    x.add_row(["Блог", user.blog, round(assessmen_profile_dict.get("blog"),2)])
    x.add_row(["Компания", user.company, round(assessmen_profile_dict.get("company"),2)])
    x.add_row(["Организации", textwrap.fill(', '.join(map(str, user.org)), width=40), round(assessmen_profile_dict.get("org"),2)])
    x.add_row(["Языки программирования", textwrap.fill(', '.join(map(str, user.languages)), width=40), round(assessmen_profile_dict.get("language"),2)])
    x.align["Field name"] = "l"
    x.align["Significance"] = "l"
    x.align["Assessment"] = "r"
    x.border = True
    x.header = True
    x.padding_width = 1

    str1 = f"Результат оценки профиля пользователя - {user.name} \n\n"
    str2 = f"Данные о профиле пользователя и их оценка:\n"
    str3 = f"\nОценка профиля: {round(assessment.score_profile,2)}\n"
    tables.append(str1)
    tables.append(str2)
    tables.append(x)
    tables.append(str3)
    tables.append("\n\n")
    if user.repos.totalCount != 0:
        str4 = f"Данные о репозиториях и их оценка: \n"
        tables.append(str4)
        if len(user.empty_repos) != 0:
            str_empty = f"Пустые репозитории: {textwrap.fill(', '.join(map(str, user.empty_repos)), width=60)}\n"
            tables.append(str_empty)
        tables.append("\n")


    for i in range(len(assessmen_repos_list)):
        str_repo1 = f"Репозиторий №-{i+1}: {user.repos_user[i].name}\n"
        x_r = PrettyTable(hrules=HRuleStyle.ALL)
        x_r.field_names = ["Field name", "Significance", "Assessment"]
        x_r.add_row(["Название репозитория", user.repos_user[i].name, "-"])
        x_r.add_row(["Язык программирования", user.repos_user[i].language, "-"])
        x_r.add_row(["Количество веток", user.repos_user[i].forks, round(assessmen_repos_list[i].get("forks"),2)])
        x_r.add_row(["Количество звезд", user.repos_user[i].stargazers_count, round(assessmen_repos_list[i].get("stargazers_count"),2)])
        x_r.add_row(["Количество контрибьюторов", user.repos_user[i].contributors_count, round(assessmen_repos_list[i].get("contributors_count"),2)])
        x_r.add_row(["Дата создания репозитория\n"
                     "Дата последнего изменения репозитория\n"
                     "Продолжительность работы (с момента первого коммита - до последнего)", f"{user.repos_user[i].created_at}\n"
                                                                                             f"{user.repos_user[i].last_date}\n"
                                                                                             f"{user.repos_user[i].days_usege} Дн(я/ей)", "-"])
        x_r.add_row(["Кол-во рабочих дней (в сколькие дни добавлялись коммиты)", str(user.repos_user[i].days_work) + " Дн(я/ей)", round(assessmen_repos_list[i].get("days_work"),2)])
        x_r.add_row(["Количество коммитов внутри репозитория", user.repos_user[i].commits_count, round(assessmen_repos_list[i].get("commits_count"),2)])
        x_r.add_row(["Средняя частота коммитов (раз в сколько дней)", (round(user.repos_user[i].commits_frequency,2) if user.repos_user[i].commits_frequency != "NULL" else "NULL"), round(assessmen_repos_list[i].get("frequencyCommits"),2)])
        x_r.add_row(["Среднее число коммитов в день", (round(user.repos_user[i].commits_inDay,2) if user.repos_user[i].commits_inDay != "NULL" else "NULL"), round(assessmen_repos_list[i].get("inDayCommits"),2)])
        x_r.add_row(["Количество просмотров репозитория", user.repos_user[i].count_views, round(assessmen_repos_list[i].get("count_views"),2)])
        x_r.align["Field name"] = "l"
        x_r.align["Significance"] = "l"
        x_r.align["Assessment"] = "r"
        x_r.border = True
        x_r.header = True
        x_r.padding_width = 1
        str_repo2 = f"\nОбщая оценка репозитория {round(sum(value for value in assessmen_repos_list[i].values() if isinstance(value, (int, float))),2)}"
        tables.append(str_repo1)
        tables.append(x_r)
        tables.append(str_repo2)
        tables.append("\n\n")

    if var_kod == 1:
        str_repo_main = f"Репозиторий, выбранный для отдельного анализа: {user.main_repo.name}\n"
        x_r_m = PrettyTable(hrules=HRuleStyle.ALL)
        x_r_m.field_names = ["Field name", "Significance", "Assessment"]
        x_r_m.add_row(["Название репозитория", user.main_repo.name, "-"])
        x_r_m.add_row(["Язык программирования", user.main_repo.language, "-"])
        x_r_m.add_row(["Количество веток", user.main_repo.forks, round(assessmen_repoMain_dict.get("forks"),2)])
        x_r_m.add_row(["Количество звезд", user.main_repo.stargazers_count, round(assessmen_repoMain_dict.get("stargazers_count"),2)])
        x_r_m.add_row(["Количество контрибьюторов", user.main_repo.contributors_count, round(assessmen_repoMain_dict.get("contributors_count"),2)])
        x_r_m.add_row(["Дата создания репозитория\n"
                       "Дата последнего изменения репозитория\n"
                       "Продолжительность работы (с момента первого коммита - до последнего)", f"{user.main_repo.created_at}\n"
                                                                                               f"{user.main_repo.last_date}\n"
                                                                                               f"{user.main_repo.days_usege} Дн(я/ей)", "-"])
        x_r_m.add_row(["Кол-во рабочих дней (в сколькие дни добавлялись коммиты)", str(user.main_repo.days_work) + " Дн(я/ей)", round(assessmen_repoMain_dict.get("days_work"),2)])
        x_r_m.add_row(["Количество коммитов внутри репозитория", user.main_repo.commits_count, round(assessmen_repoMain_dict.get("commits_count"),2)])
        x_r_m.add_row(["Средняя частота коммитов (раз в сколько дней)", (round(user.main_repo.commits_frequency,2) if user.main_repo.commits_frequency != "NULL" else "NULL"), round(assessmen_repoMain_dict.get("frequencyCommits"),2)])
        x_r_m.add_row(["Среднее число коммитов в день", (round(user.main_repo.commits_inDay,2) if user.main_repo.commits_inDay != "NULL" else "NULL"), round(assessmen_repoMain_dict.get("inDayCommits"),2)])
        x_r_m.add_row(["Среднее число добавляемых строк в коммите", round(user.main_repo.commits_addLines, 2), round(assessmen_repoMain_dict.get("addLine"),2)])
        x_r_m.add_row(["Среднее число удаляемых строк в коммите", round(user.main_repo.commits_delLines,2), round(assessmen_repoMain_dict.get("delLine"),2)])
        x_r_m.add_row(["Количество просмотров репозитория", user.main_repo.count_views, round(assessmen_repoMain_dict.get("count_views"),2)])
        x_r_m.align["Field name"] = "l"
        x_r_m.align["Significance"] = "l"
        x_r_m.align["Assessment"] = "r"
        x_r_m.border = True
        x_r_m.header = True
        x_r_m.padding_width = 1
        str_repo_main2 = f"\nОбщая оценка репозитория {round(assessment.score_MainRepos, 2)}"
        tables.append(str_repo_main)
        tables.append(x_r_m)
        tables.append(str_repo_main2)
        tables.append("\n\n")

        str_files = f"Файлы, скаченные для анализа из выбранного репозитория:\n{textwrap.fill(user.main_repo.nameFiles, width=60)}\n\n"
        tables.append(str_files)
        str_kod1 = f"Оценка файлов с программным кодом. Оцениваемый репозиторий - {user.main_repo.name}\n"
        tables.append(str_kod1)

        # Данные об оценке кода
        x_y_r = PrettyTable(hrules=HRuleStyle.ALL)
        x_y_r.field_names = ["Field name", "Assessment", "Explanation"]
        for j in range(len(assessment_kod_list)):
            text, marks, file_name = assessment_kod_list[j]
            x_y_r.add_row([file_name, marks, textwrap.fill(text, width=80)])
        x_y_r.align["Field name"] = "l"
        x_y_r.align["Assessment"] = "l"
        x_y_r.align["Explanation"] = "l"
        x_y_r.border = True
        x_y_r.header = True
        x_y_r.padding_width = 1
        tables.append(x_y_r)
        str_kod_score = f"\nОбщая оценка всех файлов с программным кодом: {round(assessment.score_kod,2)}\n"
        tables.append(str_kod_score)
        tables.append("\n\n")

    str3 = f"Общая оценка данных о профиле пользователя: {round(assessment.score_profile,2)}\n"
    tables.append(str3)
    if assessment.average_score_repos!=0:
        str_repo = f"Средняя оценка всех репозиториев: {round(assessment.average_score_repos,2)}\n"
        tables.append(str_repo)
    if var_kod == 1:
        str_mainRepo = f"Оценка основного репозитория: {round(assessment.score_MainRepos,2)}\n"
        str_kod = f"Средняя оценка всех файлов с кодом: {round(assessment.score_kod,2)}\n"
        tables.append(str_mainRepo)
        tables.append(str_kod)

    str_sum = f"Итоговая оценка: {round((assessment.score_profile + assessment.average_score_repos+ assessment.score_MainRepos + assessment.score_kod),2)}\n\n\n\n"
    tables.append(str_sum)
    return tables