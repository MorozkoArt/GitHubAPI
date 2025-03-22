from StartMethods.M_Start_UserAssessment_generation import Start_userAssessment_generation
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken

def Get_user_auth_method():
    print("How would you like to authenticate? \n"
          " 1 - Login with username \n"
          " 2 - Login with username and password \n"
          " 3 - Login with access token")
    while True:
        choice = input("Enter the number of the authentication method (1 to 3): ")
        if choice in ("1", "2", "3"):
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def authenticate_user(method, MyToken=None):
    if method == "1":
        login = input("Enter the username: ")
        return Login(MyToken, login), "public"
    elif method == "2":
        login = input("Enter the username: ")
        password = input("Enter the password: ")
        return LoginPassword(login, password), "private"
    elif method == "3":
        access_token = input("Enter the access token: ")
        return LoginToken(access_token), "private"

def Chois_start(var_aut, MyToken=None):
    try:
        user, publicOrPrivate = authenticate_user(var_aut, MyToken)
        Start_userAssessment_generation(user, publicOrPrivate)
    except Exception as e:
        print(f"An error occurred: {e}")