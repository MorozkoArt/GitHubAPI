<div id="header" align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGQ5eWhlcHZ0dTd3bWEzcmk5OXJ1YWt2aTVtb3gzcnV4bDNoYWxsbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yf5t7jramBz6YN9w0U/giphy.gif?raw=true" width="400"/>
</div>

<div id="header" align="center">
    <h1>🎨 Составление информационного портрета по профилю GitHub</h1>
    <h3>💻 Проект по практике</h3>
</div>

---

### Кратко о проекте 🌐

- *💾 Инструмент для автоматической оценки GitHub-профилей. Анализирует активность пользователя, качество репозиториев и код основного репозитория, возвращая числовую оценку до 250 баллов*
- *💿 Полная информация опубликована на [Google Drive](https://drive.google.com/drive/folders/18Q0nS8e0jUeByKjYreqZ1MXWn0KfvMVV?usp=drive_link)*

---

### Язык 👅 и инструменты 🔧

<img src="https://raw.githubusercontent.com/MorozkoArt/MorozkoArt/446de453fb12c56c11adfb43cde081d484777abb/Resources/python-original.svg" title="python" width="40" height="40"/>&nbsp;
<img src="https://raw.githubusercontent.com/MorozkoArt/MorozkoArt/446de453fb12c56c11adfb43cde081d484777abb/Resources/pycharm-original.svg" title="pycharm" width="40" height="40"/>&nbsp;

---

## Как работает оценка

| Блок          | Максимум | Что оценивается                                     |
|---------------|----------|-----------------------------------------------------|
| Профиль       | 100      | followers, repos, commits, языки, организации и др. |
| Репозиторий   | 100      | stars, forks, коммиты, активные дни, просмотры      |
| Качество кода | 50       | анализ файлов через LLM (HuggingFace API)           |

## Установка и запуск

### Шаг 1 — Клонировать репозиторий

```bash
git clone https://github.com/MorozkoArt/GitHubAPI
cd GitHubAPI
```

### Шаг 2 — Настроить переменные окружения

```bash
cp .env.example .env
```

Открыть `.env` и заполнить обязательные поля:

```env
# GitHub токен: Settings → Developer settings → Personal access tokens → Classic
# Необходимые права: repo, read:user, read:org
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=твой_логин

# HuggingFace токен: https://huggingface.co/settings/tokens (бесплатно)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Шаг 3 — Обучить модель (один раз, ~20–40 минут)

```bash
docker compose --profile train up --build
```

После завершения в консоли появится:

```bash
Training complete.
```

Артефакты (`model.onnx`, `scaler.pkl`) сохраняются в Docker volume `data` автоматически.

### Шаг 4 — Запустить приложение

```bash
docker compose --profile app up --build
```

> **Повторные запуски** (модель уже обучена):

> ```bash
> docker compose --profile app up
> ```
---

## Архитектура проекта

<details>
<summary><b>📂 Структура директорий</b></summary>
<br>

```plaintext
📂project/
├── 📂src/
│   ├──📂app/
│   │   ├──📄Dockerfile
│   │   ├──📄requirements.txt
│   │   ├──📂Assessment         # Методы оценки пользователя
│   │   ├──📂Interface/         # Методы визуализации
│   │   ├──📂StartMethods/      # Методы запуска
│   │   ├──📂User_and_Repo/     # Классы для работы с пользователями
│   │   └──📄main.py            # Главный скрипт
│   ├──📂common/
│   │   ├──📂Config
│   │   └──📂Utils
│   └──📂ml/
│       ├──📄Dockerfile
│       ├──📄requirements.txt
│       ├──📂GenerationUsers/   # Генерация обучающих данных
│       ├──📂ForModel/          # Архитектура модели
│       └──📄train.py           # Обучение модели
├──📂data/                      # Обучающие данные
├──📂tests/                     # Тесты
├──📄docker-compose.yaml
└──📄.env.example
```

</details>

---

## Пример вывода

<details>
<summary><b>📊 Показать пример оценки профиля</b></summary>
<br>

```plaintext
User profile assessment results - MorozkoArt 

Profile data and their assessment:
+-------------------------------------------------+---------------------------------------+------------+
| Field name                                      | Significance                          | Assessment |
+-------------------------------------------------+---------------------------------------+------------+
| Username                                        | MorozkoArt                            |            |
+-------------------------------------------------+---------------------------------------+------------+
| Profile access                                  | public                                |            |
+-------------------------------------------------+---------------------------------------+------------+
| Number of followers                             | 7                                     |       1.37 |
+-------------------------------------------------+---------------------------------------+------------+
| Number of following                             | 17                                    |        1.6 |
+-------------------------------------------------+---------------------------------------+------------+
| Hireable status                                 | True                                  |          1 |
+-------------------------------------------------+---------------------------------------+------------+
| Number of private repositories                  | 2                                     |       9.33 |
| Number of public repositories                   | 49                                    |            |
+-------------------------------------------------+---------------------------------------+------------+
| Account creation date                           | 2024-06-07 13:38:22+00:00             |            |
+-------------------------------------------------+---------------------------------------+------------+
| Last update date                                | 2025-04-29 16:31:32+00:00             |            |
+-------------------------------------------------+---------------------------------------+------------+
| Account age                                     | 10 Month(s)                           |        9.0 |
+-------------------------------------------------+---------------------------------------+------------+
| Average number of commits per repository        | 10.98                                 |       3.61 |
+-------------------------------------------------+---------------------------------------+------------+
| Average commit frequency (days between commits) | 5.58                                  |       0.31 |
+-------------------------------------------------+---------------------------------------+------------+
| Average number of commits per day               | 2.88                                  |       2.95 |
+-------------------------------------------------+---------------------------------------+------------+
| Subscription plan                               | Plan(name="free")                     |          0 |
+-------------------------------------------------+---------------------------------------+------------+
| Blog                                            | https://vk.com/poc_norm               |          2 |
+-------------------------------------------------+---------------------------------------+------------+
| Company                                         | What Entertainment                    |          3 |
+-------------------------------------------------+---------------------------------------+------------+
| Organizations                                   | BigShishkaLove                        |       0.86 |
+-------------------------------------------------+---------------------------------------+------------+
| Programming languages                           | C++, Python, C#, HTML, SCSS, CMake, C |       6.76 |
+-------------------------------------------------+---------------------------------------+------------+
Profile assessment: 41.8

...
```

</details>

---

## Переменные окружения

<details>
<summary><b>⚙️ Полный список переменных .env</b></summary>
<br>

| Переменная          | Описание                                | Пример                                              |
|---------------------|-----------------------------------------|-----------------------------------------------------|
| `GITHUB_TOKEN`      | Токен GitHub API                        | `ghp_xxx`                                           |
| `GITHUB_USERNAME`   | Логин для анализа                       | `MorozkoArt`                                        |
| `GITHUB_USER_TOKEN` | Токен для полного доступа (опционально) |                                                     |
| `HF_TOKEN`          | Токен HuggingFace                       | `hf_xxx`                                            |
| `HF_API_URL`        | URL HuggingFace API                     | `https://router.huggingface.co/v1/chat/completions` |
| `HF_MODEL_NAME`     | LLM для оценки кода                     | `Qwen/Qwen2.5-Coder-32B-Instruct`                   |
| `DATA_DIR`          | Путь к ML-артефактам                    | `/app/data`                                         |
| `OUTPUT_DIR`        | Папка для результатов                   | `/app/output`                                       |
| `MODEL_PATH`        | Путь к ONNX-модели                      | `/app/data/model.onnx`                              |
| `SCALER_PATH`       | Путь к scaler                           | `/app/data/scaler.pkl`                              |
| `CHECKPOINT_PATH`   | Путь к PyTorch checkpoint               | `/app/data/best_model.pth`                          |
| `DATASET_PATH`      | Путь к датасету                         | `/app/data/training.csv`                            |
| `AUTH_METHOD`       | Метод аутентификации                    | `login` или `token`                                 |
| `ACCESS_LEVEL`      | Уровень доступа                         | `public` или `private`                              |
| `CODE_ASSESS_MODE`  | Режим оценки кода                       | `1` (все файлы) или `2` (5 файлов)                  |
| `MAX_WORKERS_USER`  | Потоки для профиля                      | `5`                                                 |
| `MAX_WORKERS_REPO`  | Потоки для репозитория                  | `10`                                                |

</details>

---

## Технологии

<details>
<summary><b>📦 Использованные библиотеки</b></summary>
<br>

| Технология    | Назначение                           | Версия   |
|---------------|--------------------------------------|----------|
| PyTorch (CPU) | Обучение нейронной сети              | 2.9.1    |
| onnxruntime   | Инференс ONNX-модели в приложении    | ≥ 1.19.0 |
| PyGithub      | Работа с GitHub API v3               | 2.6.1    |
| requests      | HTTP-запросы к HuggingFace API       | 2.32.3   |
| pandas        | Обработка и анализ данных            | 2.2.3    |
| scikit-learn  | Нормализация данных (StandardScaler) | 1.7.0    |
| joblib        | Сохранение и загрузка StandardScaler | ≥ 1.3.0  |
| numpy         | Научные вычисления                   | ≥ 1.26.0 |
| PrettyTable   | Форматированный вывод таблиц         | 3.16.0   |
| tqdm          | Индикаторы прогресса                 | 4.67.1   |
| python-dotenv | Загрузка конфигурации из .env        | ≥ 1.0.1  |
| pytest        | Тестирование кода                    | 8.3.5    |

</details>

---

## Технические детали

<details>
<summary><b>🔬 Устройство модели и Docker-образов</b></summary>
<br>

**Модель:** MLP с residual-блоками, LayerNorm, GELU, 28 входов → 28 выходов.
Обучается на CPU за ~30 минут, экспортируется в ONNX (~1.5 MB).

**Функция потерь:** `ZeroConstrainedLoss = SmoothL1 + штраф за ненулевые предсказания при нулевых целевых значениях (weight=1.5)`

**Разделение образов:**

| Образ                | Зависимости               | Размер  |
|----------------------|---------------------------|---------|
| `src/ml/Dockerfile`  | PyTorch CPU + ONNX        | ~1.1 GB |
| `src/app/Dockerfile` | onnxruntime (без PyTorch) | ~350 MB |

**Результаты обучения:**

- Test MAE: `0.17`
- Test R²: `0.96`

**Зависимости разделены по сервисам:**

- `src/ml/requirements.txt` — для обучения (PyTorch, ONNX, scikit-learn)
- `src/app/requirements.txt` — для приложения (onnxruntime, PyGithub, requests)

</details>