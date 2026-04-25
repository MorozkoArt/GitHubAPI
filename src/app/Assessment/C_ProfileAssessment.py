import os
import numpy as np
import pandas as pd
import joblib
import onnxruntime as ort

from Assessment.C_GPT import GPT
from common.Scoring.C_Assessment import Assessment
from common.Config.M_LoadConfig import load_config
from common.Utils.constants import NO_FREQUENCY_SENTINEL


class ProfileAssessment:

    def __init__(self, user, config_file2: str = "max_value.json"):
        self.max_value    = load_config(config_file2)
        self._field_score = load_config("field_score.json")
        self.user         = user
        self._assessment  = Assessment()

        self.predicted_scores = self._model_assessment()
        self.field_index_map  = self._create_field_index_map()

        self.assessment_kod_list: list       = []
        self.assessment_profile_dict: dict   = {}
        self.assessment_repo_main_dict: dict = {}
        self.score_profile:    float = 0.0
        self.score_main_repos: float = 0.0
        self.score_kod:        float = 0.0

    def assessment_profile(self) -> float:
        key_map = {"repositories": "repos", "month_usege": "created_update"}
        keys = [
            "followers", "following", "hireable", "plan", "blog", "company",
            "org", "forks", "stars", "avg_cont", "avg_a_days",
            "countCommits", "inDayCommits", "frequencyCommits", "avg_views",
            "repositories", "month_usege",
        ]
        for k in keys:
            mapped = key_map.get(k, k)
            self.assessment_profile_dict[k] = self._get_predicted_value(mapped)

        # ── Энтропия Шеннона (1.3) ───────────────────────────────────────────
        self.assessment_profile_dict["language"] = self._assessment.language_shannon_score(
            self.user.language_counts
        )

        # ── CV-бонус регулярности коммитов (1.2) ────────────────────────────
        cv_bonus = self._assessment.frequency_consistency_score(
            self.user.frequency_intervals,
            len(self.user.repos_user),
        )
        self.assessment_profile_dict["frequencyCommits"] = min(
            self.assessment_profile_dict["frequencyCommits"] + cv_bonus,
            self._field_score["frequencyCommits"],
        )

        self.score_profile = sum(
            v for v in self.assessment_profile_dict.values() if isinstance(v, (int, float))
        )
        return self.score_profile

    def assessment_mainrepo(self) -> float:
        repo_keys = {
            "forks":              "forks_r",
            "stargazers_count":   "stars_r",
            "contributors_count": "cont_count",
            "commits_count":      "commits_repo",
            "inDayCommits":       "inDay_repo",
            "frequencyCommits":   "frequency_repo",
            "addLine":            "addLine",
            "delLine":            "delLine",
            "days_work":          "active_days_r",
            "count_views":        "count_views",
        }
        for dict_key, model_key in repo_keys.items():
            self.assessment_repo_main_dict[dict_key] = self._get_predicted_value(model_key)

        # ── CV-бонус для основного репозитория (1.2) ────────────────────────
        cv_bonus_repo = self._assessment.frequency_repo_consistency_score(
            self.user.main_repo.commits_frequency_intervals,
            len(self.user.repos_user),
        )
        self.assessment_repo_main_dict["frequencyCommits"] = min(
            self.assessment_repo_main_dict.get("frequencyCommits", 0) + cv_bonus_repo,
            self._field_score["frequencyComm_MainRepo"],
        )

        self.score_main_repos = sum(
            v for v in self.assessment_repo_main_dict.values() if isinstance(v, (int, float))
        )
        return self.score_main_repos

    def assessment_kod(self, full_or_three: int) -> float:
        scale_mark = 5
        list_of_path = self.user.main_repo.download_mainRepo()
        gpt = GPT(list_of_path)
        self.assessment_kod_list = gpt.evaluate_codeS(full_or_three)

        total = sum(marks for _, marks, _ in self.assessment_kod_list)
        n = len(self.assessment_kod_list)
        self.score_kod = (total / n) * scale_mark if n > 0 else 0.0
        return self.score_kod

    def _build_feature_row(self) -> dict:
        """
        Формирует словарь входных признаков для ONNX-модели.

        Вынесено из _model_assessment для читаемости и тестируемости:
        можно проверить значения признаков отдельно от инференса модели.
        """
        u  = self.user
        mv = self.max_value
        scale = 5

        return {
            "followers":        min(self._get_value(int(u.followers)),               scale * mv["followers"]),
            "following":        min(self._get_value(int(u.following)),               scale * mv["following"]),
            "hireable":         self._check_string(u.hireable),
            "plan":             self._check_plan(u.plan),
            "blog":             self._check_string(u.blog),
            "company":          self._check_string(u.company),
            "org":              min(self._get_value(len(u.org)),                     scale * mv["org"]),
            "languages":        min(self._get_value(len(u.languages)),               scale * mv["languages"]),
            "forks":            min(self._get_value(u.forks),                        scale * mv["forks"]),
            "stars":            min(self._get_value(u.stars),                        scale * mv["stars"]),
            "avg_cont":         min(self._get_value(u.avg_cont),                     scale * mv["avg_cont"]),
            "avg_a_days":       min(self._get_value(u.avg_a_days),                   scale * mv["avg_a_days"]),
            "frequencyCommits": self._get_value(u.frequency_commits),
            "inDayCommits":     min(self._get_value(u.in_day_commits),               scale * mv["inDayCommits"]),
            "countCommits":     min(self._get_value(u.count_commits),                scale * mv["countCommits"]),
            "avg_views":        min(self._get_value(u.avg_views),                    scale * mv["avg_views"]),
            "repos":            min(self._get_value(len(u.repos_user)),              scale * mv["repos"]),
            "created_update":   min(self._get_value(u.account_age_months),           scale * mv["created_update"]),
            "forks_r":          min(self._get_value(u.main_repo.forks),              scale * mv["forks_r"])       if u.main_repo else 0,
            "stars_r":          min(self._get_value(u.main_repo.stargazers_count),   scale * mv["stars_r"])       if u.main_repo else 0,
            "cont_count":       min(self._get_value(u.main_repo.contributors_count), scale * mv["cont_count"])    if u.main_repo else 0,
            "commits_repo":     min(self._get_value(u.main_repo.commits_count),      scale * mv["commits_repo"])  if u.main_repo else 0,
            "frequency_repo":   self._get_value(u.main_repo.commits_frequency)                                    if u.main_repo else NO_FREQUENCY_SENTINEL,
            "inDay_repo":       min(self._get_value(u.main_repo.commits_in_day),     scale * mv["inDay_repo"])    if u.main_repo else 0,
            "addLine":          min(self._get_value(u.main_repo.commits_add_lines),  scale * mv["addLine"])       if u.main_repo else 0,
            "delLine":          min(self._get_value(u.main_repo.commits_del_lines),  scale * mv["delLine"])       if u.main_repo else 0,
            "count_views":      min(self._get_value(u.main_repo.count_views),        scale * mv["count_views"])   if u.main_repo else 0,
            "active_days_r":    min(self._get_value(u.main_repo.days_work),          scale * mv["active_days_r"]) if u.main_repo else 0,
        }

    def _model_assessment(self) -> np.ndarray:
        ort_session = ort.InferenceSession(
            os.getenv("MODEL_PATH"),
            providers=["CPUExecutionProvider"],
        )
        scaler = joblib.load(os.getenv("SCALER_PATH"))

        raw_df      = pd.DataFrame([self._build_feature_row()])
        scaled      = scaler.transform(raw_df.values).astype("float32")
        input_name  = ort_session.get_inputs()[0].name
        predictions = ort_session.run(None, {input_name: scaled})[0]

        return self._apply_zero_constraints(predictions, raw_df.iloc[0].to_dict())

    def _apply_zero_constraints(self, predictions: np.ndarray, raw: dict) -> np.ndarray:
        result = predictions.copy()

        direct_zero_map = {
            "followers":    0,  "following":    1,  "hireable":   2,  "plan":          3,
            "blog":         4,  "company":      5,  "org":        6,  "languages":     7,
            "forks":        8,  "stars":        9,  "avg_cont":  10,  "avg_a_days":   11,
            "inDayCommits": 13, "countCommits": 14, "avg_views": 15,  "repos":        16,
            "forks_r":      18, "stars_r":      19, "cont_count": 20,
            "commits_repo": 21, "inDay_repo":   23, "addLine":   24,
            "delLine":      25, "count_views":  26, "active_days_r": 27,
        }
        for field, idx in direct_zero_map.items():
            if raw.get(field, 0) == 0:
                result[0][idx] = 0.0

        if raw.get("repos", 0) == 0 or raw.get("frequencyCommits", NO_FREQUENCY_SENTINEL) >= 30:
            result[0][12] = 0.0
        if raw.get("repos", 0) == 0 or raw.get("frequency_repo", NO_FREQUENCY_SENTINEL) >= 30:
            result[0][22] = 0.0

        if raw.get("repos", 0) == 0:
            for idx in range(7, 28):
                result[0][idx] = 0.0

        return result

    def _create_field_index_map(self) -> dict:
        return {
            "followers": 0,       "following": 1,       "hireable": 2,        "plan": 3,
            "blog": 4,            "company": 5,          "org": 6,             "languages": 7,
            "forks": 8,           "stars": 9,            "avg_cont": 10,       "avg_a_days": 11,
            "frequencyCommits": 12, "inDayCommits": 13,  "countCommits": 14,   "avg_views": 15,
            "repos": 16,          "created_update": 17,
            "forks_r": 18,        "stars_r": 19,         "cont_count": 20,
            "commits_repo": 21,   "frequency_repo": 22,  "inDay_repo": 23,
            "addLine": 24,        "delLine": 25,         "count_views": 26,    "active_days_r": 27,
        }

    def _get_predicted_value(self, field_name: str) -> float:
        idx = self.field_index_map[field_name]
        return float(self.predicted_scores[0][idx])

    def _get_value(self, value, default=0):
        if value is None or value is False:
            return default
        if isinstance(value, str) and value.strip() in ("", "None", "NULL", "-"):
            return default
        return value

    def _check_string(self, value) -> int:
        if not value:
            return 0
        if isinstance(value, str) and (not value.strip() or value == "None"):
            return 0
        return 1

    def _check_plan(self, plan) -> int:
        if plan is None or plan == "None":
            return 0
        try:
            if plan.name == "free":
                return 0
        except AttributeError:
            pass
        return 1