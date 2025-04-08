import math
from src.api.Config.M_LoadConfig import load_config

class Assessment:

    def __init__(self, config_file="field_score.json", config_file2 = "max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value = load_config(config_file2)


    def followers_to_score_log(self, followers):
        if followers not in (0, 1):
            score = (min(self.field_score["followers"] * math.log(followers) / math.log(5000), self.field_score["followers"]))
        elif followers == 1:
            score = (min(self.field_score["followers"] * math.log(followers+1) / math.log(5000), self.field_score["followers"]))/3
        else:
            score = 0
        return round(score,3)

    def following_to_score_log(self, following):
        if following not in (0, 1):
            score = (min(self.field_score["following"] * math.log(following) / math.log(200), self.field_score["following"]))
        elif following == 1:
            score = (min(self.field_score["following"] * math.log(following+1) / math.log(200), self.field_score["following"]))/2
        else:
            score = 0
        return round(score,3)

    def org_to_score_log(self, orgs):
        if orgs not in  (0, 1):
            score = (min(self.field_score["org"] * math.log(orgs) / math.log(5), self.field_score["org"]))
        elif orgs == 1:
            score = (min(self.field_score["org"] * math.log(orgs+1) / math.log(5), self.field_score["org"]))/1.5
        else:
            score = 0
        return round(score,3)

    def company_to_score(self, company):
        score = (self.field_score["company"] if company == 1 else 0)
        return round(score,3)

    def hireable_to_score(self, hireable):
        score = (self.field_score["hireable"] if hireable == 1  else 0)
        return round(score,3)

    def plan_to_score(self, plan):
        score = (self.field_score["plan"] if plan == 1  else 0)
        return round(score,3)

    def blog_to_score(self, blog):
        score = (self.field_score["blog"]if blog == 1 else 0)
        return round(score, 3)

    def language_to_score_log(self, languages):
        if languages not in  (0, 1):
            score = (min(self.field_score["languages"] * math.log(languages) / math.log(10), self.field_score["languages"]))
        elif languages == 1:
            score = (min(self.field_score["languages"] * math.log(languages+1) / math.log(10), self.field_score["languages"]))/2
        else:
            score = 0
        return round(score, 3)

    def count_commits_to_score_log(self, count_commits, coefficient_count_commits, max_value):
        power = 1.4
        if count_commits not in  (0, 1):
            score = (min(coefficient_count_commits * (math.log(count_commits) / math.log(max_value)) ** power, coefficient_count_commits))
        elif count_commits == 1:
            score = (min(coefficient_count_commits * (math.log(count_commits + 1) / math.log(max_value)) ** power, coefficient_count_commits)) / 3
        else:
            score = 0
        return round(score, 3)

    def in_day_commits_to_score_log(self, in_day_commits, coefficient_in_day_commits, max_value):
        if in_day_commits not in  (0, 1):
            score = (min(coefficient_in_day_commits * math.log(in_day_commits) / math.log(max_value), coefficient_in_day_commits))
        elif in_day_commits == 1:
            score = (min(coefficient_in_day_commits * math.log(in_day_commits + 1) / math.log(max_value), coefficient_in_day_commits)) / 3
        else:
            score = 0
        return round(score,3)

    def frequency_commits_to_score_exp(self, repos, frequency_commits, coefficient_frequency_commits):
        decay_rate = 0.5
        if repos != 0:
            return round(coefficient_frequency_commits * math.exp(-decay_rate * frequency_commits), 3)
        return 0

    def evaluate_repositories(self, frequency, in_day_commits, count_commits, num_repos):
        if num_repos != 0:
            normalized_frequency = (frequency / self.field_score["frequencyCommits"])
            normalized_in_day_commits = min(in_day_commits / self.field_score["inDayCommits"], 1)
            normalized_count_commits = min(count_commits / self.field_score["countCommits"], 1)
            max_num_repos = 25
            normalized_num_repos = min(num_repos / max_num_repos, 1)
            repos_log = normalized_num_repos + normalized_count_commits + normalized_frequency + normalized_in_day_commits

            if repos_log > 1:
                score = (min(self.field_score["repos"] * (math.log(repos_log) / math.log(4)), self.field_score["repos"]))
            elif 1 >= repos_log > 0:
                score = (min(self.field_score["repos"] * (math.log(repos_log + 1) / math.log(4)),
                             self.field_score["repos"])) / 3
            else:
                score = 0
            return round(score, 3)
        else: return 0


    def created_update_to_score_linear(self, repos_log , created_update):
        normalized_repos_log = min(repos_log/self.field_score["repos"], 1)
        normalized_created_update = min(created_update / self.max_value["created_update"], 1)
        created_update_log = (normalized_repos_log + normalized_created_update)*10

        if created_update_log > 1:
            score = (min(self.field_score["created_update"] * (math.log(created_update_log) / math.log(20)), self.field_score["created_update"]))
        elif 1 >= created_update_log > 0:
            score = (min(self.field_score["created_update"] * (math.log(created_update_log + 1) / math.log(20)), self.field_score["created_update"])) / 1.3
        else:
            score = 0
        return round(score, 3)

    def forks_to_score_log(self, forks):
        if forks not in  (0, 1):
            score = (min(self.field_score["forks"] * math.log(forks) / math.log(10), self.field_score["forks"]))
        elif forks == 1:
            score = (min(self.field_score["forks"] * math.log(forks+1) / math.log(10), self.field_score["forks"]))/2
        else:
            score = 0
        return round(score, 3)

    def stargazers_count_to_score_log(self, stargazers_count):
        if stargazers_count not in  (0, 1):
            score = (min(self.field_score["stargazers_count"] * math.log(stargazers_count) / math.log(1000), self.field_score["stargazers_count"]))
        elif stargazers_count == 1:
            score = (min(self.field_score["stargazers_count"] * math.log(stargazers_count+1) / math.log(1000), self.field_score["stargazers_count"]))/2
        else:
            score = 0
        return round(score, 3)

    def contributors_count_to_score_log(self, contributors_count):
        if contributors_count not in (0, 1):
            score = (min(self.field_score["contributors_count"] * math.log(contributors_count) / math.log(10),
                         self.field_score["contributors_count"]))
        elif contributors_count == 1:
            score = (min(self.field_score["contributors_count"] * math.log(contributors_count + 1) / math.log(10),
                         self.field_score["contributors_count"])) / 2
        else:
            score = 0
        return round(score, 3)

    def count_views_count_to_score_log(self, count_views):
        if count_views == "-": return 0
        elif count_views not in (0, 1):
            score = (min(self.field_score["count_views"] * math.log(count_views) / math.log(3000), self.field_score["count_views"]))
        elif count_views == 1:
            score = (min(self.field_score["count_views"] * math.log(count_views + 1) / math.log(3000), self.field_score["count_views"])) / 2
        else:
            score = 0
        return round(score, 3)

    def in_day_commits_repo(self, in_day_commits, day_work, coefficient_1, coefficient_2):
        coefficient_in_day_commits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.in_day_commits_to_score_log(in_day_commits, coefficient_in_day_commits, self.max_value["inDayCommitsRepo"])
        return round(score, 3)

    def frequency_commits_repo(self,repos, frequency_commits, day_work, coefficient_1, coefficient_2):
        coefficient_frequency_commits = (coefficient_1 if day_work!=1 else coefficient_2)
        score = self.frequency_commits_to_score_exp(repos,frequency_commits, coefficient_frequency_commits)
        return round(score, 3)

    def days_repo(self, frequency, in_day_commits, count_commits, count_day):
        normalized_frequency = (frequency / self.field_score["frequency_repo"])
        normalized_in_day_commits = min(in_day_commits / self.field_score["inDay_repo"], 1)
        normalized_count_commits = min(count_commits / self.field_score["commits_repo"], 1)
        normalized_count_day = min(count_day / self.max_value["count_day"], 1)
        days_log = normalized_count_day + normalized_count_commits*2 + normalized_frequency*0.5 + normalized_in_day_commits*0.5

        if days_log > 1:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log) / math.log(4)), self.field_score["created_update_r"]))
        elif 1 >= days_log > 0:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log + 1) / math.log(4)), self.field_score["created_update_r"])) / 3
        else:
            score = 0
        return round(score, 3)

    def add_line_log(self, add_line):
        if add_line not in (0, 1):
            score = (min(self.field_score["addLine"] * math.log(add_line) / math.log(100), self.field_score["addLine"]))
        elif add_line == 1:
            score = (min(self.field_score["addLine"] * math.log(add_line + 1) / math.log(100), self.field_score["addLine"])) / 3
        else:
            score = 0
        return round(score, 3)

    def del_line_log(self, del_line):
        if del_line not in (0, 1):
            score = (min(self.field_score["delLine"] * math.log(del_line) / math.log(30), self.field_score["delLine"]))
        elif del_line == 1:
            score = (min(self.field_score["delLine"] * math.log(del_line + 1) / math.log(30), self.field_score["delLine"])) / 3
        else:
            score = 0
        return round(score, 3)

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
        elif 1 >= days_log > 0:
            score = (min(self.field_score["created_update_r"] * (math.log(days_log + 1) / math.log(5)), self.field_score["created_update_r"])) / 3
        else:
            score = 0
        return round(score, 3)










