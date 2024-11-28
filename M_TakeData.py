from User_and_Repo.C_User import User_GitHub
from Assessment.C_ProfileAssessment import ProfileAssessment
from Interface.M_SaveInformation import save_user_information
from M_GetInformation import print_assessment

def take_data (user, publicOrPrivate, var_kod, var_kod_2):
    user_git = User_GitHub(user, publicOrPrivate)
    assessment = ProfileAssessment(user_git)

    assessment_profile = assessment.assessment_profile()

#    var_kod = 2
    if publicOrPrivate == "public" and user_git.public_repos == 0:
        assessment_repos = 0
        assessment_kod = 0
        print("У пользователя не обнаружены репозитории")
        print(f"Оценка профиля: {assessment_profile}")
    elif publicOrPrivate == "private" and user_git.public_repos+ user_git.private_repos == 0:
        assessment_repos = 0
        assessment_kod = 0
        print("У пользователя не обнаружены репозитории")
        print(f"Оценка профиля: {assessment_profile}")
    else:
        assessment_repos = assessment.assessment_repos()
        assessment_kod = 0
        if var_kod == 1:
            assessment_kod = assessment.assessment_kod(var_kod_2)
        print(f"Оценка профиля: {assessment_profile}, Оценка репозиториев: {assessment_repos}, Оценка кода: {assessment_kod}")
        assessmet = assessment_profile + assessment_repos + assessment_kod
        print(f"Общая оценка: {assessmet}")

    save_user_information(user_git, assessment, var_kod)

    """print("Желаете ли вы получить подробную информацию об оценке?\n"
          " 1 - если желаете загрузить файл с информациеей\n"
          " 2 - если выгрузить всю подробную информацию в консоль\n"
          " 3 - если вам не нужна подробная информация")
#    var = int(input("Введите число от 1-го до 3-ех: "))
    if var == 1:
        save_user_information(user_git, assessment, var_kod)
    elif var == 2:
        tables = print_assessment(user_git, assessment, var_kod)
        for table in tables:
            print(str(table))
    else:
        exit()"""
