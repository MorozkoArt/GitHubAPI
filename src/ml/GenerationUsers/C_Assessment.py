import math
from common.Config.M_LoadConfig import load_config


class Assessment:
    def __init__(self, config_file="field_score.json", config_file2="max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value   = load_config(config_file2)

    # ══════════════════════════════════════════════════════════════
    #  МАТЕМАТИЧЕСКИЕ ПРИМИТИВЫ
    # ══════════════════════════════════════════════════════════════

    def _hill_score(self, value: float, k: float, field_score: float, n: float = 2.0) -> float:
        """
        Уравнение Хилла (обобщённое уравнение Михаэлиса-Ментен):

            f(x) = field_score · xⁿ / (xⁿ + kⁿ)

        Свойства:
          - Гладкая, монотонно возрастающая, без разрывов и особых точек
          - f(0) = 0, f(k) = field_score / 2, f(∞) → field_score
          - k  — «полунасыщение»: значение x, дающее 50% максимума
          - n  — «кооперативность»: n=1 гиперболическая кривая,
                 n≥2 сигмоидальная (более резкий порог)

        Применяется вместо кусочного _log_score.
        """
        if value <= 0 or k <= 0:
            return 0.0
        xn = value ** n
        kn = k ** n
        return round(field_score * xn / (xn + kn), 3)

    def _exp_score(self, value: float, coefficient: float, decay_rate: float = 0.5) -> float:
        """
        Экспоненциальное затухание для метрик «меньше = лучше» (частота коммитов):

            f(x) = coefficient · e^(−decay_rate · x)

        При x=0 → coefficient (идеально), при x→∞ → 0.
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

        Почему WGM вместо арифметического среднего:
          - Если хотя бы один компонент = 0, итог → 0 (нельзя компенсировать
            нулевую активность высокими значениями других метрик)
          - Штрафует за дисбаланс показателей сильнее, чем среднее арифметическое
          - Веса задают «важность» компонента, а не просто линейный коэффициент

        components: [(normalized_value, weight), ...]
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

          - value          — наблюдаемое значение метрики
          - count          — размер выборки (кол-во репозиториев)
          - population_avg — prior: ожидаемое «среднее» значение метрики
          - C              — вес prior'а (виртуальные «голоса» с базовым рейтингом)

        Семантика:
          При count → 0  результат стремится к population_avg (не доверяем малой выборке).
          При count → ∞  результат стремится к value (большая выборка говорит сама за себя).

        Используется для метрик stars / forks, чтобы репозиторий с 1 форком
        при 2 репозиториях не получал столько же, сколько зрелый проект.
        """
        if count <= 0:
            return 0.0
        return (C * population_avg + count * value) / (C + count)

    # ══════════════════════════════════════════════════════════════
    #  МЕТРИКИ ПРОФИЛЯ
    # ══════════════════════════════════════════════════════════════

    def followers_to_score_log(self, followers: float) -> float:
        """
        Hill, n=1.3 — мягкая кривая (даже малое число фолловеров оценивается).
        k = 2% от max: 50% балла при небольшом, но ненулевом сообществе.
        """
        k = max(self.max_value["followers"] * 0.02, 1.0)
        return self._hill_score(followers, k, self.field_score["followers"], n=1.3)

    def following_to_score_log(self, following: float) -> float:
        """Hill, n=1.3. k = 10% от max."""
        k = max(self.max_value["following"] * 0.10, 1.0)
        return self._hill_score(following, k, self.field_score["following"], n=1.3)

    def org_to_score_log(self, orgs: float) -> float:
        """
        Hill, n=2.0 — чёткий порог.
        k = 25% от max: участие в нескольких организациях уже хорошо.
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
        k = 25% от max: умеренное поощрение мультиязычности.
        """
        k = max(self.max_value["languages"] * 0.25, 1.0)
        return self._hill_score(languages, k, self.field_score["languages"], n=1.5)

    def forks_to_score_log(self, forks: float, repos: float = 1) -> float:
        """
        Байесово сглаживание + Hill, n=2.0.

        Байесовский prior = 8% от max (ожидаемое среднее кол-во форков).
        При малом числе репо (repos≤2) байесовское среднее «тянет» результат
        к prior'у, не давая завысить оценку за единственный популярный репо.
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

        Звёзды — социальное доказательство; один случайно завирусившийся репо
        не должен давать максимум при пустом профиле.
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
        """Hill, n=2.0. k = 10% от max: порог «среднего разработчика»."""
        k = max(self.max_value["countCommits"] * 0.10, 1.0)
        return self._hill_score(count_commits, k, self.field_score["countCommits"], n=2.0)

    def in_day_to_score_log(self, in_day_commits: float) -> float:
        """Hill, n=1.8. k = 25% от max."""
        k = max(self.max_value["inDayCommits"] * 0.25, 1.0)
        return self._hill_score(in_day_commits, k, self.field_score["inDayCommits"], n=1.8)

    def frequency_to_score_exp(self, repos: float, frequency_commits: float) -> float:
        """
        Экспоненциальное затухание по среднему интервалу между коммитами.
        При repos=0 — ноль (нет репозиториев, нет смысла).
        """
        if repos == 0:
            return 0.0
        return self._exp_score(frequency_commits, self.field_score["frequencyCommits"])

    def evaluate_repositories(
        self, frequency: float, in_day_commits: float, count_commits: float, num_repos: float
    ) -> float:
        """
        Взвешенное геометрическое среднее показателей репозиторной активности.

        Веса:
          35% — среднее кол-во коммитов (core productivity)
          25% — кол-во репозиториев     (breadth)
          20% — коммитов в день         (intensity)
          20% — частота коммитов        (regularity)

        WGM: ни один показатель не «тянет» весь блок в одиночку.
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

        Логика: долгий, но неактивный аккаунт ≠ молодой, но насыщенный —
        оба фактора одинаково важны и не компенсируют друг друга.
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
        Коэффициент поощрения зависит от того, работал ли репозиторий >1 дня.
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
        """Экспоненциальное затухание по частоте коммитов репозитория."""
        coefficient = (
            self.field_score["frequencyComm_MainRepo"] if day_work != 1
            else self.field_score["oneDay_frequency"]
        )
        return self._exp_score(frequency_commits, coefficient) if repos != 0 else 0.0

    def add_line_log(self, add_line: float) -> float:
        """
        Hill, n=2.0.
        k = 20 строк: 50% балла при «умеренных» коммитах (не пустые, не монстрообразные).
        Абсолютный порог, не зависящий от конфига — имеет смысл как есть.
        """
        return self._hill_score(add_line, 20.0, self.field_score["addLine"], n=2.0)

    def del_line_log(self, del_line: float) -> float:
        """
        Hill, n=2.0. k = 10 строк.
        Удаление кода — признак рефакторинга и «уборки» — ценится.
        """
        return self._hill_score(del_line, 10.0, self.field_score["delLine"], n=2.0)

    def days_repo(
        self, frequency: float, in_day_commits: float, count_commits: float, count_day: float
    ) -> float:
        """
        Взвешенное геометрическое среднее показателей активности репозитория.

        Веса (сумма = 1.0):
          40% — активные дни   (основной временно́й след)
          35% — коммиты        (объём работы)
          15% — коммитов в день (интенсивность)
          10% — частота        (регулярность)

        Входы frequency, in_day_commits, count_commits — уже вычисленные
        score-значения; нормализуются относительно своих field_score.
        count_day — сырое значение; нормализуется по max_value.
        """
        fs = self.field_score
        mv = self.max_value

        components = [
            (min(count_day      / mv["active_days_r"],    1.0), 0.40),
            (min(count_commits  / fs["commits_repo"],     1.0), 0.35),
            (min(in_day_commits / fs["inDay_repo"],       1.0), 0.15),
            (min(frequency      / fs["frequency_repo"],   1.0), 0.10),
        ]
        return self._weighted_geometric_mean(components, fs["created_update_r"])

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
          30% — активные дни   (временно́й след)
          30% — коммиты        (объём работы)
          15% — коммитов в день (интенсивность)
          10% — частота        (регулярность)
          10% — добавленные строки (содержательность коммитов)
           5% — удалённые строки   (признак рефакторинга)

        Нулевые строки изменений или нулевые активные дни → итог → 0.
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