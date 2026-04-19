import os
import math
from common.Config.M_LoadConfig import load_config

class User_repo:
    def __init__(self, repo, publicOrPrivate, config_file="tour_field.json"):
        all_commits = repo.get_commits()

        if all_commits.totalCount == 0:
            raise ValueError(f"Repo '{repo.name}' has no commits, skipping.")

        limit = int(os.getenv("MAX_COMMITS"))
        self.commits_list: list = list(all_commits[:limit] if limit > 0 else all_commits)
        self.commits_count: int = all_commits.totalCount

        commits_frequency_value, commits_in_day_value, commits_days, frequency_intervals = \
            self.commits_frequency_in_day()
        self.commits_frequency  = commits_frequency_value
        self.commits_in_day     = commits_in_day_value
        self.name               = repo.name
        self.language           = repo.language
        self.forks              = repo.forks
        self.stargazers_count   = repo.stargazers_count
        self.commits_frequency_intervals: list[float] = frequency_intervals
        self.commits_frequency_cv: float              = self._compute_cv(frequency_intervals)

        try:
            self.contributors_count = repo.get_contributors().totalCount
        except Exception:
            self.contributors_count = 0

        self.created_at    = repo.created_at.date()
        self.last_date     = self.commits_list[0].commit.author.date.date()
        self.days_usage    = (self.last_date - self.created_at).days + 1
        self.days_work     = commits_days
        self.publicOrPrivate = publicOrPrivate

        if self.publicOrPrivate == "public":
            self.count_views = "-"
        else:
            try:
                self.count_views = repo.get_views_traffic()["uniques"]
            except Exception:
                self.count_views = "-"

        self.tour_field = load_config(config_file)

    def commits_frequency_in_day(self):
        frequency_list = []
        in_day_list = []
        current_day = self.commits_list[0].commit.author.date.date()
        count_in_day = 0

        for i, commit in enumerate(self.commits_list):
            commit_date = commit.commit.author.date.date()

            if i < len(self.commits_list) - 1:
                next_date = self.commits_list[i + 1].commit.author.date.date()
                gap = (commit_date - next_date).days
                frequency_list.append(gap)

            if commit_date == current_day:
                count_in_day += 1
            else:
                in_day_list.append(count_in_day)
                count_in_day = 1
                current_day = commit_date

        in_day_list.append(count_in_day)

        frequency_value = sum(frequency_list) / len(frequency_list) if frequency_list else "NULL"
        in_day_value = sum(in_day_list) / len(in_day_list) if in_day_list else "NULL"

        # Возвращаем frequency_list дополнительно — для CV-оценки регулярности
        return frequency_value, in_day_value, len(in_day_list), frequency_list

    def _compute_cv(self, intervals: list[float]) -> float:
        """
        Коэффициент вариации (CV = σ / μ) для списка интервалов между коммитами.

        CV ∈ [0, +∞):
          0     — идеально регулярные коммиты (σ = 0)
          0.5   — умеренная нерегулярность
          ≥ 1.0 — высокая нерегулярность (σ ≥ μ)

        Возвращает 0.0 при недостаточном числе данных.
        """
        if not intervals or len(intervals) < 2:
            return 0.0
        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return 0.0
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        return variance ** 0.5 / mean

    def tournament(self):
        normalize_commits_count = min(self.commits_count / self.tour_field["commits_count"], 1)
        decay_rate = 0.5
        normalize_commits_frequency = (math.exp(-decay_rate * self.commits_frequency) if self.commits_frequency != "NULL" else 0)
        normalize_commits_in_day = (min(self.commits_in_day / self.tour_field["commits_inDay"], 1) if self.commits_in_day != "NULL" else 0)
        normalize_days_work = min(self.days_work / self.tour_field["days_work"], 1)
        normalize_stars = min(self.stargazers_count / self.tour_field["stars"], 1)
        normalize_forks = min(self.forks / self.tour_field["forks"], 1)
        repos_log = (normalize_commits_count * 4 + normalize_commits_frequency * 0.25
                     + normalize_commits_in_day * 0.25 + normalize_days_work * 2
                     + normalize_stars + normalize_forks)
        if repos_log > 1:
            judgement = min(100 * (math.log(repos_log) / math.log(8.5)), 100)
        elif 0 < repos_log <= 1:
            judgement = min(100 * (math.log(repos_log + 1) / math.log(8.5)), 100) / 20
        else:
            judgement = 0
        return judgement

    @staticmethod
    def search_repo(repos, name):
        return next((repo for repo in repos if repo.name == name), None)
