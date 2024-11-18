import tkinter as tk
from tkinter import filedialog

def save_user_information(user):
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
            tables = user.Print_user_information()
            for i in range(len(tables)):
                f.write(str(tables[i]))
                if i == 0:
                    f.write('\n Репозитории: \n')
                else:
                    f.write('\n\n')
        print("Информация пользователя сохранена в файл:", file_path)
    else:
        print("Сохранение файла отменено.")
    root.destroy()