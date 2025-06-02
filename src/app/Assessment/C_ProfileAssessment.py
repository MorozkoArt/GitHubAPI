import torch
import pandas as pd
from pathlib import Path
from src.app.Assessment.C_GPT import GPT
from src.app.Config.M_LoadConfig import load_config
from src.ml.ForModel.C_model import GitHubModel

class ProfileAssessment:

    def __init__(self, user, config_file2 = "max_value.json"):
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

    def assessment_profile(self):
        self.assessment_profile_dict["followers"] = self.get_predicted_value("followers")
        self.assessment_profile_dict["following"] = self.get_predicted_value("following")
        self.assessment_profile_dict["hireable"] = self.get_predicted_value("hireable")
        self.assessment_profile_dict["plan"] = self.get_predicted_value("plan")
        self.assessment_profile_dict["blog"] = self.get_predicted_value("blog")
        self.assessment_profile_dict["company"] = self.get_predicted_value("company")
        self.assessment_profile_dict["org"] = self.get_predicted_value("org")
        self.assessment_profile_dict["language"] = self.get_predicted_value("languages")
        self.assessment_profile_dict["forks"] = self.get_predicted_value("forks")
        self.assessment_profile_dict["stars"] = self.get_predicted_value("stars")
        self.assessment_profile_dict["avg_cont"] = self.get_predicted_value("avg_cont")
        self.assessment_profile_dict["avg_a_days"] = self.get_predicted_value("avg_a_days")
        self.assessment_profile_dict["countCommits"] = self.get_predicted_value("countCommits")
        self.assessment_profile_dict["inDayCommits"] = self.get_predicted_value("inDayCommits")
        self.assessment_profile_dict["frequencyCommits"] = self.get_predicted_value("frequencyCommits")
        self.assessment_profile_dict["avg_views"] = self.get_predicted_value("avg_views")
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
    

    def model_assessment(self):
        model = GitHubModel(input_size=28, output_size=28)
        base_dir = Path(__file__).parents[3]
        path_model = base_dir / "best_model.pth"
        path_scaler = base_dir / "scaler.pth"
        model.load_state_dict(torch.load(path_model))
        model.eval()

        scaler = torch.load(path_scaler, weights_only=False) 

        scale = 5

        new_data = pd.DataFrame({
            "followers": [min(self.get_value(int(self.user.followers)), scale * self.max_value["followers"])],
            "following": [min(self.get_value(int(self.user.following)), scale * self.max_value["following"])],
            "hireable": [self.check_string(self.user.hireable)],  
            "plan": [self.check_plan(self.user.plan)],
            "blog": [self.check_string(self.user.blog)], 
            "company": [self.check_string(self.user.company)],
            "org": [min(self.get_value(len(self.user.org)), scale * self.max_value["org"])],
            "languages": [min(self.get_value(len(self.user.languages)), scale * self.max_value["languages"])],
            "forks": [min(self.get_value(self.user.forks), scale * self.max_value["forks"])],
            "stars": [min(self.get_value(self.user.stars), scale * self.max_value["stars"])],
            "avg_cont": [min(self.get_value(self.user.avg_cont), scale * self.max_value["avg_cont"])],
            "avg_a_days": [min(self.get_value(self.user.avg_a_days), scale * self.max_value["avg_a_days"])],
            "frequencyCommits": [self.get_value(self.user.frequency_commits)],
            "inDayCommits": [min(self.get_value(self.user.in_day_commits), scale * self.max_value["inDayCommits"])],
            "countCommits": [min(self.get_value(self.user.count_commits), scale * self.max_value["countCommits"])],
            "avg_views": [min(self.get_value(self.user.avg_views), scale * self.max_value["avg_views"])],
            "repos": [min(self.get_value(len(self.user.repos_user)), scale * self.max_value["repos"])],
            "created_update": [min(self.get_value(self.user.month_usege), scale * self.max_value["created_update"])],
            "forks_r": [min(self.get_value(self.user.main_repo.forks), scale * self.max_value["forks_r"])],
            "stars_r": [min(self.get_value(self.user.main_repo.stargazers_count), scale * self.max_value["stars_r"])],
            "cont_count": [min(self.get_value(self.user.main_repo.contributors_count), scale * self.max_value["cont_count"])],
            "commits_repo": [min(self.get_value(self.user.main_repo.commits_count), scale * self.max_value["commits_repo"])],
            "frequency_repo": [self.get_value(self.user.main_repo.commits_frequency)],
            "inDay_repo": [min(self.get_value(self.user.main_repo.commits_in_day), scale * self.max_value["inDay_repo"])],
            "addLine": [min(self.get_value(self.user.main_repo.commits_add_lines), scale * self.max_value["addLine"])],
            "delLine": [min(self.get_value(self.user.main_repo.commits_del_lines), scale * self.max_value["delLine"])],
            "count_views": [min(self.get_value(self.user.main_repo.count_views), scale * self.max_value["count_views"])],
            "active_days_r": [min(self.get_value(self.user.main_repo.days_work), scale * self.max_value["active_days_r"])]
        })

        inputs = torch.tensor(scaler.transform(new_data.values), dtype=torch.float32)

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
        elif isinstance(value, str) and not value.strip():
            return default
        elif isinstance(value, bool) and not value:
            return default
        elif value == "-":
            return default
        elif value == "None":
            return default
        return value
    
    def check_string(self, value):
        if not value:
            return 0
        elif isinstance(value, str) and not value.strip():
            return 0
        elif value == "None":
            return 0
        return 1
    
    def check_plan(self, plan):
        if plan is None or plan.name == "free" or plan == "None" :
            return 0
        return 1
    
    def get_predicted_value(self, field_name):
        index = self.field_index_map[field_name]
        return float(self.predicted_scores[0][index])
    




