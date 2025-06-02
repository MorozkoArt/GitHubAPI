from src.app.StartMethods.M_Start_UserAssessment_generation import start_user_assessment_generation
from src.app.StartMethods.M_Authentication import login_auth, login_token

def get_user_auth_method():
    print("How would you like to authenticate? \n"
          " 1 - Login with username \n"
          " 2 - Login with access token")
    while True:
        choice = input("Enter the number of the authentication method (1 or 2): ")
        if choice in ("1", "2"):
            return choice
        print("Invalid choice. Please enter 1 or 2")

def authenticate_user(method, my_token=None):
    if method == "1":
        login = input("Enter the username: ")
        return login_auth(my_token, login), "public"
    elif method == "2":
        access_token = input("Enter the access token: ")
        return login_token(access_token), "private"

def option_start(var_aut, my_token=None):
    try:
        user, public_or_private = authenticate_user(var_aut, my_token)
        start_user_assessment_generation(user, public_or_private)
    except Exception as e:
        print(f"An error occurred: {e}")