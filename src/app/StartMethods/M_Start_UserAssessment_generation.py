import textwrap
from src.app.User_and_Repo.C_User import User_GitHub
from src.app.Assessment.C_ProfileAssessment import ProfileAssessment
from src.app.Interface.M_SaveInformation import save_user_information

def start_main_repo_generation(user_git):
    user_git.find_main_repo()
    return user_git.main_repo.name_files


def start_assessment_generation_empty(user_git):
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()

    if user_git.repos.totalCount == 0:
        print("The user has no repositories.")
        print(f"Profile assessment: {round(assessment_profile, 2)}")
    elif user_git.main_repo_name == "":
        print("The user has no repositories containing code files.")
        if len(user_git.repos_user) != 0:
            print(f"Profile assessment: {round(assessment_profile, 2)}")
            assessment_value = round((assessment_profile), 2)
        else:
            print("All existing repositories are empty.")
            print(f"Profile assessment: {round(assessment_profile, 2)}")
            assessment_value = round(assessment_profile, 2)
        print(f"Total assessment: {assessment_value}")

    save_user_information(user_git, assessment, var_kod=2)


def start_assessment_generation(user_git, var_kod_2):
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    assessment_kod = 0
    assessment_main_repo = 0

    assessment_main_repo = assessment.assessment_mainrepo()
    assessment_kod = assessment.assessment_kod(var_kod_2)

    print(
        f"Profile assessment: {round(assessment_profile, 2)}, "
        f"Main repository assessment: {round(assessment_main_repo, 2)}, "
        f"Code assessment: {round(assessment_kod, 2)}"
    )
    assessment_value = round((assessment_profile + assessment_main_repo + assessment_kod), 2)
    print(f"Total assessment: {assessment_value}")

    save_user_information(user_git, assessment)


def start_user_assessment_generation(user, public_or_private):
    user_git = User_GitHub(user, public_or_private)

    if user_git.repos.totalCount == 0:
        start_assessment_generation_empty(user_git)
    else:
        var_kod_2 = 2
        if user_git.main_repo_name:
            content_kod = start_main_repo_generation(user_git)
            print("\nCode assessment may take a significant amount of time (from 1 to 15 minutes).")
            print(f"Code files in the repository {user_git.main_repo.name} for assessment:\n"
                    f"{textwrap.fill(content_kod, width=65)}\n")
            print("If the repository contains many code files, assess all or the first five?")
            var_kod_2 = int(input("Enter 1 to assess all, or 2 to assess the first five: "))
            start_assessment_generation(user_git, var_kod_2)
        else:
            start_assessment_generation_empty(user_git)