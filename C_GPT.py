from g4f.client import Client
import re

class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths
    def evaluate_codeS(self, full_or_three):
        list_evaluate_codeS = []
        range_gpt = 0
        if full_or_three == 1:
            range_gpt = len(self.listOfPaths)
        else:
            range_gpt = 3
        for i in range (range_gpt):
            list_evaluate_codeS.append(self.evaluate_code(self.listOfPaths[i]))
        return list_evaluate_codeS
    # Чат GPT
    def evaluate_code(self, file_path):
        while True:
            try:
                with open(file_path, 'rb') as file:
                    code = file.read()
                text = (f"{code}: оцени этот код от 1 до 10-ти, и выведи ответ в следующем формате: "
                        f"Оценка: [число оценки] Пояснение оценки: [пояснение оценки]")
                client = Client()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": text}]
                )
                if self.is_request_ended_with_status_code(response.choices[0].message.content) == False:
                    marks = self.check_grade_format(response.choices[0].message.content)
                    if marks >=0:
                        print(response.choices[0].message.content)
                        return response.choices[0].message.content, marks
                        break  # Выход из цикла при успешном выполнении
            except Exception as e:
                print(f"Произошла ошибка: {e}. Попробуйте снова.")

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



