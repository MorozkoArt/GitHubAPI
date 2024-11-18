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

    assessmen_repos = []
    def __init__(self, user):
        self.user = user
    def assessment_profile(self):
        assessment = (self.coefficient_followers*int(self.user.followers)
                      + self.coefficient_following*int(self.user.following)
                      + self.coefficient_org* len(self.user.org)
                      + self.coefficient_languages * len(self.user.languages))
        if self.user.hireable is not None:
            assessment += 1 *  self.coefficient_hireable
        if self.user.plan is not None:
            if self.user.plan.name != "free":
                assessment += 1 * self.coefficient_plan
        if self.user.company is not None:
            assessment += 1 * self.coefficient_company
        if self.user.private_repos is not None:
            assessment += int(self.user.private_repos)*self.coefficient_private_repos
        if self.user.public_repos is not None:
            assessment += int(self.user.public_repos)*self.coefficient_public_repos
        if self.user.blog is not None and self.user.blog != "":
            assessment += 1*self.coefficient_blog
        if self.user.updated_at is not None and self.user.created_at is not None:
            years_diff = self.user.updated_at.year - self.user.created_at.year
            months_diff = self.user.updated_at.month - self.user.created_at.month
            total_months = years_diff * 12 + months_diff
            if self.user.updated_at.day < self.user.created_at.day:
                total_months -= 1
            assessment += total_months * self.coefficient_created_update
        return assessment

    def assessment_repos(self):
        assessment_repo = []
        overall_assessment = 0
        average_score = 0
        for i in range (len(self.user.repos_user)):
            assessment_repo.append(int(self.user.repos_user[i].forks) * self.coefficient_forks)
            assessment_repo.append(int(self.user.repos_user[i].stargazers_count) * self.coefficient_stargazers_count)
            assessment_repo.append(int(self.user.repos_user[i].contributors_count) * self.coefficient_contributors_count)
            assessment_repo.append(int(self.user.repos_user[i].commits) * self.coefficient_commits)
            if self.user.publicOrPrivate == "public":
                assessment_repo.append(0)
            else:
                assessment_repo.append(int(self.user.repos_user[i].count_views) * self.coefficient_count_views)
            total_days = (int((self.user.repos_user[i].last_date - self.user.repos_user[i].created_at).days))
            assessment_repo.append(total_days * self.coefficient_created_update_r)
            copy_assessment_repo = deepcopy(assessment_repo)
            self.assessmen_repos.append(copy_assessment_repo)
            for j in range (len(assessment_repo)):
                overall_assessment += assessment_repo[j]
            assessment_repo.clear()
        average_score = overall_assessment / len(self.user.repos_user)
        return average_score
    def assessment_kod(self, full_or_three):
        list_of_path = User_repo.dounloud_mainRepo(self.user.main_repo)
        chat_gpt = GPT(list_of_path)
        list_test = chat_gpt.evaluate_codeS(full_or_three)
        kod_mark = 0
        for i in range (len(list_test)):
            text, marks = list_test[i]
            kod_mark+=marks
        kod_mark = (kod_mark/len(list_test))*5
        return kod_mark
