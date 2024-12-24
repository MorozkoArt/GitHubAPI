import textwrap
import pytest
from Assessment.C_GPT import GPT
from g4f.client import Client
from Assessment import C_ProfileAssessment

file_path = C_ProfileAssessment.__file__
@pytest.mark.parametrize("listOfPaths" , [([file_path])])
def test_Gpt(listOfPaths):
    gpt = GPT(listOfPaths)
    results = gpt.evaluate_codeS(1)
    for result in results:
        message, marks, file_name = result
        print(f"Файл: {file_name}, Оценка: {marks}, Пояснение оценки: {textwrap.fill(message, width=80)}")

