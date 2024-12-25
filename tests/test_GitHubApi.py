import os
import pytest
import textwrap
from StartMethods.M_Start_UserAssessment_generation import (Start_user_generation, Start_assessment_generation
, Start_assessment_generation_empty, Start_mainRepo_generation)
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken

# Пользователь "Lucik19, не имеет репозиториев
# Пользователь "Sahil0101", имеет только один пустой репозиторий
# Пользователь, "Arun953", имеет тололько один репозиторий, не содержащий файлов с кодом

MyToken = os.environ.get("GITHUB_TOKEN")
@pytest.mark.parametrize("MyToken, login,  var_kod, var_kod_2",
                         [(MyToken, "Lucik19", 1, 1),
                          (MyToken, "Sahil0101", 1, 1),
                          (MyToken, "Arun953", 1, 1),
                          (MyToken, "ProNinjaDev", 1, 2),
                          (MyToken, "MorozkoArt", 1, 1),
                          (MyToken, "Tulen4ick", 1, 2),
                          (MyToken, "ArtemFedorov2004", 1, 2)])
def test_FullData(MyToken, login, var_kod, var_kod_2):
    publicOrPrivate = "public"
    user = Login(MyToken, login)
    user_git = Start_user_generation(user, publicOrPrivate)
    if user_git.repos.totalCount == 0:
        Start_assessment_generation_empty(user_git)
    else:
        if user_git.main_repo_name:
            if var_kod == 1:
                contentKod = Start_mainRepo_generation(user_git)
            Start_assessment_generation(user_git, var_kod, var_kod_2)
        else:
            Start_assessment_generation_empty(user_git)


