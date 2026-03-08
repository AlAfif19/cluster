# Setup Guide for KMeans Engine

This guide provides detailed instructions for setting up and running the KMeans Engine project on your local machine.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation (Docker Method - Recommended)](#installation-docker-method-recommended)
- [Installation (Local Development Method)](#installation-local-development-method)
- [Configuration](#configuration)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | How to Check |
|----------|------------------|---------|--------------|
| Docker Desktop | 4.20+ | Containerization | `docker --version` |
| Docker Compose | 2.0+ | Multi-container orchestration | `docker-compose --version` |
| Git | 2.30+ | Version control | `git --version` |

### Optional Software (for local development without Docker)

| Software | Minimum Version | Purpose |
|----------|------------------|---------|
| Node.js | 18+ | Frontend development |
| npm or pnpm | 8+ | Package manager |
| Python | 3.11+ | Backend development |
| pip | 23.0+ | Python package manager |

### Installing Prerequisites

#### Docker Desktop

**Windows:**
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Run the installer and follow the prompts
3. Restart your computer
4. Verify installation: `docker --version`

**macOS:**
1. Download Docker Desktop for Mac from https://www.docker.com/products/docker-desktop
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker Desktop from Applications
4. Verify installation: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker-compose --version
```

#### Git

**Windows:**
1. Download Git from https://git-scm.com/downloads
2. Run the installer with default settings
3. Verify installation: `git --version`

**macOS (with Homebrew):**
```bash
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install git
```

## Installation (Docker Method - Recommended)

The Docker method is the recommended way to run KMeans Engine as it provides a consistent environment across all platforms.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/kmeans-engine.git
cd kmeans-engine
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env.local
```

Edit `.env.local` with your configuration:

```bash
# Database Configuration
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_DATABASE=kmeans_engine
MYSQL_USER=kmeans_user
MYSQL_PASSWORD=your_secure_password

# Backend Configuration
BACKEND_PORT=8000
DATABASE_URL=mysql://kmeans_user:your_secure_password@db:3306/kmeans_engine
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=KMeans Engine
```

**Important:** Replace placeholder values with secure, randomly generated passwords and keys.

### Step 3: Start the Application

**Windows:**
```bash
start.bat
```

This will:
- Build Docker images for frontend, backend, and database
- Start all services in detached mode
- Display service status

**Linux/Mac:**
```bash
docker-compose up -d
```

### Step 4: Verify Services Are Running

```bash
# Check service status
docker-compose ps

# All services should show "Up" status
```

Expected output:
```
NAME                  STATUS          PORTS
kmeans-backend        Up              0.0.0.0:8000->8000/tcp
kmeans-db            Up              0.0.0.0:3306->3306/tcp
kmeans-frontend       Up              0.0.0.0:3000->3000/tcp
```

## Installation (Local Development Method)

This method is for developers who want to work on the codebase without Docker.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/kmeans-engine.git
cd kmeans-engine
```

### Step 2: Set Up MySQL Database

**Option A: Use Docker for Database Only**
```bash
docker-compose up -d db
```

**Option B: Install MySQL Locally**
- Install MySQL 8.0+ from https://dev.mysql.com/downloads/mysql/
- Start MySQL service
- Create database: `CREATE DATABASE kmeans_engine;`

### Step 3: Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations (if applicable)
# alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --port 8000
```

### Step 4: Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API URL

# Start the frontend development server
npm run dev
```

### Step 5: Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Configuration

### Environment Variables

Create `.env.local` in the project root with the following variables:

```bash
# Database
MYSQL_ROOT_PASSWORD=change_me
MYSQL_DATABASE=kmeans_engine
MYSQL_USER=kmeans_user
MYSQL_PASSWORD=change_me

# Backend
BACKEND_PORT=8000
DATABASE_URL=mysql://kmeans_user:change_me@db:3306/kmeans_engine
SECRET_KEY=generate-secure-random-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=KMeans Engine
```

### Security Best Practices

1. **Generate strong passwords** for database credentials
2. **Use a strong SECRET_KEY** for JWT tokens (minimum 32 characters)
3. **Never commit .env files** to version control
4. **Change default values** before production deployment

### Generating Secure Keys

```bash
# Generate a random 32-character key for SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Verifying Installation

### Health Check

1. **Check Frontend**
   - Open http://localhost:3000 in your browser
   - You should see the KMeans Engine landing page

2. **Check Backend API**
   ```bash
   curl http://localhost:8000/health
   # Expected response: {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
   ```

3. **Check API Documentation**
   - Open http://localhost:8000/docs in your browser
   - You should see the FastAPI interactive documentation

4. **Check Database Connection**
   ```bash
   # From backend container
   docker-compose exec backend python -c "from app.database import engine; print('Database connected successfully')"
   ```

### Service Status Check

```bash
# Check all services
docker-compose ps

# Check logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## Troubleshooting

### Docker Won't Start

**Symptoms:**
- Docker Desktop won't open
- `docker` command not found

**Solutions:**
1. Ensure Docker Desktop is running
2. Restart Docker Desktop
3. Check Docker logs for errors
4. Verify Docker daemon is running: `docker info`
5. On Linux, ensure your user is in the docker group: `groups $USER`

### Port Conflicts (3000, 8000, 3306)

**Symptoms:**
- Error: "port is already allocated"
- Services fail to start

**Solutions:**
1. Identify what's using the port:
   ```bash
   # Windows PowerShell
   netstat -ano | findstr :3000

   # Linux/Mac
   lsof -i :3000
   ```

2. Stop the conflicting service or change the port in `.env.local`

3. Modify `docker-compose.yml` to use different ports

### Database Connection Errors

**Symptoms:**
- Backend can't connect to database
- Error: "Can't connect to MySQL server"

**Solutions:**
1. Verify database container is running:
   ```bash
   docker-compose ps db
   ```

2. Check database logs:
   ```bash
   docker-compose logs db
   ```

3. Verify credentials in `.env.local` match database container configuration

4. Test database connection:
   ```bash
   docker-compose exec backend python -c "import pymysql; conn = pymysql.connect(host='db', user='kmeans_user', password='your_password', database='kmeans_engine'); print('Connected!')"
   ```

### Permission Issues (Linux/Mac)

**Symptoms:**
- Permission denied errors
- Can't write to directories

**Solutions:**
1. Ensure your user has proper permissions:
   ```bash
   sudo chown -R $USER:$USER .
   ```

2. Check file permissions:
   ```bash
   ls -la
   ```

3. Fix Docker socket permissions:
   ```bash
   sudo chmod 666 /var/run/docker.sock
   ```

### Build Errors

**Symptoms:**
- Docker build fails
- npm install errors
- pip install errors

**Solutions:**
1. Clear Docker cache and rebuild:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

2. For npm/pip errors:
   ```bash
   # Clear npm cache
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install

   # Clear pip cache
   pip cache purge
   pip install -r requirements.txt
   ```

3. Check for network connectivity issues

### Application Not Loading

**Symptoms:**
- Browser shows "Connection refused"
- Page loads but shows errors

**Solutions:**
1. Verify all containers are running:
   ```bash
   docker-compose ps
   ```

2. Check container logs for errors:
   ```bash
   docker-compose logs -f
   ```

3. Restart specific services:
   ```bash
   docker-compose restart backend
   docker-compose restart frontend
   ```

4. Clear browser cache and reload

### Environment Variables Not Working

**Symptoms:**
- Application using default values instead of configured values
- Configuration errors

**Solutions:**
1. Verify `.env.local` file exists in project root
2. Check for typos in variable names
3. Ensure no extra spaces or quotes around values
4. Restart services after changing environment variables:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Next Steps

After successful installation:

1. **Explore the Application**
   - Navigate to http://localhost:3000
   - Explore the dashboard and features
   - Read the API documentation at http://localhost:8000/docs

2. **Learn About the Project**
   - Read the main [README.md](../README.md)
   - Review the project [roadmap](../.planning/ROADMAP.md)
   - Check the [architecture documentation](ARCHITECTURE.md) (coming soon)

3. **Development**
   - Read the [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
   - Set up your development environment
   - Start working on features

4. **Stay Updated**
   - Watch the repository for updates
   - Review project issues and pull requests
   - Follow development progress in the roadmap

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Project Roadmap](../.planning/ROADMAP.md)

## Support

If you encounter issues not covered in this guide:

1. Check existing [GitHub issues](https://github.com/yourusername/kmeans-engine/issues)
2. Search for similar problems in the documentation
3. Create a new issue with detailed information about your problem

---

Happy clustering!
