---
phase: 01-infrastructure-foundation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - docker-compose.yml
  - backend/Dockerfile
  - backend/requirements.txt
  - backend/app/main.py
  - frontend/Dockerfile
  - frontend/package.json
  - .env.example
  - .gitignore
autonomous: true
requirements:
  - INFRA-01
  - INFRA-02
  - INFRA-03
  - INFRA-04
user_setup: []

must_haves:
  truths:
    - "Developer can run 'docker-compose up' to start all containers"
    - "MySQL database container runs and accepts connections on port 3306"
    - "FastAPI backend container runs and returns 'Hello World' at localhost:8000"
    - "Next.js frontend container runs and serves the application on localhost:3000"
    - "All containers use the same Docker network for inter-service communication"
  artifacts:
    - path: "docker-compose.yml"
      provides: "Orchestration of all three services"
      contains: "services: db, backend, frontend"
    - path: "backend/Dockerfile"
      provides: "FastAPI container image"
      contains: "FROM python:3.11-slim"
    - path: "backend/app/main.py"
      provides: "FastAPI application with Hello World endpoint"
      contains: "app.get('/')"
    - path: "frontend/Dockerfile"
      provides: "Next.js container image"
      contains: "FROM node:20-alpine"
    - path: ".env.example"
      provides: "Environment variable template"
      contains: "MYSQL_ROOT_PASSWORD, DATABASE_URL"
  key_links:
    - from: "docker-compose.yml"
      to: "backend/app/main.py"
      via: "environment variables"
      pattern: "DATABASE_URL"
    - from: "docker-compose.yml"
      to: "mysql container"
      via: "service definition"
      pattern: "image: mysql:"
    - from: "frontend/Dockerfile"
      to: "backend container"
      via: "Docker network"
      pattern: "depends_on: backend"
---

<objective>
Set up Docker Compose orchestration with MySQL database, FastAPI backend, and Next.js frontend containers.

Purpose: Establish the foundational infrastructure for local development with isolated, reproducible environments for each service.

Output: Three running Docker containers (db, backend, frontend) that can be started with a single command.
</objective>

<execution_context>
@C:/Users/Abdurr/.claude/get-shit-done/workflows/execute-plan.md
@C:/Users/Abdurr/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create Docker Compose configuration</name>
  <files>docker-compose.yml</files>
  <action>
    Create docker-compose.yml with three services:

    1. **db service** (MySQL):
       - Image: mysql:8.0
       - Ports: 3306:3306
       - Environment variables from .env file (MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)
       - Volume: ./mysql-data:/var/lib/mysql for persistence
       - Health check: mysqladmin ping -h localhost

    2. **backend service** (FastAPI):
       - Build from ./backend/Dockerfile
       - Ports: 8000:8000
       - Environment: DATABASE_URL=mysql+pymysql://user:password@db:3306/kmeans_db
       - Depends on: db service with healthcheck condition
       - Command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    3. **frontend service** (Next.js):
       - Build from ./frontend/Dockerfile
       - Ports: 3000:3000
       - Environment: NEXT_PUBLIC_API_URL=http://localhost:8000
       - Depends on: backend service
       - Command: npm run dev

    Use a shared network named "kmeans-network" for all services.
  </action>
  <verify>docker-compose config validates without errors</verify>
  <done>docker-compose.yml created with all three services properly configured</done>
</task>

<task type="auto">
  <name>Task 2: Create backend Dockerfile and application</name>
  <files>backend/Dockerfile, backend/requirements.txt, backend/app/main.py</files>
  <action>
    Create the backend Docker infrastructure:

    **backend/Dockerfile:**
    - Base: python:3.11-slim
    - Workdir: /app
    - Install: requirements.txt
    - Copy: ./app to /app/app
    - Expose port 8000
    - Command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    **backend/requirements.txt:**
    - fastapi==0.104.1
    - uvicorn[standard]==0.24.0
    - pymysql==1.1.0
    - pandas==2.1.1
    - scikit-learn==1.3.2
    - python-multipart==0.0.6
    - python-jose[cryptography]==3.3.0
    - passlib[bcrypt]==1.7.4
    - python-dotenv==1.0.0

    **backend/app/main.py:**
    - Import FastAPI
    - Create app instance
    - GET / endpoint returning {"message": "Hello World from KMeans Engine API"}
    - GET /health endpoint returning {"status": "healthy"}
    - CORS middleware allowing frontend origin
  </action>
  <verify>docker-compose build backend completes successfully</verify>
  <done>Backend Dockerfile, requirements.txt, and main.py created with Hello World endpoint</done>
