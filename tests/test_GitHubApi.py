import os
import pytest
import textwrap
from StartMethods.M_Start_UserAssessment_generation import (Start_user_generation, Start_assessment_generation
, Start_assessment_generation_empty)
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken


MyToken = os.environ.get("GITHUB_TOKEN")

@pytest.mark.parametrize("MyToken, login,  var_kod, var_kod_2",
                         [(MyToken, "ProNinjaDev", 2, 2),
                          (MyToken, "MorozkoArt", 1, 2),
                          (MyToken, "Tulen4ick", 1, 1),
                          (MyToken, "ArtemFedorov2004", 1, 2)])
def test_FullData(MyToken, login, var_kod, var_kod_2):
    try:
        publicOrPrivate = "public"
        user = Login(MyToken, login)
        user_git, contentKod = Start_user_generation(user, publicOrPrivate)
        if len(user_git.repos_user) == 0:
            Start_assessment_generation_empty(user_git)
        else:
            Start_assessment_generation(user_git, var_kod, var_kod_2)

    except Exception as e:
        pytest.fail(f"Test failed: {e}")