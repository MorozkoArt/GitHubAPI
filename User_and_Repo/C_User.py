from Interface.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo
from User_and_Repo.C_MainRepo import Main_repo
from github import Github, UnknownObjectException
from typing import List, Tuple, Optional

class User_GitHub:
    def __init__(self, user, publicOrPrivate):
        self.repos = user.get_repos()
        total = (self.repos.totalCount+2 if self.repos.totalCount!=0 else 1 )
        self.prbar = ProgressBar(total)
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
        self.publicOrPrivate = publicOrPrivate
        self.org = [org_.login for org_ in user.get_orgs()]
        self.month_usege = self.month_usege()
        self.prbar.updatePd()
        self.generate_data()
        self.prbar.closePd()

    def generate_data(self):
        """Calculates and stores user data from repositories."""
        repo_data = self.process_repositories()

        if not repo_data:
            # Handle empty repos gracefully
            self.frequencyCommits = 0
            self.inDayCommits = 0
            self.countCommits = 0
            self.languages = []
            self.repos_user = []
            self.main_repo = None
            return

        frequencies, daily_commits, counts, languages, repos, main_repo_name = repo_data
        self.frequencyCommits = self._calculate_average(frequencies)
        self.inDayCommits = self._calculate_average(daily_commits)
        self.countCommits = self._calculate_average(counts)
        self.languages = languages
        self.repos_user = repos
        self.main_repo =  self._find_main_repo(main_repo_name)


    def process_repositories(self) -> Optional[Tuple[List[float], List[float], List[int], List[str], List['User_repo'], str]]:
        """Processes user repositories to extract data."""
        commits_frequency = []
        commits_in_day = []
        commits_count = []
        languages = []
        repos_user = []
        main_repo_name = ""
        max_judgement = 0

        for repo in self.repos:
            try:
                repo_user = User_repo(repo, self.publicOrPrivate)
                commits_frequency.append(repo_user.commits_frequency if repo_user.commits_frequency != "NULL" else 0)
                commits_in_day.append(repo_user.commits_inDay if repo_user.commits_inDay != "NULL" else 0)
                commits_count.append(repo_user.commits_count)
                repos_user.append(repo_user)
                max_judgement, main_repo_name = self._find_main_repo_helper(repo_user, repo, max_judgement, main_repo_name)
                if repo_user.language and repo_user.language not in languages:
                    languages.append(repo_user.language)

            except UnknownObjectException as e:
                print(f"Error processing repository {repo.name}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred processing {repo.name}: {e}")
            finally:
                self.prbar.updatePd()

        return commits_frequency, commits_in_day, commits_count, languages, repos_user, main_repo_name


    def _find_main_repo_helper(self, repo_user, repo, max_judgement, main_repo_name):
        if repo_user.language and repo.name != self.name:  # Simplified condition
            judgement = repo_user.tournament()
            if judgement > max_judgement:
                max_judgement = judgement
                main_repo_name = repo_user.name
        return max_judgement, main_repo_name


    def _calculate_average(self, data):
        """Calculates average, handling empty lists."""
        return sum(data) / len(data) if data else 0

    def _find_main_repo(self, main_repo_name):
        """Finds main repo."""
        if main_repo_name:
            main_repo = Main_repo(User_repo.search_repo(self.repos, main_repo_name), self.publicOrPrivate)
            self.prbar.updatePd()
            return main_repo
        return None

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


