import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv("C:/PycharmProjects/GitHubAPI/data/training.csv")


X = df.drop(columns=["user", "followers", "following", "hireable", "repos", "created_update",
    "plan", "blog", "company", "org", "languages", "frequencyCommits",
    "inDayCommits", "countCommits", "forks", "stargazers_count",
    "contributors_count", "created_update_r", "commits_repo",
    "frequency_repo", "inDay_repo", "count_views", "addLine", "delLine"])

y = df[["followers_s", "following_s", "hireable_s", "plan_s", "blog_s", "company_s",
    "org_s", "langs_s", "freq_commits_s", "in_day_commits_s", "count_commits_s",
    "forks_s", "stars_s", "contributors_s", "repos_s", "created_update_s", "count_views_s"]]


X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

