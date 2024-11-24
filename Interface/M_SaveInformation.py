import tkinter as tk
from tkinter import filedialog
from M_GetInformation import print_assessment

def save_user_information(user, assessment, var_kod):
    # Создание диалогового окна для выбора места сохранения файла
    root = tk.Tk()
    root.withdraw() # Скрыть главное окно
    root.attributes('-topmost', True)
    root.geometry("400x300+400+100")
    default_filename = f"GitHub_{user.name}.txt"
    # Открытие диалога для выбора пути и имени файла
    file_path = filedialog.asksaveasfilename(defaultextension = ".txt",
                                             initialfile=default_filename,
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            tables_assesment = print_assessment(user, assessment, var_kod)
            for tables in tables_assesment:
                f.write(str(tables))

        print("Информация пользователя сохранена в файл:", file_path)
    else:
        print("Сохранение файла отменено.")
    root.destroy()