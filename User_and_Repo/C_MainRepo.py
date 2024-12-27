import os
import shutil
from User_and_Repo.C_UserRepo import User_repo
from Interface.C_ProgressBar import ProgressBar

class Main_repo(User_repo):

    code_extensions = code_extensions = (
        '.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
        '.html', '.css', '.swift', '.ts', '.json', '.sh', '.pl', '.r',
        '.cs', '.bat', '.scala', '.lua', '.rust', '.kotlin', '.vb',
        '.sql', '.yaml', '.dockerfile', '.m', '.swift',
        '.d', '.user', '.clj', '.coffee', '.groovy', '.f90', '.asm'
    )

    def __init__(self, user_repo, repo):
        total = (repo.get_commits().totalCount + 2)
        self.prbar = ProgressBar(total, "Загрузка данных о репозитории: ")
        self.__dict__.update(user_repo.__dict__)
        self.prbar.updatePd()
        commits_addLines_value, commits_delLines_value = self.Commits_LineChange()
        self.repo = repo
        self.commits_addLines = commits_addLines_value
        self.commits_delLines = commits_delLines_value
        self.contentsKod = self.get_contentKod()
        self.prbar.updatePd()
        self.nameFiles = ", ".join(content_file.name for content_file in self.contentsKod)
        self.prbar.closePd()

    def Commits_LineChange(self):
        commits_addLines_list = []
        commits_delLines_list = []
        for i in range (self.commits.totalCount):
            line_changes = self.get_commit_lines_changed(self.commits[i])
            if line_changes:
                added, removed = line_changes
                if added!=0 or removed!=0:
                    commits_addLines_list.append(added)
                    commits_delLines_list.append(removed)
            self.prbar.updatePd()

        if len(commits_addLines_list)!=0:
            commits_addLines_value = sum(commits_addLines_list) / len(commits_addLines_list)
        else:
            commits_addLines_value = "NULL"
        if len(commits_delLines_list)!=0:
            commits_delLines_value = sum(commits_delLines_list) / len(commits_delLines_list)
        else:
            commits_delLines_value = "NULL"
        return  commits_addLines_value, commits_delLines_value

    def get_commit_lines_changed(self, commit):
        try:
            lines_added = 0
            lines_removed = 0
            if hasattr(commit, 'files'):
                for file_data in commit.files:
                    if file_data.filename.lower().endswith(tuple(self.code_extensions)):
                        lines_added += file_data.additions
                        lines_removed += file_data.deletions
            return (lines_added, lines_removed)
        except AttributeError as e:
            print(f"Error accessing commit file data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_contentKod(self):
        contentsKod = []
        contents = self.repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            elif file_content.type == "file":
                if file_content.name.lower().endswith(self.code_extensions):
                    contentsKod.append(file_content)
        return contentsKod


    def dounloud_mainRepo(self):
        list_of_paths = []
        print(f"Загрузка файлов из репозитория: {self.repo.name}")
        if not os.path.exists("storage"):
            os.makedirs("storage")
        else:
            # Проверка, пуста ли директория
            if os.listdir("storage"):
                shutil.rmtree("storage")  # Удаляем директорию и всё её содержимое
                os.makedirs("storage")  # Создаём директорию заново

        for file_content in self.contentsKod:
            path = os.path.join("storage", file_content.name)
            with open(path, 'wb') as f:
                f.write(file_content.decoded_content)
            list_of_paths.append(path)
        return list_of_paths


