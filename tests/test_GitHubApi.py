from github import Github, Auth
from M_TakeData import take_data
import os
import pytest

MyToken = os.environ.get("GITHUB_TOKEN")

@pytest.mark.parametrize("auth_method, auth_data, expected_login, expected_publicOrPrivate, var_kod, var_kod_2",
                         [(1, MyToken, "MorozkoArt", "public", 1, 2)])
def test_FullData(auth_method, auth_data, expected_login, expected_publicOrPrivate, var_kod, var_kod_2):
    try:
        if auth_method == 1:
            g = Github(auth_data)
            user = g.get_user(expected_login)  # Use expected_login for user retrieval
            take_data(user, expected_publicOrPrivate, var_kod, var_kod_2)

    except Exception as e:
        pytest.fail(f"Test failed: {e}")