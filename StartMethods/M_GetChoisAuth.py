from StartMethods.M_Start_UserAssessment_generation import  Start_userAssessment_generation
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken

def Get_user_auth_method():
    print("Каким способом вы желаете авторизоваться? \n"
          " 1 - Авторизация через логин \n"
          " 2 - Авторизация через логин и пароль \n"
          " 3 - Авторизация через токен доступа")
    while True:
        choice = input("Введите номер варианта авторизации (от 1 до 3): ")
        if choice in ("1", "2", "3"):
            return choice
        print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

def Chois_start(var_aut, MyToken):
    if var_aut == "1":
        publicOrPrivate = "public"
        login = input(" Введите логин пользователя: ")
        try:
            user = Login(MyToken, login)
            Start_userAssessment_generation(user, publicOrPrivate)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    elif var_aut == "2":
        publicOrPrivate = "private"
        login = input(" Введите логин пользователя: ")
        password = input(" Введите пароль: ")
        try:
            user = LoginPassword(login, password)
            Start_userAssessment_generation(user, publicOrPrivate)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    elif var_aut == "3":
        publicOrPrivate = "private"
        access_token = input(" Введите токен доступа пользователя: ")
        try:
            user = LoginToken(access_token)
            Start_userAssessment_generation(user, publicOrPrivate)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

