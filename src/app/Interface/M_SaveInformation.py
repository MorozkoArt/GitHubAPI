import os
from pathlib import Path
from Interface.M_GetInformation import print_assessment


def save_user_information(user, assessment):
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"GitHub_{user.name}.txt"
    save_to_file(file_path, user, assessment)
    print(f"User information saved to: {file_path}")

def save_to_file(file_path, user, assessment):
    tables = print_assessment(user, assessment)
    with open(file_path, "w", encoding="utf-8") as f:
        for table in tables:
            f.write(str(table))


