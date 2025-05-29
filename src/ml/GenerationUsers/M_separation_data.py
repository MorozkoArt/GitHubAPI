import pandas as pd
from sklearn.model_selection import train_test_split


def separation(path):
    df = pd.read_csv(path)

    X = df.drop(columns=["followers", "following", "hireable","plan", "blog", 
        "company", "org", "languages", "forks", "stars", "avg_cont","avg_a_days", 
        "frequencyCommits", "inDayCommits", "countCommits", "avg_views", "repos", "created_update",
        "forks_r", "stars_r", "cont_count", "commits_repo","frequency_repo", "inDay_repo", 
        "addLine", "delLine", "count_views", "active_days_r"])

    y = df[["followers_s", "following_s", "hireable_s","plan_s", "blog_s", 
        "company_s", "org_s", "langs_s", "forks_s", "stars_s",
        "avg_cont_s", "avg_a_days_s", "freq_commits_s", "in_day_commits_s",
        "count_commits_s", "avg_views_s", "repos_s", "created_update_s",
        "forks_r_s", "stars_r_s", "contributors_s", "commits_repo_s", "frequency_repo_s", 
        "in_day_repo_s", "add_line_s", "del_line_s", "count_views_s", "active_days_r_s"]]

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    return X_train, y_train, X_val, y_val, X_test, y_test