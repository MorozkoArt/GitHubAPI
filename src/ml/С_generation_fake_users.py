from C_Assessment import Assessment
from typing import Dict, Any
import pandas as pd
import random
import os



class GitHubUserGenerator:
    def __init__(self):
        self.assessment = Assessment()
        self.columns = [
            "followers", "following", "hireable", "repos", "created_update",
            "plan", "blog", "company", "org", "languages", "forks", "stars", "avg_cont",
            "avg_a_days", "frequencyCommits", "inDayCommits", "countCommits", "avg_views",

            "forks_r", "stars_r",
            "cont_count", "active_days_r", "commits_repo",
            "frequency_repo", "inDay_repo", "addLine", "delLine", "count_views",

            "followers_s", "following_s", "hireable_s", "repos_s", "created_update_s",
            "plan_s", "blog_s", "company_s", "org_s", "langs_s", "forks_s", "stars_s",
            "avg_cont_s", "avg_a_days_s", "freq_commits_s", "in_day_commits_s",
            "count_commits_s", "avg_views_s",

            "forks_r_s", "stars_r_s", "contributors_s", "active_days_r_s", "commits_repo_s",
            "in_day_repo_s", "frequency_repo_s", "add_line_s", "del_line_s",
            "count_views_s"
        ]

    def _generate_user_data(self, user_type: str) -> dict[str | Any, int | Any] | None:
        if user_type == "low_values":
            return {
                "followers": 0,
                "following": 0,
                "hireable": 0,
                "repos": 0,
                "created_update": 0,
                "plan": 0,
                "blog": 0,
                "company": 0,
                "org": 0,
                "languages": 0,
                "forks": 0,
                "stars": 0,
                "avg_cont": 0,
                "avg_a_days": 0,
                "frequencyCommits": 0,
                "inDayCommits": 0,
                "countCommits": 0,
                "avg_views": 0,
                "forks_r": 0,
                "stars_r": 0,
                "cont_count": 0,
                "active_days_r": 0,
                "commits_repo": 0,
                "frequency_repo": -1,
                "inDay_repo": 0,
                "addLine": 0,
                "delLine": 0,
                "count_views": 0
            }
        elif user_type == "beginner":
            return {
                "followers": random.randint(0, 30),
                "following": random.randint(0, 10),
                "hireable": random.randint(0, 1),
                "repos": random.randint(1, 5),
                "created_update": random.randint(1, 4),
                "plan": random.randint(0, 1),
                "blog": random.randint(0, 1),
                "company": random.randint(0, 1),
                "org": random.randint(0, 2),
                "languages": random.randint(1, 3),
                "forks": random.randint(0, 5),
                "stars": random.randint(0, 5),
                "avg_cont": random.randint(0, 2),
                "avg_a_days": random.randint(0,3),
                "frequencyCommits": round(random.uniform(5.0, 20), 2),
                "inDayCommits": round(random.uniform(1, 2), 2),
                "countCommits": round(random.uniform(1, 10), 2),
                "avg_views": random.randint(0, 5),
                "forks_r": random.randint(0, 2),
                "stars_r": random.randint(0, 10),
                "cont_count": random.randint(1, 2),
                "active_days_r": random.randint(1, 5),
                "commits_repo": random.randint(1, 10),
                "frequency_repo": round(random.uniform(4, 10), 2),
                "inDay_repo": round(random.uniform(1.0, 2), 2),
                "addLine": random.randint(0, 15),
                "delLine": random.randint(0, 8),
                "count_views": random.randint(0, 50)
            }
        elif user_type == "intermediate":
            return {
                "followers": random.randint(5, 1000),
                "following": random.randint(10, 60),
                "hireable": random.randint(0, 1),
                "repos": random.randint(0, 15),
                "created_update": random.randint(4, 20),
                "plan": random.randint(0, 1),
                "blog": random.randint(0, 1),
                "company": random.randint(0, 1),
                "org": random.randint(0, 4),
                "languages": random.randint(1, 7),
                "forks": random.randint(0, 15),
                "stars": random.randint(0, 20),
                "avg_cont": random.randint(0, 4),
                "avg_a_days": random.randint(0, 5),
                "frequencyCommits": round(random.uniform(2.4, 5), 2),
                "inDayCommits": round(random.uniform(2, 3.5), 2),
                "countCommits": round(random.uniform(10, 38), 2),
                "avg_views": random.randint(0, 20),
                "forks_r": random.randint(0, 6),
                "stars_r": random.randint(5, 200),
                "cont_count": random.randint(0, 6),
                "active_days_r": random.randint(3, 8),
                "commits_repo": random.randint(10, 30),
                "frequency_repo": round(random.uniform(1.8, 4), 2),
                "inDay_repo": round(random.uniform(2.0, 3.0), 2),
                "addLine": random.randint(15, 65),
                "delLine": random.randint(8, 18),
                "count_views": random.randint(0, 550)
            }
        elif user_type == "advanced":  # advanced
            return {
                "followers": random.randint(1000, 5000),
                "following": random.randint(60, 200),
                "hireable": random.randint(0, 1),
                "repos": random.randint(15, 30),
                "created_update": random.randint(20, 36),
                "plan": random.randint(0, 1),
                "blog": random.randint(0, 1),
                "company": random.randint(0, 1),
                "org": random.randint(4, 7),
                "languages": random.randint(7, 12),
                "forks": random.randint(15, 500),
                "stars": random.randint(20, 1000),
                "avg_cont": random.randint(4, 10),
                "avg_a_days": random.randint(5, 20),
                "frequencyCommits": round(random.uniform(0.0, 2.4), 2),
                "inDayCommits": round(random.uniform(3.5, 7), 2),
                "countCommits": round(random.uniform(38, 150), 2),
                "avg_views": random.randint(20, 400),
                "forks_r": random.randint(6, 13),
                "stars_r": random.randint(200, 1000),
                "cont_count": random.randint(6, 12),
                "active_days_r": random.randint(8, 25),
                "commits_repo": random.randint(30, 170),
                "frequency_repo": round(random.uniform(0.0, 1.8), 2),
                "inDay_repo": round(random.uniform(3.0, 5), 2),
                "addLine": random.randint(65, 150),
                "delLine": random.randint(18, 50),
                "count_views": random.randint(550, 3000)
            }
        elif user_type == "maximum_values":
            return {
                "followers": self.assessment.max_value["followers"],
                "following": self.assessment.max_value["following"],
                "hireable": 1,
                "repos": self.assessment.max_value["repos"],
                "created_update": self.assessment.max_value["created_update"],
                "plan": 1,
                "blog": 1,
                "company": 1,
                "org": self.assessment.max_value["org"],
                "languages": self.assessment.max_value["languages"],
                "forks": self.assessment.max_value["forks"],
                "stars": self.assessment.max_value["stars"],
                "avg_cont": self.assessment.max_value["avg_cont"],
                "avg_a_days": self.assessment.max_value["avg_a_days"],
                "frequencyCommits": 0,
                "inDayCommits": self.assessment.max_value["inDayCommits"],
                "countCommits": self.assessment.max_value["countCommits"],
                "avg_views": self.assessment.max_value["avg_views"],
                "forks_r": self.assessment.max_value["forks_r"],
                "stars_r": self.assessment.max_value["stars_r"],
                "cont_count": self.assessment.max_value["cont_count"],
                "active_days_r": self.assessment.max_value["active_days_r"],
                "commits_repo": self.assessment.max_value["commits_repo"],
                "frequency_repo": 0,
                "inDay_repo": self.assessment.max_value["inDay_repo"],
                "addLine": self.assessment.max_value["addLine"],
                "delLine": self.assessment.max_value["delLine"],
                "count_views": self.assessment.max_value["count_views"]
            }

    def _calculate_scores(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        scores = {}

        scores["followers_s"] = self.assessment.followers_to_score_log(user_data["followers"])
        scores["following_s"] = self.assessment.following_to_score_log(user_data["following"])
        scores["hireable_s"] = self.assessment.hireable_to_score(user_data["hireable"])
        scores["plan_s"] = self.assessment.plan_to_score(user_data["plan"])
        scores["blog_s"] = self.assessment.blog_to_score(user_data["blog"])
        scores["company_s"] = self.assessment.company_to_score(user_data["company"])
        scores["org_s"] = self.assessment.org_to_score_log(user_data["org"])
        scores["langs_s"] = self.assessment.language_to_score_log(user_data["languages"])
        scores["forks_s"] = self.assessment.forks_to_score_log(user_data["forks"])
        scores["stars_s"] = self.assessment.stars_to_score_log(user_data["stars"])
        scores["avg_cont_s"] = self.assessment.avg_cont_to_score_log(user_data["avg_cont"])
        scores["avg_a_days_s"] = self.assessment.avg_a_days_to_score_log(user_data["avg_a_days"])
        scores["freq_commits_s"] = self.assessment.frequency_to_score_exp(user_data["repos"],user_data["frequencyCommits"])
        scores["in_day_commits_s"] = self.assessment.in_day_to_score_log(user_data["inDayCommits"])
        scores["count_commits_s"] = self.assessment.commits_to_score_log(user_data["countCommits"])
        scores["avg_views_s"] = self.assessment.avg_views_to_score_log(user_data["avg_views"])
        scores["repos_s"] = self.assessment.evaluate_repositories(
            scores["freq_commits_s"],
            scores["in_day_commits_s"],
            scores["count_commits_s"],
            user_data["repos"]
        )
        scores["created_update_s"] = self.assessment.created_update_to_score_linear(
            scores["repos_s"],
            user_data["created_update"]
        )

        scores["forks_r_s"] = self.assessment.forks_r_to_score_log(user_data["forks_r"])
        scores["stars_r_s"] = self.assessment.stars_r_to_score_log(user_data["stars_r"])
        scores["contributors_s"] = self.assessment.contributors_count_to_score_log(user_data["cont_count"])
        scores["commits_repo_s"] = self.assessment.commits_r_to_score_log(user_data["commits_repo"])
        scores["frequency_repo_s"] = self.assessment.frequency_r_to_score_exp(user_data["repos"], user_data["frequency_repo"], user_data["active_days_r"])
        scores["in_day_repo_s"] = self.assessment.in_day_r_to_score_log(user_data["inDay_repo"],user_data["active_days_r"])
        scores["add_line_s"] = self.assessment.add_line_log(user_data["addLine"])
        scores["del_line_s"] = self.assessment.del_line_log(user_data["delLine"])
        scores["count_views_s"] = self.assessment.count_views_count_to_score_log(user_data["count_views"])
        scores["active_days_r_s"] = self.assessment.days_main_repo(
            scores["frequency_repo_s"],
            scores["in_day_repo_s"],
            scores["commits_repo_s"],
            scores["add_line_s"],
            scores["del_line_s"],
            user_data["active_days_r"]
        )
        return scores

    def generate_users(self, count: int = 450) -> pd.DataFrame:
        data = []
        for i in range(count):
            if i == 0:
                user_type = "low_values"
            elif 1 <= i < 150:
                user_type = "beginner"
            elif 150 <= i < 300:
                user_type = "intermediate"
            elif 300 <= i < 449:
                user_type = "advanced"
            else:
                user_type = "maximum_values"

            user_data = self._generate_user_data(user_type)
            scores = self._calculate_scores(user_data)

            row = {}
            row.update(user_data)
            row.update(scores)
            data.append(row)

        return pd.DataFrame(data, columns=self.columns)

    def save_to_csv(self, df: pd.DataFrame, path: str) -> None:
        df.to_csv(path, index=False)