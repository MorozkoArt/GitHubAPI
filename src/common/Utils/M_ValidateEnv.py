import os

_REQUIRED_VARS: list[str] = [
    "GITHUB_TOKEN",
    "HF_TOKEN",
    "HF_API_URL",
    "HF_MODEL_NAME",
    "MODEL_PATH",
    "SCALER_PATH",
    "STORAGE_DIR",
    "OUTPUT_DIR",
]


def validate_env() -> None:
    """
    Проверяет наличие всех обязательных переменных окружения.
    Вызывается один раз при старте приложения в main.py.
    Завершает процесс с понятным сообщением вместо падения в глубине стека.
    """
    missing = [var for var in _REQUIRED_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            f"Check your .env file against .env.example."
        )