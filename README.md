# FMU Control Panel

FMU project live dashboard - A comprehensive control panel for managing FMU projects, tasks, and GitHub integrations.

## Current Status - Stage 1 Complete ✅

This project has completed Stage 0 and Stage 1, with the following features:

### Stage 0 - Base Skeleton
- Django 5.2.8 project structure
- Tailwind CSS integration (CDN)
- HTMX integration (CDN)
- Basic homepage displaying "FMU Control Panel – Dev"
- Docker setup for deployment

### Stage 1 - Core Models + Manual Dashboard
- **Models**: Project, Task, Link, LogEntry with full relationships
- **Dashboard**: View all projects with status, risk, and summary
- **Project Detail**: Editable project fields, task management, links, and activity logs
- **HTMX Task Toggle**: Interactive status changes without page reload
- **Today View**: Urgent and high-priority tasks across all projects
- **Seed Data**: 5 pre-configured FMU projects with sample data

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
- [x] **Stage 1**: Core Models + Manual Dashboard - Project management with tasks, links, and logs
- [ ] **Stage 2**: GitHub Read-Only Integration
- [ ] **Stage 3**: Auto Status + Webhooks + Issue→Task Sync
- [ ] **Stage 4**: Production Hardening + Deployment Docs

## Contributing

This project is being developed in stages. Each stage will have its own branch and pull request.

## License

See LICENSE file for details.