</task>

<task type="auto">
  <name>Task 3: Create frontend Dockerfile and Next.js app</name>
  <files>frontend/Dockerfile, frontend/package.json, frontend/next.config.js</files>
  <action>
    Create the frontend Docker infrastructure:

    **frontend/Dockerfile:**
    - Base: node:20-alpine
    - Workdir: /app
    - Copy package.json and package-lock.json
    - Run npm install
    - Copy . to /app
    - Expose port 3000
    - Command: npm run dev

    **frontend/package.json:**
    - Next.js 14.0.4
    - React 18.2.0
    - Tailwind CSS 3.3.6
    - Dependencies: class-variance-authority, clsx, tailwind-merge, lucide-react
    - DevDependencies: @types/node, @types/react, @types/react-dom, typescript, tailwindcss, postcss, autoprefixer, eslint, eslint-config-next

    **frontend/next.config.js:**
    - Output: standalone (for Docker)
    - No external images or domains configured yet

    Initialize basic app structure:
    - app/layout.tsx with basic HTML structure and Tailwind CSS
    - app/page.tsx with "Welcome to KMeans Engine" heading
    - app/globals.css with Tailwind directives
    - tailwind.config.ts with content paths and theme
    - postcss.config.js with tailwindcss plugin
  </action>
  <verify>docker-compose build frontend completes successfully</verify>
  <done>Frontend Dockerfile, package.json, and basic Next.js app created with Tailwind CSS</done>
</task>

<task type="auto">
  <name>Task 4: Create environment configuration template and .gitignore</name>
  <files>.env.example, .gitignore</files>
  <action>
    **.env.example:**
    - Database configuration:
      MYSQL_ROOT_PASSWORD=your_root_password
      MYSQL_DATABASE=kmeans_db
      MYSQL_USER=kmeans_user
      MYSQL_PASSWORD=your_password
      DATABASE_URL=mysql+pymysql://kmeans_user:your_password@db:3306/kmeans_db
    - Backend configuration:
      SECRET_KEY=your_secret_key_here
      ACCESS_TOKEN_EXPIRE_MINUTES=30
    - Frontend configuration:
      NEXT_PUBLIC_API_URL=http://localhost:8000
    - Environment mode:
      ENVIRONMENT=development

    **.gitignore:**
    - Node.js: node_modules, .next, out, build
    - Python: __pycache__, *.pyc, .pytest_cache, .venv, venv
    - Docker: *.log, .env (but not .env.example)
    - IDE: .vscode, .idea, *.swp, *.swo
    - OS: .DS_Store, Thumbs.db
    - MySQL: mysql-data/
    - Temporary files: *.tmp, *.bak
    - Excel data files: *.xlsx (except sample files in exported_data/)
  </action>
  <verify>git status shows only .env.example and .gitignore tracked (not .env)</verify>
  <done>Environment template and comprehensive .gitignore created</done>
</task>

</tasks>

<verification>
1. Verify docker-compose config is valid: `docker-compose config`
2. Build all containers: `docker-compose build`
3. Start all containers: `docker-compose up -d`
4. Check container status: `docker-compose ps` (all 3 services should be "running")
5. Test MySQL connection: `docker-compose exec db mysql -u kmeans_user -p kmeans_db -e "SELECT 1"`
6. Test FastAPI endpoint: `curl http://localhost:8000` (should return "Hello World")
7. Test health endpoint: `curl http://localhost:8000/health` (should return "healthy")
8. Test Next.js frontend: `curl http://localhost:3000` (should return HTML with "Welcome to KMeans Engine")
9. Verify logs: `docker-compose logs backend` shows FastAPI running, `docker-compose logs frontend` shows Next.js running
</verification>

<success_criteria>
1. All three containers (db, backend, frontend) start successfully with `docker-compose up -d`
2. MySQL container accepts connections and executes SQL commands
3. FastAPI backend returns "Hello World" at http://localhost:8000
4. FastAPI health check returns {"status": "healthy"} at http://localhost:8000/health
5. Next.js frontend serves HTML content at http://localhost:3000
6. All services communicate via Docker network (backend can connect to db:3306)
7. Environment variables are properly loaded from .env file
8. .gitignore excludes sensitive files (.env) but includes template (.env.example)
</success_criteria>

<output>
After completion, create `.planning/phases/01-infrastructure-foundation/01-01-SUMMARY.md` with:
- Actual files created
- Container configurations used
- Environment variable decisions
- Any deviations from the plan
</output>
