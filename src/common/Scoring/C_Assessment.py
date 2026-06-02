import math
from common.Config.M_LoadConfig import load_config


# ══════════════════════════════════════════════════════════════
#  МАТЕМАТИЧЕСКИЕ ПРИМИТИВЫ
# ══════════════════════════════════════════════════════════════

class Assessment:
    def __init__(self, config_file="field_score.json", config_file2="max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value   = load_config(config_file2)

    def _hill_score(self, value: float, k: float, field_score: float, n: float = 2.0) -> float:
        """
        Уравнение Хилла (обобщённое уравнение Михаэлиса-Ментен):

            f(x) = field_score · xⁿ / (xⁿ + kⁿ)

        Свойства:
          - Гладкая, монотонно возрастающая, без разрывов и особых точек
          - f(0) = 0, f(k) = field_score / 2, f(∞) → field_score
          - k  - «полунасыщение»: значение x, дающее 50% максимума
          - n  - «кооперативность»: n=1 гиперболическая кривая,
                 n≥2 сигмоидальная (более резкий порог)
        """
        if value <= 0 or k <= 0:
            return 0.0
        xn = value ** n
        kn = k ** n
        return round(field_score * xn / (xn + kn), 3)

    def _exp_score(self, value: float, coefficient: float, decay_rate: float = 0.5) -> float:
        """
        Экспоненциальное затухание:
            f(x) = coefficient · e^(−decay_rate · x)
        """
        return round(coefficient * math.exp(-decay_rate * value), 3)

    def _binary_score(self, value, field_score: float) -> float:
        """Бинарная оценка: 0 или field_score."""
        return round(field_score if value else 0.0, 3)

    def _weighted_geometric_mean(
        self, components: list[tuple[float, float]], field_score: float
    ) -> float:
        """
        Взвешенное геометрическое среднее (WGM) нормализованных компонентов:

            WGM = field_score · ∏ vᵢ^wᵢ,   где Σwᵢ = 1, vᵢ ∈ [0,1]
        """
        if not components:
            return 0.0
        # log-space для численной стабильности (избегаем переполнения при перемножении)
        log_sum = sum(w * math.log(max(v, 1e-9)) for v, w in components)
        return round(min(field_score * math.exp(log_sum), field_score), 3)

    def _bayesian_adjusted(
        self, value: float, count: float, population_avg: float, C: float = 5.0
    ) -> float:
        """
        Байесовское среднее (Bayesian Average):

            x̄_B = (C · m + n · x) / (C + n)

          - value          - наблюдаемое значение метрики
          - count          - размер выборки (кол-во репозиториев)
          - population_avg - prior: ожидаемое «среднее» значение метрики
          - C              - вес prior'а (виртуальные «голоса» с базовым рейтингом)
        """
        if count <= 0:
            return 0.0
        return (C * population_avg + count * value) / (C + count)

    # ══════════════════════════════════════════════════════════════
    #  МЕТРИКИ ПРОФИЛЯ
    # ══════════════════════════════════════════════════════════════

    def followers_to_score_log(self, followers: float) -> float:
        """
        Hill, n=1.3 - мягкая кривая
        k = 2% от max
        """
        k = max(self.max_value["followers"] * 0.02, 1.0)
        return self._hill_score(followers, k, self.field_score["followers"], n=1.3)

    def following_to_score_log(self, following: float) -> float:
        """Hill, n=1.3. k = 10% от max"""
        k = max(self.max_value["following"] * 0.10, 1.0)
        return self._hill_score(following, k, self.field_score["following"], n=1.3)

    def org_to_score_log(self, orgs: float) -> float:
        """
        Hill, n=2.0 - чёткий порог.
        k = 25% от max
        """
        k = max(self.max_value["org"] * 0.25, 1.0)
        return self._hill_score(orgs, k, self.field_score["org"], n=2.0)

    def company_to_score(self, company) -> float:
        return self._binary_score(company, self.field_score["company"])

    def hireable_to_score(self, hireable) -> float:
        return self._binary_score(hireable, self.field_score["hireable"])

    def plan_to_score(self, plan) -> float:
        return self._binary_score(plan, self.field_score["plan"])

    def blog_to_score(self, blog) -> float:
        return self._binary_score(blog, self.field_score["blog"])

    def language_to_score_log(self, languages: float) -> float:
        """
        Hill, n=1.5.
        k = 25% от max
        """
        k = max(self.max_value["languages"] * 0.25, 1.0)
        return self._hill_score(languages, k, self.field_score["languages"], n=1.5)

    def _shannon_diversity_score(
            self, language_counts: dict[str, int], field_score: float
    ) -> float:
        """
        Нормализованная энтропия Шеннона для оценки разнообразия языков:

            H      = -Σ pᵢ · ln(pᵢ)
            H_norm = H / ln(L)         ∈ [0, 1]
            Score  = field_score · H_norm

        pᵢ - доля репозиториев на языке i,  L - количество уникальных языков.
        """
        if not language_counts:
            return 0.0

        total = sum(language_counts.values())
        if total == 0:
            return 0.0

        probs = [c / total for c in language_counts.values() if c > 0]
        L = len(probs)

        if L == 1:
            # За владение одним языком - базовый балл (30%)
            return round(field_score * 0.30, 3)

        H = -sum(p * math.log(p) for p in probs)
        H_max = math.log(L)
        return round(field_score * (H / H_max), 3)

    def language_shannon_score(self, language_counts: dict[str, int]) -> float:
        """
        Энтропия Шеннона по словарю {язык: кол-во репо}.
        """
        return self._shannon_diversity_score(
            language_counts, self.field_score["languages"]
        )

    def forks_to_score_log(self, forks: float, repos: float = 1) -> float:
        """
        Байесово сглаживание + Hill, n=2.0.

        Байесовский prior = 8% от max
        """
        if repos == 0:
            return 0.0
        pop_avg = self.max_value["forks"] * 0.08
        adjusted = self._bayesian_adjusted(forks, repos, pop_avg, C=5.0)
        k = max(self.max_value["forks"] * 0.08, 1.0)
        return self._hill_score(adjusted, k, self.field_score["forks"], n=2.0)

    def stars_to_score_log(self, stars: float, repos: float = 1) -> float:
        """
        Байесово сглаживание + Hill, n=2.0.
        """
        if repos == 0:
            return 0.0
        pop_avg = self.max_value["stars"] * 0.08
        adjusted = self._bayesian_adjusted(stars, repos, pop_avg, C=5.0)
        k = max(self.max_value["stars"] * 0.08, 1.0)
        return self._hill_score(adjusted, k, self.field_score["stars"], n=2.0)

    def avg_cont_to_score_log(self, avg_cont: float) -> float:
        """Hill, n=1.8. k = 20% от max."""
        k = max(self.max_value["avg_cont"] * 0.20, 1.0)
        return self._hill_score(avg_cont, k, self.field_score["avg_cont"], n=1.8)

    def avg_views_to_score_log(self, avg_views: float) -> float:
        """Hill, n=1.8. k = 10% от max."""
        k = max(self.max_value["avg_views"] * 0.10, 1.0)
        return self._hill_score(avg_views, k, self.field_score["avg_views"], n=1.8)

    def avg_a_days_to_score_log(self, avg_a_days: float) -> float:
        """Hill, n=1.8. k = 20% от max."""
        k = max(self.max_value["avg_a_days"] * 0.20, 1.0)
        return self._hill_score(avg_a_days, k, self.field_score["avg_a_days"], n=1.8)

    def commits_to_score_log(self, count_commits: float) -> float:
        """Hill, n=2.0. k = 10% от max"""
        k = max(self.max_value["countCommits"] * 0.10, 1.0)
        return self._hill_score(count_commits, k, self.field_score["countCommits"], n=2.0)

    def in_day_to_score_log(self, in_day_commits: float) -> float:
        """Hill, n=1.8. k = 25% от max."""
        k = max(self.max_value["inDayCommits"] * 0.25, 1.0)
        return self._hill_score(in_day_commits, k, self.field_score["inDayCommits"], n=1.8)

    def frequency_to_score_exp(self, repos: float, frequency_commits: float) -> float:
        """
        Экспоненциальное затухание по среднему интервалу между коммитами.
        """
        if repos == 0:
            return 0.0
        return self._exp_score(frequency_commits, self.field_score["frequencyCommits"])

    def _consistency_score(
            self, intervals: list[float], field_score: float, lam: float = 1.5
    ) -> float:
        """
        Оценка регулярности коммитов через Коэффициент Вариации (CV):

            CV    = σ / μ
            Score = field_score · e^(−λ · CV)

        Где μ - среднее, σ - стандартное отклонение интервалов между коммитами, λ (lam) - скорость затухания
        """
        if not intervals or len(intervals) < 2:
            return 0.0

        mean = sum(intervals) / len(intervals)
        if mean == 0:
            return round(field_score, 3)

        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        cv = variance ** 0.5 / mean
        return round(min(field_score * math.exp(-lam * cv), field_score), 3)

    def frequency_consistency_score(
            self, intervals: list[float], repos: float
    ) -> float:
        """
        CV-оценка регулярности коммитов профиля.
        Используется как бонус поверх frequency_to_score_exp.

        Возвращает до 20% от field_score["frequencyCommits"] -
        не заменяет базовую оценку частоты, а дополняет её.
        """
        if repos == 0 or not intervals:
            return 0.0
        bonus_cap = self.field_score["frequencyCommits"] * 0.20
        return self._consistency_score(intervals, bonus_cap, lam=1.5)

    def frequency_repo_consistency_score(
            self, intervals: list[float], repos: float
    ) -> float:
        """
        То же самое, но для основного репозитория (frequencyComm_MainRepo).
        Бонус до 20% от field_score["frequencyComm_MainRepo"].
        """
        if repos == 0 or not intervals:
            return 0.0
        bonus_cap = self.field_score["frequencyComm_MainRepo"] * 0.20
        return self._consistency_score(intervals, bonus_cap, lam=1.5)

    def evaluate_repositories(
        self, frequency: float, in_day_commits: float, count_commits: float, num_repos: float
    ) -> float:
        """
        Взвешенное геометрическое среднее показателей репозиторной активности.

        Веса:
          35% - среднее кол-во коммитов (core productivity)
          25% - кол-во репозиториев     (breadth)
          20% - коммитов в день         (intensity)
          20% - частота коммитов        (regularity)
        """
        if num_repos == 0:
            return 0.0

        fs = self.field_score
        mv = self.max_value

        components = [
            (min(count_commits  / fs["countCommits"],   1.0), 0.35),
            (min(num_repos      / mv["repos"],          1.0), 0.25),
            (min(in_day_commits / fs["inDayCommits"],   1.0), 0.20),
            (min(frequency      / fs["frequencyCommits"], 1.0), 0.20),
        ]
        return self._weighted_geometric_mean(components, fs["repos"])

    def created_update_to_score_linear(self, repos_log: float, created_update: float) -> float:
        """
        WGM: возраст аккаунта (45%) × репозиторная активность (55%).
        """
        fs = self.field_score
        mv = self.max_value

        components = [
            (min(repos_log      / fs["repos"],          1.0), 0.55),
            (min(created_update / mv["created_update"], 1.0), 0.45),
        ]
        return self._weighted_geometric_mean(components, fs["created_update"])

    # ══════════════════════════════════════════════════════════════
    #  МЕТРИКИ ОСНОВНОГО РЕПОЗИТОРИЯ
    # ══════════════════════════════════════════════════════════════

    def forks_r_to_score_log(self, forks: float) -> float:
        """Hill, n=2.0. k = 8% от max."""
        k = max(self.max_value["forks_r"] * 0.08, 1.0)
        return self._hill_score(forks, k, self.field_score["forks_r"], n=2.0)

    def stars_r_to_score_log(self, stars: float) -> float:
        """Hill, n=2.0. k = 8% от max."""
        k = max(self.max_value["stars_r"] * 0.08, 1.0)
        return self._hill_score(stars, k, self.field_score["stars_r"], n=2.0)

    def contributors_count_to_score_log(self, contributors_count: float) -> float:
        """Hill, n=1.8. k = 20% от max."""
        k = max(self.max_value["cont_count"] * 0.20, 1.0)
        return self._hill_score(contributors_count, k, self.field_score["contributors_count"], n=1.8)

    def count_views_count_to_score_log(self, count_views) -> float:
        if count_views == "-":
            return 0.0
        k = max(self.max_value["count_views"] * 0.10, 1.0)
        return self._hill_score(count_views, k, self.field_score["count_views"], n=1.8)

    def commits_r_to_score_log(self, count_commits: float) -> float:
        """Hill, n=2.0. k = 10% от max."""
        k = max(self.max_value["commits_repo"] * 0.10, 1.0)
        return self._hill_score(count_commits, k, self.field_score["commits_MainRepo"], n=2.0)

    def in_day_r_to_score_log(self, in_day_commits: float, day_work: float) -> float:
        """
        Hill, n=1.8. k = 25% от max.
        """
        coefficient = (
            self.field_score["inDayComm_MainRepo"] if day_work != 1
            else self.field_score["oneDay_inDay"]
        )
        k = max(self.max_value["inDay_repo"] * 0.25, 1.0)
        return self._hill_score(in_day_commits, k, coefficient, n=1.8)

    def frequency_r_to_score_exp(
        self, repos: float, frequency_commits: float, day_work: float
    ) -> float:
        coefficient = (
            self.field_score["frequencyComm_MainRepo"] if day_work != 1
            else self.field_score["oneDay_frequency"]
        )
        return self._exp_score(frequency_commits, coefficient) if repos != 0 else 0.0

    def add_line_log(self, add_line: float) -> float:
        """
        Hill, n=2.0.
        k = 20 строк: 50% балла
        """
        return self._hill_score(add_line, 20.0, self.field_score["addLine"], n=2.0)

    def del_line_log(self, del_line: float) -> float:
        """
        Hill, n=2.0. k = 10 строк.
        """
        return self._hill_score(del_line, 10.0, self.field_score["delLine"], n=2.0)

    def days_main_repo(
        self,
        frequency: float,
        in_day_commits: float,
        count_commits: float,
        add_line: float,
        del_line: float,
        count_day: float,
    ) -> float:
        """
        Расширенная WGM для основного репозитория с учётом качества изменений.

        Веса (сумма = 1.0):
          30% - активные дни   (временно́й след)
          30% - коммиты        (объём работы)
          15% - коммитов в день (интенсивность)
          10% - частота        (регулярность)
          10% - добавленные строки (содержательность коммитов)
           5% - удалённые строки   (признак рефакторинга)
        """
        fs = self.field_score
        mv = self.max_value

        components = [
            (min(count_day      / mv["active_days_r"],           1.0), 0.30),
            (min(count_commits  / fs["commits_MainRepo"],         1.0), 0.30),
            (min(in_day_commits / fs["inDayComm_MainRepo"],       1.0), 0.15),
            (min(frequency      / fs["frequencyComm_MainRepo"],   1.0), 0.10),
            (min(add_line       / fs["addLine"],                  1.0), 0.10),
            (min(del_line       / fs["delLine"],                  1.0), 0.05),
        ]
        return self._weighted_geometric_mean(components, fs["created_update_r"])