from GenerationUsers.C_Assessment import Assessment
from typing import Dict, Any, List
import pandas as pd
import random


class GitHubUserGenerator:
    def __init__(self):
        self.assessment = Assessment()
        self.columns = [
            "followers", "following", "hireable", "plan", "blog",
            "company", "org", "languages", "forks", "stars", "avg_cont",
            "avg_a_days", "frequencyCommits", "inDayCommits", "countCommits",
            "avg_views", "repos", "created_update",
            "forks_r", "stars_r", "cont_count", "commits_repo", "frequency_repo",
            "inDay_repo", "addLine", "delLine", "count_views", "active_days_r",

            "followers_s", "following_s", "hireable_s", "plan_s", "blog_s",
            "company_s", "org_s", "langs_s", "forks_s", "stars_s",
            "avg_cont_s", "avg_a_days_s", "freq_commits_s", "in_day_commits_s",
            "count_commits_s", "avg_views_s", "repos_s", "created_update_s",
            "forks_r_s", "stars_r_s", "contributors_s", "commits_repo_s",
            "frequency_repo_s", "in_day_repo_s", "add_line_s", "del_line_s",
            "count_views_s", "active_days_r_s"
        ]

        self._intermediate_template = {
            "followers": 200,
            "following": 30,
            "hireable": 1,
            "plan": 0,
            "blog": 1,
            "company": 1,
            "org": 2,
            "languages": 4,
            "forks": 5,
            "stars": 10,
            "avg_cont": 2,
            "avg_a_days": 3,
            "frequencyCommits": 3.0,
            "inDayCommits": 2.0,
            "countCommits": 20.0,
            "avg_views": 10,
            "repos": 10,
            "created_update": 12,
            "forks_r": 3,
            "stars_r": 20,
            "cont_count": 3,
            "commits_repo": 20,
            "frequency_repo": 2.5,
            "inDay_repo": 2.5,
            "addLine": 30,
            "delLine": 10,
            "count_views": 25,
            "active_days_r": 5,
        }

    def _generate_user_data(self, user_type: str) -> Dict[str, Any] | None:
        if user_type == "absolute_zero":   return self._absolute_zero()
        if user_type == "field_zero":      return self._field_zero_random()
        if user_type == "sparse_zero":     return self._sparse_zero()
        if user_type == "low_values":      return self._low_values()
        if user_type == "beginner":        return self._beginner()
        if user_type == "intermediate":    return self._intermediate()
        if user_type == "advanced":        return self._advanced()
        if user_type == "maximum_values":  return self._maximum_values()
        return None

    def _absolute_zero(self) -> Dict[str, Any]:
        return {
            "followers": 0, "following": 0, "hireable": 0, "plan": 0,
            "blog": 0, "company": 0, "org": 0, "languages": 0,
            "forks": 0, "stars": 0, "avg_cont": 0, "avg_a_days": 0,
            "frequencyCommits": 666, "inDayCommits": 0, "countCommits": 0,
            "avg_views": 0, "repos": 0, "created_update": 0,
            "forks_r": 0, "stars_r": 0, "cont_count": 0, "commits_repo": 0,
            "frequency_repo": 666, "inDay_repo": 0, "addLine": 0,
            "delLine": 0, "count_views": 0, "active_days_r": 0,
        }

    def _field_zero_random(self) -> Dict[str, Any]:
        zeroable_fields = [
            "followers", "following", "hireable", "plan", "blog", "company",
            "org", "languages", "forks", "stars", "avg_cont", "avg_a_days",
            "inDayCommits", "countCommits", "avg_views", "repos",
            "forks_r", "stars_r", "cont_count", "commits_repo",
            "inDay_repo", "addLine", "delLine", "count_views", "active_days_r",
        ]
        data = dict(self._intermediate_template)
        data[random.choice(zeroable_fields)] = 0
        return data

    def _sparse_zero(self) -> Dict[str, Any]:
        sparse_fields = [
            "stars", "forks", "org", "avg_views",
            "avg_cont", "count_views", "stars_r", "forks_r",
        ]
        data = dict(self._intermediate_template)

        fields_to_zero = random.sample(sparse_fields, k=random.randint(1, 3))
        for f in fields_to_zero:
            data[f] = 0

        return data

    def _low_values(self) -> Dict[str, Any]:
        return {
            "followers": 0,
            "following": 0,
            "hireable": 0,
            "plan": 0,
            "blog": 0,
            "company": 0,
            "org": 0,
            "languages": random.randint(0, 1),
            "forks": 0,
            "stars": 0,
            "avg_cont": 0,
            "avg_a_days": random.randint(0, 1),
            "frequencyCommits": round(random.uniform(30.0, 60.0), 2),
            "inDayCommits": round(random.uniform(0, 1), 2),
            "countCommits": round(random.uniform(0, 3), 2),
            "avg_views": 0,
            "repos": random.randint(0, 2),
            "created_update": random.randint(0, 2),
            "forks_r": 0,
            "stars_r": 0,
            "cont_count": 0,
            "commits_repo": random.randint(0, 2),
            "frequency_repo": round(random.uniform(10.0, 50.0), 2),
            "inDay_repo": round(random.uniform(0, 1.0), 2),
            "addLine": random.randint(0, 7),
            "delLine": random.randint(0, 4),
            "count_views": 0,
            "active_days_r": random.randint(0, 2),
        }

    def _beginner(self) -> Dict[str, Any]:
        return {
            "followers": random.randint(0, 30),
            "following": random.randint(0, 10),
            "hireable": random.randint(0, 1),
            "plan": random.randint(0, 1),
            "blog": random.randint(0, 1),
            "company": random.randint(0, 1),
            "org": random.randint(0, 2),
            "languages": random.randint(1, 3),
            "forks": random.randint(0, 5),
            "stars": random.randint(0, 5),
            "avg_cont": random.randint(0, 2),
            "avg_a_days": random.randint(0, 3),
            "frequencyCommits": round(random.uniform(5.0, 30.0), 2),
            "inDayCommits": round(random.uniform(1, 3), 2),
            "countCommits": round(random.uniform(1, 10), 2),
            "avg_views": random.randint(0, 5),
            "repos": random.randint(1, 5),
            "created_update": random.randint(1, 4),
            "forks_r": random.randint(0, 2),
            "stars_r": random.randint(0, 10),
            "cont_count": random.randint(1, 2),
            "commits_repo": random.randint(1, 10),
            "frequency_repo": round(random.uniform(4, 10), 2),
            "inDay_repo": round(random.uniform(1.0, 3), 2),
            "addLine": random.randint(0, 15),
            "delLine": random.randint(0, 8),
            "count_views": random.randint(0, 10),
            "active_days_r": random.randint(1, 5),
        }

    def _intermediate(self) -> Dict[str, Any]:
        return {
            "followers": random.randint(0, 1000),
            "following": random.randint(0, 60),
            "hireable": random.randint(0, 1),
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
            "inDayCommits": round(random.uniform(1, 4), 2),
            "countCommits": round(random.uniform(10, 38), 2),
            "avg_views": random.randint(0, 20),
            "repos": random.randint(0, 15),
            "created_update": random.randint(4, 20),
            "forks_r": random.randint(0, 6),
            "stars_r": random.randint(0, 50),
            "cont_count": random.randint(0, 6),
            "commits_repo": random.randint(10, 30),
            "frequency_repo": round(random.uniform(1.8, 4), 2),
            "inDay_repo": round(random.uniform(1.0, 5.0), 2),
            "addLine": random.randint(15, 65),
            "delLine": random.randint(8, 18),
            "count_views": random.randint(0, 50),
            "active_days_r": random.randint(3, 8),
        }

    def _advanced(self) -> Dict[str, Any]:
        return {
            "followers": random.randint(1000, 5000),
            "following": random.randint(60, 200),
            "hireable": random.randint(0, 1),
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
            "inDayCommits": round(random.uniform(3, 10), 2),
            "countCommits": round(random.uniform(38, 200), 2),
            "avg_views": random.randint(20, 400),
            "repos": random.randint(15, 30),
            "created_update": random.randint(20, 36),
            "forks_r": random.randint(6, 13),
            "stars_r": random.randint(200, 1000),
            "cont_count": random.randint(6, 12),
            "commits_repo": random.randint(30, 170),
            "frequency_repo": round(random.uniform(0.0, 1.8), 2),
            "inDay_repo": round(random.uniform(3.0, 12), 2),
            "addLine": random.randint(65, 150),
            "delLine": random.randint(18, 50),
            "count_views": random.randint(50, 1000),
            "active_days_r": random.randint(8, 25),
        }

    def _maximum_values(self) -> Dict[str, Any]:
        scale = 10
        mv = self.assessment.max_value
        return {
            "followers": random.randint(0, scale * mv["followers"]),
            "following": random.randint(0, scale * mv["following"]),
            "hireable": random.randint(0, 1),
            "plan": random.randint(0, 1),
            "blog": random.randint(0, 1),
            "company": random.randint(0, 1),
            "org": random.randint(0, scale * mv["org"]),
            "languages": random.randint(0, scale * mv["languages"]),
            "forks": random.randint(0, scale * mv["forks"]),
            "stars": random.randint(0, scale * mv["stars"]),
            "avg_cont": random.randint(0, scale * mv["avg_cont"]),
            "avg_a_days": random.randint(0, scale * mv["avg_a_days"]),
            "frequencyCommits": round(random.uniform(0.0, 10.0), 2),
            "inDayCommits": round(random.uniform(0, scale * mv["inDayCommits"]), 2),
            "countCommits": round(random.uniform(0, scale * mv["countCommits"]), 2),
            "avg_views": random.randint(0, scale * mv["avg_views"]),
            "repos": random.randint(0, scale * mv["repos"]),
            "created_update": random.randint(0, scale * mv["created_update"]),
            "forks_r": random.randint(0, scale * mv["forks_r"]),
            "stars_r": random.randint(0, scale * mv["stars_r"]),
            "cont_count": random.randint(0, scale * mv["cont_count"]),
            "commits_repo": random.randint(0, scale * mv["commits_repo"]),
            "frequency_repo": round(random.uniform(0.0, 5.0), 2),
            "inDay_repo": round(random.uniform(0, scale * mv["inDay_repo"]), 2),
            "addLine": random.randint(0, scale * mv["addLine"]),
            "delLine": random.randint(0, scale * mv["delLine"]),
            "count_views": random.randint(0, scale * mv["count_views"]),
            "active_days_r": random.randint(0, scale * mv["active_days_r"]),
        }


    def _validate_and_fix_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        d = user_data.copy()

        if d["repos"] == 0:
            d.update({
                "languages": 0, "forks": 0, "stars": 0, "avg_cont": 0,
                "avg_a_days": 0, "frequencyCommits": 666, "inDayCommits": 0,
                "countCommits": 0, "avg_views": 0, "forks_r": 0, "stars_r": 0,
                "cont_count": 0, "commits_repo": 0, "frequency_repo": 666,
                "inDay_repo": 0, "addLine": 0, "delLine": 0,
                "count_views": 0, "active_days_r": 0,
            })

        if d["countCommits"] == 0:
            d.update({
                "inDayCommits": 0, "frequencyCommits": 666,
                "commits_repo": 0, "frequency_repo": 666,
                "inDay_repo": 0, "addLine": 0, "delLine": 0,
            })

        if d["countCommits"] > 0 and d["countCommits"] < d["inDayCommits"]:
            d["countCommits"], d["inDayCommits"] = d["inDayCommits"], d["countCommits"]
        elif d["countCommits"] == d["inDayCommits"] and d["countCommits"] > 0:
            d["avg_a_days"] = 1

        if d["commits_repo"] > 0 and d["commits_repo"] < d["inDay_repo"]:
            d["commits_repo"], d["inDay_repo"] = d["inDay_repo"], d["commits_repo"]
        elif d["commits_repo"] == d["inDay_repo"] and d["commits_repo"] > 0:
            d["active_days_r"] = 1

        return d


    def _calculate_scores(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        a = self.assessment
        scores = {}

        scores["followers_s"]      = a.followers_to_score_log(user_data["followers"])
        scores["following_s"]      = a.following_to_score_log(user_data["following"])
        scores["hireable_s"]       = a.hireable_to_score(user_data["hireable"])
        scores["plan_s"]           = a.plan_to_score(user_data["plan"])
        scores["blog_s"]           = a.blog_to_score(user_data["blog"])
        scores["company_s"]        = a.company_to_score(user_data["company"])
        scores["org_s"]            = a.org_to_score_log(user_data["org"])
        scores["langs_s"]          = a.language_to_score_log(user_data["languages"])
        scores["forks_s"]          = a.forks_to_score_log(user_data["forks"])
        scores["stars_s"]          = a.stars_to_score_log(user_data["stars"])
        scores["avg_cont_s"]       = a.avg_cont_to_score_log(user_data["avg_cont"])
        scores["avg_a_days_s"]     = a.avg_a_days_to_score_log(user_data["avg_a_days"])
        scores["freq_commits_s"]   = a.frequency_to_score_exp(user_data["repos"], user_data["frequencyCommits"])
        scores["in_day_commits_s"] = a.in_day_to_score_log(user_data["inDayCommits"])
        scores["count_commits_s"]  = a.commits_to_score_log(user_data["countCommits"])
        scores["avg_views_s"]      = a.avg_views_to_score_log(user_data["avg_views"])
        scores["repos_s"]          = a.evaluate_repositories(
            scores["freq_commits_s"],
            scores["in_day_commits_s"],
            scores["count_commits_s"],
            user_data["repos"],
        )
        scores["created_update_s"] = a.created_update_to_score_linear(
            scores["repos_s"], user_data["created_update"])
        scores["forks_r_s"]        = a.forks_r_to_score_log(user_data["forks_r"])
        scores["stars_r_s"]        = a.stars_r_to_score_log(user_data["stars_r"])
        scores["contributors_s"]   = a.contributors_count_to_score_log(user_data["cont_count"])
        scores["commits_repo_s"]   = a.commits_r_to_score_log(user_data["commits_repo"])
        scores["frequency_repo_s"] = a.frequency_r_to_score_exp(
            user_data["repos"], user_data["frequency_repo"], user_data["active_days_r"])
        scores["in_day_repo_s"]    = a.in_day_r_to_score_log(
            user_data["inDay_repo"], user_data["active_days_r"])
        scores["add_line_s"]       = a.add_line_log(user_data["addLine"])
        scores["del_line_s"]       = a.del_line_log(user_data["delLine"])
        scores["count_views_s"]    = a.count_views_count_to_score_log(user_data["count_views"])
        scores["active_days_r_s"]  = a.days_main_repo(
            scores["frequency_repo_s"],
            scores["in_day_repo_s"],
            scores["commits_repo_s"],
            scores["add_line_s"],
            scores["del_line_s"],
            user_data["active_days_r"],
        )
        return scores

    def generate_users(self, count: int = 150_000) -> pd.DataFrame:
        schedule: List[str] = (
            ["absolute_zero"]  *  5_000 +
            ["field_zero"]     * 10_000 +
            ["sparse_zero"]    * 10_000 +
            ["low_values"]     * 20_000 +
            ["beginner"]       * 25_000 +
            ["intermediate"]   * 30_000 +
            ["advanced"]       * 30_000 +
            ["maximum_values"] * 20_000
        )
        random.shuffle(schedule)

        data = []
        for user_type in schedule:
            raw = self._generate_user_data(user_type)
            if raw is None:
                continue
            user_data = self._validate_and_fix_user_data(raw)
            scores    = self._calculate_scores(user_data)
            data.append({**user_data, **scores})

        return pd.DataFrame(data, columns=self.columns)

    def save_to_csv(self, df: pd.DataFrame, path: str) -> None:
        df.to_csv(path, index=False)