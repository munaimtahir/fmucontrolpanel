# FMU Control Panel

FMU project live dashboard - A comprehensive control panel for managing FMU projects, tasks, and GitHub integrations.

## Current Status - All Stages Complete ✅

This project has completed all 5 stages (0-4), with the following features:

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

### Stage 2 - GitHub Read-Only Integration
- **GitHub API Client**: Fetch PRs, commits, and issues from repositories
- **Repository Mapping**: `repo_name` field added to Project model
- **GitHub Activity Section**: Display PRs, commits, and issues on project detail pages
- **Review & Merge Queue**: Centralized view of all open PRs across repositories
- **Environment Configuration**: GITHUB_TOKEN support for API authentication

### Stage 3 - Auto Status/Risk + Webhooks + Issue→Task Sync
- **Automatic Status Engine**: Auto-set IN_PROGRESS, BLOCKED, STALE based on GitHub activity
- **Automatic Risk Calculation**: Set HIGH risk when critical issues exist
- **GitHub Webhooks**: Endpoint at `/webhooks/github/` for real-time updates
- **Event Handling**: pull_request, issues, workflow_run webhook events
- **Issue-to-Task Sync**: Automatically create/close tasks from GitHub issues
- **UI Indicators**: AUTO STATUS and AUTO SYNC badges on project pages
- **Manual Trigger**: Button to manually trigger status updates
- **Configuration**: Per-project auto_status_enabled, auto_sync_issues, stale_days settings

### Stage 4 - Production Hardening + Docker + Deployment Docs
- **Production Settings**: DEBUG=False, secure cookies, HSTS, XSS protection
- **PostgreSQL Database**: Production-ready database in docker-compose
- **Gunicorn**: Production WSGI server with 3 workers
- **Nginx**: Reverse proxy with compression, caching, rate limiting
- **WhiteNoise**: Efficient static file serving
- **Docker Compose**: Multi-container setup with health checks
- **SSL/HTTPS Support**: Configuration for Let's Encrypt certificates
- **DEPLOYMENT.md**: Complete deployment guide with step-by-step instructions
- **Environment Configuration**: Comprehensive .env.example with all settings
- **Security Best Practices**: Cookie security, CSRF protection, secure headers

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
- **Database**: SQLite (development), PostgreSQL 16 (production)
- **Web Server**: Nginx with reverse proxy
- **Application Server**: Gunicorn with 3 workers
- **Containerization**: Docker & Docker Compose
- **Static Files**: WhiteNoise for production serving

## Development Stages

- [x] **Stage 0**: Base Skeleton - Django setup with Tailwind CSS and HTMX
- [x] **Stage 1**: Core Models + Manual Dashboard - Project management with tasks, links, and logs
- [x] **Stage 2**: GitHub Read-Only Integration - PR, commit, and issue display
- [x] **Stage 3**: Auto Status + Webhooks + Issue→Task Sync - Intelligent automation
- [x] **Stage 4**: Production Hardening + Deployment Docs - Production-ready deployment

## Production Deployment

For production deployment to a VPS, see the comprehensive guide:

**📖 [DEPLOYMENT.md](./DEPLOYMENT.md)**

The deployment guide includes:
- VPS setup and configuration
- Docker installation
- SSL/HTTPS setup with Let's Encrypt
- GitHub webhook configuration
- Database backups
- Troubleshooting guide
- Security best practices

### Quick Production Start

```bash
# Clone repository on VPS
git clone https://github.com/munaimtahir/fmucontrolpanel.git
cd fmucontrolpanel

# Configure environment
cp .env.example .env
nano .env  # Edit with your production values

# Deploy with Docker Compose
docker-compose up -d --build

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access at http://your-domain.com
```

## Contributing

This project is being developed in stages. Each stage will have its own branch and pull request.

## License

See LICENSE file for details.
