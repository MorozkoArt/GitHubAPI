import textwrap
from User_and_Repo.C_User import User_GitHub
from Assessment.C_ProfileAssessment import ProfileAssessment
from Interface.M_SaveInformation import save_user_information


def Start_user_generation(user, publicOrPrivate):
    return User_GitHub(user, publicOrPrivate)


def Start_mainRepo_generation(user_git):
    user_git._find_main_repo()
    return user_git.main_repo.nameFiles


def Start_assessment_generation_empty(user_git):
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()

    if user_git.repos.totalCount == 0:
        print("The user has no repositories.")
        print(f"Profile assessment: {round(assessment_profile, 2)}")
    elif user_git.main_repo_name == "":
        print("The user has no repositories containing code files.")
        if len(user_git.repos_user) != 0:
            assessment_repos = assessment.assessment_repos()
            print(f"Profile assessment: {round(assessment_profile, 2)}")
            print(f"Repositories assessment: {round(assessment_repos, 2)}")
            assessmet = round((assessment_profile + assessment_repos), 2)
        else:
            print("All existing repositories are empty.")
            print(f"Profile assessment: {round(assessment_profile, 2)}")
            assessmet = round(assessment_profile, 2)
        print(f"Total assessment: {assessmet}")

    save_user_information(user_git, assessment, var_kod=2)


def Start_assessment_generation(user_git, var_kod, var_kod_2):
    """Generate a detailed assessment for a user with repositories."""
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    assessment_repos = assessment.assessment_repos()
    assessment_kod = 0
    assessment_Mainrepo = 0

    if var_kod == 1:
        assessment_Mainrepo = assessment.assessment_Mainrepo()
        assessment_kod = assessment.assessment_kod(var_kod_2)

    print(
        f"Profile assessment: {round(assessment_profile, 2)}, "
        f"Repositories assessment: {round(assessment_repos, 2)}, "
        f"Main repository assessment: {round(assessment_Mainrepo, 2)}, "
        f"Code assessment: {round(assessment_kod, 2)}"
    )
    assessmet = round((assessment_profile + assessment_repos + assessment_Mainrepo + assessment_kod), 2)
    print(f"Total assessment: {assessmet}")

    save_user_information(user_git, assessment, var_kod)


def Start_userAssessment_generation(user, publicOrPrivate):
    user_git = Start_user_generation(user, publicOrPrivate)

    if user_git.repos.totalCount == 0:
        Start_assessment_generation_empty(user_git)
    else:
        var_kod_2 = 2
        if user_git.main_repo_name:
            print(
                f"\nWould you like to assess the main repository ({user_git.main_repo_name}) in more detail? "
                "(The repository was selected based on activity level)\n"
                "This will assess the repository and the code files within it."
            )
            var_kod = int(input("Enter 1 to assess, or 2 to skip: "))
            if var_kod == 1:
                contentKod = Start_mainRepo_generation(user_git)
                print("\nCode assessment may take a significant amount of time (from 1 to 15 minutes).")
                print(f"Code files in the repository {user_git.main_repo.name} for assessment:\n"
                      f"{textwrap.fill(contentKod, width=65)}\n")
                print("If the repository contains many code files, assess all or the first five?")
                var_kod_2 = int(input("Enter 1 to assess all, or 2 to assess the first five: "))
            Start_assessment_generation(user_git, var_kod, var_kod_2)
        else:
            Start_assessment_generation_empty(user_git)