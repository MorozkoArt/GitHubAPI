from Interface.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo

class User_GitHub:
    languages = []
    repos_user = []
    max_judgement = 0
    judgement_rName = ""
    main_repo = None
    def __init__(self, name, followers, following, hireable, private_repos, public_repos,
                 updated_at, created_at, plan, blog, repos, company, org, publicOrPrivate):
        total = (repos.totalCount+1)
        prbar = ProgressBar(total)
        self.name = name
        self.followers = followers
        self.following = following
        self.hireable = hireable
        self.private_repos = private_repos
        self.public_repos = public_repos
        self.updated_at = updated_at
        self.created_at = created_at
        self.plan = plan
        self.blog = blog
        self.repos = repos
        self.company = company
        self.publicOrPrivate = publicOrPrivate
        self.org = [org_.login for org_ in org]
        prbar.updatePd()
        for repo in self.repos:
            if self.publicOrPrivate == "public":
                repo_user = User_repo(repo.name, repo.language, repo.forks, repo.stargazers_count,
                                      repo.get_contributors().totalCount,
                                      repo.created_at,
                                      repo.updated_at, repo.get_commits().totalCount, "-")
            else:
                repo_user = User_repo(repo.name, repo.language, repo.forks, repo.stargazers_count,
                                      repo.get_contributors().totalCount,
                                      repo.created_at,
                                      repo.updated_at, repo.get_commits().totalCount, repo.get_views_traffic()['count'])
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
