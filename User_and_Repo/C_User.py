from Interface.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo
from User_and_Repo.C_MainRepo import Main_repo
from github import Github, UnknownObjectException

class User_GitHub:
    languages = []
    repos_user = []
    max_judgement = 0
    judgement_rName = ""
    main_repo = None
    def __init__(self, user, publicOrPrivate):
        self.repos = user.get_repos()
        total = (self.repos.totalCount+2 if self.repos.totalCount!=0 else 1 )
        prbar = ProgressBar(total)
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
        prbar.updatePd()

        if self.repos.totalCount !=0:
            commits_frequency_list = []
            commits_inDay_list = []
            commits_count = []
            for repo in self.repos:
                try:
                    repo_user = User_repo(repo, publicOrPrivate)  # This might raise an exception if the repo is empty.
                    commits_frequency_list.append(repo_user.commits_frequency if repo_user.commits_frequency != "NULL" else 0)
                    commits_inDay_list.append(repo_user.commits_inDay if repo_user.commits_inDay != "NULL" else 0)
                    commits_count.append(repo_user.commits_count)
                    self.repos_user.append(repo_user)
                    if repo_user.language is not None:
                        judgement = repo_user.tournament(repo_user)
                        if judgement > self.max_judgement:
                            self.max_judgement = judgement
                            self.judgement_rName = repo_user.name
                    if repo_user.language not in self.languages and repo_user.language is not None:
                        self.languages.append(repo_user.language)
                except UnknownObjectException as e:
                    print(f"Repository {repo.name} not found or is empty: {e}")
                    # Consider adding a more sophisticated error logging technique for production-level code.
                except Exception as e:
                    ddd= 0
                finally:
                    prbar.updatePd()

            self.frequencyCommits = sum(commits_frequency_list) / len(commits_frequency_list)
            self.inDayCommits = sum(commits_inDay_list) / len(commits_inDay_list)
            self.countCommits = sum(commits_count) / len(commits_count)
            mainRepo_give = User_repo.serch_repo(self.repos, self.judgement_rName)
            self.main_repo = Main_repo(mainRepo_give, self.publicOrPrivate)
            prbar.updatePd()
        else:
            self.frequencyCommits = 0
            self.inDayCommits = 0
            self.countCommits = 0
        prbar.closePd()


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
