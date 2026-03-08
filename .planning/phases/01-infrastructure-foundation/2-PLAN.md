---
phase: 01-infrastructure-foundation
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - start.bat
  - stop.bat
  - restart.bat
  - scripts/docker-healthcheck.ps1
  - .env.local
  - .env.production
autonomous: true
requirements:
  - INFRA-05
  - INFRA-06
user_setup: []

must_haves:
  truths:
    - "Developer can run 'start.bat' to launch all services in Docker"
    - "Developer can run 'stop.bat' to stop all running containers"
    - "Developer can run 'restart.bat' to restart all services"
    - "Start script shows clear status messages during startup"
    - "Local environment uses development-specific settings"
    - "Production environment uses production-specific settings"
    - "Health check script verifies all services are running"
  artifacts:
    - path: "start.bat"
      provides: "One-command startup for all services"
      contains: "docker-compose up -d"
    - path: "stop.bat"
      provides: "One-command shutdown for all services"
      contains: "docker-compose down"
    - path: "restart.bat"
      provides: "One-command restart for all services"
      contains: "docker-compose restart"
    - path: "scripts/docker-healthcheck.ps1"
      provides: "Health verification for all containers"
      contains: "docker-compose ps"
    - path: ".env.local"
      provides: "Local development environment variables"
      contains: "ENVIRONMENT=development"
    - path: ".env.production"
      provides: "Production environment variables"
      contains: "ENVIRONMENT=production"
  key_links:
    - from: "start.bat"
      to: "docker-compose.yml"
      via: "docker-compose command"
      pattern: "docker-compose"
    - from: "start.bat"
      to: ".env.local"
      via: "environment loading"
      pattern: ".env.local"
    - from: "scripts/docker-healthcheck.ps1"
      to: "running containers"
      via: "docker ps"
      pattern: "docker-compose ps"
---

<objective>
Create Windows batch scripts for local development workflow and environment configuration files for local vs production modes.

Purpose: Simplify local development with single-command operations and ensure proper environment configuration for both development and production.

Output: Batch scripts (start, stop, restart) and environment files (.env.local, .env.production) that enable quick service management.
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
  <name>Task 1: Create start.bat startup script</name>
  <files>start.bat</files>
  <action>
    Create start.bat with the following functionality:

    1. Check if .env.local exists, if not copy from .env.example
    2. Display startup banner: "Starting KMeans Engine Development Environment..."
    3. Run `docker-compose --env-file .env.local up -d`
    4. Wait 5 seconds for containers to initialize
    5. Run health check script (scripts/docker-healthcheck.ps1)
    6. Display success message with URLs:
       - Frontend: http://localhost:3000
       - Backend API: http://localhost:8000
       - API Docs: http://localhost:8000/docs
    7. Display command to view logs: `docker-compose logs -f`
    8. Display command to stop: `stop.bat`

    Include error handling:
    - Check if Docker is running
    - Check if docker-compose exists
    - Display helpful error messages if commands fail

    Use ANSI color codes for better readability:
    - Green for success
    - Yellow for warnings
    - Red for errors
  </action>
  <verify>start.bat executes successfully and starts all containers</verify>
  <done>start.bat creates and starts all three containers with status feedback</done>
</task>

<task type="auto">
  <name>Task 2: Create stop.bat and restart.bat scripts</name>
  <files>stop.bat, restart.bat</files>
  <action>
    **stop.bat:**
    1. Display shutdown banner: "Stopping KMeans Engine Development Environment..."
    2. Run `docker-compose down` to stop and remove containers
    3. Display confirmation message: "All services stopped successfully"
    4. Optionally offer to remove volumes (add prompt with default 'no')

    **restart.bat:**
    1. Display restart banner: "Restarting KMeans Engine Development Environment..."
    2. Run `docker-compose restart` to restart all containers
    3. Wait 5 seconds for containers to reinitialize
    4. Run health check script (scripts/docker-healthcheck.ps1)
    5. Display success message with same URLs as start.bat

    Both scripts should include error handling and colored output matching start.bat style.
  </action>
  <verify>stop.bat stops all containers, restart.bat restarts all containers</verify>
  <done>stop.bat and restart.bat successfully manage container lifecycle</done>
</task>

