from g4f.client import Client
import os
import re


class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths
        self.MinNumfiles = 5

    def evaluate_codeS(self, full_or_three):
        list_evaluate_codeS = []
        range_gpt = self._get_range_gpt(full_or_three)

        for i in range(range_gpt):
            result = self.evaluate_code(self.listOfPaths[i])
            if result:
                list_evaluate_codeS.append(result)

        return list_evaluate_codeS

    def evaluate_code(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            code = self._read_file(file_path)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return None

        text = self._generate_prompt(code)

        while True:
            try:
                response = self._get_gpt_response(text)
                if self._is_valid_response(response):
                    marks = self._extract_grade(response)
                    if marks >= 0:
                        print(f"Оценка файла {file_name}: {marks}")
                        return response, marks, file_name
            except Exception as e:
                continue

    def _get_range_gpt(self, full_or_three):
        if full_or_three == 1:
            return len(self.listOfPaths)
        return min(self.MinNumfiles, len(self.listOfPaths))

    def _read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()

    def _generate_prompt(self, code):
        return (f"{code} Оцени этот код от 1 до 10-ти (1 - низшее качество, 10 - высочайшее качество)."
                f"Предоставьте оценку и пояснение без копирования кода строго в этом формате:\n "
                f"Оценка: [число от 1 до 10]]\n"
                f"Пояснение оценки: [краткое пояснение, макс. 60 слов на русском языке]")

    def _get_gpt_response(self, text):
        client = Client()
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        ).choices[0].message.content

    def _is_valid_response(self, response):
        return not self._is_request_ended_with_status_code(response)

    def _is_request_ended_with_status_code(self, s):
        pattern = r'^Request ended with status code \d+$'
        return bool(re.match(pattern, s))

    def _extract_grade(self, input_string):
        pattern = r"(?i)\s*оценка:\s*(\d+)"
        match = re.search(pattern, input_string)
        return int(match.group(1)) if match else -1