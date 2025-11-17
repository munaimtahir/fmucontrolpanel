# FMU Control Panel

FMU project live dashboard - A comprehensive control panel for managing FMU projects, tasks, and GitHub integrations.

## Stage 0 - Base Skeleton ✅

This project is currently at Stage 0, with the following features:
- Django 5.2.8 project structure
- Tailwind CSS integration (CDN)
- HTMX integration (CDN)
- Basic homepage displaying "FMU Control Panel – Dev"
- Docker setup for deployment

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/munaimtahir/fmucontrolpanel.git
   cd fmucontrolpanel
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and navigate to: http://127.0.0.1:8000

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   Open your browser and navigate to: http://localhost:8000

## Project Structure

```
fmucontrolpanel/
├── backend/
│   ├── fmucontrolpanel/      # Django project settings
│   ├── main/                  # Main application
│   ├── templates/             # HTML templates
│   ├── manage.py
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Technology Stack

- **Backend**: Django 5.2.8
- **Frontend**: Tailwind CSS (CDN), HTMX (CDN)
- **Database**: SQLite (development), PostgreSQL (production - Stage 4)
- **Server**: Gunicorn
- **Containerization**: Docker & Docker Compose

## Development Stages

- [x] **Stage 0**: Base Skeleton - Django setup with Tailwind CSS and HTMX
- [ ] **Stage 1**: Core Models + Manual Dashboard
- [ ] **Stage 2**: GitHub Read-Only Integration
- [ ] **Stage 3**: Auto Status + Webhooks + Issue→Task Sync
- [ ] **Stage 4**: Production Hardening + Deployment Docs

## Contributing

This project is being developed in stages. Each stage will have its own branch and pull request.

## License

See LICENSE file for details.
