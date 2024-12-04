import math
from copy import deepcopy
from User_and_Repo.C_UserRepo import User_repo
from Assessment.C_GPT import GPT


class ProfileAssessment:
    """Коэффиценты для оценки"""

    """Коэффициенты для оценки профиля"""
    coefficient_followers = 10
    coefficient_following = 3
    coefficient_hireable = 1
    coefficient_repos = 40
    coefficient_created_update = 8
    coefficient_plan = 2
    coefficient_blog = 2
    coefficient_company = 3
    coefficient_org = 3
    coefficient_languages = 9
    coefficient_frequencyCommits = 5
    coefficient_inDayCommits = 5
    coefficient_countCommits = 9

    max_value_inDayCommits = 6
    max_value_countCommits = 100

    max_value_inDayCommitsRepo = 4
    max_value_countCommitsRepo = 150

    """Коэффициенты для оценки репозиториев"""
    coefficient_forks = 4
    coefficient_stargazers_count = 6
    coefficient_contributors_count = 5
    coefficient_created_update_r = 10
    coefficient_commits_repo = 30
    coeff_frequency_repo = 20
    coeff_inDay_repo = 20
    coeffOneDay_frequency_repo = 5
    coeffOneDay_inDay_repo = 5
    coefficient_count_views = 5
    """Коэффиценты для оценки выбранного репозитория"""
    coeff_commits_MainRepo = 24
    coeff_frequencyCommits_MainRepo = 13
    coeff_inDayCommits_MainRepo = 13
    coeffOneDay_frequency = 3
    coeffOneDay_inDay = 3
    coeff_AddLine = 15
    coeff_DelLine = 5



    def __init__(self, user):
        self.user = user
        self.assessmen_repos_list = []
        self.assessment_kod_list = []
        self.assessmen_profile_dict = {}
        self.assessmen_repoMain_dict = {}
        self.score_profile = 0
        self.average_score_repos = 0
        self.score_MainRepos = 0
        self.score_kod = 0

    def assessment_profile(self):
        self.assessmen_profile_dict["followers"] = self.followers_to_score_log(int(self.user.followers))
        self.assessmen_profile_dict["following"] = self.following_to_score_log(int(self.user.following))
        self.assessmen_profile_dict["hireable"] = self.hireable_to_score(self.coefficient_hireable)
        self.assessmen_profile_dict["plan"] = self.plan_to_score(self.user.plan)
        self.assessmen_profile_dict["blog"] = self.blog_to_score(self.user.blog)
        self.assessmen_profile_dict["company"] = self.company_to_score(self.user.company)
        self.assessmen_profile_dict["org"] = self.org_to_score_log(len(self.user.org))
        self.assessmen_profile_dict["language"] = self.language_to_score_log(len(self.user.languages))
        self.assessmen_profile_dict["countCommits"] = self.countCommits_to_score_log(self.user.countCommits, self.coefficient_countCommits, self.max_value_countCommits)
        self.assessmen_profile_dict["inDayCommits"] = self.inDayCommits_to_score_log(self.user.inDayCommits, self.coefficient_inDayCommits, self.max_value_inDayCommits)
        self.assessmen_profile_dict["frequencyCommits"] = self.frequencyCommits_to_score_exp(self.user.frequencyCommits, self.coefficient_frequencyCommits)
        self.assessmen_profile_dict["repositories"] = self.evaluate_repositories(self.assessmen_profile_dict.get("frequencyCommits"),
                                                                          self.assessmen_profile_dict.get("inDayCommits"),
                                                                          self.assessmen_profile_dict.get("countCommits"),
                                                                          len(self.user.repos_user))
        self.assessmen_profile_dict["month_usege"] = self.created_update_to_score_linear(self.assessmen_profile_dict.get("repositories"), self.user.month_usege)
        self.score_profile = sum(value for value in self.assessmen_profile_dict.values() if isinstance(value, (int, float)))
        return self.score_profile

    def assessment_repos(self):
        overall_assessment = 0
        average_score = 0
        for i in range (len(self.user.repos_user)):
            assessment_repo_dict = {}
            assessment_repo_dict["forks"] = self.forks_to_score_log(self.user.repos_user[i].forks)
            assessment_repo_dict["stargazers_count"] = self.stargazers_count_to_score_log(self.user.repos_user[i].stargazers_count)
            assessment_repo_dict["contributors_count"] = self.contributors_count_to_score_log(self.user.repos_user[i].contributors_count)
            assessment_repo_dict["commits_count"] = self.countCommits_to_score_log(self.user.repos_user[i].commits_count, self.coefficient_commits_repo, self.max_value_countCommitsRepo)
            assessment_repo_dict["inDayCommits"] = self.inDayCommits_repo(self.user.repos_user[i].commits_inDay, self.user.repos_user[i].days_work, self.coeff_inDay_repo, self.coeffOneDay_inDay_repo )
            assessment_repo_dict["frequencyCommits"] = self.frequencyCommits_repo(self.user.repos_user[i].commits_frequency,self.user.repos_user[i].days_work, self.coeff_frequency_repo, self.coeffOneDay_frequency_repo )
            assessment_repo_dict["days_work"] = self.days_repo(assessment_repo_dict.get("frequencyCommits"),
                                                               assessment_repo_dict.get("inDayCommits"),
                                                               assessment_repo_dict.get("commits_count"),
                                                               self.user.repos_user[i].days_work)
            assessment_repo_dict["count_views"] = self.count_views_count_to_score_log(self.user.repos_user[i].count_views)
            self.assessmen_repos_list.append(assessment_repo_dict)
            overall_assessment += sum(value for value in assessment_repo_dict.values() if isinstance(value, (int, float)))
        self.average_score_repos = overall_assessment / len(self.user.repos_user)
        return self.average_score_repos

    def assessment_Mainrepo(self):
        self.assessmen_repoMain_dict["forks"] = self.forks_to_score_log(self.user.main_repo.forks)
        self.assessmen_repoMain_dict["stargazers_count"] = self.stargazers_count_to_score_log(self.user.main_repo.stargazers_count)
        self.assessmen_repoMain_dict["contributors_count"] = self.contributors_count_to_score_log(self.user.main_repo.contributors_count)
        self.assessmen_repoMain_dict["commits_count"] = self.countCommits_to_score_log(self.user.main_repo.commits_count,
                                                                               self.coeff_commits_MainRepo,
                                                                               self.max_value_countCommitsRepo)
        self.assessmen_repoMain_dict["inDayCommits"] = self.inDayCommits_repo(self.user.main_repo.commits_inDay,
                                                                              self.user.main_repo.days_work,
                                                                              self.coeff_inDayCommits_MainRepo,
                                                                              self.coeffOneDay_inDay)
        self.assessmen_repoMain_dict["frequencyCommits"] = self.frequencyCommits_repo(self.user.main_repo.commits_frequency,
                                                                                      self.user.main_repo.days_work,
                                                                                      self.coeff_frequencyCommits_MainRepo,
                                                                                      self.coeffOneDay_frequency)
        self.assessmen_repoMain_dict["addLine"] = self.addLine_log(self.user.main_repo.commits_addLines)
        self.assessmen_repoMain_dict["delLine"] = self.delLine_log(self.user.main_repo.commits_delLines)
        self.assessmen_repoMain_dict["days_work"] = self.days_MainRepo(self.assessmen_repoMain_dict.get("frequencyCommits"),
                                                                   self.assessmen_repoMain_dict.get("inDayCommits"),
                                                                   self.assessmen_repoMain_dict.get("commits_count"),
                                                                   self.assessmen_repoMain_dict.get("addLine"),
                                                                   self.assessmen_repoMain_dict.get("delLine"),
                                                                   self.user.main_repo.days_work)
        self.assessmen_repoMain_dict["count_views"] = self.count_views_count_to_score_log(self.user.main_repo.count_views)
        self.score_MainRepos = sum(value for value in self.assessmen_repoMain_dict.values() if isinstance(value, (int, float)))
        return self.score_MainRepos


    def assessment_kod(self, full_or_three):
        list_of_path = self.user.main_repo.dounloud_mainRepo()
        chat_gpt = GPT(list_of_path)
        self.assessment_kod_list = chat_gpt.evaluate_codeS(full_or_three)
        for i in range (len(self.assessment_kod_list)):
            text, marks, file_name = self.assessment_kod_list[i]
            self.score_kod+=marks
        self.score_kod = (self.score_kod/len(self.assessment_kod_list))*5
        return self.score_kod

    """Profile Fields Assessment"""

    def followers_to_score_log(self, followers):
        if followers not in (0, 1):
            score = (min(self.coefficient_followers * math.log(followers) / math.log(5000), self.coefficient_followers))
        elif followers == 1:
            score = (min(self.coefficient_followers * math.log(followers+1) / math.log(5000), self.coefficient_followers))/3
        else:
            score = 0
        return score

    def following_to_score_log(self, following):
        if following not in (0, 1):
            score = (min(self.coefficient_following * math.log(following) / math.log(200), self.coefficient_following))
        elif following == 1:
            score = (min(self.coefficient_following * math.log(following+1) / math.log(200), self.coefficient_following))/2
        else:
            score = 0
        return score

    def org_to_score_log(self, orgs):
        if orgs not in  (0, 1):
            score = (min(self.coefficient_org * math.log(orgs) / math.log(5), self.coefficient_org))
        elif orgs == 1:
            score = (min(self.coefficient_org * math.log(orgs+1) / math.log(5), self.coefficient_org))/1.5
        else:
            score = 0
        return score

    def company_to_score(self, company):
        score = (self.coefficient_company if company is not None else 0)
        return score

    def hireable_to_score(self, hireable):
        score = (self.coefficient_hireable if hireable is not None and hireable != "" else 0)
        return score

    def plan_to_score(self, plan):
        score = (self.coefficient_plan if plan is not None and plan.name != "free"  else 0)
        return score

    def blog_to_score(self, blog):
        score = (self.coefficient_blog if blog not in (None, "") else 0)
        return score

    def language_to_score_log(self, languages):
        if languages not in  (0, 1):
            score = (min(self.coefficient_languages * math.log(languages) / math.log(10), self.coefficient_languages))
        elif languages == 1:
            score = (min(self.coefficient_languages * math.log(languages+1) / math.log(10), self.coefficient_languages))/2
        else:
            score = 0
        return score

    def countCommits_to_score_log(self, countCommits, coefficient_countCommits, max_value):
        power = 1.4
        if countCommits not in  (0, 1):
            score = (min(coefficient_countCommits * (math.log(countCommits) / math.log(max_value))**power, coefficient_countCommits))
        elif countCommits == 1:
            score = (min(coefficient_countCommits * (math.log(countCommits+1) / math.log(max_value))**power, coefficient_countCommits))/3
        else:
            score = 0
        return score

    def inDayCommits_to_score_log(self, inDayCommits, coefficient_inDayCommits, max_value):
        if inDayCommits == "NULL": return 0
        elif inDayCommits not in  (0, 1):
            score = (min(coefficient_inDayCommits * math.log(inDayCommits) / math.log(max_value), coefficient_inDayCommits))
        elif inDayCommits == 1:
            score = (min(coefficient_inDayCommits * math.log(inDayCommits+1) / math.log(max_value), coefficient_inDayCommits))/3
        else:
            score = 0
        return score

    def frequencyCommits_to_score_exp(self, frequencyCommits, coefficient_frequencyCommits):
        decay_rate = 0.5
        if len(self.user.repos_user) != 0 and frequencyCommits != "NULL":
            return coefficient_frequencyCommits * math.exp(-decay_rate * frequencyCommits)
        return 0

    def evaluate_repositories(self, frequency, inDayCommits, countCommits, num_repos):
        normalized_frequency = 1 - (frequency / self.coefficient_frequencyCommits)
        normalized_inDayCommits = min(inDayCommits / self.coefficient_inDayCommits, 1)
        normalized_countCommits = min(countCommits / self.coefficient_countCommits, 1)
        max_num_repos = 25
        normalized_num_repos = min(num_repos / max_num_repos, 1)
        repos_log = normalized_num_repos+normalized_countCommits+normalized_frequency+normalized_inDayCommits

        if repos_log >1:
            score = (min(self.coefficient_repos * (math.log(repos_log) / math.log(4)),self.coefficient_repos))
        elif repos_log <=1 and repos_log > 0 :
            score = (min(self.coefficient_repos * (math.log(repos_log + 1) / math.log(4)),self.coefficient_repos)) / 3
        else:
            score = 0

        return score

    def created_update_to_score_linear(self, repos_log , created_update):

        normalized_repos_log = min(repos_log/self.coefficient_repos, 1)

        max_created_update = 36
        normalized_created_update = min(created_update/max_created_update, 1 )

        created_update_log = (normalized_repos_log + normalized_created_update)*10

        if created_update_log > 1:
            score = (min(self.coefficient_created_update * (math.log(created_update_log) / math.log(20)), self.coefficient_created_update))
        elif created_update_log <= 1 and created_update_log > 0:
            score = (min(self.coefficient_created_update * (math.log(created_update_log + 1) / math.log(20)), self.coefficient_created_update)) / 1.3
        else:
            score = 0
        return score

    """Evaluating Repository Fields"""

    def forks_to_score_log(self, forks):
        if forks not in  (0, 1):
            score = (min(self.coefficient_forks * math.log(forks) / math.log(10), self.coefficient_forks))
        elif forks == 1:
            score = (min(self.coefficient_forks * math.log(forks+1) / math.log(10), self.coefficient_forks))/2
        else:
            score = 0
        return score

    def stargazers_count_to_score_log(self, stargazers_count):
        if stargazers_count not in  (0, 1):
            score = (min(self.coefficient_stargazers_count * math.log(stargazers_count) / math.log(1000), self.coefficient_stargazers_count))
        elif stargazers_count == 1:
            score = (min(self.coefficient_stargazers_count * math.log(stargazers_count+1) / math.log(1000), self.coefficient_stargazers_count))/2
        else:
            score = 0
        return score

    def contributors_count_to_score_log(self, contributors_count):
        if contributors_count not in (0, 1):
            score = (min(self.coefficient_contributors_count * math.log(contributors_count) / math.log(10),
                         self.coefficient_contributors_count))
        elif contributors_count == 1:
            score = (min(self.coefficient_contributors_count * math.log(contributors_count + 1) / math.log(10),
                         self.coefficient_contributors_count)) / 2
        else:
            score = 0
        return score

    def count_views_count_to_score_log(self, count_views):
        if count_views == "-": return 0
        elif count_views not in (0, 1):
            score = (min(self.coefficient_count_views * math.log(count_views) / math.log(10),self.coefficient_count_views))
        elif count_views == 1:
            score = (min(self.coefficient_count_views * math.log(count_views + 1) / math.log(10),self.coefficient_count_views)) / 2
        else:
            score = 0
        return score

    def inDayCommits_repo(self, inDayCommits, day_work, coefficient_1, coefficient_2):
        coefficient_inDayCommits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.inDayCommits_to_score_log(inDayCommits, coefficient_inDayCommits, self.max_value_inDayCommitsRepo)
        return score

    def frequencyCommits_repo(self, frequencyCommits, day_work, coefficient_1, coefficient_2):
        coefficient_frequencyCommits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.frequencyCommits_to_score_exp(frequencyCommits, coefficient_frequencyCommits)
        return score

    def days_repo(self, frequency, inDayCommits, countCommits, count_day):
        normalized_frequency = 1 - (frequency / self.coeff_frequency_repo)
        normalized_inDayCommits = min(inDayCommits / self.coeff_inDay_repo, 1)
        normalized_countCommits = min(countCommits / self.coefficient_commits_repo, 1)
        max_count_day = 10
        normalized_count_day = min(count_day / max_count_day, 1)
        days_log = normalized_count_day + normalized_countCommits*2 + normalized_frequency*0.5 + normalized_inDayCommits*0.5

        if days_log > 1:
            score = (min(self.coefficient_created_update_r * (math.log(days_log) / math.log(4)), self.coefficient_created_update_r))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.coefficient_created_update_r * (math.log(days_log + 1) / math.log(4)), self.coefficient_created_update_r)) / 3
        else:
            score = 0
        return score

    """Evaluate the fields of the selected repository"""

    def addLine_log(self, addLine):
        if addLine not in (0, 1):
            score = (min(self.coeff_AddLine * math.log(addLine) / math.log(100),self.coeff_AddLine))
        elif addLine == 1:
            score = (min(self.coeff_AddLine * math.log(addLine + 1) / math.log(100),self.coeff_AddLine)) / 3
        else:
            score = 0
        return score

    def delLine_log(self, delLine):
        if delLine not in (0, 1):
            score = (min(self.coeff_DelLine * math.log(delLine) / math.log(30),self.coeff_DelLine))
        elif delLine == 1:
            score = (min(self.coeff_DelLine * math.log(delLine + 1) / math.log(30),self.coeff_DelLine)) / 3
        else:
            score = 0
        return score

    def days_MainRepo(self, frequency, inDayCommits, countCommits, addLine, delLine, count_day):
        normalized_frequency = 1 - (frequency / self.coeff_frequencyCommits_MainRepo)
        normalized_inDayCommits = min(inDayCommits / self.coeff_inDayCommits_MainRepo, 1)
        normalized_countCommits = min(countCommits / self.coeff_commits_MainRepo, 1)
        normalized_addLine = min(addLine / self.coeff_AddLine, 1)
        normalized_delLine = min(delLine / self.coeff_DelLine, 1)
        max_count_day = 10
        normalized_count_day = min(count_day / max_count_day, 1)
        days_log = (normalized_count_day + normalized_countCommits*2 + normalized_frequency*0.5
                    + normalized_inDayCommits*0.5 + normalized_addLine*0.5 + normalized_delLine*0.5)

        if days_log > 1:
            score = (min(self.coefficient_created_update_r * (math.log(days_log) / math.log(5)), self.coefficient_created_update_r))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.coefficient_created_update_r * (math.log(days_log + 1) / math.log(5)), self.coefficient_created_update_r)) / 3
        else:
            score = 0
        return score










