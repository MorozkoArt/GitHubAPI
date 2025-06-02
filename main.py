import os
import sys
from src.app.StartMethods.M_GetChoisAuth import option_start, get_user_auth_method

if __name__ == "__main__":
    my_token = os.environ.get("GITHUB_TOKEN")
    
    if my_token is None:
        print("Error: The GITHUB_TOKEN environment variable is not set")
        sys.exit(1)
    
    option_start(get_user_auth_method(), my_token)