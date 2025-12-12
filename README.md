# Lab23
## Требования
- Python 3.10+
- uv (пакетный менеджер) — https://astral.sh/uv

## Установка (через uv)
```bash
# установить uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# или перейти в папку
cd news_project

# создать venv
uv venv

# активировать
source .venv/bin/activate

# установить Django
uv pip install "django>=4.2"

# установить миграции
python manage.py migrate

# создать суперпользователя
python manage.py createsuperuser

# запустить сервер
python manage.py runserver