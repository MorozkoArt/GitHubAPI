import os
from common.Utils.M_ValidateEnv import validate_env
from StartMethods.M_GetChoisAuth import option_start

if __name__ == "__main__":
    validate_env()
    option_start(os.getenv("GITHUB_TOKEN"))