import os
from api.StartMethods.M_GetChoisAuth import option_start, get_user_auth_method

if __name__ == "__main__":
    my_token = os.environ.get("GITHUB_TOKEN")
    option_start(get_user_auth_method(), my_token)


