import pandas as pd
from faker import Faker
import random
from C_Assessment import Assessment
import os
from typing import Dict, Any


class GitHubUserGenerator:
    def __init__(self):
        self.fake = Faker()
        self.assessment = Assessment()
        self.columns = [
            "user", "followers", "following", "hireable", "repos", "created_update",
            "plan", "blog", "company", "org", "languages", "frequencyCommits",
            "inDayCommits", "countCommits", "forks", "stargazers_count",
            "contributors_count", "created_update_r", "commits_repo",
            "frequency_repo", "inDay_repo", "addLine", "delLine", "count_views",
            "followers_s", "following_s", "hireable_s", "repos_s", "created_update_s",
            "plan_s", "blog_s", "company_s", "org_s", "langs_s", "freq_commits_s",
            "in_day_commits_s", "count_commits_s", "forks_s", "stars_s",
            "contributors_s", "created_update_r_s", "commits_repo_s",
            "in_day_repo_s", "frequency_repo_s", "add_line_s", "del_line_s",
            "count_views_s"
        ]

    def _generate_user_data(self, user_type: str) -> Dict[str, Any]:
        if user_type == "beginner":
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
                "frequencyCommits": round(random.uniform(5.0, 20), 2),
                "inDayCommits": round(random.uniform(1, 2), 2),
                "countCommits": round(random.uniform(1, 10), 2),
                "forks": random.randint(0, 2),
                "stargazers_count": random.randint(0, 10),
                "contributors_count": random.randint(1, 2),
                "created_update_r": random.randint(1, 5),
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
                "frequencyCommits": round(random.uniform(2.4, 5), 2),
                "inDayCommits": round(random.uniform(2, 3.5), 2),
                "countCommits": round(random.uniform(10, 38), 2),
                "forks": random.randint(0, 6),
                "stargazers_count": random.randint(5, 200),
                "contributors_count": random.randint(0, 6),
                "created_update_r": random.randint(3, 8),
                "commits_repo": random.randint(10, 30),
                "frequency_repo": round(random.uniform(1.8, 4), 2),
                "inDay_repo": round(random.uniform(2.0, 3.0), 2),
                "addLine": random.randint(15, 65),
                "delLine": random.randint(8, 18),
                "count_views": random.randint(0, 550)
            }
        else:  # advanced
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
                "frequencyCommits": round(random.uniform(0.0, 2.4), 2),
                "inDayCommits": round(random.uniform(3.5, 7), 2),
                "countCommits": round(random.uniform(38, 150), 2),
                "forks": random.randint(6, 13),
                "stargazers_count": random.randint(200, 1000),
                "contributors_count": random.randint(6, 12),
                "created_update_r": random.randint(8, 14),
                "commits_repo": random.randint(30, 170),
                "frequency_repo": round(random.uniform(0.0, 1.8), 2),
                "inDay_repo": round(random.uniform(3.0, 5), 2),
                "addLine": random.randint(65, 150),
                "delLine": random.randint(18, 50),
                "count_views": random.randint(550, 3000)
            }

    def _calculate_scores(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        scores = {}

        scores["followers_s"] = round(self.assessment.followers_to_score_log(user_data["followers"]), 2)
        scores["following_s"] = round(self.assessment.following_to_score_log(user_data["following"]), 2)
        scores["hireable_s"] = self.assessment.hireable_to_score(user_data["hireable"])
        scores["plan_s"] = self.assessment.plan_to_score(user_data["plan"])
        scores["blog_s"] = self.assessment.blog_to_score(user_data["blog"])
        scores["company_s"] = self.assessment.company_to_score(user_data["company"])
        scores["org_s"] = self.assessment.org_to_score_log(user_data["org"])
        scores["langs_s"] = self.assessment.language_to_score_log(user_data["languages"])

        scores["freq_commits_s"] = self.assessment.frequency_commits_to_score_exp(
            user_data["repos"],
            user_data["frequencyCommits"],
            self.assessment.field_score["frequencyCommits"]
        )
        scores["in_day_commits_s"] = self.assessment.in_day_commits_to_score_log(
            user_data["inDayCommits"],
            self.assessment.field_score["inDayCommits"],
            self.assessment.max_value["inDayCommits"]
        )
        scores["count_commits_s"] = self.assessment.count_commits_to_score_log(
            user_data["countCommits"],
            self.assessment.field_score["countCommits"],
            self.assessment.max_value["countCommits"]
        )

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

        scores["forks_s"] = self.assessment.forks_to_score_log(user_data["forks"])
        scores["stars_s"] = self.assessment.stargazers_count_to_score_log(user_data["stargazers_count"])
        scores["contributors_s"] = self.assessment.contributors_count_to_score_log(user_data["contributors_count"])
        scores["commits_repo_s"] = self.assessment.count_commits_to_score_log(
            user_data["commits_repo"],
            self.assessment.field_score["commits_MainRepo"],
            self.assessment.max_value["countCommitsRepo"]
        )
        scores["frequency_repo_s"] = self.assessment.frequency_commits_repo(
            user_data["repos"],
            user_data["frequency_repo"],
            user_data["created_update_r"],
            self.assessment.field_score["frequencyComm_MainRepo"],
            self.assessment.field_score["oneDay_frequency"]
        )
        scores["in_day_repo_s"] = self.assessment.in_day_commits_repo(
            user_data["inDay_repo"],
            user_data["created_update_r"],
            self.assessment.field_score["inDayComm_MainRepo"],
            self.assessment.field_score["oneDay_inDay"]
        )
        scores["add_line_s"] = self.assessment.add_line_log(user_data["addLine"])
        scores["del_line_s"] = self.assessment.del_line_log(user_data["delLine"])
        scores["count_views_s"] = self.assessment.count_views_count_to_score_log(user_data["count_views"])
        scores["created_update_r_s"] = self.assessment.days_main_repo(
            scores["frequency_repo_s"],
            scores["in_day_repo_s"],
            scores["commits_repo_s"],
            scores["add_line_s"],
            scores["del_line_s"],
            user_data["created_update_r"]
        )
        return scores

    def generate_users(self, count: int = 450) -> pd.DataFrame:
        data = []
        for i in range(count):
            if i < 150:
                user_type = "beginner"
            elif 150 <= i < 300:
                user_type = "intermediate"
            else:
                user_type = "advanced"

            user_data = self._generate_user_data(user_type)
            scores = self._calculate_scores(user_data)

            row = {"user": self.fake.user_name()}
            row.update(user_data)
            row.update(scores)
            data.append(row)

        return pd.DataFrame(data, columns=self.columns)

    def save_to_csv(self, df: pd.DataFrame, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)