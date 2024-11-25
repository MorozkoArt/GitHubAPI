from copy import deepcopy
from User_and_Repo.C_UserRepo import User_repo
from Assessment.C_GPT import GPT

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
        self.assessmen_profile_list.append(self.user.month_usege * self.coefficient_created_update)
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
            assessment_repo.append(self.user.repos_user[i].days_usege * self.coefficient_created_update_r)
            assessment_repo.append(int(self.user.repos_user[i].commits_count) * self.coefficient_commits)
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

