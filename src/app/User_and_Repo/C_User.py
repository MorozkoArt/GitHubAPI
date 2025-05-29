from src.app.Interface.C_ProgressBar import ProgressBar
from src.app.User_and_Repo.C_UserRepo import User_repo
from src.app.User_and_Repo.C_MainRepo import Main_repo
from github import UnknownObjectException


class User_GitHub:
    def __init__(self, user, public_or_private):
        self.repos = user.get_repos()
        total = (self.repos.totalCount+1)
        self.prbar = ProgressBar(total, "Loading user data: ")
        self.name = user.login
        self.followers = user.followers
        self.following = user.following
        self.hireable = user.hireable
        self.private_repos = user.owned_private_repos
        self.public_repos = user.public_repos
        self.updated_at = user.updated_at
        self.created_at = user.created_at
        self.plan = user.plan
        self.blog = user.blog
        self.company = user.company
        self.public_or_private = public_or_private
        self.org = [org_.login for org_ in user.get_orgs()]
        self.month_usege = self.month_usege()
        self.prbar.update_pd()
        self.main_repo = None
        self.generate_data()
        self.prbar.close_pd()

    def generate_data(self):
        repo_data = self.process_repositories()

        if not repo_data:
            self.frequency_commits = 0
            self.in_day_commits = 0
            self.count_commits = 0
            self.languages = []
            self.repos_user = []
            self.main_repo_name = ""
            self.empty_repos = []
            return

        frequencies, daily_commits, counts, languages, repos, main_repo_name, empty_repos = repo_data
        self.frequency_commits = self.calculate_average(frequencies)
        self.in_day_commits = self.calculate_average(daily_commits)
        self.count_commits = self.calculate_average(counts)
        self.languages = languages
        self.repos_user = repos
        self.main_repo_name =  main_repo_name
        self.empty_repos = empty_repos


    def process_repositories(self):
        commits_frequency = []
        commits_in_day = []
        commits_count = []
        languages = []
        repos_user = []
        empty_repos = []
        main_repo_name = ""
        max_judgement = 0

        for repo in self.repos:
            try:
                repo_user = User_repo(repo, self.public_or_private)
                commits_frequency.append(repo_user.commits_frequency if repo_user.commits_frequency != "NULL" else 0)
                commits_in_day.append(repo_user.commits_in_day if repo_user.commits_in_day != "NULL" else 0)
                commits_count.append(repo_user.commits_count)
                repos_user.append(repo_user)
                max_judgement, main_repo_name = self.find_main_repo_helper(repo_user, max_judgement, main_repo_name)
                if repo_user.language and repo_user.language not in languages:
                    languages.append(repo_user.language)

            except UnknownObjectException as e:
                print(f"Error processing repository {repo.name}: {e}")
            except Exception as e:
                empty_repos.append(repo.name)
            finally:
                self.prbar.update_pd()

        return commits_frequency, commits_in_day, commits_count, languages, repos_user, main_repo_name, empty_repos


    def find_main_repo_helper(self, repo_user, max_judgement, main_repo_name):
        if repo_user.language is not None and repo_user.name != self.name:  # Simplified condition
            judgement = repo_user.tournament()
            if judgement > max_judgement:
                max_judgement = judgement
                main_repo_name = repo_user.name
        return max_judgement, main_repo_name


    def calculate_average(self, data):
        return sum(data) / len(data) if data else 0

    def find_main_repo(self):
        if self.main_repo_name:
            user_repo_main = self.repos_user[0]
            for user_repo in self.repos_user:
                if user_repo.name == self.main_repo_name:
                    user_repo_main = user_repo
                    break
            self.main_repo = Main_repo(user_repo_main, User_repo.search_repo(self.repos, self.main_repo_name))

    def month_usege(self):
        if self.updated_at is not None and self.created_at is not None:
            years_diff = self.updated_at.year - self.created_at.year
            months_diff = self.updated_at.month - self.created_at.month
            total_months = years_diff * 12 + months_diff
            if self.updated_at.day < self.created_at.day:
                total_months -= 1
            return total_months
        else:
            return 0


