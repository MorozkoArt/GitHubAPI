import os
import shutil
import concurrent.futures
import threading
from src.app.User_and_Repo.C_UserRepo import User_repo
from src.app.Interface.C_ProgressBar import ProgressBar
from src.app.Config.file_extensions import is_code_file

class Main_repo(User_repo):

    def __init__(self, user_repo, repo):
        self.__dict__.update(user_repo.__dict__)
        commits_add_lines_value, commits_del_lines_value = self.commits_line_change_parallel()
        self.repo = repo
        self.commits_add_lines = commits_add_lines_value
        self.commits_del_lines = commits_del_lines_value
        self.contents_kod = self.get_content_kod_parallel()
        self.name_files = ", ".join(content_file.name for content_file in self.contents_kod)

    def commits_line_change_parallel(self):
        if self.commits.totalCount == 0:
            return "NULL", "NULL"
        
        prbar = ProgressBar(self.commits.totalCount, "Loading repo data: ")
        commits_add_lines_list = []
        commits_del_lines_list = []
        lock = threading.Lock()
        
        def process_commit(commit):
            try:
                line_changes = self.get_commit_lines_changed(commit)
                if line_changes:
                    added, removed = line_changes
                    if added != 0 or removed != 0:
                        with lock:
                            commits_add_lines_list.append(added)
                            commits_del_lines_list.append(removed)
            finally:
                prbar.update_pd()
        
        try:
            max_workers = min(10, self.commits.totalCount)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                list(executor.map(process_commit, list(self.commits)))
                
        finally:
            prbar.close_pd()

        commits_add_lines_value = self._calculate_average(commits_add_lines_list)
        commits_del_lines_value = self._calculate_average(commits_del_lines_list)
        
        return commits_add_lines_value, commits_del_lines_value

    def _calculate_average(self, data_list):
        if not data_list:
            return "NULL"
        return sum(data_list) / len(data_list)

    def get_content_kod_parallel(self):
        contents_kod = []
        lock = threading.Lock()
        
        def process_directory(path):
            try:
                contents = self.repo.get_contents(path)
                for content in contents:
                    if content.type == "dir":
                        process_directory(content.path)
                    elif content.type == "file" and is_code_file(content.name):
                        with lock:
                            contents_kod.append(content)
            except Exception as e:
                print(f"Error processing directory {path}: {e}")

        process_directory("")

        return contents_kod

    def get_content_kod_optimized(self):
        contents_kod = []
        directories_to_process = [""]
        lock = threading.Lock()
        
        def process_single_directory(path):
            try:
                contents = self.repo.get_contents(path)
                files = []
                new_directories = []
                
                for content in contents:
                    if content.type == "dir":
                        new_directories.append(content.path)
                    elif content.type == "file" and is_code_file(content.name):
                        files.append(content)
                
                with lock:
                    contents_kod.extend(files)
                
                return new_directories
            except Exception as e:
                print(f"Error processing directory {path}: {e}")
                return []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while directories_to_process:
                futures = []
                current_batch = directories_to_process[:10]
                directories_to_process = directories_to_process[10:]
                
                for directory in current_batch:
                    futures.append(executor.submit(process_single_directory, directory))
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        new_dirs = future.result()
                        directories_to_process.extend(new_dirs)
                    except Exception as e:
                        print(f"Error in directory processing: {e}")
        
        return contents_kod

    def get_commit_lines_changed(self, commit):
        try:
            lines_added = 0
            lines_removed = 0
            if hasattr(commit, 'files'):
                for file_data in commit.files:
                    if is_code_file(file_data.filename):
                        lines_added += file_data.additions
                        lines_removed += file_data.deletions
            return (lines_added, lines_removed)
        except AttributeError as e:
            print(f"Error accessing commit file data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def dounloud_mainRepo(self):
        list_of_paths = []
        print(f"Downloading files from the repository: {self.repo.name}")
        
        if not os.path.exists("storage"):
            os.makedirs("storage")
        elif os.listdir("storage"):
            shutil.rmtree("storage")
            os.makedirs("storage")
        
        def download_file(file_content):
            try:
                path = os.path.join("storage", file_content.name)
                with open(path, 'wb') as f:
                    f.write(file_content.decoded_content)
                return path
            except Exception as e:
                print(f"Error downloading {file_content.name}: {e}")
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(download_file, file_content) 
                    for file_content in self.contents_kod]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    path = future.result()
                    if path:
                        list_of_paths.append(path)
                except Exception as e:
                    print(f"Error in file download: {e}")
        
        return list_of_paths
