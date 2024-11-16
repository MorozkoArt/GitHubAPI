import requests

from github import Github
from github import Auth

from C_User import User_GitHub
from C_ProfileAssessment import ProfileAssessment
from M_SaveInformation import save_user_information



#Основной метод вызозова
def take_data (user, publicOrPrivate):
    user_git = User_GitHub(user.login, user.followers, user.following, user.hireable, user.owned_private_repos, user.public_repos,
                           user.updated_at, user.created_at, user.plan, user.blog, user.get_repos(), user.company, user.get_orgs(), publicOrPrivate)
    assessment = ProfileAssessment(user_git)
    assessment_profile = assessment.assessment_profile()
    assessment_repos = assessment.assessment_repos()
    assessmet = assessment_profile + assessment_repos
    test = 0 #Оценка кода
    print("Желаете ли вы оценить код внутри одного репозитория? (репозиторий выбирался по количеству комитов, звезд, ветвей и простмотров)")
    print("Оценка кода займет достаточно много времени (от 1 минуты до 15)")
    var_kod = int(input("Введите 1, если - оценить, введите 2 - оценка не нужна: "))
    if var_kod == 1:
        print("Если репозиторий содержит много файлов с кодом, оценивать все или первые три?")
        var_kod_2 = int(input("Введите 1, если - оценить все, введите 2 - оценить первые три: "))
        test = assessment.assessment_kod(var_kod_2)
    print(f"Оценка профиля: {assessment_profile}, Оценка репозиториев: {assessment_repos}, Общая оценка: {assessmet}",)
    if var_kod == 1:
        print(f"Оценка кода:{test}")
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


#######################  Main
print("Каким способом вы желаете авторизоваться? \n" 
      " 1 - Авторизация через логин \n"
      " 2 - Авторизация через логин и пароль \n"
      " 3 - Авторизация через токен доступа")
var_aut  = input(" Введите номер варианта авторизации (от 1-цы до 3-ех) или полность навзвание варианта: ")

#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

MyToken = "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"
if var_aut == "1":
    login = input(" Введите логин пользователя: ")
    try:
        g = Github(MyToken)
        user = g.get_user(login)
        publicOrPrivate = "public"
        take_data(user, publicOrPrivate)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

elif var_aut == "2":
    login= input(" Введите логин пользователя: ")
    password = input(" Введите пароль: " )
    try:
        auth = Auth.Login(login, password)
        g = Github(auth=auth)
        user = g.get_user()
        publicOrPrivate = "private"
        take_data(user,publicOrPrivate)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

elif var_aut == "3":
    access_token = input(" Введите токен доступа пользователя: ")
    try:
        auth = Auth.Token(access_token)
        login = Github(auth=auth)
        user = login.get_user()
        publicOrPrivate = "private"
        take_data(user, publicOrPrivate)
    except Exception as e:
        print(f"Произошла ошибка: {e}")





