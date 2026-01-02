from dotenv import load_dotenv
load_dotenv()

import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from StartMethods.M_GetChoisAuth import option_start

if __name__ == "__main__":
    my_token = os.getenv("GITHUB_TOKEN")
    print(my_token)
    if not my_token:
        print("GITHUB_TOKEN is not set")
        sys.exit(1)

    option_start(my_token)