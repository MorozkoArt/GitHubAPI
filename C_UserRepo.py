import os
class User_repo:

    def __init__(self, name, language, forks, stargazers_count, contributors_count, created_at, last_date, commits, count_views):
        self.name = name
        self.language = language
        self.forks = forks
        self.stargazers_count = stargazers_count
        self.contributors_count = contributors_count
        self.created_at = created_at
        self.last_date = last_date
        self.commits = commits
        self.count_views = count_views

    def tournament(self, repo_user):
        coefficient_com = 0.8
        coefficient_views = 0.08
        coefficient_stars = 0.1
        coefficient_forks = 0.2
        judgement = 0
        if int(repo_user.contributors_count) <= 1:
            judgement = (int(repo_user.commits)*coefficient_com
            + int(repo_user.stargazers_count)*coefficient_stars
            + int(repo_user.forks) * coefficient_forks)
            if repo_user.count_views != "-":
                judgement += int(repo_user.count_views) * coefficient_views
        return judgement

    # Проход по файлам в репозитории
    def dounloud_mainRepo(repo):
        print(repo.name)
        code_extensions = ('.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
                           '.html', '.css', '.swift', '.ts', '.json', '.sh', '.pl', '.r')
        if not os.path.exists("storage"):
            os.makedirs("storage")

        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                # Если это директория, получаем содержимое директории
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.type == "file":
                # Проверяем, является ли файл кодом по его расширению
                if file_content.name.endswith(code_extensions):
                    print(f"Загрузка {file_content.name}...")
                    path = os.path.join("storage", file_content.name)
                    with open(path, 'wb') as f:
                        f.write(file_content.decoded_content)
                    print(f"{path} загружен.")

    def serch_repo(repos, name):
        for repo in repos:
            if repo.name == name:
                return repo

