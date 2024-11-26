class User_repo:

    code_extensions = ('.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
                       '.html', '.css', '.swift', '.ts', '.json', '.sh', '.pl', '.r', '.cs')

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

        for i in range (self.commits.totalCount):
            if i != (self.commits.totalCount)-1:
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



    def tournament(self, repo_user):
        coefficient_com = 0.8
        coefficient_views = 0.08
        coefficient_stars = 0.1
        coefficient_forks = 0.2
        judgement = 0
        if int(repo_user.contributors_count) <= 1:
            judgement = (int(repo_user.commits_count)*coefficient_com
            + int(repo_user.stargazers_count)*coefficient_stars
            + int(repo_user.forks) * coefficient_forks)
            if repo_user.count_views != "-":
                judgement += int(repo_user.count_views) * coefficient_views
        return judgement

    # Проход по файлам в репозитории

    def serch_repo(repos, name):
        for repo in repos:
            if repo.name == name:
                return repo

