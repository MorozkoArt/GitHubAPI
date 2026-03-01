import os
import re
import requests
import time
from common.Utils.M_Clear_text import sanitize_response


class GPT:
    def __init__(self, listOfPaths):
        self.listOfPaths = listOfPaths
        self.MinNumfiles = 5

        self.api_token  = os.getenv("HF_TOKEN")
        self.api_url    = os.getenv("HF_API_URL")
        self.model_name = os.getenv("HF_MODEL_NAME")

        if not self.api_token:
            raise RuntimeError("HF_TOKEN is not set. Check your .env file.")
        if not self.api_url:
            raise RuntimeError("HF_API_URL is not set. Check your .env file.")
        if not self.model_name:
            raise RuntimeError("HF_MODEL_NAME is not set. Check your .env file.")

    def evaluate_codeS(self, full_or_three):
        results   = []
        range_gpt = self.get_range_gpt(full_or_three)

        for i in range(min(len(self.listOfPaths), range_gpt)):
            result = self.evaluate_code(self.listOfPaths[i])
            if result:
                results.append(result)
        return results

    def evaluate_code(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            code      = self.read_file(file_path)

            if len(code) > 15000:
                code = code[:15000] + "\n... [Code truncated]"
        except Exception as e:
            print(f"[ERROR] Reading file {file_path}: {e}")
            return None

        prompt = self.generate_prompt(code)

        try:
            raw_response = self.get_gpt_response(prompt)
            if not raw_response:
                return None

            response = sanitize_response(raw_response)
            marks    = self.extract_grade(response)

            if 1 <= marks <= 10:
                print(f"[OK] File: {file_name} | Rating: {marks}")
                return response, marks, file_name
            else:
                print(f"[WARN] Could not parse rating for {file_name}. Response: {response[:50]}...")
                return None

        except Exception as e:
            print(f"[ERROR] Request failed for {file_name}: {e}")
            return None

    def get_gpt_response(self, text):
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type":  "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role":    "system",
                    "content": "You are a professional code auditor. Return rating from 1 to 10 and a brief explanation.",
                },
                {"role": "user", "content": text},
            ],
            "temperature": 0.1,
            "max_tokens":  200,
        }

        for attempt in range(3):
            try:
                response = requests.post(
                    self.api_url, headers=headers, json=payload, timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]

                elif response.status_code == 429:
                    print(f"[WAIT] Rate limit hit, retrying in 20s... (attempt {attempt + 1}/3)")
                    time.sleep(20)
                elif response.status_code == 503:
                    print(f"[WAIT] Model loading, retrying in 15s... (attempt {attempt + 1}/3)")
                    time.sleep(15)
                else:
                    print(f"[ERROR] API status {response.status_code}: {response.text}")
                    break

            except Exception as e:
                print(f"[ERROR] Connection error (attempt {attempt + 1}/3): {e}")
                time.sleep(5)

        return None

    def get_range_gpt(self, full_or_three):
        if full_or_three == 1:
            return len(self.listOfPaths)
        return min(self.MinNumfiles, len(self.listOfPaths))

    def read_file(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def generate_prompt(self, code):
        return (
            f"Analyze the following code:\n\n```\n{code}\n```\n\n"
            "Format your response exactly as follows:\n"
            "Rating: [number 1-10]\n"
            "Explanation: [max 50 words]"
        )

    def extract_grade(self, text):
        match = re.search(r"Rating\s*:\s*(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return -1