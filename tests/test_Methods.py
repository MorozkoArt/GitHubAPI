import pytest
import os
from src.api.Assessment.C_ProfileAssessment import ProfileAssessment
from src.api.User_and_Repo.C_UserRepo import User_repo
from src.api.User_and_Repo.C_User import User_GitHub
from src.api.StartMethods.M_Authentication import login_auth

my_token = os.environ.get("GITHUB_TOKEN")
user = login_auth(my_token, "Lucik19")
user_git = User_GitHub(user, "public")
user_git.repos_user.append("repo")
assessment = ProfileAssessment(user_git)

@pytest.mark.parametrize("frequency_commits, expected_score", [(1 , 3.03), (0.5, 3.89), (2, 1.84),
                                                               (23 , 0), (0.01, 4.98),
                                                               (0, 5.0), ("NULL", 0)])
def test_frequency_commits_to_score_exp(frequency_commits, expected_score):
    coefficient_frequency_commits = 5
    actual_score =  round(assessment.frequency_commits_to_score_exp(frequency_commits, coefficient_frequency_commits), 2)
    assert actual_score == expected_score


@pytest.mark.parametrize("followers, expected_score" , [(0, 0), (10, 2.7), (100, 5.41),
                                                        (1000, 8.11), (3000, 9.4),
                                                        (5000, 10.0), (5500, 10)])
def test_followers_to_score_log(followers, expected_score):
    actual_score = round(assessment.followers_to_score_log(followers), 2)
    assert actual_score == expected_score

@pytest.mark.parametrize("following, expected_score" , [(0, 0), (5, 0.91), (10, 1.3), (100, 2.61),
                                                        (150, 2.84), (200, 3), (400, 3)])
def test_following_to_score_log(following, expected_score):
    actual_score = round(assessment.following_to_score_log(following), 2)
    assert actual_score == expected_score


@pytest.mark.parametrize("language, expected_score" , [(0, 0), (1, 1.35), (3, 4.29), (5, 6.29),
                                                       (7, 7.61), (10, 9), (15, 9)])
def test_language_to_score_log(language, expected_score):
    actual_score = round(assessment.language_to_score_log(language), 2)
    assert actual_score == expected_score

@pytest.mark.parametrize("in_day_commits, day_work, expected_score", [(2, 1, 2.5), (2, 2, 10.0), (1.76, 1, 2.04),
                                                                      (1.76, 2, 8.16), (1000, 1, 5),
                                                                      (1000, 2 ,20), (1000, 3, 20)])
def test_in_day_commits(in_day_commits, day_work, expected_score):
    max_value_in_day_commits_repo = 4
    coefficient_in_day_commits_repo = 20
    coefficient_one_day_commits_repo = 5
    coefficient_in_day_commits = (coefficient_in_day_commits_repo if day_work != 1 else coefficient_one_day_commits_repo)
    score = round(assessment.in_day_commits_to_score_log(in_day_commits, coefficient_in_day_commits, max_value_in_day_commits_repo), 2)
    assert score == expected_score



@pytest.mark.parametrize("add_line, expected_score", [(5, 5.24), (10, 7.5), (20, 9.76), (40, 12.02),
                                                      (80, 14.27), (160, 15), (320, 15)])
def test_add_line_log(add_line, expected_score):
    actual_score = round(assessment.add_line_log(add_line), 2)
    assert actual_score == expected_score



@pytest.mark.parametrize("frequency, in_day_commits, count_commits, num_repos, expected_score", [(5, 5, 9 , 25, 30.0),
                                                                                                 (0.01, 0.01, 0.01, 1, 0.32),
                                                                                                 (2.5, 2.5, 4.5, 13, 15.22),
                                                                                                 (4, 4, 8, 100, 27.04)])
def test_evaluate_repositories(frequency, in_day_commits, count_commits, num_repos, expected_score):
    actual_score = round(assessment.evaluate_repositories(frequency, in_day_commits, count_commits, num_repos), 2)
    assert actual_score == expected_score


@pytest.mark.parametrize("repos_log, created_update, expected_score" , [(30, 36, 18.0),(0.01, 0, 0.02),(15, 18, 13.84),(29, 100, 17.9)])
def test_created_update_to_score_linear(repos_log, created_update, expected_score):
    actual_score = round(assessment.created_update_to_score_linear(repos_log , created_update), 2)
    assert actual_score == expected_score


@pytest.mark.parametrize("frequency, in_day_commits, count_commits, count_day, expected_score", [(20, 20, 30, 10, 10.0),
                                                                                                 (0.01, 0.01, 0.01, 1, 0.23),
                                                                                                 (10, 10, 15, 5, 5.0),
                                                                                                 (19, 19, 29, 100, 9.79)])
def test_days_repo(frequency, in_day_commits, count_commits, count_day, expected_score):
    actual_score = round(assessment.days_repo(frequency, in_day_commits, count_commits, count_day), 2)
    assert actual_score == expected_score


@pytest.mark.parametrize("frequency, in_day_commits, count_commits,add_line, del_line, count_day, expected_score", [(13, 13, 24, 15, 5, 10, 10.0),
                                                                                                                    (0.01, 0.01, 0.01, 0.01, 0.01, 1, 0.2),
                                                                                                                    (6.5, 6.5, 12, 7.5, 2.5, 5.0, 5.69),
                                                                                                                    (12, 12, 23, 14, 4, 100, 9.62)])
def test_days_main_repo(frequency, in_day_commits, count_commits, add_line, del_line, count_day, expected_score):
    actual_score = round(assessment.days_main_repo(frequency, in_day_commits, count_commits, add_line, del_line, count_day), 2)
    assert actual_score == expected_score


"""testing the repository evaluation method for separate analysis"""
@pytest.mark.parametrize("my_token, login", [(my_token, "MorozkoArt"), (my_token, "ProNinjaDev")])
def test_tournament(my_token, login):
    public_or_private = "public"
    repos = login_auth(my_token, login).get_repos()
    for repo in repos:
        user_repo = User_repo(repo, public_or_private)
        score = user_repo.tournament()
        print(f"\n{repo.name} - {score},   ({user_repo.commits_count} , {user_repo.commits_frequency}, {user_repo.commits_in_day}, "
                 f"{user_repo.days_work}, {user_repo.stargazers_count}, {user_repo.forks})")








