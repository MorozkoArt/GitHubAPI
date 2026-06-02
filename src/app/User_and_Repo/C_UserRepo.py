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

        return frequency_value, in_day_value, len(in_day_list), frequency_list

    def _compute_cv(self, intervals: list[float]) -> float:
        """
        Коэффициент вариации (CV = σ / μ).
        """
        if not intervals or len(intervals) < 2:
            return 0.0
        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return 0.0
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        return variance ** 0.5 / mean

    def tournament(self) -> float:
        """
        Выбор главного репозитория для детального анализа.
        Взвешенное геометрическое среднее нормализованных метрик.

        Веса (сумма = 1.0):
          35% — кол-во коммитов     (основной вклад разработчика)
          25% — активные дни        (продолжительность работы)
          20% — частота коммитов    (регулярность, exp-decay)
          10% — коммитов в день     (интенсивность)
           5% — звёзды              (социальное доказательство)
           5% — форки               (социальное доказательство)
        """
        tf = self.tour_field

        n_commits = min(self.commits_count / tf["commits_count"], 1.0)
        n_days = min(self.days_work / tf["days_work"], 1.0)
        n_frequency = (
            math.exp(-0.5 * self.commits_frequency)
            if self.commits_frequency != "NULL" else 0.0
        )
        n_in_day = (
            min(self.commits_in_day / tf["commits_inDay"], 1.0)
            if self.commits_in_day != "NULL" else 0.0
        )
        n_stars = min(self.stargazers_count / tf["stars"], 1.0)
        n_forks = min(self.forks / tf["forks"], 1.0)

        components = [
            (n_commits, 0.35),
            (n_days, 0.25),
            (n_frequency, 0.20),
            (n_in_day, 0.10),
            (n_stars, 0.05),
            (n_forks, 0.05),
        ]

        log_sum = sum(w * math.log(max(v, 1e-9)) for v, w in components)
        return min(100.0 * math.exp(log_sum), 100.0)

    @staticmethod
    def search_repo(repos, name):
        return next((repo for repo in repos if repo.name == name), None)
