from prettytable import PrettyTable, HRuleStyle
import textwrap


def _create_profile_table(user, assessment):
    table = PrettyTable(hrules=HRuleStyle.ALL)
    table.field_names = ["Field name", "Significance", "Assessment"]
    
    profile_data = [
        ("Username", user.name, " "),
        ("Profile access", user.public_or_private, " "),
        ("Number of followers", user.followers, round(assessment.assessment_profile_dict.get("followers"), 2)),
        ("Number of following", user.following, round(assessment.assessment_profile_dict.get("following"), 2)),
        ("Hireable status", user.hireable, round(assessment.assessment_profile_dict.get("hireable"), 2)),
        ("Number of private repositories\nNumber of public repositories", 
            f"{user.private_repos}\n{user.public_repos}", 
            round(assessment.assessment_profile_dict.get("repositories"), 2)),
        ("Account creation date\nLast update date\nAccount age", 
            f"{user.created_at}\n{user.updated_at}\n{user.month_usege} Month(s)", 
            round(assessment.assessment_profile_dict.get("month_usege"), 2)),
        ("Subscription plan", user.plan, round(assessment.assessment_profile_dict.get("plan"), 2)),
        ("Blog", user.blog, round(assessment.assessment_profile_dict.get("blog"), 2)),
        ("Company", user.company, round(assessment.assessment_profile_dict.get("company"), 2)),
        ("Organizations", textwrap.fill(', '.join(map(str, user.org)), width=40), 
            round(assessment.assessment_profile_dict.get("org"), 2)),
        ("Programming languages", textwrap.fill(', '.join(map(str, user.languages)), width=40), 
            round(assessment.assessment_profile_dict.get("language"), 2)),
    ]
    
    if len(user.repos_user) != 0:
        repo_data = [
            ("Average number of commits per repository", round(user.count_commits, 2), 
                round(assessment.assessment_profile_dict.get("countCommits"), 2)),
            ("Average commit frequency (days between commits)", round(user.frequency_commits, 2), 
                round(assessment.assessment_profile_dict.get("frequencyCommits"), 2)),
            ("Average number of commits per day", round(user.in_day_commits, 2), 
                round(assessment.assessment_profile_dict.get("inDayCommits"), 2)),
            ("Average number of working days over the repository", round(user.avg_a_days, 2), 
                round(assessment.assessment_profile_dict.get("avg_a_days"), 2)),
            ("Average number of contributors in each repository", round(user.avg_cont, 2), 
                round(assessment.assessment_profile_dict.get("avg_cont"), 2)),
            ("Average number of views in each repository", round(user.avg_views, 2), 
                round(assessment.assessment_profile_dict.get("avg_views"), 2)),
            ("Number of stars", user.stars, round(assessment.assessment_profile_dict.get("stars"), 2)),
            ("Number of forks", user.forks, round(assessment.assessment_profile_dict.get("forks"), 2)),
        ]
        profile_data[7:7] = repo_data
    
    for row in profile_data:
        table.add_row(row)
    
    table.align["Field name"] = "l"
    table.align["Significance"] = "l"
    table.align["Assessment"] = "r"
    table.border = True
    table.header = True
    table.padding_width = 1
    
    return table


