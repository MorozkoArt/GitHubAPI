from User_and_Repo.C_User import User_GitHub
from Assessment.C_ProfileAssessment import ProfileAssessment
from Interface.M_SaveInformation import save_user_information

def take_data (user, publicOrPrivate):
    user_git = User_GitHub(user.login, user.followers, user.following, user.hireable, user.owned_private_repos, user.public_repos,
                           user.updated_at, user.created_at, user.plan, user.blog, user.get_repos(), user.company, user.get_orgs(), publicOrPrivate)
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    assessment_repos = assessment.assessment_repos()
    assessment_kod = 0 #Оценка кода
    print("Желаете ли вы оценить код внутри одного репозитория? (репозиторий выбирался по количеству комитов, звезд, ветвей и простмотров)")
    print("Оценка кода займет достаточно много времени (от 1 минуты до 15)")
    var_kod = int(input("Введите 1, если - оценить, введите 2 - оценка не нужна: "))
    if var_kod == 1:
        print("Если репозиторий содержит много файлов с кодом, оценивать все или первые три?")
        var_kod_2 = int(input("Введите 1, если - оценить все, введите 2 - оценить первые три: "))
        assessment_kod = assessment.assessment_kod(var_kod_2)
    if var_kod == 1:
        print(f"Оценка профиля: {assessment_profile}, Оценка репозиториев: {assessment_repos}, Оценка кода: {assessment_kod}")
    else:
        print(f"Оценка профиля: {assessment_profile}, Оценка репозиториев: {assessment_repos}")
    assessmet = assessment_profile + assessment_repos + assessment_kod
    print(f"Общая оценка: {assessmet}")
    print("Желаете ли вы получить подробную информацию об оценке?\n"
          " 1 - если желаете загрузить файл с информациеей\n"
          " 2 - если выгрузить всю подробную информацию в консоль\n"
          " 3 - если вам не нужна подробная информация")
    var = int(input("Введите число от 1-го до 3-ех: "))
    if var == 1:
        save_user_information(user_git)
    elif var == 2:
        tables = user_git.Print_user_information()
        for i in range(len(tables)):
            print(str(tables[i]))
            if i == 0:
                print('\n Репозитории: \n')
            else:
                print('\n\n')
    else:
        exit()