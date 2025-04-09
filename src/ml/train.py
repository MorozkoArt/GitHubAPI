import pandas as pd
from sklearn.model_selection import train_test_split
from С_generation_fake_users import GitHubUserGenerator
import os

base_dir = "C:/PycharmProjects/GitHubAPI"
path = os.path.join(base_dir, "data", "training.csv")

generator = GitHubUserGenerator()
dff = generator.generate_users()
generator.save_to_csv(dff, path)

df = pd.read_csv(path)

X = df.drop(columns=["followers", "following", "hireable", "repos", "created_update",
    "plan", "blog", "company", "org", "languages", "forks", "stars", "frequencyCommits",
    "inDayCommits", "countCommits", "forks_r", "stars_r",
    "contributors_count", "active_days_r", "commits_repo",
    "frequency_repo", "inDay_repo", "addLine", "delLine", "count_views"])

y = df[["followers_s", "following_s", "hireable_s", "repos_s", "created_update_s", "plan_s", "blog_s", "company_s",
    "org_s", "langs_s", "forks_s", "stars_s", "freq_commits_s", "in_day_commits_s", "count_commits_s",
    "forks_r_s", "stars_r_s", "contributors_s", "active_days_r_s", "commits_repo_s", "in_day_repo_s",
    "frequency_repo_s", "add_line_s", "del_line_s","count_views_s"]]


X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

