import math
from Assessment.C_GPT import GPT
from Config.M_LoadConfig import load_config

class ProfileAssessment:

    def __init__(self, user, config_file="field_score.json", config_file2 = "max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value = load_config(config_file2)
        self.user = user
        self.assessment_repos_list = []
        self.assessment_kod_list = []
        self.assessment_profile_dict = {}
        self.assessment_repo_main_dict = {}
        self.score_profile = 0
        self.average_score_repos = 0
        self.score_main_repos = 0
        self.score_kod = 0

    def assessment_profile(self):
        self.assessment_profile_dict["followers"] = self.followers_to_score_log(int(self.user.followers))
        self.assessment_profile_dict["following"] = self.following_to_score_log(int(self.user.following))
        self.assessment_profile_dict["hireable"] = self.hireable_to_score(self.user.hireable)
        self.assessment_profile_dict["plan"] = self.plan_to_score(self.user.plan)
        self.assessment_profile_dict["blog"] = self.blog_to_score(self.user.blog)
        self.assessment_profile_dict["company"] = self.company_to_score(self.user.company)
        self.assessment_profile_dict["org"] = self.org_to_score_log(len(self.user.org))
        self.assessment_profile_dict["language"] = self.language_to_score_log(len(self.user.languages))
        self.assessment_profile_dict["countCommits"] = self.count_commits_to_score_log(self.user.count_commits, self.field_score["countCommits"], self.max_value["countCommits"])
        self.assessment_profile_dict["inDayCommits"] = self.in_day_commits_to_score_log(self.user.in_day_commits, self.field_score["inDayCommits"], self.max_value["inDayCommits"])
        self.assessment_profile_dict["frequencyCommits"] = self.frequency_commits_to_score_exp(self.user.frequency_commits, self.field_score["frequencyCommits"])
        self.assessment_profile_dict["repositories"] = self.evaluate_repositories(self.assessment_profile_dict.get("frequencyCommits"),
                                                                                  self.assessment_profile_dict.get("inDayCommits"),
                                                                                  self.assessment_profile_dict.get("countCommits"),
                                                                                  len(self.user.repos_user))
        self.assessment_profile_dict["month_usege"] = self.created_update_to_score_linear(self.assessment_profile_dict.get("repositories"), self.user.month_usege)
        self.score_profile = sum(value for value in self.assessment_profile_dict.values() if isinstance(value, (int, float)))
        return self.score_profile

    def assessment_repos(self):
        overall_assessment = 0
        average_score = 0
        for i in range (len(self.user.repos_user)):
            assessment_repo_dict = {}
            assessment_repo_dict["forks"] = self.forks_to_score_log(self.user.repos_user[i].forks)
            assessment_repo_dict["stargazers_count"] = self.stargazers_count_to_score_log(self.user.repos_user[i].stargazers_count)
            assessment_repo_dict["contributors_count"] = self.contributors_count_to_score_log(self.user.repos_user[i].contributors_count)
            assessment_repo_dict["commits_count"] = self.count_commits_to_score_log(self.user.repos_user[i].commits_count, self.field_score["commits_repo"], self.max_value["countCommitsRepo"])
            assessment_repo_dict["inDayCommits"] = self.in_day_commits_repo(self.user.repos_user[i].commits_in_day, self.user.repos_user[i].days_work, self.field_score["inDay_repo"], self.field_score["oneDay_inDay_repo"])
            assessment_repo_dict["frequencyCommits"] = self.frequency_commits_repo(self.user.repos_user[i].commits_frequency, self.user.repos_user[i].days_work, self.field_score["frequency_repo"], self.field_score["oneDay_frequency_repo"])
            assessment_repo_dict["days_work"] = self.days_repo(assessment_repo_dict.get("frequencyCommits"),
                                                               assessment_repo_dict.get("inDayCommits"),
                                                               assessment_repo_dict.get("commits_count"),
                                                               self.user.repos_user[i].days_work)
            assessment_repo_dict["count_views"] = self.count_views_count_to_score_log(self.user.repos_user[i].count_views)
            self.assessment_repos_list.append(assessment_repo_dict)
            overall_assessment += sum(value for value in assessment_repo_dict.values() if isinstance(value, (int, float)))
        self.average_score_repos = overall_assessment / len(self.user.repos_user)
        return self.average_score_repos

    def assessment_mainrepo(self):
        self.assessment_repo_main_dict["forks"] = self.forks_to_score_log(self.user.main_repo.forks)
        self.assessment_repo_main_dict["stargazers_count"] = self.stargazers_count_to_score_log(self.user.main_repo.stargazers_count)
        self.assessment_repo_main_dict["contributors_count"] = self.contributors_count_to_score_log(self.user.main_repo.contributors_count)
        self.assessment_repo_main_dict["commits_count"] = self.count_commits_to_score_log(self.user.main_repo.commits_count,
                                                                                          self.field_score["commits_MainRepo"],
                                                                                          self.max_value["countCommitsRepo"])
        self.assessment_repo_main_dict["inDayCommits"] = self.in_day_commits_repo(self.user.main_repo.commits_in_day,
                                                                                  self.user.main_repo.days_work,
                                                                                  self.field_score["inDayComm_MainRepo"],
                                                                                  self.field_score["oneDay_inDay"])
        self.assessment_repo_main_dict["frequencyCommits"] = self.frequency_commits_repo(self.user.main_repo.commits_frequency,
                                                                                         self.user.main_repo.days_work,
                                                                                         self.field_score["frequencyComm_MainRepo"],
                                                                                         self.field_score["oneDay_frequency"])
        self.assessment_repo_main_dict["addLine"] = self.add_line_log(self.user.main_repo.commits_add_lines)
        self.assessment_repo_main_dict["delLine"] = self.del_line_log(self.user.main_repo.commits_del_lines)
        self.assessment_repo_main_dict["days_work"] = self.days_main_repo(self.assessment_repo_main_dict.get("frequencyCommits"),
                                                                          self.assessment_repo_main_dict.get("inDayCommits"),
                                                                          self.assessment_repo_main_dict.get("commits_count"),
                                                                          self.assessment_repo_main_dict.get("addLine"),
                                                                          self.assessment_repo_main_dict.get("delLine"),
                                                                          self.user.main_repo.days_work)
        self.assessment_repo_main_dict["count_views"] = self.count_views_count_to_score_log(self.user.main_repo.count_views)
        self.score_main_repos = sum(value for value in self.assessment_repo_main_dict.values() if isinstance(value, (int, float)))
        return self.score_main_repos


    def assessment_kod(self, full_or_three):
        list_of_path = self.user.main_repo.dounloud_mainRepo()
        chat_gpt = GPT(list_of_path)
        self.assessment_kod_list = chat_gpt.evaluate_codeS(full_or_three)
        for i in range (len(self.assessment_kod_list)):
            text, marks, file_name = self.assessment_kod_list[i]
            self.score_kod+=marks
        self.score_kod = (self.score_kod/len(self.assessment_kod_list))*5
        return self.score_kod

    def followers_to_score_log(self, followers):
        if followers not in (0, 1):
            score = (min(self.field_score["followers"] * math.log(followers) / math.log(5000), self.field_score["followers"]))
        elif followers == 1:
            score = (min(self.field_score["followers"] * math.log(followers+1) / math.log(5000), self.field_score["followers"]))/3
        else:
            score = 0
        return score

    def following_to_score_log(self, following):
        if following not in (0, 1):
            score = (min(self.field_score["following"] * math.log(following) / math.log(200), self.field_score["following"]))
        elif following == 1:
            score = (min(self.field_score["following"] * math.log(following+1) / math.log(200), self.field_score["following"]))/2
        else:
            score = 0
        return score

    def org_to_score_log(self, orgs):
        if orgs not in  (0, 1):
            score = (min(self.field_score["org"] * math.log(orgs) / math.log(5), self.field_score["org"]))
        elif orgs == 1:
            score = (min(self.field_score["org"] * math.log(orgs+1) / math.log(5), self.field_score["org"]))/1.5
        else:
            score = 0
        return score

    def company_to_score(self, company):
        score = (self.field_score["company"] if company is not None else 0)
        return score

    def hireable_to_score(self, hireable):
        score = (self.field_score["hireable"] if hireable is not None and hireable != "" else 0)
        return score

    def plan_to_score(self, plan):
        score = (self.field_score["plan"] if plan is not None and plan.name != "free"  else 0)
        return score

    def blog_to_score(self, blog):
        score = (self.field_score["blog"]if blog not in (None, "") else 0)
        return score

    def language_to_score_log(self, languages):
        if languages not in  (0, 1):
            score = (min(self.field_score["languages"] * math.log(languages) / math.log(10), self.field_score["languages"]))
        elif languages == 1:
            score = (min(self.field_score["languages"] * math.log(languages+1) / math.log(10), self.field_score["languages"]))/2
        else:
            score = 0
        return score

    def count_commits_to_score_log(self, count_commits, coefficient_count_commits, max_value):
        power = 1.4
        if count_commits not in  (0, 1):
            score = (min(coefficient_count_commits * (math.log(count_commits) / math.log(max_value)) ** power, coefficient_count_commits))
        elif count_commits == 1:
            score = (min(coefficient_count_commits * (math.log(count_commits + 1) / math.log(max_value)) ** power, coefficient_count_commits)) / 3
        else:
            score = 0
        return score

    def in_day_commits_to_score_log(self, in_day_commits, coefficient_in_day_commits, max_value):
        if in_day_commits == "NULL": return 0
        elif in_day_commits not in  (0, 1):
            score = (min(coefficient_in_day_commits * math.log(in_day_commits) / math.log(max_value), coefficient_in_day_commits))
        elif in_day_commits == 1:
            score = (min(coefficient_in_day_commits * math.log(in_day_commits + 1) / math.log(max_value), coefficient_in_day_commits)) / 3
        else:
            score = 0
        return score

    def frequency_commits_to_score_exp(self, frequency_commits, coefficient_frequency_commits):
        decay_rate = 0.5
        if len(self.user.repos_user) != 0 and frequency_commits != "NULL":
            return coefficient_frequency_commits * math.exp(-decay_rate * frequency_commits)
        return 0

    def evaluate_repositories(self, frequency, in_day_commits, count_commits, num_repos):
        if len(self.user.repos_user) != 0:
            normalized_frequency = (frequency / self.field_score["frequencyCommits"])
            normalized_inDayCommits = min(in_day_commits / self.field_score["inDayCommits"], 1)
            normalized_countCommits = min(count_commits / self.field_score["countCommits"], 1)
            max_num_repos = 25
            normalized_num_repos = min(num_repos / max_num_repos, 1)
            repos_log = normalized_num_repos + normalized_countCommits + normalized_frequency + normalized_inDayCommits

            if repos_log > 1:
                score = (min(self.field_score["repos"] * (math.log(repos_log) / math.log(4)), self.field_score["repos"]))
            elif repos_log <= 1 and repos_log > 0:
                score = (min(self.field_score["repos"] * (math.log(repos_log + 1) / math.log(4)),
                             self.field_score["repos"])) / 3
            else:
                score = 0
            return score
        else: return 0


    def created_update_to_score_linear(self, repos_log , created_update):
        normalized_repos_log = min(repos_log/self.field_score["repos"], 1)
        normalized_created_update = min(created_update / self.max_value["created_update"], 1)
        created_update_log = (normalized_repos_log + normalized_created_update)*10

        if created_update_log > 1:
            score = (min(self.field_score["created_update"] * (math.log(created_update_log) / math.log(20)), self.field_score["created_update"]))
        elif created_update_log <= 1 and created_update_log > 0:
            score = (min(self.field_score["created_update"] * (math.log(created_update_log + 1) / math.log(20)), self.field_score["created_update"])) / 1.3
        else:
            score = 0
        return score

    def forks_to_score_log(self, forks):
        if forks not in  (0, 1):
            score = (min(self.field_score["forks"] * math.log(forks) / math.log(10), self.field_score["forks"]))
        elif forks == 1:
            score = (min(self.field_score["forks"] * math.log(forks+1) / math.log(10), self.field_score["forks"]))/2
        else:
            score = 0
        return score

    def stargazers_count_to_score_log(self, stargazers_count):
        if stargazers_count not in  (0, 1):
            score = (min(self.field_score["stargazers_count"] * math.log(stargazers_count) / math.log(1000), self.field_score["stargazers_count"]))
        elif stargazers_count == 1:
            score = (min(self.field_score["stargazers_count"] * math.log(stargazers_count+1) / math.log(1000), self.field_score["stargazers_count"]))/2
        else:
            score = 0
        return score

    def contributors_count_to_score_log(self, contributors_count):
        if contributors_count not in (0, 1):
            score = (min(self.field_score["contributors_count"] * math.log(contributors_count) / math.log(10),
                         self.field_score["contributors_count"]))
        elif contributors_count == 1:
            score = (min(self.field_score["contributors_count"] * math.log(contributors_count + 1) / math.log(10),
                         self.field_score["contributors_count"])) / 2
        else:
            score = 0
        return score

    def count_views_count_to_score_log(self, count_views):
        if count_views == "-": return 0
        elif count_views not in (0, 1):
            score = (min(self.field_score["count_views"] * math.log(count_views) / math.log(3000), self.field_score["count_views"]))
        elif count_views == 1:
            score = (min(self.field_score["count_views"] * math.log(count_views + 1) / math.log(3000), self.field_score["count_views"])) / 2
        else:
            score = 0
        return score

    def in_day_commits_repo(self, in_day_commits, day_work, coefficient_1, coefficient_2):
        coefficient_in_day_commits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.in_day_commits_to_score_log(in_day_commits, coefficient_in_day_commits, self.max_value["inDayCommitsRepo"])
        return score

    def frequency_commits_repo(self, frequency_commits, day_work, coefficient_1, coefficient_2):
        coefficient_frequency_commits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.frequency_commits_to_score_exp(frequency_commits, coefficient_frequency_commits)
        return score

    def days_repo(self, frequency, in_day_commits, count_commits, count_day):
        normalized_frequency = (frequency / self.field_score["frequency_repo"])
        normalized_in_day_commits = min(in_day_commits / self.field_score["inDay_repo"], 1)
        normalized_count_commits = min(count_commits / self.field_score["commits_repo"], 1)
        normalized_count_day = min(count_day / self.max_value["count_day"], 1)
        days_log = normalized_count_day + normalized_count_commits*2 + normalized_frequency*0.5 + normalized_in_day_commits*0.5

        if days_log > 1:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log) / math.log(4)), self.field_score["created_update_r"]))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log + 1) / math.log(4)), self.field_score["created_update_r"])) / 3
        else:
            score = 0
        return score

    def add_line_log(self, add_line):
        if add_line not in (0, 1):
            score = (min(self.field_score["addLine"] * math.log(add_line) / math.log(100), self.field_score["addLine"]))
        elif add_line == 1:
            score = (min(self.field_score["addLine"] * math.log(add_line + 1) / math.log(100), self.field_score["addLine"])) / 3
        else:
            score = 0
        return score

    def del_line_log(self, del_line):
        if del_line not in (0, 1):
            score = (min(self.field_score["delLine"] * math.log(del_line) / math.log(30), self.field_score["delLine"]))
        elif del_line == 1:
            score = (min(self.field_score["delLine"] * math.log(del_line + 1) / math.log(30), self.field_score["delLine"])) / 3
        else:
            score = 0
        return score

    def days_main_repo(self, frequency, in_day_commits, count_commits, add_line, del_line, count_day):
        normalized_frequency =  (frequency / self.field_score["frequencyComm_MainRepo"])
        normalized_in_day_commits = min(in_day_commits / self.field_score["inDayComm_MainRepo"], 1)
        normalized_count_commits = min(count_commits / self.field_score["commits_MainRepo"], 1)
        normalized_add_line = min(add_line / self.field_score["addLine"], 1)
        normalized_del_line = min(del_line / self.field_score["delLine"], 1)
        normalized_count_day = min(count_day / self.max_value["count_day"], 1)

        days_log = (normalized_count_day + normalized_count_commits*2 + normalized_frequency*0.5
                    + normalized_in_day_commits*0.5 + normalized_add_line*0.5 + normalized_del_line*0.5)

        if days_log > 1:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log) / math.log(5)), self.field_score["created_update_r"]))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log + 1) / math.log(5)), self.field_score["created_update_r"])) / 3
        else:
            score = 0
        return score










