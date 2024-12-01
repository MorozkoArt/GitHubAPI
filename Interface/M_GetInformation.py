from prettytable import PrettyTable, HRuleStyle
import textwrap

def print_assessment(user, assessment, var_kod):
    tables = []
    assessmen_profile_dict = assessment.assessmen_profile_dict
    assessmen_repos_list = assessment.assessmen_repos_list
    assessment_kod_list = assessment.assessment_kod_list

    # Данные об оценке профиля
    x = PrettyTable(hrules=HRuleStyle.ALL)
    x.field_names = ["Field name", "Significance", "Assessment"]
    x.add_row(["Имя пользователя", user.name, " "])
    x.add_row(["Доступ к профилю", user.publicOrPrivate, " "])
    x.add_row(["Количество подписчиков", user.followers, assessmen_profile_dict.get("followers")])
    x.add_row(["Количество подписок", user.following, assessmen_profile_dict.get("following")])
    x.add_row(["Доступность для найма", user.hireable, assessmen_profile_dict.get("hireable")])
    x.add_row(["Количество приватных репозиториев\nКоличество публичных репозиториев",
               f"{user.private_repos}\n {user.public_repos}", assessmen_profile_dict.get("repositories")])
    x.add_row(["Дата создания аккаунта", user.created_at, " "])
    x.add_row(["Дата последнего изменения", user.updated_at, " "])
    x.add_row(["Продолжительность пользования", str(user.month_usege) + " Месяц(ев/а)", assessmen_profile_dict.get("month_usege")])
    if len(user.repos_user)!=0:
        x.add_row(["Среднее число коммитов в репозиториях", user.countCommits, assessmen_profile_dict.get("countCommits")])
        x.add_row(["Средняя частота коммитов (раз в сколько дней) в репозиториях", user.frequencyCommits, assessmen_profile_dict.get("frequencyCommits")])
        x.add_row(["Среднее число коммитов в день в репозиториях", user.inDayCommits, assessmen_profile_dict.get("inDayCommits")])
    x.add_row(["Подписка", user.plan, assessmen_profile_dict.get("plan")])
    x.add_row(["Блог", user.blog, assessmen_profile_dict.get("blog")])
    x.add_row(["Компания", user.company, assessmen_profile_dict.get("company")])
    x.add_row(["Организации", ' '.join(map(str, user.org)), assessmen_profile_dict.get("org")])
    x.add_row(["Языки программирования", ' '.join(map(str, user.languages)), assessmen_profile_dict.get("language")])
    x.align["Field name"] = "l"  # Выравнивание текста в столбце
    x.align["Significance"] = "l"  # Выравнивание текста в столбце
    x.align["Assessment"] = "r"  # Выравнивание текста в столбце
    x.border = True  # Отображать границы таблицы
    x.header = True  # Отображать заголовок таблицы
    x.padding_width = 1  # Отступ между ячейками

    str1 = f"Результат оценки профиля пользователя - {user.name} \n\n"
    str2 = f"Данные о профиле пользователя и их оценка:\n"
    tables.append(str1)
    tables.append(str2)
    tables.append(x)
    tables.append("\n\n")
    if user.repos.totalCount != 0:
        str4 = f"Данные о репозиториях и их оценка: \n\n"
        tables.append(str4)

    # Данные об оценке репозиториев
    for i in range(len(assessmen_repos_list)):
        str_repo1 = f"Репозиторий №-{i+1}: {user.repos_user[i].name}\n"
        x_r = PrettyTable(hrules=HRuleStyle.ALL)
        x_r.field_names = ["Field name", "Significance", "Assessment"]
        x_r.add_row(["Название репозитория", user.repos_user[i].name, "-"])
        x_r.add_row(["Язык программирования", user.repos_user[i].language, "-"])
        x_r.add_row(["Количество веток", user.repos_user[i].forks, assessmen_repos_list[i][0]])
        x_r.add_row(["Количество звезд", user.repos_user[i].stargazers_count, assessmen_repos_list[i][1]])
        x_r.add_row(["Количество контрибьюторов", user.repos_user[i].contributors_count, assessmen_repos_list[i][2]])
        x_r.add_row(["Дата создания репозитория", user.repos_user[i].created_at, "-"])
        x_r.add_row(["Дата последнего изменения репозитория", user.repos_user[i].last_date, "-"])
        x_r.add_row(["Продолжительность работы (с момента первого коммита - до последнего)", str(user.repos_user[i].days_usege) + " Дн(я/ей)", assessmen_repos_list[i][3]])
        x_r.add_row(["Кол-во рабочих дней (в сколькии дни добавлялись коммиты)", str(user.repos_user[i].days_work) + " Дн(я/ей)", "-"])
        x_r.add_row(["Количество коммитов внутри репозитория", user.repos_user[i].commits_count,assessmen_repos_list[i][4]])
        x_r.add_row(["Средняя частота коммитов (раз в сколько дней)", user.repos_user[i].commits_frequency, "-"])
        x_r.add_row(["Среднее число коммитов в день", user.repos_user[i].commits_inDay, "-"])
        x_r.add_row(["Количество просмотров репозитория", user.repos_user[i].count_views, assessmen_repos_list[i][5]])
        x_r.align["Field name"] = "l"  # Выравнивание текста в столбце
        x_r.align["Significance"] = "l"  # Выравнивание текста в столбце
        x_r.align["Assessment"] = "r"  # Выравнивание текста в столбце
        x_r.border = True  # Отображать границы таблицы
        x_r.header = True  # Отображать заголовок таблицы
        x_r.padding_width = 1  # Отступ между ячейками
        str_repo2 = f"\nОбщая оценка репозитория {sum(assessmen_repos_list[i])}"
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
        x_r_m.add_row(["Количество веток", user.main_repo.forks, "-"])
        x_r_m.add_row(["Количество звезд", user.main_repo.stargazers_count, "-"])
        x_r_m.add_row(["Количество контрибьюторов", user.main_repo.contributors_count, "-"])
        x_r_m.add_row(["Дата создания репозитория", user.main_repo.created_at, "-"])
        x_r_m.add_row(["Дата последнего изменения репозитория", user.main_repo.last_date, "-"])
        x_r_m.add_row(["Продолжительность работы (с момента первого коммита - до последнего)", str(user.main_repo.days_usege) + " Дн(я/ей)", "-"])
        x_r_m.add_row(["Кол-во рабочих дней (в сколькии дни добавлялись коммиты)", str(user.main_repo.days_work) + " Дн(я/ей)", "-"])
        x_r_m.add_row(["Количество коммитов внутри репозитория", user.main_repo.commits_count, "-"])
        x_r_m.add_row(["Средняя частота коммитов (раз в сколько дней)", user.main_repo.commits_frequency, "-"])
        x_r_m.add_row(["Среднее число коммитов в день", user.main_repo.commits_inDay, "-"])
        x_r_m.add_row(["Среднее число добавляемых строк в коммите", user.main_repo.commits_addLines, "-"])
        x_r_m.add_row(["Среднее число удаляемых строк в коммите", user.main_repo.commits_delLines, "-"])
        x_r_m.add_row(["Количество просмотров репозитория", user.main_repo.count_views, "-"])
        x_r_m.align["Field name"] = "l"  # Выравнивание текста в столбце
        x_r_m.align["Significance"] = "l"  # Выравнивание текста в столбце
        x_r_m.align["Assessment"] = "r"  # Выравнивание текста в столбце
        x_r_m.border = True  # Отображать границы таблицы
        x_r_m.header = True  # Отображать заголовок таблицы
        x_r_m.padding_width = 1  # Отступ между ячейками
        str_repo_main2 = f"\nОбщая оценка репозитория "
        tables.append(str_repo_main)
        tables.append(x_r_m)
        tables.append(str_repo2)
        tables.append("\n\n")

        str_files = f"Файлы, скаченные для анализа из выбранного репозитория {user.main_repo.name}:\n {textwrap.fill(user.main_repo.nameFiles, width=60)}\n\n"
        tables.append(str_files)
        str_kod1 = f"Оценка файлов с программным кодом. Оцениваемы репозиторий - {user.main_repo.name}\n"
        tables.append(str_kod1)

        # Данные об оценке кода
        x_y_r = PrettyTable(hrules=HRuleStyle.ALL)
        x_y_r.field_names = ["Field name", "Assessment", "Explanation"]
        for j in range(len(assessment_kod_list)):
            text, marks, file_name = assessment_kod_list[j]
            x_y_r.add_row([file_name, marks, textwrap.fill(text, width=80)])
        x_y_r.align["Field name"] = "l"  # Выравнивание текста в столбце
        x_y_r.align["Assessment"] = "l"  # Выравнивание текста в столбце
        x_y_r.align["Explanation"] = "l"  # Выравнивание текста в столбце
        x_y_r.border = True  # Отображать границы таблицы
        x_y_r.header = True  # Отображать заголовок таблицы
        x_y_r.padding_width = 1  # Отступ между ячейками
        tables.append(x_y_r)
        tables.append("\n\n")

    str3 = f"Общая оценка данных о профиле пользователя: {assessment.score_profile}\n"
    tables.append(str3)
    if assessment.average_score_repos!=0:
        str_repo = f"Средняя оценка всех репозиториев: {assessment.average_score_repos}\n"
        tables.append(str_repo)
    if var_kod == 1:
        str_kod = f"Средняя оценка всех файлов с кодом: {assessment.score_kod}\n"
        tables.append(str_kod)

    str_sum = f"Итоговая оценка: {assessment.score_profile + assessment.average_score_repos+ assessment.score_kod}\n\n\n\n"
    tables.append(str_sum)
    return tables