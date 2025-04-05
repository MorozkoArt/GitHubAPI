import os
import pytest
import textwrap
from StartMethods.M_Start_UserAssessment_generation import (start_user_generation, start_assessment_generation
, start_assessment_generation_empty, start_main_repo_generation)
from StartMethods.M_Authentication import login_auth, login_password, login_token

my_token = os.environ.get("GITHUB_TOKEN")
@pytest.mark.parametrize("my_token, login,  var_kod, var_kod_2",
                         [(my_token, "Lucik19", 1, 1),
                          (my_token, "Sahil0101", 1, 1),
                          (my_token, "Arun953", 1, 1),
                          (my_token, "ProNinjaDev", 1, 2),
                          (my_token, "MorozkoArt", 1, 1),
                          (my_token, "Tulen4ick", 1, 2),
                          (my_token, "ArtemFedorov2004", 1, 2)])
def test_full_data(my_token, login, var_kod, var_kod_2):
    public_or_private = "public"
    user = login_auth(my_token, login)
    user_git = start_user_generation(user, public_or_private)
    if user_git.repos.totalCount == 0:
        start_assessment_generation_empty(user_git)
    else:
        if user_git.main_repo_name:
            if var_kod == 1:
                content_kod = start_main_repo_generation(user_git)
            start_assessment_generation(user_git, var_kod, var_kod_2)
        else:
            start_assessment_generation_empty(user_git)


