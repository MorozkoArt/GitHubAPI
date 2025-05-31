import os
import shutil
from src.app.User_and_Repo.C_UserRepo import User_repo
from src.app.Interface.C_ProgressBar import ProgressBar

class Main_repo(User_repo):

    code_extensions = code_extensions = (
        '.py', '.java', '.js', '.cpp', '.c', '.rb', '.go', '.php',
        '.html', '.css', '.swift', '.ts', '.sh', '.pl', '.r',
        '.cs', '.bat', '.scala', '.lua', '.rust', '.kotlin', '.vb',
        '.sql', '.yaml', '.dockerfile', '.m', '.swift',
        '.d', '.user', '.clj', '.coffee', '.groovy', '.f90', '.asm',
        '.hs', '.erl', '.ex', '.elm', '.fs', '.fsx', '.ml', '.mli',
        '.jl', '.nim', '.pas', '.purs', '.re', '.v', '.vhd', '.vhdl',
        '.zig', '.odin', '.dart', '.tcl', '.awk', '.sed', '.ps1',
        '.jsx', '.tsx', '.vue', '.svelte', '.pug', '.jade', '.ejs',
        '.hbs', '.handlebars', '.mustache', '.twig', '.haml', '.scss',
        '.less', '.styl', '.sass', '.stylus',
    )

    def __init__(self, user_repo, repo):
        self.__dict__.update(user_repo.__dict__)
        commits_add_lines_value, commits_del_lines_value = self.commits_line_change()
        self.repo = repo
        self.commits_add_lines = commits_add_lines_value
        self.commits_del_lines = commits_del_lines_value
        self.contents_kod = self.get_content_kod()
        self.name_files = ", ".join(content_file.name for content_file in self.contents_kod)

    def commits_line_change(self):
        prbar = ProgressBar(self.commits.totalCount, "Loading repo data: ")
        commits_add_lines_list = []
        commits_del_lines_list = []
        for i in range (self.commits.totalCount):
            line_changes = self.get_commit_lines_changed(self.commits[i])
            if line_changes:
                added, removed = line_changes
                if added!=0 or removed!=0:
                    commits_add_lines_list.append(added)
                    commits_del_lines_list.append(removed)
            prbar.update_pd()

        if len(commits_add_lines_list)!=0:
            commits_add_lines_value = sum(commits_add_lines_list) / len(commits_add_lines_list)
        else:
            commits_add_lines_value = "NULL"
        if len(commits_del_lines_list)!=0:
            commits_del_lines_value = sum(commits_del_lines_list) / len(commits_del_lines_list)
        else:
            commits_del_lines_value = "NULL"
        
        prbar.close_pd()
        return  commits_add_lines_value, commits_del_lines_value

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

    def get_content_kod(self):
        contents_kod = []
        contents = self.repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            elif file_content.type == "file":
                if file_content.name.lower().endswith(self.code_extensions):
                    contents_kod.append(file_content)
        return contents_kod


    def dounloud_mainRepo(self):
        list_of_paths = []
        print(f"Загрузка файлов из репозитория: {self.repo.name}")
        if not os.path.exists("storage"):
            os.makedirs("storage")
        else:
            if os.listdir("storage"):
                shutil.rmtree("storage")
                os.makedirs("storage")

        for file_content in self.contents_kod:
            path = os.path.join("storage", file_content.name)
            with open(path, 'wb') as f:
                f.write(file_content.decoded_content)
            list_of_paths.append(path)
        return list_of_paths


