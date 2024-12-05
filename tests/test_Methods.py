import pytest
import os
import math
from Assessment.C_ProfileAssessment import ProfileAssessment
from User_and_Repo.C_UserRepo import User_repo
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken
from github import Github
from github import Auth

MyToken = os.environ.get("GITHUB_TOKEN")

@pytest.mark.parametrize("frequencyCommits, coefficient_frequencyCommits" , [(1 , 5), (0.5, 5), (2, 5), (23 ,5), (0.01, 5), (0, 5)])
def test_frequencyCommits_to_score_exp(frequencyCommits, coefficient_frequencyCommits):
    decay_rate = 0.5
    if frequencyCommits != "NULL":
        actual_score =  coefficient_frequencyCommits * math.exp(-decay_rate * frequencyCommits)
    else: actual_score = 0
    print(f"{frequencyCommits} - {actual_score}")

@pytest.mark.parametrize("followers" , [(0), (10), (100), (1000), (3000), (5000), (5500)])
def test_followers_to_score_log(followers):
    actual_score = ProfileAssessment.followers_to_score_log(ProfileAssessment, followers)
    print(f"{followers} - {actual_score}")

@pytest.mark.parametrize("following" , [(0), (5), (10), (100), (150), (200), (400)])
def test_following_to_score_log(following):
    actual_score = ProfileAssessment.following_to_score_log(ProfileAssessment, following)
    print(f"{following} - {actual_score}")

@pytest.mark.parametrize("language" , [(0), (1), (3), (5), (7), (10), (15)])
def test_language_to_score_log(language):
    actual_score = ProfileAssessment.language_to_score_log(ProfileAssessment, language)
    print(f"{language} - {actual_score}")

@pytest.mark.parametrize("inDayCommits, day_work" , [(2, 1), (2, 2), (1.7692307692307692, 1), (1.7692307692307692, 2), (1000, 1), (1000, 2), (1000, 3)])
def test_inDayCommits(inDayCommits,day_work ):
    max_value_inDayCommitsRepo = 4;
    coefficient_inDayCommits_repo = 20
    coeffOneDay_inDayCommits_repo = 5
    coefficient_inDayCommits = (coefficient_inDayCommits_repo if day_work != 1 else coeffOneDay_inDayCommits_repo)
    score = ProfileAssessment.inDayCommits_to_score_log(ProfileAssessment, inDayCommits, coefficient_inDayCommits, max_value_inDayCommitsRepo)
    print(f"{inDayCommits}, {day_work} - {score}")



@pytest.mark.parametrize("MyToken, login" , [(MyToken, "MorozkoArt"), (MyToken, "ProNinjaDev")])
def test_tournament(MyToken, login):
    publicOrPrivate = "public"
    user = Login(MyToken, login)
    repos = user.get_repos()
    for repo in repos:
        user_repo = User_repo(repo, publicOrPrivate)
        score = user_repo.tournament()
        print(f"\n{repo.name} - {score},   ({user_repo.commits_count} , {user_repo.commits_frequency}, {user_repo.commits_inDay}, "
                 f"{user_repo.days_work}, {user_repo.stargazers_count}, {user_repo.forks})")








