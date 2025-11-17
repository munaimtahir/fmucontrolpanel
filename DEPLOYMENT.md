# FMU Control Panel - Production Deployment Guide

This guide explains how to deploy the FMU Control Panel to a production VPS using Docker Compose.

## Table of Contents
- [Prerequisites](#prerequisites)
- [VPS Setup](#vps-setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [GitHub Webhooks](#github-webhooks)
- [SSL/HTTPS Setup](#sslhttps-setup)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Server Requirements
- **VPS**: Ubuntu 22.04 LTS or newer (2GB RAM minimum, 4GB recommended)
- **Docker**: Version 20.10 or newer
- **Docker Compose**: Version 2.0 or newer
- **Domain**: A domain name pointing to your VPS IP address
- **Ports**: 80 (HTTP) and 443 (HTTPS) open in firewall

### Local Requirements
- Git
- SSH access to your VPS

## VPS Setup

### 1. Connect to Your VPS
```bash
ssh root@your-server-ip
```

### 2. Update System
```bash
apt update && apt upgrade -y
```

### 3. Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Start Docker service
systemctl start docker
systemctl enable docker

# Verify installation
docker --version
```

### 4. Install Docker Compose
```bash
# Download Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### 5. Configure Firewall (UFW)
```bash
# Install UFW if not installed
apt install ufw -y

# Allow SSH (important! do this first)
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

## Installation

### 1. Clone the Repository
```bash
# Create application directory
mkdir -p /var/www
cd /var/www

# Clone the repository
git clone https://github.com/munaimtahir/fmucontrolpanel.git
cd fmucontrolpanel
```

### 2. Checkout Production Branch (if applicable)
```bash
# If you have a production branch
git checkout production

# Or use main branch
git checkout main
```

## Configuration

### 1. Create Environment File
```bash
# Copy example file
cp .env.example .env

# Edit the file with your production values
nano .env
```

### 2. Configure Environment Variables

Edit `.env` and update these **critical** values:

```bash
# Django Settings
DEBUG=0
SECRET_KEY=your-very-long-random-secret-key-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
POSTGRES_DB=fmucontrolpanel
POSTGRES_USER=fmuuser
POSTGRES_PASSWORD=your-very-secure-database-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security Settings
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# GitHub Integration
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_WEBHOOK_SECRET=your-webhook-secret-for-verification
```

#### Generating SECRET_KEY
```bash
# Generate a secure secret key
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Creating GitHub Token
1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`
4. Copy the token to `GITHUB_TOKEN`

### 3. Update docker-compose.yml (Optional)

If you need to change database credentials, edit `docker-compose.yml`:

```bash
nano docker-compose.yml
```

Update the `db` service environment variables to match your `.env` file.

## Deployment

### 1. Build and Start Services
```bash
# Build and start all services
docker-compose up -d --build

# This will:
# - Build the Django application
# - Start PostgreSQL database
# - Run migrations
# - Collect static files
# - Start Gunicorn
# - Start Nginx
```

### 2. Verify Services are Running
```bash
# Check running containers
docker-compose ps

# Should show 3 containers:
# - fmucontrolpanel_db (postgres)
# - fmucontrolpanel_web (django+gunicorn)
# - fmucontrolpanel_nginx (nginx)
```

### 3. Check Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Follow logs in real-time
docker-compose logs -f
```

### 4. Create Superuser
```bash
# Access the web container
docker-compose exec web python manage.py createsuperuser

# Follow prompts to create admin user
```

### 5. Seed Initial Data (Optional)
```bash
# Seed the 5 FMU projects
docker-compose exec web python manage.py seed_projects
```

### 6. Access the Application
Open your browser and navigate to:
```
http://your-domain.com
```

Admin panel:
```
http://your-domain.com/admin/
```

## GitHub Webhooks

### 1. Configure Webhook in GitHub Repository

For each repository you want to monitor:

1. **Go to Repository Settings**
   - Navigate to your GitHub repository
   - Click "Settings" → "Webhooks" → "Add webhook"

2. **Configure Webhook**
   - **Payload URL**: `https://yourdomain.com/webhooks/github/`
   - **Content type**: `application/json`
   - **Secret**: Enter the same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
   
3. **Select Events**
   - Choose "Let me select individual events"
   - Select:
     - ✅ Pull requests
     - ✅ Issues
     - ✅ Workflow runs
   
4. **Activate Webhook**
   - Ensure "Active" is checked
   - Click "Add webhook"

5. **Verify Webhook**
   - GitHub will send a `ping` event
   - Check "Recent Deliveries" tab to see if it succeeded
   - Response should be `200 OK` with `{"status": "pong"}`

### 2. Enable Auto Features in Projects

1. **Log in to Admin Panel**
   ```
   https://yourdomain.com/admin/
   ```

2. **Edit Project**
   - Go to Projects
   - Click on a project
   - Edit fields:
     - ✅ **Auto status enabled**: Enable automatic status updates
     - ✅ **Auto sync issues**: Enable issue-to-task synchronization
     - **Stale days**: Days before project marked STALE (default: 7)
   - Save changes

3. **Or Edit via UI**
   - Navigate to project detail page
   - Scroll to "Update Project Information"
   - Check "Enable Auto Status" and/or "Auto Sync Issues"
   - Set "Stale After (days)"
   - Click "Update Project"

## SSL/HTTPS Setup

### Option 1: Certbot with Let's Encrypt (Recommended)

1. **Install Certbot**
```bash
apt install certbot python3-certbot-nginx -y
```

2. **Stop Nginx Container Temporarily**
```bash
docker-compose stop nginx
```

3. **Obtain Certificate**
```bash
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

4. **Update Nginx Configuration**

Edit `nginx/nginx.conf` to add SSL:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... rest of configuration
}
```

5. **Update docker-compose.yml** to mount SSL certificates:

```yaml
nginx:
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - static_volume:/app/staticfiles:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro  # Add this line
  ports:
    - "80:80"
    - "443:443"  # Add HTTPS port
```

6. **Restart Services**
```bash
docker-compose up -d
```

7. **Set Up Auto-Renewal**
```bash
# Test renewal
certbot renew --dry-run

# Add to crontab
crontab -e

# Add this line (runs twice daily)
0 0,12 * * * certbot renew --quiet --post-hook "docker-compose restart nginx"
```

### Option 2: Cloudflare SSL (Alternative)

If using Cloudflare:
1. Add your domain to Cloudflare
2. Set SSL/TLS mode to "Full"
3. Enable "Always Use HTTPS"
4. No Nginx SSL configuration needed (Cloudflare handles it)

## Maintenance

### Viewing Logs
```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Restarting Services
```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
docker-compose restart nginx
```

### Updating the Application
```bash
# Pull latest code
cd /var/www/fmucontrolpanel
git pull

# Rebuild and restart
docker-compose up -d --build

# Run migrations (if any)
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U fmuuser fmucontrolpanel > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose exec -T db psql -U fmuuser fmucontrolpanel < backup_20241117.sql
```

### Stopping Services
```bash
# Stop all services (preserves data)
docker-compose stop

# Stop and remove containers (data in volumes is preserved)
docker-compose down

# Stop and remove everything including volumes (DANGER: destroys data)
docker-compose down -v
```

## Troubleshooting

### Issue: Cannot connect to database
```bash
# Check database container
docker-compose logs db

# Verify database is healthy
docker-compose ps

# Restart database
docker-compose restart db
```

### Issue: Static files not loading
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check nginx logs
docker-compose logs nginx

# Verify static volume
docker volume inspect fmucontrolpanel_static_volume
```

### Issue: Webhooks not working
```bash
# Check webhook endpoint logs
docker-compose logs web | grep webhook

# Verify webhook configuration in GitHub
# Check "Recent Deliveries" in GitHub webhook settings

# Test webhook endpoint
curl -X POST https://yourdomain.com/webhooks/github/ \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen": "test"}'
```

### Issue: Permission denied errors
```bash
# Fix permissions
cd /var/www/fmucontrolpanel
chown -R 1000:1000 backend/
```

### Issue: Application not accessible
```bash
# Check if containers are running
docker-compose ps

# Check nginx logs
docker-compose logs nginx

# Check firewall
ufw status

# Verify port binding
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

### Getting Shell Access
```bash
# Django shell
docker-compose exec web python manage.py shell

# PostgreSQL shell
docker-compose exec db psql -U fmuuser -d fmucontrolpanel

# Container bash shell
docker-compose exec web /bin/sh
```

## Production Checklist

Before going live, ensure:

- [ ] `.env` file has all production values set
- [ ] `DEBUG=0` in `.env`
- [ ] Strong `SECRET_KEY` generated
- [ ] Secure database password set
- [ ] `ALLOWED_HOSTS` contains your domain
- [ ] SSL certificate installed and working
- [ ] Firewall configured (ports 22, 80, 443)
- [ ] GitHub webhook configured and tested
- [ ] Superuser account created
- [ ] Initial projects seeded (if applicable)
- [ ] Database backups configured
- [ ] SSL auto-renewal configured
- [ ] Monitoring/logging set up (optional but recommended)

## Support

For issues or questions:
- **Repository**: https://github.com/munaimtahir/fmucontrolpanel
- **Issues**: https://github.com/munaimtahir/fmucontrolpanel/issues

## Security Notes

1. **Never commit `.env` file to Git**
2. **Use strong passwords** for database and Django admin
3. **Keep GitHub token secure** - it has access to your repositories
4. **Regularly update** Docker images and dependencies
5. **Monitor logs** for suspicious activity
6. **Enable SSL/HTTPS** in production
7. **Use webhook secret** to verify GitHub requests
8. **Limit SSH access** to specific IPs if possible
9. **Regular backups** of database
10. **Keep system updated** with security patches