def _create_main_repo_table(user, assessment):
    table = PrettyTable(hrules=HRuleStyle.ALL)
    table.field_names = ["Field name", "Significance", "Assessment"]
    
    repo_data = [
        ("Repository name", user.main_repo.name, "-"),
        ("Programming language", user.main_repo.language, "-"),
        ("Number of forks", user.main_repo.forks, round(assessment.assessment_repo_main_dict.get("forks"), 2)),
        ("Number of stars", user.main_repo.stargazers_count, 
            round(assessment.assessment_repo_main_dict.get("stargazers_count"), 2)),
        ("Number of contributors", user.main_repo.contributors_count, 
            round(assessment.assessment_repo_main_dict.get("contributors_count"), 2)),
        ("Repository creation date\nLast update date\nActive duration (from first to last commit)", 
            f"{user.main_repo.created_at}\n{user.main_repo.last_date}\n{user.main_repo.days_usege} Day(s)", "-"),
        ("Number of active days (days with commits)", f"{user.main_repo.days_work} Day(s)", 
            round(assessment.assessment_repo_main_dict.get("days_work"), 2)),
        ("Number of commits", user.main_repo.commits_count, 
            round(assessment.assessment_repo_main_dict.get("commits_count"), 2)),
        ("Average commit frequency (days between commits)", 
            (round(user.main_repo.commits_frequency, 2) if user.main_repo.commits_frequency != "NULL" else "NULL"), 
            round(assessment.assessment_repo_main_dict.get("frequencyCommits"), 2)),
        ("Average number of commits per day", 
            (round(user.main_repo.commits_in_day, 2) if user.main_repo.commits_in_day != "NULL" else "NULL"), 
            round(assessment.assessment_repo_main_dict.get("inDayCommits"), 2)),
        ("Average number of lines added per commit", round(user.main_repo.commits_add_lines, 2), 
            round(assessment.assessment_repo_main_dict.get("addLine"), 2)),
        ("Average number of lines deleted per commit", round(user.main_repo.commits_del_lines, 2), 
            round(assessment.assessment_repo_main_dict.get("delLine"), 2)),
        ("Number of repository views", user.main_repo.count_views, 
            round(assessment.assessment_repo_main_dict.get("count_views"), 2)),
    ]
    
    for row in repo_data:
        table.add_row(row)
    
    table.align["Field name"] = "l"
    table.align["Significance"] = "l"
    table.align["Assessment"] = "r"
    table.border = True
    table.header = True
    table.padding_width = 1
    
    return table


def _create_code_files_table(assessment):
    table = PrettyTable(hrules=HRuleStyle.ALL)
    table.field_names = ["Field name", "Assessment", "Explanation"]
    
    for text, marks, file_name in assessment.assessment_kod_list:
        table.add_row([file_name, marks, textwrap.fill(text, width=80)])
    
    table.align["Field name"] = "l"
    table.align["Assessment"] = "l"
    table.align["Explanation"] = "l"
    table.border = True
    table.header = True
    table.padding_width = 1
    
    return table


def print_assessment(user, assessment):
    tables = []
    tables.append(f"User profile assessment results - {user.name}\n\n")
    tables.append("Profile data and their assessment:\n")
    tables.append(_create_profile_table(user, assessment))
    tables.append(f"\nProfile assessment: {round(assessment.score_profile, 2)}\n\n")
    if user.repos.totalCount != 0 or user.main_repo_name != "":
        tables.append(f"Repository selected for detailed analysis: {user.main_repo.name}\n")
        tables.append(_create_main_repo_table(user, assessment))
        tables.append(f"\nTotal repository assessment: {round(assessment.score_main_repos, 2)}\n\n")
        tables.append(f"Files downloaded for analysis from the selected repository:\n"
                        f"{textwrap.fill(user.main_repo.name_files, width=60)}\n\n")
        tables.append(f"Code files assessment. Repository being assessed - {user.main_repo.name}\n")
        tables.append(_create_code_files_table(assessment))
        tables.append(f"\nTotal code files assessment: {round(assessment.score_kod, 2)}\n\n")
    tables.append(f"Total profile assessment: {round(assessment.score_profile, 2)}\n")
    if user.repos.totalCount != 0 or user.main_repo_name != "":
        tables.append(f"Main repository assessment: {round(assessment.score_main_repos, 2)}\n")
        tables.append(f"Average code files assessment: {round(assessment.score_kod, 2)}\n")
    
    tables.append(f"Final assessment: {round((assessment.score_profile + assessment.score_main_repos + assessment.score_kod), 2)}\n\n\n")
    
    return tables