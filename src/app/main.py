import os
import sys
from StartMethods.M_GetChoisAuth import option_start

if __name__ == "__main__":
    my_token = os.getenv("GITHUB_TOKEN")
    if not my_token:
        print("GITHUB_TOKEN is not set")
        sys.exit(1)

    option_start(my_token)