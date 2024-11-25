from Interface.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo

class User_GitHub:
    languages = []
    repos_user = []
    max_judgement = 0
    judgement_rName = ""
    main_repo = None
    def __init__(self, user, publicOrPrivate):
        self.repos = user.get_repos()
        total = (self.repos.totalCount+1)
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
        for repo in self.repos:
            repo_user = User_repo(repo, publicOrPrivate)
            self.repos_user.append(repo_user)
            if repo_user.language is not None:
                judgement = repo_user.tournament(repo_user)
                if judgement > self.max_judgement:
                    self.max_judgement = judgement
                    self.judgement_rName = repo_user.name
            prbar.updatePd()
            if repo_user.language not in self.languages and repo_user.language is not None:
                self.languages.append(repo_user.language)
        prbar.closePd()
        self.main_repo = User_repo.serch_repo(self.repos, self.judgement_rName)

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
