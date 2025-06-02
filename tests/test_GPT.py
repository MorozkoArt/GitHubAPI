import textwrap
import pytest
from src.app.Assessment.C_GPT import GPT
from src.app.Assessment import C_ProfileAssessment

file_path = C_ProfileAssessment.__file__
@pytest.mark.parametrize("list_of_paths", [([file_path])])
def test_gpt(list_of_paths):
    gpt = GPT(list_of_paths)
    results = gpt.evaluate_codeS(1)
    for result in results:
        message, marks, file_name = result
        print(f"Файл: {file_name}, Оценка: {marks}, Пояснение оценки: {textwrap.fill(message, width=80)}")

