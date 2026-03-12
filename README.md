## Robotics School Site

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Poetry](https://img.shields.io/badge/Poetry-deps-60A5FA?logo=python&logoColor=white)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

A single-page website for a robotics school built with Django, featuring multilingual support and Tailwind CSS.

### Main features

- **Home page**: promo landing page describing robotics and programming courses.
- **Multilingual**: supports at least Estonian (`et`, default language) and Russian (`ru`) via Django i18n.
- **Templates**: clean layout in `templates/base.html` and `templates/home.html`.
- **Static files**: styles in `static/css/app.css` and compiled Tailwind in `static/css/style.css`.

### Technologies

- **Backend**: Django 5.2
- **Language**: Python 3.11
- **Dependency management**: Poetry (`pyproject.toml`)
- **Database**: SQLite (default for development)
- **Frontend/styles**: Tailwind CSS (via a separate Node container)
- **Containerization**: Docker, Docker Compose

### Project structure (simplified)

- **`config/`** – Django project configuration.
  - `settings.py` – main settings, including:
    - `SITE_NAME`, `DEBUG`, `ALLOWED_HOSTS` and other parameters via `Settings` from `settings_env.py`.
    - `LANGUAGE_CODE = 'et'`, `LANGUAGES = [('et', 'Estonian'), ('ru', 'Russian')]`.
    - `LOCALE_PATHS = BASE_DIR / "locale"`.
  - `urls.py` – routing:
    - `/` – home page (`core.views.home`).
    - i18n routes via `i18n_patterns`.
- **`core/`** – application logic.
  - `views.py` – views, including `home`.
  - `context_processors.py` – `site_settings` to pass `SITE_NAME` and other settings into templates.
- **`templates/`** – HTML templates.
  - `base.html` – base layout.
  - `home.html` – home page (greeting, benefits, call-to-action buttons).
- **`static/`** – static files (CSS etc.).
- **`locale/`** – translations (`.po`/`.mo` files, e.g. `locale/ru/LC_MESSAGES/django.po`).
- **`docker/`** – Dockerfile and docker-compose.

### Running in Docker

Requirements:

- Docker and Docker Compose installed.
- `.env` file in the project root with settings (e.g. `SITE_NAME`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, etc. – see `config/settings_env.py`).

#### 1. Build and start containers

From the project root (where `docker/docker-compose.yml` is available):

```bash
docker compose -f docker/docker-compose.yml up --build
```

Two services will be started:

- **`web`** – Django application.
  - On startup runs:
    - `python manage.py compilemessages`
    - `python manage.py runserver 0.0.0.0:8000`
  - Available at `http://localhost:8000/`.
- **`tailwind`** – Node container for building styles.
  - Installs dependencies via `npm install`.
  - Starts Tailwind CLI in `--watch` mode:
    - input: `./static/css/app.css`
    - output: `./static/css/style.css`

The project code is mounted into the containers via the `..:/app` volume, so file changes are immediately visible inside the containers.

#### 2. Stop containers

From the project root:

```bash
docker compose -f docker/docker-compose.yml down
```

### Local run without Docker (optional)

If you want to run the project without Docker:

1. **Install Poetry and dependencies**:

```bash
pip install poetry
poetry install
```

2. **Create `.env` from an example** (see `config/settings_env.py` and the existing `.env`):

```bash
cp .env.example .env  # if there is an example file, otherwise create it manually
```

3. **Apply migrations and compile translations**:

```bash
python manage.py migrate
python manage.py compilemessages
```

4. **Run the development server**:

```bash
python manage.py runserver
```

### Internationalization

- Default language: **Estonian** (`LANGUAGE_CODE = 'et'`).
- Additional language: **Russian** (`'ru'`).
- Translations are stored in `locale/<lang>/LC_MESSAGES/django.po`.
- To update translations:

```bash
python manage.py makemessages -l ru
python manage.py compilemessages
```

### Useful information for development

- **Static files**: path `STATICFILES_DIRS = [BASE_DIR / "static"]`.
- **Database**: standard SQLite file `db.sqlite3` in the project root.
- **Django version**: see `pyproject.toml` (at the time of writing – 5.2.12).
