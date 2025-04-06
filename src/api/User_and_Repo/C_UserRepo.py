import math
from src.api.Config.M_LoadConfig import load_config

class User_repo:
    def __init__(self, repo,  publicOrPrivate, config_file="tour_field.json"):
        self.commits = repo.get_commits()
        commits_frequency_value, commits_in_day_value, commits_days = self.commits_frequency_in_day()
        self.commits_count = self.commits.totalCount
        self.commits_frequency = commits_frequency_value
        self.commits_in_day = commits_in_day_value
        self.name = repo.name
        self.language = repo.language
        self.forks = repo.forks
        self.stargazers_count = repo.stargazers_count
        self.contributors_count = repo.get_contributors().totalCount
        self.created_at = repo.created_at.date()
        self.last_date = self.commits[0].commit.author.date.date()
        self.days_usege = (int((self.last_date - self.created_at).days)+1)
        self.days_work = commits_days
        self.publicOrPrivate = publicOrPrivate
        self.count_views = "-" if self.publicOrPrivate == "public" else repo.get_views_traffic()['uniques']
        self.tour_field = load_config(config_file)

    def commits_frequency_in_day(self):
        commits_frequency_list = []
        commits_in_day_list = []
        day = self.commits[0].commit.author.date.date()
        count_commits_in_day = 0
        max_coomits = 1000
        range_commits = (self.commits.totalCount if self.commits.totalCount<=max_coomits else max_coomits)

        for i in range (range_commits):
            if i != (range_commits)-1:
                frequency = (self.commits[i].commit.author.date.date() - self.commits[i+1].commit.author.date.date()).days
                commits_frequency_list.append(frequency)
            if day == self.commits[i].commit.author.date.date():
                count_commits_in_day += 1
            else:
                commits_in_day_list.append(count_commits_in_day)
                count_commits_in_day = 1
                day = self.commits[i].commit.author.date.date()
            if i == (self.commits.totalCount)-1:
                commits_in_day_list.append(count_commits_in_day)

        if len(commits_frequency_list)!=0:
            commits_frequency_value = sum(commits_frequency_list) / len(commits_frequency_list)
        else:
            commits_frequency_value = "NULL"

        if len(commits_in_day_list)!=0:
            commits_in_day_value = sum(commits_in_day_list) / len(commits_in_day_list)
        else:
            commits_in_day_value = "NULL"

        return commits_frequency_value, commits_in_day_value , len(commits_in_day_list)


    def tournament(self):
        normalize_commits_count = min(self.commits_count / self.tour_field["commits_count"], 1)
        decay_rate = 0.5
        normalize_commits_frequency = (math.exp(-decay_rate * self.commits_frequency) if self.commits_frequency != "NULL" else 0)
        normalize_commits_in_day = (min(self.commits_in_day / self.tour_field["commits_inDay"], 1) if self.commits_in_day != "NULL" else 0)
        normalize_days_work = min(self.days_work / self.tour_field["days_work"], 1)
        normalize_stars = min(self.stargazers_count / self.tour_field["stars"], 1)
        normalize_forks = min(self.forks / self.tour_field["forks"], 1)
        repos_log = (normalize_commits_count*4 + normalize_commits_frequency* 0.25+ normalize_commits_in_day*0.25 +
                     normalize_days_work*2 + normalize_stars + normalize_forks)
        if repos_log >1:
            judgement = (min(100 * (math.log(repos_log) / math.log(8.5)),100))
        elif repos_log <=1 and repos_log > 0 :
            judgement = (min(100 * (math.log(repos_log + 1) / math.log(8.5)),100)) / 20
        else:
            judgement = 0
        return judgement

    def search_repo(repos, name):
        for repo in repos:
            if repo.name == name:
                return repo

