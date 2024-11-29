import os
from StartMethods.M_Start_UserAssessment_generation import (Start_user_generation, Start_assessment_generation
, Start_assessment_generation_empty, Start_userAssessment_generation)
from StartMethods.M_Authentication import Login, LoginPassword, LoginToken
MyToken = os.environ.get("GITHUB_TOKEN")


print("Каким способом вы желаете авторизоваться? \n" 
      " 1 - Авторизация через логин \n"
      " 2 - Авторизация через логин и пароль \n"
      " 3 - Авторизация через токен доступа")
var_aut  = input(" Введите номер варианта авторизации (от 1-цы до 3-ех): ")

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
    login= input(" Введите логин пользователя: ")
    password = input(" Введите пароль: " )
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