<task type="auto">
  <name>Task 3: Create Docker health check script</name>
  <files>scripts/docker-healthcheck.ps1</files>
  <action>
    Create scripts/docker-healthcheck.ps1 with PowerShell:

    1. Display "Checking service health..."
    2. Run `docker-compose ps` and parse output
    3. Check each service status:
       - db: Should be "Up" with health check passing
       - backend: Should be "Up"
       - frontend: Should be "Up"
    4. Display status table:
       | Service | Status | Ports |
       |---------|--------|-------|
       | db      | Up     | 3306  |
       | backend | Up     | 8000  |
       | frontend| Up     | 3000  |
    5. If any service is down, display in red
    6. If all services are up, display in green: "All services healthy!"
    7. Return exit code 0 if all healthy, 1 if any down

    Include error handling for:
      - Docker daemon not running
      - No containers running
      - Parse errors

    Use PowerShell Write-Host with -ForegroundColor for colored output.
  </action>
  <verify>scripts/docker-healthcheck.ps1 reports accurate status of all containers</verify>
  <done>Health check script displays status table and returns correct exit codes</done>
</task>

<task type="auto">
  <name>Task 4: Create local and production environment files</name>
  <files>.env.local, .env.production</files>
  <action>
    **.env.local (Development):**
    - Database:
      MYSQL_ROOT_PASSWORD=dev_root_password
      MYSQL_DATABASE=kmeans_db
      MYSQL_USER=kmeans_dev
      MYSQL_PASSWORD=dev_password
      DATABASE_URL=mysql+pymysql://kmeans_dev:dev_password@db:3306/kmeans_db
    - Backend:
      SECRET_KEY=dev_secret_key_change_this_in_production
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      ENVIRONMENT=development
      DEBUG=true
    - Frontend:
      NEXT_PUBLIC_API_URL=http://localhost:8000
      NODE_ENV=development
    - Logging:
      LOG_LEVEL=debug

    **.env.production (Production):**
    - Database:
      MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE=kmeans_prod
      MYSQL_USER=${MYSQL_USER}
      MYSQL_PASSWORD=${MYSQL_PASSWORD}
      DATABASE_URL=${DATABASE_URL}
    - Backend:
      SECRET_KEY=${SECRET_KEY}
      ACCESS_TOKEN_EXPIRE_MINUTES=15
      ENVIRONMENT=production
      DEBUG=false
    - Frontend:
      NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
      NODE_ENV=production
    - Logging:
      LOG_LEVEL=info

    Production file uses ${VAR_NAME} placeholders to indicate these should be set via CI/CD or deployment platform.

    Update .gitignore to ensure:
      - .env.local is NOT ignored (safe to commit)
      - .env is ignored (actual secrets)
      - .env.production is NOT ignored (template with placeholders)
  </action>
  <verify>.env.local loads correctly with start.bat, .env.production is properly formatted</verify>
  <done>Both environment files created with appropriate settings for each environment</done>
</task>

</tasks>

<verification>
1. Run start.bat and verify all three containers start successfully
2. Verify start.bat displays colored output with all service URLs
3. Run scripts/docker-healthcheck.ps1 and verify accurate status table
4. Run stop.bat and verify all containers stop
5. Run start.bat again, then run restart.bat and verify containers restart
6. Verify .env.local loads correctly by checking container environment: `docker-compose exec backend env | grep DATABASE_URL`
7. Verify .env.production has ${VAR_NAME} placeholders instead of actual secrets
8. Test error handling: Stop Docker daemon and run start.bat (should display helpful error)
9. Verify ANSI colors work in Windows Command Prompt and PowerShell
</verification>

<success_criteria>
1. start.bat launches all three containers in a single command
2. stop.bat stops all containers cleanly
3. restart.bat restarts all containers without data loss (volumes persist)
4. Health check script displays accurate status table with colored output
5. .env.local contains development-appropriate settings (debug=true, longer token expiry)
6. .env.production contains production-appropriate settings with ${VAR_NAME} placeholders
7. All scripts display helpful error messages when commands fail
8. Scripts work in both Command Prompt and PowerShell
9. Output is readable with color-coded status information
</success_criteria>

<output>
After completion, create `.planning/phases/01-infrastructure-foundation/01-02-SUMMARY.md` with:
- Script configurations and commands used
- Environment variable decisions for local vs production
- Color scheme and output format decisions
- Any issues encountered and solutions
</output>
