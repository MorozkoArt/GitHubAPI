import os
import shutil
class User_repo:

    def __init__(self, repo,  publicOrPrivate):
        self.commits = repo.get_commits()
        commits_frequency_value, commits_inDay_value, commits_addLines_value, commits_delLines_value = self.commits_frequency_inDay()
        self.commits_count = self.commits.totalCount
        self.commits_frequency = commits_frequency_value
        self.commits_inDay = commits_inDay_value
        self.commits_addLines = commits_addLines_value
        self.commits_delLines = commits_delLines_value

        self.name = repo.name
        self.language = repo.language
        self.forks = repo.forks
        self.stargazers_count = repo.stargazers_count
        self.contributors_count = repo.get_contributors().totalCount
        self.created_at = repo.created_at.date()
        self.last_date = self.commits[0].commit.author.date.date()
        self.days_usege = (int((self.last_date - self.created_at).days))
        self.publicOrPrivate = publicOrPrivate

        self.count_views = "-" if self.publicOrPrivate == "public" else repo.get_views_traffic()['count']

    def commits_frequency_inDay(self):
        commits_frequency_list = []
        commits_inDay_list = []
        commits_addLines_list = []
        commits_delLines_list = []
        day = self.commits[0].commit.author.date.date()
        count_commits_inDay = 0
        max_countCommits = 10
        range_commits = max_countCommits if self.commits.totalCount>max_countCommits else self.commits.totalCount

        for i in range (range_commits):
            if i != (self.commits.totalCount)-1:
                frequency = (self.commits[i].commit.author.date.date() - self.commits[i+1].commit.author.date.date()).days
                commits_frequency_list.append(frequency)
            if day == self.commits[i].commit.author.date.date():
                count_commits_inDay += 1
            else:
                commits_inDay_list.append(count_commits_inDay)
                count_commits_inDay = 1
                day = self.commits[i].commit.author.date.date()
            if i == (self.commits.totalCount)-1:
                commits_inDay_list.append(count_commits_inDay)

            line_changes = self.get_commit_lines_changed(self.commits[i])
            if line_changes:
                added, removed = line_changes
                commits_addLines_list.append(added)
                commits_delLines_list.append(removed)


        if len(commits_frequency_list)!=0:
            commits_frequency_value = sum(commits_frequency_list) / len(commits_frequency_list)
        else:
            commits_frequency_value = "NULL"

        if len(commits_inDay_list)!=0:
            commits_inDay_value = sum(commits_inDay_list) / len(commits_inDay_list)
        else:
            commits_inDay_value = "NULL"

        if len(commits_addLines_list)!=0:
            commits_addLines_value = sum(commits_addLines_list) / len(commits_addLines_list)
        else:
            commits_addLines_value = "NULL"

        if len(commits_delLines_list)!=0:
            commits_delLines_value = sum(commits_delLines_list) / len(commits_delLines_list)
        else:
            commits_delLines_value = "NULL"

        return commits_frequency_value, commits_inDay_value , commits_addLines_value, commits_delLines_value

    def get_commit_lines_changed(self, commit):
        try:
            lines_added = 0
            lines_removed = 0
            for file in commit.files:
                lines_added += file.additions
                lines_removed += file.deletions
            return (lines_added, lines_removed)
        except AttributeError as e:
            print(f"Error accessing commit file data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def tournament(self, repo_user):
        coefficient_com = 0.8
        coefficient_views = 0.08
        coefficient_stars = 0.1
        coefficient_forks = 0.2
        judgement = 0
        if int(repo_user.contributors_count) <= 1:
            judgement = (int(repo_user.commits_count)*coefficient_com
            + int(repo_user.stargazers_count)*coefficient_stars
            + int(repo_user.forks) * coefficient_forks)
            if repo_user.count_views != "-":
                judgement += int(repo_user.count_views) * coefficient_views
        return judgement

    # Проход по файлам в репозитории
    def dounloud_mainRepo(repo):
        list_of_paths = []
        print(repo.name)
        code_extensions = ('.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
                           '.html', '.css', '.swift', '.ts', '.json', '.sh', '.pl', '.r', '.cs')
        if not os.path.exists("storage"):
            os.makedirs("storage")
        else:
            # Проверка, пуста ли директория
            if os.listdir("storage"):
                # Удаление всего содержимого директории
                shutil.rmtree("storage")  # Удаляем директорию и всё её содержимое
                os.makedirs("storage")  # Создаём директорию заново

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
                    list_of_paths.append(path)
        return list_of_paths

    def serch_repo(repos, name):
        for repo in repos:
            if repo.name == name:
                return repo

