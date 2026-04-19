import os
import concurrent.futures
import threading
from common.Utils.C_ProgressBar import ProgressBar
from User_and_Repo.C_UserRepo import User_repo
from User_and_Repo.C_MainRepo import Main_repo


class User_GitHub:
    def __init__(self, user, public_or_private):
        self.repos = user.get_repos()
        self.name = user.login
        self.followers = user.followers
        self.following = user.following
        self.hireable = user.hireable
        self.private_repos = user.owned_private_repos
        self.public_repos = user.public_repos
        self.updated_at = self.get_last_activity(user) or user.updated_at
        self.created_at = user.created_at
        self.plan = user.plan
        self.blog = user.blog
        self.company = user.company
        self.public_or_private = public_or_private
        self.org = [org_.login for org_ in user.get_orgs()]
        self.month_usege = self.month_usege()
        self.generate_data()

    def generate_data(self):
        repo_data = self.process_repositories()

        if not repo_data:
            self._set_default_values()
            return

        self._process_repo_data(repo_data)

    def _set_default_values(self):
        self.language_counts: dict[str, int] = {}
        self.frequency_intervals: list[float] = []
        self.frequency_commits = 0
        self.in_day_commits = 0
        self.count_commits = 0
        self.languages = []
        self.repos_user = []
        self.main_repo = None
        self.forks = 0
        self.stars = 0
        self.avg_a_days = 0
        self.avg_cont = 0
        self.avg_views = 0

    def _process_repo_data(self, repo_data):
        (frequencies, daily_commits, counts, languages, repos,
         main_repo, stars, forks,
         avg_a_days, avg_cont, avg_views,
         frequency_intervals) = repo_data

        self.frequency_commits = self.calculate_average(frequencies)
        self.in_day_commits = self.calculate_average(daily_commits)
        self.count_commits = self.calculate_average(counts)
        self.avg_a_days = self.calculate_average(avg_a_days)
        self.avg_cont = self.calculate_average(avg_cont)
        self.avg_views = self.calculate_average(avg_views)
        self.forks = forks
        self.stars = stars
        self.language_counts: dict[str, int] = languages
        self.languages = list(languages.keys())
        self.repos_user = repos
        self.frequency_intervals: list[float] = frequency_intervals
        self.main_repo = Main_repo(main_repo, User_repo.search_repo(self.repos, main_repo.name))

    def process_repositories(self):
        repos_list = list(self.repos)
        total_repos = len(repos_list)

        pbar = ProgressBar(total_repos, "Loading repositories: ")

        try:
            results = self._process_repos_parallel(repos_list, pbar)
            return self._process_parallel_results(results)
        finally:
            pbar.close_pd()

    def _process_repos_parallel(self, repos_list, pbar):
        lock = threading.Lock()

        def update_progress():
            with lock:
                pbar.update_pd()

        def process_repo_wrapper(repo):
            try:
                return User_repo(repo, self.public_or_private)
            except Exception:
                return None
            finally:
                update_progress()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=int(os.getenv("MAX_WORKERS_USER"))
        ) as executor:
            futures = [executor.submit(process_repo_wrapper, repo) for repo in repos_list]
            return self._collect_results(futures)

    def _collect_results(self, futures):
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error in future: {e}")
        return results

    def _process_parallel_results(self, repos_user):
        if not repos_user:
            return None

        commits_frequency: list[float] = []
        commits_in_day: list[float] = []
        commits_count: list[int] = []
        languages: dict[str, int] = {}
        all_frequency_intervals: list[float] = []
        main_repo = repos_user[0]
        max_judgement = 0
        stars = 0
        forks = 0
        avg_a_days: list[float] = []
        avg_cont: list[float] = []
        avg_views: list[float] = []

        for repo_user in repos_user:
            self._process_single_repo_result(
                repo_user, commits_frequency, commits_in_day, commits_count,
                languages, avg_a_days, avg_cont, avg_views,
            )
            stars += repo_user.stargazers_count
            forks += repo_user.forks
            # Агрегируем интервалы здесь — all_frequency_intervals в области видимости
            all_frequency_intervals.extend(repo_user.commits_frequency_intervals)

            max_judgement, main_repo = self.find_main_repo_helper(
                repo_user, max_judgement, main_repo
            )

        return (
            commits_frequency, commits_in_day, commits_count, languages,
            repos_user, main_repo, stars, forks,
            avg_a_days, avg_cont, avg_views,
            all_frequency_intervals,
        )

    def _process_single_repo_result(
        self, repo_user, commits_frequency, commits_in_day,
        commits_count, languages, avg_a_days, avg_cont, avg_views,
    ):
        commits_frequency.append(
            repo_user.commits_frequency if repo_user.commits_frequency != "NULL" else 0
        )
        commits_in_day.append(
            repo_user.commits_in_day if repo_user.commits_in_day != "NULL" else 0
        )
        commits_count.append(repo_user.commits_count)
        avg_a_days.append(repo_user.days_work)
        avg_cont.append(repo_user.contributors_count)
        avg_views.append(repo_user.count_views if repo_user.count_views != "-" else 0)

        if repo_user.language:
            languages[repo_user.language] = languages.get(repo_user.language, 0) + 1

    def find_main_repo_helper(self, repo_user, max_judgement, main_repo):
        if repo_user.language is not None and repo_user.name != self.name:
            judgement = repo_user.tournament()
            if judgement > max_judgement:
                return judgement, repo_user
        return max_judgement, main_repo

    def calculate_average(self, data):
        return sum(data) / len(data) if data else 0

    def month_usege(self):
        if self.updated_at is None or self.created_at is None:
            return 0

        years_diff = self.updated_at.year - self.created_at.year
        months_diff = self.updated_at.month - self.created_at.month
        total_months = years_diff * 12 + months_diff

        if self.updated_at.day < self.created_at.day:
            total_months -= 1

        return total_months

    def get_last_activity(self, user):
        try:
            events = user.get_public_events()
            if events.totalCount > 0:
                return list(events)[0].created_at
        except AttributeError:
            try:
                events = user.get_events()
                if events.totalCount > 0:
                    return list(events)[0].created_at
            except Exception as e:
                print(f"Error getting user events: {e}")
        except Exception as e:
            print(f"Error getting user events: {e}")
        return None