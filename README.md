# DocuTrust

**Enterprise Advanced RAG Platform with Automated Self-Correction**

DocuTrust is a production-grade Retrieval-Augmented Generation (RAG) platform
built with Django. Upload your documents and receive grounded, cited answers
produced by a self-correcting, multi-agent retrieval pipeline (retrieve →
grade → rewrite → answer → cite).

> This project is being built **module by module**. This document reflects the
> state after **Module 1 — Django Project Setup**.

---

## Tech Stack

| Layer      | Technology                                             |
|------------|--------------------------------------------------------|
| Backend    | Django 5.x, Django REST Framework                      |
| Database   | SQLite                                                 |
| Frontend   | HTML, CSS, Bootstrap 5, Vanilla JavaScript             |
| AI         | Agno Framework, OpenAI API, Sentence Transformers      |
| Vector DB  | ChromaDB                                               |
| Parsing    | PyMuPDF, python-docx                                   |

---

## Project Structure (Module 1)

```
docutrust-rag/
├── docutrust/              # Project configuration package
│   ├── __init__.py
│   ├── settings.py         # Environment-driven settings (SQLite, DRF, CORS, logging)
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI entrypoint
│   └── asgi.py             # ASGI entrypoint (enables streaming later)
├── core/                   # Base layout, landing page, shared mixins
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py           # TimeStampedModel abstract base
│   ├── views.py            # Landing page + health check
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── templates/
│   ├── base.html           # Global layout: navbar, dark mode, toasts, footer
│   └── core/home.html      # Marketing landing page
├── static/
│   ├── css/main.css        # DocuTrust theme (light + dark)
│   └── js/main.js          # Theme toggle, toasts, CSRF helper
├── logs/                   # Rotating application logs
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

Feature apps — `accounts`, `documents`, `chat`, `dashboard`, `rag`, `agents`,
`api` — are added in their respective modules.

---

## Installation

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

For Module 1 you only need the core web dependencies:

```bash
pip install "Django>=5.1,<5.2" djangorestframework python-dotenv django-cors-headers Pillow
```

The full stack (installed as later modules are built):

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Generate a secret key:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Paste it into DJANGO_SECRET_KEY in .env
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver 0.0.0.0:8000
```

Visit:

- **Landing page:** http://localhost:8000/
- **Health check:** http://localhost:8000/health/
- **Admin panel:** http://localhost:8000/admin/

---

## Running Tests

```bash
python manage.py test
```

---

## Security

DocuTrust follows Django security best practices out of the box:

- Secrets loaded from `.env` (never hardcoded)
- CSRF protection enabled
- XSS protection headers (`X-Content-Type-Options`, browser XSS filter)
- Clickjacking protection (`X-Frame-Options: SAMEORIGIN`)
- HTTPS/HSTS enforced automatically when `DJANGO_DEBUG=False`
- Parameterized queries via the Django ORM (SQL-injection safe)

---

## Roadmap

- [x] **Module 1** — Django Project Setup
- [x] Module 2 — Authentication
- [x] Module 3 — Document Upload
- [x] Module 4 — Document Parsing
- [x] Module 5 — ChromaDB
- [x] Module 6 — Embeddings
- [x] Module 7 — Agno Agents
- [x] Module 8 — RAG Pipeline
- [x] Module 9 — Chat UI
- [x] Module 10 — Dashboard
- [x] Module 11 — Admin
- [x] Module 12 — API
- [ ] Module 13 — Deployment
- [ ] Module 14 — Documentation
## Note
- I am currently working on this project.
