import math
from src.app.Config.M_LoadConfig import load_config


class Assessment:
    def __init__(self, config_file="field_score.json", config_file2="max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value = load_config(config_file2)

    def _log_score(self, value, max_value, field_score, power=1.0, one_divider=2.0):
        if value not in (0, 1):
            score = min(field_score * (math.log(value) / math.log(max_value)) ** power, field_score)
        elif value == 1:
            score = (min(field_score * (math.log(value + 1) / math.log(max_value)) ** power, field_score)) / one_divider
        else:
            score = 0
        return round(score, 3)

    def _exp_score(self, value, coefficient, decay_rate=0.5):
        return round(coefficient * math.exp(-decay_rate * value), 3)

    def _combined_log_score(self, components, field_score, log_base, divider=3.0):
        combined_value = sum(components)
        if combined_value > 1:
            score = min(field_score * (math.log(combined_value) / math.log(log_base)), field_score)
        elif 1 >= combined_value > 0:
            score = min(field_score * (math.log(combined_value + 1) / math.log(log_base)), field_score) / divider
        else:
            score = 0
        return round(score, 3)

    def _binary_score(self, value, field_score):
        return round(field_score if value == 1 else 0, 3)

    def followers_to_score_log(self, followers):
        return self._log_score(followers, self.max_value["followers"], self.field_score["followers"], one_divider=3)

    def following_to_score_log(self, following):
        return self._log_score(following, self.max_value["following"], self.field_score["following"])

    def org_to_score_log(self, orgs):
        return self._log_score(orgs, self.max_value["org"], self.field_score["org"], one_divider=1.5)

    def company_to_score(self, company):
        return self._binary_score(company, self.field_score["company"])

    def hireable_to_score(self, hireable):
        return self._binary_score(hireable, self.field_score["hireable"])

    def plan_to_score(self, plan):
        return self._binary_score(plan, self.field_score["plan"])

    def blog_to_score(self, blog):
        return self._binary_score(blog, self.field_score["blog"])

    def language_to_score_log(self, languages):
        return self._log_score(languages, self.max_value["languages"], self.field_score["languages"])

    def forks_to_score_log(self, forks):
        return self._log_score(forks, self.max_value["forks"], self.field_score["forks"])

    def stars_to_score_log(self, stars):
        return self._log_score(stars, self.max_value["stars"], self.field_score["stars"])

    def avg_cont_to_score_log(self, avg_cont):
        return self._log_score(avg_cont, self.max_value["avg_cont"], self.field_score["avg_cont"])

    def avg_views_to_score_log(self, avg_views):
        return self._log_score(avg_views, self.max_value["avg_views"], self.field_score["avg_views"])

    def avg_a_days_to_score_log(self, avg_a_days):
        return self._log_score(avg_a_days, self.max_value["avg_a_days"], self.field_score["avg_a_days"])

    def commits_to_score_log(self, count_commits):
        return self._log_score(count_commits, self.max_value["countCommits"], self.field_score["countCommits"], power=1.4, one_divider=3)

    def in_day_to_score_log(self, in_day_commits):
        return self._log_score(in_day_commits, self.max_value["inDayCommits"], self.field_score["inDayCommits"], one_divider=3)

    def frequency_to_score_exp(self, repos, frequency_commits):
        return self._exp_score(frequency_commits, self.field_score["frequencyCommits"]) if repos != 0 else 0

    def evaluate_repositories(self, frequency, in_day_commits, count_commits, num_repos):
        if num_repos == 0:
            return 0

        components = [
            min(frequency / self.field_score["frequencyCommits"], 1),
            min(in_day_commits / self.field_score["inDayCommits"], 1),
            min(count_commits / self.field_score["countCommits"], 1),
            min(num_repos / self.max_value["repos"], 1)
        ]
        return self._combined_log_score(components, self.field_score["repos"], 4)

    def created_update_to_score_linear(self, repos_log, created_update):
        components = [
            min(repos_log / self.field_score["repos"], 1) * 10,
            min(created_update / self.max_value["created_update"], 1) * 10
        ]
        return self._combined_log_score(components, self.field_score["created_update"], 20, divider=1.3)

    def forks_r_to_score_log(self, forks):
        return self._log_score(forks, self.max_value["forks_r"], self.field_score["forks_r"])

    def stars_r_to_score_log(self, stars):
        return self._log_score(stars, self.max_value["stars_r"], self.field_score["stars_r"])

    def contributors_count_to_score_log(self, contributors_count):
        return self._log_score(contributors_count, self.max_value["cont_count"], self.field_score["contributors_count"])

    def count_views_count_to_score_log(self, count_views):
        if count_views == "-":
            return 0
        return self._log_score(count_views, self.max_value["count_views"], self.field_score["count_views"])

    def commits_r_to_score_log(self, count_commits):
        return self._log_score(count_commits, self.max_value["commits_repo"], self.field_score["commits_MainRepo"], power=1.4, one_divider=3)

    def in_day_r_to_score_log(self, in_day_commits, day_work):
        coefficient = self.field_score["inDayComm_MainRepo"] if day_work != 1 else self.field_score["oneDay_inDay"]
        return self._log_score(in_day_commits, self.max_value["inDay_repo"], coefficient, one_divider=3)

    def frequency_r_to_score_exp(self, repos, frequency_commits, day_work):
        coefficient = self.field_score["frequencyComm_MainRepo"] if day_work != 1 else self.field_score["oneDay_frequency"]
        return self._exp_score(frequency_commits, coefficient) if repos != 0 else 0

    def days_repo(self, frequency, in_day_commits, count_commits, count_day):
        components = [
            min(count_day / self.max_value["active_days_r"], 1),
            min(count_commits / self.field_score["commits_repo"], 1) * 2,
            (frequency / self.field_score["frequency_repo"]) * 0.5,
            min(in_day_commits / self.field_score["inDay_repo"], 1) * 0.5
        ]
        return self._combined_log_score(components, self.field_score["created_update_r"], 4)

    def add_line_log(self, add_line):
        return self._log_score(add_line, 100, self.field_score["addLine"], one_divider=3)

    def del_line_log(self, del_line):
        return self._log_score(del_line, 30, self.field_score["delLine"], one_divider=3)

    def days_main_repo(self, frequency, in_day_commits, count_commits, add_line, del_line, count_day):
        components = [
            min(count_day / self.max_value["active_days_r"], 1),
            min(count_commits / self.field_score["commits_MainRepo"], 1) * 2,
            (frequency / self.field_score["frequencyComm_MainRepo"]) * 0.5,
            min(in_day_commits / self.field_score["inDayComm_MainRepo"], 1) * 0.5,
            min(add_line / self.field_score["addLine"], 1) * 0.5,
            min(del_line / self.field_score["delLine"], 1) * 0.5
        ]
        return self._combined_log_score(components, self.field_score["created_update_r"], 5)