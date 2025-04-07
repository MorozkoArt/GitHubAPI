import pandas as pd
from faker import Faker
import random
from C_Assessment import Assessment
import os


fake = Faker()
assessment = Assessment()
data = []
for _ in range(150):
    user = fake.user_name()
    followers = random.randint(0, 5000)
    following = random.randint(0, 200)
    hireable = random.randint(0, 1)
    repos = random.randint(1, 30)
    created_update = random.randint(1, 36)
    plan = random.randint(0, 1)
    blog = random.randint(0, 1)
    company = random.randint(0, 1)
    org = random.randint(0, 7)
    langs = random.randint(1, 12)
    freq_commits = round(random.uniform(0.0, 20), 2)
    in_day_commits = round(random.uniform(0.1, 6), 2)
    count_commits = round(random.uniform(1, 100), 2)
    forks = random.randint(0, 13)
    stars = random.randint(0, 1000)
    contributors = random.randint(1, 12)

    created_update_r = random.randint(1, 365 * 3)
    commits_repo = random.randint(1, 100)
    frequency_repo = round(random.uniform(0.1, 5), 2)
    in_day_repo = round(random.uniform(0.1, 3), 2)
    add_line = random.randint(0, 500)
    del_line = random.randint(0, 300)
    count_views = random.randint(0, 3000)

    followers_s = round(assessment.followers_to_score_log(followers), 2)
    following_s = round(assessment.following_to_score_log(following), 2)
    hireable_s = assessment.hireable_to_score(hireable)
    plan_s = assessment.plan_to_score(plan)
    blog_s = assessment.blog_to_score(blog)
    company_s = assessment.company_to_score(company)
    org_s = assessment.org_to_score_log(org)
    langs_s = assessment.language_to_score_log(langs)
    freq_commits_s = assessment.frequency_commits_to_score_exp(repos, freq_commits, assessment.field_score["frequencyCommits"])
    in_day_commits_s = assessment.in_day_commits_to_score_log(in_day_commits, assessment.field_score["inDayCommits"], assessment.max_value["inDayCommits"])
    count_commits_s = assessment.count_commits_to_score_log(count_commits, assessment.field_score["countCommits"], assessment.max_value["countCommits"])
    forks_s = assessment.forks_to_score_log(forks)
    stars_s = assessment.stargazers_count_to_score_log(stars)
    contributors_s = assessment.contributors_count_to_score_log(contributors)
    repos_s = assessment.evaluate_repositories(freq_commits_s, in_day_commits_s, count_commits_s, repos)
    created_update_s = assessment.created_update_to_score_linear(repos_s, created_update)
    count_views_s = assessment.count_views_count_to_score_log(count_views)


    data.append([
        user,
        followers,
        following,
        hireable,
        repos,
        created_update,
        plan,
        blog,
        company,
        org,
        langs,
        freq_commits,
        in_day_commits,
        count_commits,
        forks,
        stars,
        contributors,
        count_views,
        created_update_r,
        commits_repo,
        frequency_repo,
        in_day_repo,
        add_line,
        del_line,

        followers_s,
        following_s,
        hireable_s,
        plan_s,
        blog_s,
        company_s,
        org_s,
        langs_s,
        freq_commits_s,
        in_day_commits_s,
        count_commits_s,
        forks_s,
        stars_s,
        contributors_s,
        repos_s,
        created_update_s,
        count_views_s
    ])

columns = [
    "user", "followers", "following", "hireable", "repos", "created_update",
    "plan", "blog", "company", "org", "languages", "frequencyCommits",
    "inDayCommits", "countCommits", "forks", "stargazers_count",
    "contributors_count", "created_update_r", "commits_repo",
    "frequency_repo", "inDay_repo", "count_views", "addLine", "delLine",

    "followers_s", "following_s", "hireable_s", "plan_s", "blog_s", "company_s",
    "org_s", "langs_s", "freq_commits_s", "in_day_commits_s", "count_commits_s",
    "forks_s", "stars_s", "contributors_s", "repos_s", "created_update_s", "count_views_s"
]

df = pd.DataFrame(data, columns=columns)
base_dir = "C:/PycharmProjects/GitHubAPI"
path = os.path.join(base_dir, "data", "training.csv")
df.to_csv(path, index=False)

