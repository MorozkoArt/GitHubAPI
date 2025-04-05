from prettytable import PrettyTable, HRuleStyle
import textwrap

def print_assessment(user, assessment, var_kod):
    tables = []
    assessment_profile_dict = assessment.assessment_profile_dict
    assessment_repos_list = assessment.assessment_repos_list
    assessment_repo_main_dict = assessment.assessment_repo_main_dict
    assessment_kod_list = assessment.assessment_kod_list

    x = PrettyTable(hrules=HRuleStyle.ALL)
    x.field_names = ["Field name", "Significance", "Assessment"]
    x.add_row(["Username", user.name, " "])
    x.add_row(["Profile access", user.public_or_private, " "])
    x.add_row(["Number of followers", user.followers, round(assessment_profile_dict.get("followers"), 2)])
    x.add_row(["Number of following", user.following, round(assessment_profile_dict.get("following"), 2)])
    x.add_row(["Hireable status", user.hireable, round(assessment_profile_dict.get("hireable"), 2)])
    x.add_row(["Number of private repositories\nNumber of public repositories",
               f"{user.private_repos}\n{user.public_repos}", round(assessment_profile_dict.get("repositories"), 2)])
    x.add_row(["Account creation date", user.created_at, " "])
    x.add_row(["Last update date", user.updated_at, " "])
    x.add_row(["Account age", f"{user.month_usege} Month(s)", round(assessment_profile_dict.get("month_usege"), 2)])
    if len(user.repos_user) != 0:
        x.add_row(["Average number of commits per repository", round(user.count_commits, 2), round(assessment_profile_dict.get("countCommits"), 2)])
        x.add_row(["Average commit frequency (days between commits)", round(user.frequency_commits, 2), round(assessment_profile_dict.get("frequencyCommits"), 2)])
        x.add_row(["Average number of commits per day", round(user.in_day_commits, 2), round(assessment_profile_dict.get("inDayCommits"), 2)])
    x.add_row(["Subscription plan", user.plan, round(assessment_profile_dict.get("plan"), 2)])
    x.add_row(["Blog", user.blog, round(assessment_profile_dict.get("blog"), 2)])
    x.add_row(["Company", user.company, round(assessment_profile_dict.get("company"), 2)])
    x.add_row(["Organizations", textwrap.fill(', '.join(map(str, user.org)), width=40), round(assessment_profile_dict.get("org"), 2)])
    x.add_row(["Programming languages", textwrap.fill(', '.join(map(str, user.languages)), width=40), round(assessment_profile_dict.get("language"), 2)])
    x.align["Field name"] = "l"
    x.align["Significance"] = "l"
    x.align["Assessment"] = "r"
    x.border = True
    x.header = True
    x.padding_width = 1

    str1 = f"User profile assessment results - {user.name} \n\n"
    str2 = f"Profile data and their assessment:\n"
    str3 = f"\nProfile assessment: {round(assessment.score_profile, 2)}\n"
    tables.append(str1)
    tables.append(str2)
    tables.append(x)
    tables.append(str3)
    tables.append("\n\n")

    if user.repos.totalCount != 0:
        str4 = f"Repositories data and their assessment: \n"
        tables.append(str4)
        if len(user.empty_repos) != 0:
            str_empty = f"Empty repositories: {textwrap.fill(', '.join(map(str, user.empty_repos)), width=60)}\n"
            tables.append(str_empty)
        tables.append("\n")

        for i in range(len(assessment_repos_list)):
            str_repo1 = f"Repository №-{i + 1}: {user.repos_user[i].name}\n"
            x_r = PrettyTable(hrules=HRuleStyle.ALL)
            x_r.field_names = ["Field name", "Significance", "Assessment"]
            x_r.add_row(["Repository name", user.repos_user[i].name, "-"])
            x_r.add_row(["Programming language", user.repos_user[i].language, "-"])
            x_r.add_row(["Number of forks", user.repos_user[i].forks, round(assessment_repos_list[i].get("forks"), 2)])
            x_r.add_row(["Number of stars", user.repos_user[i].stargazers_count, round(assessment_repos_list[i].get("stargazers_count"), 2)])
            x_r.add_row(["Number of contributors", user.repos_user[i].contributors_count, round(assessment_repos_list[i].get("contributors_count"), 2)])
            x_r.add_row(["Repository creation date\n"
                         "Last update date\n"
                         "Active duration (from first to last commit)", f"{user.repos_user[i].created_at}\n"
                                                                       f"{user.repos_user[i].last_date}\n"
                                                                       f"{user.repos_user[i].days_usege} Day(s)", "-"])
            x_r.add_row(["Number of active days (days with commits)", f"{user.repos_user[i].days_work} Day(s)", round(assessment_repos_list[i].get("days_work"), 2)])
            x_r.add_row(["Number of commits", user.repos_user[i].commits_count, round(assessment_repos_list[i].get("commits_count"), 2)])
            x_r.add_row(["Average commit frequency (days between commits)", (round(user.repos_user[i].commits_frequency, 2) if user.repos_user[i].commits_frequency != "NULL" else "NULL"), round(assessment_repos_list[i].get("frequencyCommits"), 2)])
            x_r.add_row(["Average number of commits per day", (round(user.repos_user[i].commits_in_day, 2) if user.repos_user[i].commits_in_day != "NULL" else "NULL"), round(assessment_repos_list[i].get("inDayCommits"), 2)])
            x_r.add_row(["Number of repository views", user.repos_user[i].count_views, round(assessment_repos_list[i].get("count_views"), 2)])
            x_r.align["Field name"] = "l"
            x_r.align["Significance"] = "l"
            x_r.align["Assessment"] = "r"
            x_r.border = True
            x_r.header = True
            x_r.padding_width = 1
            str_repo2 = f"\nTotal repository assessment: {round(sum(value for value in assessment_repos_list[i].values() if isinstance(value, (int, float))), 2)}"
            tables.append(str_repo1)
            tables.append(x_r)
            tables.append(str_repo2)
            tables.append("\n\n")

    if var_kod == 1:
        str_repo_main = f"Repository selected for detailed analysis: {user.main_repo.name}\n"
        x_r_m = PrettyTable(hrules=HRuleStyle.ALL)
        x_r_m.field_names = ["Field name", "Significance", "Assessment"]
        x_r_m.add_row(["Repository name", user.main_repo.name, "-"])
        x_r_m.add_row(["Programming language", user.main_repo.language, "-"])
        x_r_m.add_row(["Number of forks", user.main_repo.forks, round(assessment_repo_main_dict.get("forks"), 2)])
        x_r_m.add_row(["Number of stars", user.main_repo.stargazers_count, round(assessment_repo_main_dict.get("stargazers_count"), 2)])
        x_r_m.add_row(["Number of contributors", user.main_repo.contributors_count, round(assessment_repo_main_dict.get("contributors_count"), 2)])
        x_r_m.add_row(["Repository creation date\n"
                       "Last update date\n"
                       "Active duration (from first to last commit)", f"{user.main_repo.created_at}\n"
                                                                     f"{user.main_repo.last_date}\n"
                                                                     f"{user.main_repo.days_usege} Day(s)", "-"])
        x_r_m.add_row(["Number of active days (days with commits)", f"{user.main_repo.days_work} Day(s)", round(assessment_repo_main_dict.get("days_work"), 2)])
        x_r_m.add_row(["Number of commits", user.main_repo.commits_count, round(assessment_repo_main_dict.get("commits_count"), 2)])
        x_r_m.add_row(["Average commit frequency (days between commits)", (round(user.main_repo.commits_frequency, 2) if user.main_repo.commits_frequency != "NULL" else "NULL"), round(assessment_repo_main_dict.get("frequencyCommits"), 2)])
        x_r_m.add_row(["Average number of commits per day", (round(user.main_repo.commits_in_day, 2) if user.main_repo.commits_in_day != "NULL" else "NULL"), round(assessment_repo_main_dict.get("inDayCommits"), 2)])
        x_r_m.add_row(["Average number of lines added per commit", round(user.main_repo.commits_add_lines, 2), round(assessment_repo_main_dict.get("addLine"), 2)])
        x_r_m.add_row(["Average number of lines deleted per commit", round(user.main_repo.commits_del_lines, 2), round(assessment_repo_main_dict.get("delLine"), 2)])
        x_r_m.add_row(["Number of repository views", user.main_repo.count_views, round(assessment_repo_main_dict.get("count_views"), 2)])
        x_r_m.align["Field name"] = "l"
        x_r_m.align["Significance"] = "l"
        x_r_m.align["Assessment"] = "r"
        x_r_m.border = True
        x_r_m.header = True
        x_r_m.padding_width = 1
        str_repo_main2 = f"\nTotal repository assessment: {round(assessment.score_main_repos, 2)}"
        tables.append(str_repo_main)
        tables.append(x_r_m)
        tables.append(str_repo_main2)
        tables.append("\n\n")

        str_files = f"Files downloaded for analysis from the selected repository:\n{textwrap.fill(user.main_repo.name_files, width=60)}\n\n"
        tables.append(str_files)
        str_kod1 = f"Code files assessment. Repository being assessed - {user.main_repo.name}\n"
        tables.append(str_kod1)

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
        str_kod_score = f"\nTotal code files assessment: {round(assessment.score_kod, 2)}\n"
        tables.append(str_kod_score)
        tables.append("\n\n")

    str3 = f"Total profile assessment: {round(assessment.score_profile, 2)}\n"
    tables.append(str3)
    if assessment.average_score_repos != 0:
        str_repo = f"Average repositories assessment: {round(assessment.average_score_repos, 2)}\n"
        tables.append(str_repo)
    if var_kod == 1:
        str_main_repo = f"Main repository assessment: {round(assessment.score_main_repos, 2)}\n"
        str_kod = f"Average code files assessment: {round(assessment.score_kod, 2)}\n"
        tables.append(str_main_repo)
        tables.append(str_kod)

    str_sum = f"Final assessment: {round((assessment.score_profile + assessment.average_score_repos + assessment.score_main_repos + assessment.score_kod), 2)}\n\n\n\n"
    tables.append(str_sum)
    return tables