from g4f.client import Client
import os
import re

class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths
        self.MinNumfiles = 5

    def evaluate_codeS(self, full_or_three):
        list_evaluate_codeS = []
        if full_or_three == 1:
            range_gpt = len(self.listOfPaths)
        else:
            if len(self.listOfPaths) > self.MinNumfiles:
                range_gpt = self.MinNumfiles
            else:
               range_gpt = len(self.listOfPaths)
        for i in range (range_gpt):
            list_evaluate_codeS.append(self.evaluate_code(self.listOfPaths[i]))
        return list_evaluate_codeS

    def evaluate_code(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:  # Specify encoding
                code = file.read()
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return

        text = (f"{code} Оцени этот код от 1 до 10-ти (1 - низшее качество, 10 - высочайшее качество)."
                f"Предоставьте оценку и пояснение без копирования кода строго в этом формате:\n "
                f"Оценка: [число от 1 до 10]]\n"
                f"Пояснение оценки: [краткое пояснение, макс. 60 слов на русском языке]")

        while True:
            try:
                client = Client()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": text}]
                )
                if self.is_request_ended_with_status_code(response.choices[0].message.content) == False:
                    marks = self.check_grade_format(response.choices[0].message.content)
                    if marks >=0:
                        print(f"Оценка файла {file_name}: {marks}")
                        return response.choices[0].message.content, marks, file_name
                        break  # Выход из цикла при успешном выполнении
            except Exception as e:
                continue


    def is_request_ended_with_status_code(self, s):
        # Определяем регулярное выражение для поиска соответствия
        pattern = r'^Request ended with status code \d+$'
        return bool(re.match(pattern, s))

    def check_grade_format(self, input_string):
        # Регулярное выражение для проверки формата "Оценка: [число оценки]" с возможным продолжением текста
        pattern = r"(?i)\s*оценка:\s*(\d+)"
        match = re.search(pattern, input_string)
        marks = -1
        if match:
            marks = int(match.group(1))
        return marks



