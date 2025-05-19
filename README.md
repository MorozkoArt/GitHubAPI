<div id="header" align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGQ5eWhlcHZ0dTd3bWEzcmk5OXJ1YWt2aTVtb3gzcnV4bDNoYWxsbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yf5t7jramBz6YN9w0U/giphy.gif?raw=true" width="400"/>
</div>

<div id="header" align="center">
    <h1>🎨Compiling an information portrait based on a profile on GitHub </h1>
    <h3>💻Practice project</h3>
</div>

---
### Brief information about the project🌐:
- *💾 A Python program that receives user data via the GitHub API and gives a numerical score to the profile, and the score value shows the user's activity level and programming skills*
- *📑 MyToken = os.environ.get("GITHUB_TOKEN") - a string with a token, for the program to work in a variable environment, you need to create such a variable and place your access token there. [Information on how to do this](https://remontka.pro/environment-variables-windows/?ysclid=m5cn3cte63157731913)*
- *💿 Full information is published on my [google drive](https://drive.google.com/drive/folders/18Q0nS8e0jUeByKjYreqZ1MXWn0KfvMVV?usp=drive_link)*
---
### Language👅 and tool🔧:
<img src="https://raw.githubusercontent.com/MorozkoArt/MorozkoArt/446de453fb12c56c11adfb43cde081d484777abb/Resources/python-original.svg" title="python" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/MorozkoArt/MorozkoArt/446de453fb12c56c11adfb43cde081d484777abb/Resources/pycharm-original.svg" title="pycharm" width="40" height="40"/>&nbsp;
---

## Main features

1. **GitHub Profile Analysis**:
   - Evaluating user activity
   - Analyze repositories and code
   - Generate a comprehensive report

2. **Machine Learning**:
   - Predicting profile quality
   - Evaluating contributions to projects

3. **Working with the GitHub API**:
   - Multiple authentication methods
   - Getting detailed information about users

## Installation and startup

1. Establish dependencies:
```bash
pip install -r requirements.txt
```

2. Set the environment variables:
```bash
export GITHUB_TOKEN="your_github_token"
```

3. Start the project:
```bash
python main.py
```

## Project Architecture

```plaintext
📂project/
├── 📂src/
│   ├──📂api/
│   │   ├──📂Assessment         # User evaluation techniques
│   │   ├──📂Config/            # Configuration files
│   │   ├──📂Interface/         # Visualization techniques
│   │   ├──📂StartMethods/      # Startup methods
│   │   ├──📂User_and_Repo/     # Classes for working with users
│   └── ml/
│       ├──📂GenerationUsers/   # Data generation
│       ├──📂ForModel/          # Model ML
│       └──📄train.py           # Model training
├──📂data/                      # Training data
├──📂tests/                     # Test directory
└──📄main.py                    # Main script
```

## Example output

```
User profile assessment results - MorozkoArt 

Profile data and their assessment:
+-------------------------------------------------+---------------------------------------+------------+
| Field name                                      | Significance                          | Assessment |
+-------------------------------------------------+---------------------------------------+------------+
| Username                                        | MorozkoArt                            |            |
+-------------------------------------------------+---------------------------------------+------------+
| Profile access                                  | public                                |            |
+-------------------------------------------------+---------------------------------------+------------+
| Number of followers                             | 7                                     |       1.37 |
+-------------------------------------------------+---------------------------------------+------------+
| Number of following                             | 17                                    |        1.6 |
+-------------------------------------------------+---------------------------------------+------------+
| Hireable status                                 | True                                  |          1 |
+-------------------------------------------------+---------------------------------------+------------+
| Number of private repositories                  | 2                                     |       9.33 |
| Number of public repositories                   | 49                                    |            |
+-------------------------------------------------+---------------------------------------+------------+
| Account creation date                           | 2024-06-07 13:38:22+00:00             |            |
+-------------------------------------------------+---------------------------------------+------------+
| Last update date                                | 2025-04-29 16:31:32+00:00             |            |
+-------------------------------------------------+---------------------------------------+------------+
| Account age                                     | 10 Month(s)                           |        9.0 |
+-------------------------------------------------+---------------------------------------+------------+
| Average number of commits per repository        | 10.98                                 |       3.61 |
+-------------------------------------------------+---------------------------------------+------------+
| Average commit frequency (days between commits) | 5.58                                  |       0.31 |
+-------------------------------------------------+---------------------------------------+------------+
| Average number of commits per day               | 2.88                                  |       2.95 |
+-------------------------------------------------+---------------------------------------+------------+
| Subscription plan                               | Plan(name="free")                     |          0 |
+-------------------------------------------------+---------------------------------------+------------+
| Blog                                            | https://vk.com/poc_norm               |          2 |
+-------------------------------------------------+---------------------------------------+------------+
| Company                                         | What Entertainment                    |          3 |
+-------------------------------------------------+---------------------------------------+------------+
| Organizations                                   | BigShishkaLove                        |       0.86 |
+-------------------------------------------------+---------------------------------------+------------+
| Programming languages                           | C++, Python, C#, HTML, SCSS, CMake, C |       6.76 |
+-------------------------------------------------+---------------------------------------+------------+
Profile assessment: 41.8

...
```

## Technologies used

| Technology   | Assignment                  | Version |
|--------------|-----------------------------|---------|
| PyTorch      | Machine Learning            | 2.0+    |
| PyGithub     | Working with the GitHub API | 1.55+   |
| PrettyTable  | Data Visualization          | 3.0+    |
| tqdm         | Progress Bars               | 4.0+    |
| pandas       | data processing             | 1.5+    |
| scikit-learn | Evaluation Metrics          | 1.2+    |
| GPT-4        | Code Analysis               | -       |

## Конфигурация

Evaluation parameters are customized via JSON files:
- `field_score.json` - weights for different metrics
- `max_value.json` - maximum values for normalization
- `tour_field.json` - tournament evaluation parameters

## Additional features

1. **Synthetic Data Generation**:
   - Creates profiles of different levels (beginner, intermediate, expert)
   - Used for model training

2. **Detailed Repository Analysis**:
   - Activity estimation
   - Commits analysis
   - Popularity estimation

3. **Saving results**:
   - TXT format
   - With a choice of saving location


