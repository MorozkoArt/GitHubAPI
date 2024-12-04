from g4f.client import Client
import os
import re

class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths

    def evaluate_codeS(self, full_or_three):
        list_evaluate_codeS = []
        MinNumfiles = 5
        if full_or_three == 1:
            range_gpt = len(self.listOfPaths)
        else:
            if len(self.listOfPaths) > MinNumfiles:
                range_gpt = MinNumfiles
            else:
               range_gpt = len(self.listOfPaths)
        for i in range (range_gpt):
            list_evaluate_codeS.append(self.evaluate_code(self.listOfPaths[i]))
        return list_evaluate_codeS

    def evaluate_code(self, file_path):
        while True:
            try:
                file_name = os.path.basename(file_path)
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:  # Specify encoding
                    code = file.read()
                text = (f"{code}: оцени этот код от 1 до 10-ти, и выведи ответ в следующем формате: "
                        f"Оценка: [число оценки] Пояснение оценки: [пояснение оценки]. Оценку произведи на русском языке, максимальное число слов не больше 50")
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

            except FileNotFoundError:
                print(f"Файл {file_path} не найден.")
                return
            except Exception as e:
                print(f"Произошла ошибка: {e}. Перезагрузка алгоритма...")


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



