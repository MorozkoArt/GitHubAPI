import math

class User_repo:

    code_extensions = ('.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
                       '.html', '.css', '.swift', '.ts', '.json', '.sh', '.pl', '.r', '.cs')

    coefficient_commits_count = 100
    coefficient_commits_inDay = 15
    coefficient_days_usege = 60
    coefficient_stars = 1000
    coefficient_forks = 10
    coefficient_frequencyCommits = 5

    def __init__(self, repo,  publicOrPrivate):
        self.commits = repo.get_commits()
        commits_frequency_value, commits_inDay_value, commits_days = self.commits_frequency_inDay()
        self.commits_count = self.commits.totalCount
        self.commits_frequency = commits_frequency_value
        self.commits_inDay = commits_inDay_value

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
        self.count_views = "-" if self.publicOrPrivate == "public" else repo.get_views_traffic()['count']

    def commits_frequency_inDay(self):
        commits_frequency_list = []
        commits_inDay_list = []
        day = self.commits[0].commit.author.date.date()
        count_commits_inDay = 0
        max_coomits = 1000
        range_commits = (self.commits.totalCount if self.commits.totalCount<=max_coomits else max_coomits)

        for i in range (range_commits):
            if i != (range_commits)-1:
                frequency = (self.commits[i].commit.author.date.date() - self.commits[i+1].commit.author.date.date()).days
                commits_frequency_list.append(frequency)
            if day == self.commits[i].commit.author.date.date():
                count_commits_inDay += 1
            else:
                commits_inDay_list.append(count_commits_inDay)
                count_commits_inDay = 1
                day = self.commits[i].commit.author.date.date()
            if i == (self.commits.totalCount)-1:
                commits_inDay_list.append(count_commits_inDay)

        if len(commits_frequency_list)!=0:
            commits_frequency_value = sum(commits_frequency_list) / len(commits_frequency_list)
        else:
            commits_frequency_value = "NULL"

        if len(commits_inDay_list)!=0:
            commits_inDay_value = sum(commits_inDay_list) / len(commits_inDay_list)
        else:
            commits_inDay_value = "NULL"

        return commits_frequency_value, commits_inDay_value , len(commits_inDay_list)



    def tournament(self):
        normalize_commits_count = min(self.commits_count / self.coefficient_commits_count, 1)
        decay_rate = 0.5
        normalize_commits_frequency = min(math.exp(-decay_rate * self.commits_frequency), 1)
        normalize_commits_inDay = min(self.commits_inDay / self.coefficient_commits_inDay, 1)
        normalize_days_usege = min(self.days_usege / self.coefficient_days_usege, 1)
        normalize_stars = min(self.stargazers_count / self.coefficient_stars, 1)
        normalize_forks = min(self.forks / self.coefficient_forks, 1)
        repos_log = (normalize_commits_count*5 + normalize_commits_frequency*(1/2) + normalize_commits_inDay +
                     normalize_days_usege*2 + normalize_stars + normalize_forks)
        if repos_log >1:
            judgement = (min(100 * (math.log(repos_log) / math.log(10.5)),100))
        elif repos_log <=1 and repos_log > 0 :
            judgement = (min(100 * (math.log(repos_log + 1) / math.log(10.5)),100)) / 3
        else:
            judgement = 0
        return judgement

    # Проход по файлам в репозитории

    def serch_repo(repos, name):
        for repo in repos:
            if repo.name == name:
                return repo

