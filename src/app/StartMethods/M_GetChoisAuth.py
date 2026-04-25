import os
from StartMethods.M_Start_UserAssessment_generation import start_user_assessment_generation
from StartMethods.M_Authentication import login_auth, login_token


def authenticate_user(my_token: str) -> tuple:
    auth_method = os.getenv("AUTH_METHOD", "login")

    if auth_method == "login":
        username = os.getenv("GITHUB_USERNAME")
        if not username:
            raise RuntimeError("GITHUB_USERNAME is required when AUTH_METHOD=login")
        return login_auth(my_token, username), "public"

    user_token = os.getenv("GITHUB_USER_TOKEN")
    if not user_token:
        raise RuntimeError("GITHUB_USER_TOKEN is required when AUTH_METHOD=token")
    return login_token(user_token), "private"


def option_start(my_token: str) -> None:
    user, access = authenticate_user(my_token)
    start_user_assessment_generation(user, access)