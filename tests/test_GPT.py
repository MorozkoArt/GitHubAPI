import textwrap
import pytest
from Assessment.C_GPT import GPT
from g4f.client import Client
import os
import re

file_path = ["C:\Python\PycharmProjects\GitHubAPI\Assessment\C_ProfileAssessment.py"]
@pytest.mark.parametrize("listOfPaths" , [(file_path)])
def test_Gpt(listOfPaths):
    gpt = GPT(listOfPaths)
    results = gpt.evaluate_codeS(1)
    for result in results:
        message, marks, file_name = result
        print(f"Файл: {file_name}, Оценка: {marks}, Пояснение оценки: {textwrap.fill(message, width=80)}")

