import pytest
import os
from Assessment.C_ProfileAssessment import ProfileAssessment
from User_and_Repo.C_UserRepo import User_repo
from github import Github
from github import Auth

MyToken = os.environ.get("GITHUB_TOKEN")

@pytest.mark.parametrize("frequencyCommits" , [(1), (0.5), (2), (23), (0.01), (0)])
def test_frequencyCommits_to_score_exp(frequencyCommits):
    actual_score = ProfileAssessment.frequencyCommits_to_score_exp(ProfileAssessment, frequencyCommits)
    print(f"{frequencyCommits} - {actual_score}")

@pytest.mark.parametrize("MyToken, login_user" , [(MyToken, "MorozkoArt")])
def test_User_repo_tournament(MyToken, login_user):
    login = Github(MyToken)
    user = login.get_user(login_user)
    repos = user.get_repos()
    publicOrPrivate = "public"
    for repo in repos:
        user_repo = User_repo(repo, publicOrPrivate)
        score = user_repo.tournament()
        print(f"{repo.name} - {score},   ({user_repo.commits_count} , {user_repo.commits_frequency}, {user_repo.commits_inDay}, "
                 f"{user_repo.days_usege}, {user_repo.stargazers_count}, {user_repo.forks})")
