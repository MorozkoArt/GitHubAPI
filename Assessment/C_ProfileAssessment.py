import json
import os
import math
from copy import deepcopy
from User_and_Repo.C_UserRepo import User_repo
from Assessment.C_GPT import GPT


class ProfileAssessment:

    def __init__(self, user, config_file="coefficients.json", config_file2 = "max_value.json"):
        self.coefficients = self._load_config(config_file)
        self.maxValue = self._load_config(config_file2)
        self.user = user
        self.assessmen_repos_list = []
        self.assessment_kod_list = []
        self.assessmen_profile_dict = {}
        self.assessmen_repoMain_dict = {}
        self.score_profile = 0
        self.average_score_repos = 0
        self.score_MainRepos = 0
        self.score_kod = 0

    def _load_config(self, config_file):
        """Loads coefficients from a single JSON config file."""
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Configuration file '{config_file}' not found. Skipping.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{config_file}': {e}")

    def assessment_profile(self):
        self.assessmen_profile_dict["followers"] = self.followers_to_score_log(int(self.user.followers))
        self.assessmen_profile_dict["following"] = self.following_to_score_log(int(self.user.following))
        self.assessmen_profile_dict["hireable"] = self.hireable_to_score(self.user.hireable)
        self.assessmen_profile_dict["plan"] = self.plan_to_score(self.user.plan)
        self.assessmen_profile_dict["blog"] = self.blog_to_score(self.user.blog)
        self.assessmen_profile_dict["company"] = self.company_to_score(self.user.company)
        self.assessmen_profile_dict["org"] = self.org_to_score_log(len(self.user.org))
        self.assessmen_profile_dict["language"] = self.language_to_score_log(len(self.user.languages))
        self.assessmen_profile_dict["countCommits"] = self.countCommits_to_score_log(self.user.countCommits, self.coefficients["countCommits"], self.maxValue["countCommits"])
        self.assessmen_profile_dict["inDayCommits"] = self.inDayCommits_to_score_log(self.user.inDayCommits, self.coefficients["inDayCommits"], self.maxValue["inDayCommits"])
        self.assessmen_profile_dict["frequencyCommits"] = self.frequencyCommits_to_score_exp(self.user.frequencyCommits, self.coefficients["frequencyCommits"])
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
            assessment_repo_dict["commits_count"] = self.countCommits_to_score_log(self.user.repos_user[i].commits_count, self.coefficients["commits_repo"], self.maxValue["countCommitsRepo"])
            assessment_repo_dict["inDayCommits"] = self.inDayCommits_repo(self.user.repos_user[i].commits_inDay, self.user.repos_user[i].days_work, self.coefficients["inDay_repo"], self.coefficients["oneDay_inDay_repo"] )
            assessment_repo_dict["frequencyCommits"] = self.frequencyCommits_repo(self.user.repos_user[i].commits_frequency,self.user.repos_user[i].days_work, self.coefficients["frequency_repo"], self.coefficients["oneDay_frequency_repo"])
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
                                                                               self.coefficients["commits_MainRepo"],
                                                                               self.maxValue["countCommitsRepo"])
        self.assessmen_repoMain_dict["inDayCommits"] = self.inDayCommits_repo(self.user.main_repo.commits_inDay,
                                                                              self.user.main_repo.days_work,
                                                                              self.coefficients["inDayComm_MainRepo"],
                                                                              self.coefficients["oneDay_inDay"])
        self.assessmen_repoMain_dict["frequencyCommits"] = self.frequencyCommits_repo(self.user.main_repo.commits_frequency,
                                                                                      self.user.main_repo.days_work,
                                                                                      self.coefficients["frequencyComm_MainRepo"],
                                                                                      self.coefficients["oneDay_frequency"])
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
            score = (min(self.coefficients["followers"] * math.log(followers) / math.log(5000), self.coefficients["followers"]))
        elif followers == 1:
            score = (min(self.coefficients["followers"] * math.log(followers+1) / math.log(5000), self.coefficients["followers"]))/3
        else:
            score = 0
        return score

    def following_to_score_log(self, following):
        if following not in (0, 1):
            score = (min(self.coefficients["following"] * math.log(following) / math.log(200), self.coefficients["following"]))
        elif following == 1:
            score = (min(self.coefficients["following"] * math.log(following+1) / math.log(200), self.coefficients["following"]))/2
        else:
            score = 0
        return score

    def org_to_score_log(self, orgs):
        if orgs not in  (0, 1):
            score = (min(self.coefficients["org"] * math.log(orgs) / math.log(5), self.coefficients["org"]))
        elif orgs == 1:
            score = (min(self.coefficients["org"] * math.log(orgs+1) / math.log(5), self.coefficients["org"]))/1.5
        else:
            score = 0
        return score

    def company_to_score(self, company):
        score = (self.coefficients["company"] if company is not None else 0)
        return score

    def hireable_to_score(self, hireable):
        score = (self.coefficients["hireable"] if hireable is not None and hireable != "" else 0)
        return score

    def plan_to_score(self, plan):
        score = (self.coefficients["plan"] if plan is not None and plan.name != "free"  else 0)
        return score

    def blog_to_score(self, blog):
        score = (self.coefficients["blog"]if blog not in (None, "") else 0)
        return score

    def language_to_score_log(self, languages):
        if languages not in  (0, 1):
            score = (min(self.coefficients["languages"] * math.log(languages) / math.log(10), self.coefficients["languages"]))
        elif languages == 1:
            score = (min(self.coefficients["languages"] * math.log(languages+1) / math.log(10), self.coefficients["languages"]))/2
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
        if len(self.user.repos_user) != 0:
            normalized_frequency = 1 - (frequency / self.coefficients["frequencyCommits"])
            normalized_inDayCommits = min(inDayCommits / self.coefficients["inDayCommits"], 1)
            normalized_countCommits = min(countCommits / self.coefficients["countCommits"], 1)
            max_num_repos = 25
            normalized_num_repos = min(num_repos / max_num_repos, 1)
            repos_log = normalized_num_repos + normalized_countCommits + normalized_frequency + normalized_inDayCommits

            if repos_log > 1:
                score = (min(self.coefficients["repos"] * (math.log(repos_log) / math.log(4)), self.coefficients["repos"]))
            elif repos_log <= 1 and repos_log > 0:
                score = (min(self.coefficients["repos"] * (math.log(repos_log + 1) / math.log(4)),
                             self.coefficients["repos"])) / 3
            else:
                score = 0
            return score
        else: return 0


    def created_update_to_score_linear(self, repos_log , created_update):

        normalized_repos_log = min(repos_log/self.coefficients["repos"], 1)

        max_created_update = 36
        normalized_created_update = min(created_update/max_created_update, 1 )

        created_update_log = (normalized_repos_log + normalized_created_update)*10

        if created_update_log > 1:
            score = (min(self.coefficients["created_update"] * (math.log(created_update_log) / math.log(20)), self.coefficients["created_update"]))
        elif created_update_log <= 1 and created_update_log > 0:
            score = (min(self.coefficients["created_update"] * (math.log(created_update_log + 1) / math.log(20)), self.coefficients["created_update"])) / 1.3
        else:
            score = 0
        return score

    """Evaluating Repository Fields"""

    def forks_to_score_log(self, forks):
        if forks not in  (0, 1):
            score = (min(self.coefficients["forks"] * math.log(forks) / math.log(10), self.coefficients["forks"]))
        elif forks == 1:
            score = (min(self.coefficients["forks"] * math.log(forks+1) / math.log(10), self.coefficients["forks"]))/2
        else:
            score = 0
        return score

    def stargazers_count_to_score_log(self, stargazers_count):
        if stargazers_count not in  (0, 1):
            score = (min(self.coefficients["stargazers_count"] * math.log(stargazers_count) / math.log(1000), self.coefficients["stargazers_count"]))
        elif stargazers_count == 1:
            score = (min(self.coefficients["stargazers_count"] * math.log(stargazers_count+1) / math.log(1000), self.coefficients["stargazers_count"]))/2
        else:
            score = 0
        return score

    def contributors_count_to_score_log(self, contributors_count):
        if contributors_count not in (0, 1):
            score = (min(self.coefficients["contributors_count"] * math.log(contributors_count) / math.log(10),
                         self.coefficients["contributors_count"]))
        elif contributors_count == 1:
            score = (min(self.coefficients["contributors_count"] * math.log(contributors_count + 1) / math.log(10),
                         self.coefficients["contributors_count"])) / 2
        else:
            score = 0
        return score

    def count_views_count_to_score_log(self, count_views):
        if count_views == "-": return 0
        elif count_views not in (0, 1):
            score = (min(self.coefficients["count_views"] * math.log(count_views) / math.log(10), self.coefficients["count_views"]))
        elif count_views == 1:
            score = (min(self.coefficients["count_views"] * math.log(count_views + 1) / math.log(10), self.coefficients["count_views"])) / 2
        else:
            score = 0
        return score

    def inDayCommits_repo(self, inDayCommits, day_work, coefficient_1, coefficient_2):
        coefficient_inDayCommits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.inDayCommits_to_score_log(inDayCommits, coefficient_inDayCommits, self.maxValue["inDayCommitsRepo"])
        return score

    def frequencyCommits_repo(self, frequencyCommits, day_work, coefficient_1, coefficient_2):
        coefficient_frequencyCommits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.frequencyCommits_to_score_exp(frequencyCommits, coefficient_frequencyCommits)
        return score

    def days_repo(self, frequency, inDayCommits, countCommits, count_day):
        normalized_frequency = 1 - (frequency / self.coefficients["frequency_repo"])
        normalized_inDayCommits = min(inDayCommits / self.coefficients["inDay_repo"], 1)
        normalized_countCommits = min(countCommits / self.coefficients["commits_repo"], 1)
        max_count_day = 10
        normalized_count_day = min(count_day / max_count_day, 1)
        days_log = normalized_count_day + normalized_countCommits*2 + normalized_frequency*0.5 + normalized_inDayCommits*0.5

        if days_log > 1:
            score = (min(self.coefficients["created_update_r"] * (math.log(days_log) / math.log(4)), self.coefficients["created_update_r"]))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.coefficients["created_update_r"] * (math.log(days_log + 1) / math.log(4)), self.coefficients["created_update_r"])) / 3
        else:
            score = 0
        return score

    """Evaluate the fields of the selected repository"""

    def addLine_log(self, addLine):
        if addLine not in (0, 1):
            score = (min(self.coefficients["addLine"] * math.log(addLine) / math.log(100),self.coefficients["addLine"]))
        elif addLine == 1:
            score = (min(self.coefficients["addLine"] * math.log(addLine + 1) / math.log(100),self.coefficients["addLine"])) / 3
        else:
            score = 0
        return score

    def delLine_log(self, delLine):
        if delLine not in (0, 1):
            score = (min(self.coefficients["delLine"] * math.log(delLine) / math.log(30),self.coefficients["delLine"]))
        elif delLine == 1:
            score = (min(self.coefficients["delLine"] * math.log(delLine + 1) / math.log(30),self.coefficients["delLine"])) / 3
        else:
            score = 0
        return score

    def days_MainRepo(self, frequency, inDayCommits, countCommits, addLine, delLine, count_day):
        normalized_frequency = 1 - (frequency / self.coefficients["frequencyComm_MainRepo"])
        normalized_inDayCommits = min(inDayCommits / self.coefficients["inDayComm_MainRepo"], 1)
        normalized_countCommits = min(countCommits / self.coefficients["commits_MainRepo"], 1)
        normalized_addLine = min(addLine / self.coefficients["addLine"], 1)
        normalized_delLine = min(delLine / self.coefficients["delLine"], 1)
        max_count_day = 10
        normalized_count_day = min(count_day / max_count_day, 1)
        days_log = (normalized_count_day + normalized_countCommits*2 + normalized_frequency*0.5
                    + normalized_inDayCommits*0.5 + normalized_addLine*0.5 + normalized_delLine*0.5)

        if days_log > 1:
            score = (min(self.coefficients["created_update_r"] * (math.log(days_log) / math.log(5)), self.coefficients["created_update_r"]))
        elif days_log <= 1 and days_log > 0:
            score = (min(self.coefficients["created_update_r"] * (math.log(days_log + 1) / math.log(5)), self.coefficients["created_update_r"])) / 3
        else:
            score = 0
        return score










