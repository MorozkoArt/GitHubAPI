import tkinter as tk
from tkinter import filedialog
from Interface.M_GetInformation import print_assessment


def save_user_information(user, assessment, var_kod):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.geometry("400x300+400+100")

    default_filename = f"GitHub_{user.name}.txt"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile=default_filename,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path:
        print("Сохранение файла отменено.")
        root.destroy()
        return
    try:
        save_to_file(file_path, user, assessment, var_kod)
        print("Информация пользователя сохранена в файл:", file_path)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
    finally:
        root.destroy()

def save_to_file(file_path, user, assessment, var_kod):
    tables_assessment = print_assessment(user, assessment, var_kod)
    with open(file_path, 'w', encoding='utf-8') as file:
        for table in tables_assessment:
            file.write(str(table))


