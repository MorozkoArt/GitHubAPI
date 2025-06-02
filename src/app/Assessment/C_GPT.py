from g4f.client import Client
import os
import re

class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths
        self.MinNumfiles = 5

    def evaluate_codeS(self, full_or_three):
        list_evaluate_codeS = []
        range_gpt = self.get_range_gpt(full_or_three)

        for i in range(range_gpt):
            result = self.evaluate_code(self.listOfPaths[i])
            if result:
                list_evaluate_codeS.append(result)

        return list_evaluate_codeS

    def evaluate_code(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            code = self.read_file(file_path)
        except FileNotFoundError:
            print(f"file {file_path} not found")
            return None

        text = self.generate_prompt(code)

        while True:
            try:
                response = self.get_gpt_response(text)
                if self.is_valid_response(response):
                    marks = self.extract_grade(response)
                    if marks >= 0:
                        print(f"File rating {file_name}: {marks}")
                        return response, marks, file_name
            except Exception as e:
                continue

    def get_range_gpt(self, full_or_three):
        if full_or_three == 1:
            return len(self.listOfPaths)
        return min(self.MinNumfiles, len(self.listOfPaths))

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()

    def generate_prompt(self, code):
        return (f"{code} Rate this code from 1 to 10 (1 - lowest quality, 10 - highest quality)."
                        f"Provide your rating and explanation without copying the code strictly in this format:\n "
                        f"Rating: [number from 1 to 10]]\n"
                        f"Explanation of rating: [brief explanation, max. 60 words in English]")

    def get_gpt_response(self, text):
        client = Client()
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        ).choices[0].message.content

    def is_valid_response(self, response):
        return not self.is_request_ended_with_status_code(response)

    def is_request_ended_with_status_code(self, s):
        pattern = r'^Request ended with status code \d+$'
        return bool(re.match(pattern, s))

    def extract_grade(self, input_string):
        pattern = r"(?i)\s*Rating:\s*(\d+)"
        match = re.search(pattern, input_string)
        return int(match.group(1)) if match else -1