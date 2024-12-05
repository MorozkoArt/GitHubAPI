import os
from StartMethods.M_GetChoisAuth import Chois_start, Get_user_auth_method

if __name__ == "__main__":
    MyToken = os.environ.get("GITHUB_TOKEN")
    Chois_start(Get_user_auth_method(), MyToken)


