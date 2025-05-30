import torch
import pandas as pd
from src.app.Assessment.C_GPT import GPT
from src.app.Config.M_LoadConfig import load_config
from src.ml.ForModel.C_model import GitHubModel

class ProfileAssessment:

    def __init__(self, user, config_file="field_score.json", config_file2 = "max_value.json"):
        self.field_score = load_config(config_file)
        self.max_value = load_config(config_file2)
        self.user = user
        self.predicted_scores = self.model_assessment()
        self.field_index_map = self.create_field_index_map()
        self.assessment_kod_list = []
        self.assessment_profile_dict = {}
        self.assessment_repo_main_dict = {}
        self.score_profile = 0
        self.score_main_repos = 0
        self.score_kod = 0

    def model_assessment(self):
        model = GitHubModel(input_size=28, output_size=28)
        model.load_state_dict(torch.load('C:/PycharmProjects/GitHubAPI/best_model.pth'))
        model.eval()

        new_data = pd.DataFrame({
            "followers": [self.get_value(int(self.user.followers))],
            "following": [self.get_value(int(self.user.following))],
            "hireable": [self.check_string(self.user.hireable)],  
            "plan": [self.check_plan(self.user.plan)],
            "blog": [self.check_string(self.user.blog)], 
            "company": [self.check_string(self.user.company)],
            "org": [self.get_value(len(self.user.org))],
            "languages": [self.get_value(len(self.user.languages))],
            "forks": [0],
            "stars": [1],
            "avg_cont": [1],
            "avg_a_days": [7],
            "frequencyCommits": [self.get_value(self.user.frequency_commits)],
            "inDayCommits": [self.get_value(self.user.in_day_commits)],
            "countCommits": [self.get_value(self.user.count_commits)],
            "avg_views": [3],
            "repos": [self.get_value(len(self.user.repos_user))],
            "created_update": [self.get_value(self.user.month_usege)],
            "forks_r": [self.get_value(self.user.main_repo.forks)],
            "stars_r": [self.get_value(self.user.main_repo.stargazers_count)],
            "cont_count": [self.get_value(self.user.main_repo.contributors_count)],
            "commits_repo": [self.get_value(self.user.main_repo.commits_count)],
            "frequency_repo": [self.get_value(self.user.main_repo.commits_frequency)],
            "inDay_repo": [self.get_value(self.user.main_repo.commits_in_day)],
            "addLine": [self.get_value(self.user.main_repo.commits_add_lines)],
            "delLine": [self.get_value(self.user.main_repo.commits_del_lines)],
            "count_views": [self.get_value(self.user.main_repo.count_views)],
            "active_days_r": [self.get_value(self.user.main_repo.days_work)]
        })

        inputs = torch.tensor(new_data.values, dtype=torch.float32)

        with torch.no_grad():
            predictions = model(inputs)

        return predictions.numpy()

    def create_field_index_map(self):
        return {
            "followers": 0,
            "following": 1,
            "hireable": 2,
            "plan": 3,
            "blog": 4,
            "company": 5,
            "org": 6,
            "languages": 7,
            "forks": 8,
            "stars": 9,
            "avg_cont": 10,
            "avg_a_days": 11,
            "frequencyCommits": 12,
            "inDayCommits": 13,
            "countCommits": 14,
            "avg_views": 15,
            "repos": 16,
            "created_update": 17,
            "forks_r": 18,
            "stars_r": 19,
            "cont_count": 20,
            "commits_repo": 21,
            "frequency_repo": 22,
            "inDay_repo": 23,
            "addLine": 24,
            "delLine": 25,
            "count_views": 26,
            "active_days_r": 27
            }
    
    def get_value(self, value, default=0):
        if value is None:
            return default
        if isinstance(value, str) and not value.strip():
            return default
        if isinstance(value, bool) and not value:
            return default
        if value == '-':
            return default
        return value
    
    def check_string(self, value):
        if not value:
            return 0
        if isinstance(value, str) and not value.strip():
            return 0
        return 1
    
    def check_plan(self, plan):
        if plan is None or plan.name == "free":
            return 0
        return 1
    
    def get_predicted_value(self, field_name):
        index = self.field_index_map[field_name]
        return float(self.predicted_scores[0][index])

    def assessment_profile(self):
        self.assessment_profile_dict["followers"] = self.get_predicted_value("followers")
        self.assessment_profile_dict["following"] = self.get_predicted_value("following")
        self.assessment_profile_dict["hireable"] = self.get_predicted_value("hireable")
        self.assessment_profile_dict["plan"] = self.get_predicted_value("plan")
        self.assessment_profile_dict["blog"] = self.get_predicted_value("blog")
        self.assessment_profile_dict["company"] = self.get_predicted_value("company")
        self.assessment_profile_dict["org"] = self.get_predicted_value("org")
        self.assessment_profile_dict["language"] = self.get_predicted_value("languages")
        self.assessment_profile_dict["countCommits"] = self.get_predicted_value("countCommits")
        self.assessment_profile_dict["inDayCommits"] = self.get_predicted_value("inDayCommits")
        self.assessment_profile_dict["frequencyCommits"] = self.get_predicted_value("frequencyCommits")
        self.assessment_profile_dict["repositories"] = self.get_predicted_value("repos")
        self.assessment_profile_dict["month_usege"] = self.get_predicted_value("created_update")
        self.score_profile = sum(value for value in self.assessment_profile_dict.values() if isinstance(value, (int, float)))
        return self.score_profile


    def assessment_mainrepo(self):
        self.assessment_repo_main_dict["forks"] = self.get_predicted_value("forks_r")
        self.assessment_repo_main_dict["stargazers_count"] = self.get_predicted_value("stars_r")
        self.assessment_repo_main_dict["contributors_count"] = self.get_predicted_value("cont_count")
        self.assessment_repo_main_dict["commits_count"] = self.get_predicted_value("commits_repo")
        self.assessment_repo_main_dict["inDayCommits"] = self.get_predicted_value("inDay_repo")
        self.assessment_repo_main_dict["frequencyCommits"] = self.get_predicted_value("frequency_repo")
        self.assessment_repo_main_dict["addLine"] = self.get_predicted_value("addLine")
        self.assessment_repo_main_dict["delLine"] = self.get_predicted_value("delLine")
        self.assessment_repo_main_dict["days_work"] = self.get_predicted_value("active_days_r")
        self.assessment_repo_main_dict["count_views"] = self.get_predicted_value("count_views")
        self.score_main_repos = sum(value for value in self.assessment_repo_main_dict.values() if isinstance(value, (int, float)))
        return self.score_main_repos


    def assessment_kod(self, full_or_three):
        list_of_path = self.user.main_repo.dounloud_mainRepo()
        chat_gpt = GPT(list_of_path)
        self.assessment_kod_list = chat_gpt.evaluate_codeS(full_or_three)
        for i in range (len(self.assessment_kod_list)):
            text, marks, file_name = self.assessment_kod_list[i]
            self.score_kod+=marks
        self.score_kod = (self.score_kod/len(self.assessment_kod_list))*5
        return self.score_kod



