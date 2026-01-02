import os
from StartMethods.M_Start_UserAssessment_generation import start_user_assessment_generation
from StartMethods.M_Authentication import login_auth, login_token

def authenticate_user(my_token):
    auth_method = os.getenv("AUTH_METHOD")
    access_level = os.getenv("ACCESS_LEVEL")
    print(auth_method)

    if auth_method == "login":
        username = os.getenv("GITHUB_USERNAME")
        print(username)
        return login_auth(my_token, username), access_level

    return login_token(os.getenv("GITHUB_USER_TOKEN")), access_level

def option_start(my_token):
    user, access = authenticate_user(my_token)
    start_user_assessment_generation(user, access)