import textwrap
from User_and_Repo.C_User import User_GitHub
from Assessment.C_ProfileAssessment import ProfileAssessment
from Interface.M_SaveInformation import save_user_information


def Start_user_generation (user, publicOrPrivate):
    user_git = User_GitHub(user, publicOrPrivate)
    contentsKod = user_git.main_repo.nameFiles
    return user_git, contentsKod

def Start_assessment_generation_empty(user_git):
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    if user_git.repos.totalCount == 0:
        assessment_repos = 0
        assessment_kod = 0
        print("У пользователя не обнаружены репозитории")
        print(f"Оценка профиля: {assessment_profile}")
    var_kod = 2
    save_user_information(user_git, assessment, var_kod)

def Start_assessment_generation (user_git, var_kod, var_kod_2):

    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    assessment_repos = assessment.assessment_repos()

    assessment_kod = 0
    if var_kod == 1:
        assessment_kod = assessment.assessment_kod(var_kod_2)
    print(
        f"Оценка профиля: {assessment_profile}, Оценка репозиториев: {assessment_repos}, Оценка кода: {assessment_kod}")
    assessmet = assessment_profile + assessment_repos + assessment_kod
    print(f"Общая оценка: {assessmet}")

    save_user_information(user_git, assessment, var_kod)

def Start_userAssessment_generation (user, publicOrPrivate):
    user_git, contentKod = Start_user_generation(user, publicOrPrivate)
    if len(user_git.repos_user) == 0:
        Start_assessment_generation_empty(user_git)
    else:
        print(
            "Желаете ли вы оценить код внутри одного репозитория? (репозиторий выбирался по количеству комитов, звезд, ветвей и простмотров)")
        print("Оценка кода займет достаточно много времени (от 1 минуты до 15)")
        print(
            f"Файлы с кодом, которые содержатся в репозитории для оценки:\n {textwrap.fill(contentKod, width=65)}")
        var_kod = int(input("Введите 1, если - оценить, введите 2 - оценка не нужна: "))
        var_kod_2 = 2
        if var_kod == 1:
            print("Если репозиторий содержит много файлов с кодом, оценивать все или первые три?")
            var_kod_2 = int(input("Введите 1, если - оценить все, введите 2 - оценить первые три: "))
        Start_assessment_generation(user_git, var_kod, var_kod_2)




