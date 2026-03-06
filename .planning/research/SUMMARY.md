# Research Summary: KMeans Engine MVP

**Synthesized:** March 7, 2026
**Confidence:** MEDIUM

## Executive Summary

This project is a SaaS platform for non-data scientists to perform K-Means clustering on their own data (CSV/Excel files up to 5,000 rows). The platform combines a Next.js React frontend with a FastAPI Python backend, using MySQL for data persistence and Scikit-Learn for clustering operations. Experts recommend a monolithic architecture with Docker containerization for the MVP, using JWT tokens with httpOnly cookies for authentication and implementing user data isolation through MySQL foreign key relationships.

The recommended approach prioritizes security-first architecture (proper JWT handling, user data isolation), data pipeline reliability (comprehensive validation, error handling, progress tracking), and separation of concerns (service layer for business logic, repository pattern for database access). Key risks include authentication security vulnerabilities, database connection exhaustion, memory issues during file processing, and N+1 query problems as data scales. Mitigation strategies include using SQLAlchemy connection pooling, implementing background tasks for long-running operations, and adding proper database indexes early in development.

## Key Technical Decisions

| Area | Decision | Rationale |
|-------|----------|-----------|
| Frontend | Next.js 15.x with React 18.x and Tailwind CSS | Built-in API routes, server components, excellent performance, strong TypeScript support, modern React patterns |
| Backend | FastAPI 0.115.x | Async support, automatic OpenAPI docs, type hints, excellent for ML APIs, native Pydantic integration |
| Database | MySQL 8.0+ with SQLAlchemy 2.0.x | Relational, ACID compliant, excellent for user/project isolation, async driver support (aiomysql) |
| Visualization | Recharts 2.12.x with d3-scale 4.0.x | Declarative, composable, excellent TypeScript support, React-native integration |
| Authentication | JWT with httpOnly cookies (passlib, bcrypt, PyJWT) | Stateless authentication, secure token storage (XSS-resistant), works with Next.js and FastAPI |

## Stack Requirements

### Frontend

| Library | Version | Purpose |
|---------|---------|---------|
| Next.js | 15.x | Frontend framework with API routes and server components |
| React | 18.x | UI library, required by Next.js |
| TypeScript | 5.x | Type safety, prevents runtime errors |
| Tailwind CSS | 3.x | Utility-first CSS framework for modern responsive design |
| Recharts | 2.12.x | React charts, declarative and composable |
| @radix-ui/react-* | Latest | UI primitives, required by Shadcn UI for accessibility |
| lucide-react | 0.400.x | Modern icon library matching design system |
| @tanstack/react-query | 5.x | Data fetching with caching, background updates, loading states |
| react-hook-form | 7.51.x | Form handling for file uploads, user registration |
| zod | 3.22.x | Schema validation, client-side validation matching Pydantic |
| react-dropzone | 14.2.x | Drag-and-drop file upload UI |
| axios | 1.6.x | HTTP client for API calls to FastAPI backend |
| socket.io-client | 4.x | WebSocket client for real-time progress updates |

### Backend

| Library | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.115.x | Backend framework with async support, automatic docs |
| uvicorn | 0.30.x | ASGI server for FastAPI |
| pandas | 2.2.x | Data manipulation, industry standard for CSV/Excel processing |
| numpy | 2.0.x | Numerical computing, required by pandas and scikit-learn |
| scikit-learn | 1.5.x | K-Means clustering, stable KMeans++ implementation |
| openpyxl | 3.1.x | Excel file parsing, reliable .xlsx reader |
| python-multipart | 0.0.9 | File upload handling, required by FastAPI for multipart uploads |
| SQLAlchemy | 2.0.x | Python ORM with async support, type-safe queries |
| PyMySQL | 1.1.x | MySQL driver, pure Python driver compatible with async |
| Alembic | 1.13.x | Database migrations, version control for schema changes |
| passlib | 1.7.x | Password hashing, secure bcrypt implementation |
| bcrypt | 4.2.x | Hash algorithm, industry standard password hashing |
| PyJWT | 2.8.x | JWT token handling, stateless authentication |
| python-jose | 3.3.x | JWT verification, fast JWT validation supports RS256 for production |
| httpx | 0.27.x | Async HTTP client, for Next.js to FastAPI API calls |
| pydantic | 2.7.x | Data validation, request/response validation, FastAPI integration |
| pydantic-settings | 2.x | Settings management, type-safe configuration |
| python-dotenv | 1.0.x | Environment variables, load .env files required for security |
| chardet | 5.2.x | Encoding detection, auto-detect CSV encoding |
| xlsxwriter | 3.1.x | Excel export, generate clean .xlsx files for results |

### Infrastructure

| Component | Configuration |
|-----------|---------------|
| Docker | 24.x+ for containerization, consistent environments, deployment isolation |
| Docker Compose | 2.24.x for multi-container orchestration (Next.js + FastAPI + MySQL) |
| nginx | 1.25.x reverse proxy for SSL termination, routing, static files |
| MySQL | 8.0+ with connection pooling (SQLAlchemy), UTF-8 support, cascade deletes |
| Environment variables | JWT_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL, MySQL credentials |

## Feature Landscape

### Table Stakes (Must Have)

**Authentication & Identity Management:**
- User registration with email/password
- Login with session persistence (JWT tokens in httpOnly cookies)
- Logout from any page (clear tokens/cookies)
- Password hash encryption (bcrypt)
- Automatic session expiration (24-hour access tokens)
- Password reset flow (defer to v1.1)

**Dashboard & Navigation:**
- Main dashboard with navigation (collapsible sidebar)
- Project list view with pagination
- System health indicators (API status, storage usage)
- Create new project action

**Data Pipeline - Upload & Validation:**
- File upload with progress (chunked upload standard)
- Excel (.xlsx) and CSV support (openpyxl, pandas)
- File size validation (5,000 row limit per project)
- Data preview after upload (table view with pagination)
- Automatic type detection (infer numeric/categorical/date)
- Required field validation
- Null value detection (highlight affected rows/cols)
- Duplicate detection (exact match detection)

**Data Pipeline - Cleaning & Preparation:**
- Null handling options (drop/fill with mean/median)
- Duplicate removal option (keep first occurrence typical)
- Data standardization (normalization) - required for K-Means algorithm

**Data Pipeline - Clustering:**
- K value selection with suggested range (2-10)
- K-Means++ algorithm execution
- Progress indicator during clustering (WebSocket or polling)
- Cluster count display

**Data Pipeline - Evaluation & Export:**
- Cluster distribution visualization (pie/bar chart)
- Silhouette score metric
- Elbow method visualization (plot for different K values)
- Results download (Excel/CSV with cluster labels)

**Visualization & Interaction:**
- Scatter plot with cluster coloring (2D projection)
- Interactive chart tooltips (hover to see point details)
- Zoom/pan on visualizations
- Responsive chart sizing (CSS media queries)
- Color-coded clusters (distinct, accessible colors)

**Data Management:**
- Project isolation (database foreign keys)
- Project deletion (manual, cascade delete associated data)
- Project renaming
- Project details view (upload date, row count, cluster count)

**Security:**
- HTTPS in production (SSL/TLS certificate)
- User data isolation (multi-tenant security, row-level patterns)
- Server-side validation (all API endpoints)
- Right to be forgotten (full user data deletion, GDPR/privacy compliance)

**UI/UX:**
- Modern, responsive design (mobile-first approach)
- Clear error messages (actionable feedback)
- Loading states (spinners/skeleton screens)
- Success confirmations (toasts/notifications)
- Consistent navigation (same sidebar across pages)

### Differentiators (Nice to Have)

- Educational pipeline stages (CRISP-DM framework visualization, guides non-data scientists)
- Automatic K optimization (Elbow method auto-detection, reduces decision paralysis)
- Business insight suggestions (transforms clusters into actions, requires domain knowledge rules)
- Pre-built templates (jumpstart common segmentation use cases: retail, telecom)
- One-click smart cleaning (auto-applies optimal cleaning strategy, heuristic-based defaults)
- Cluster comparison (compare clustering runs with different K, side-by-side metrics)
- Data snapshot versions (revert to previous data states, version control for datasets)
- Export to presentation format (PowerPoint/Word integration, shareable business-ready outputs)
- Anomaly detection (identify outliers within clusters, distance-based detection)
- Customer lifecycle mapping (map clusters to lifecycle stages, requires predefined stages)

### Anti-Features (Don't Add)

- Social login (Google, Facebook) - increases complexity, not MVP need, use email/password only
- Real-time collaborative editing - out of scope for v1, single user per account
- Advanced clustering algorithms (DBSCAN, Hierarchical) - complexity explosion, K-Means is sufficient
- Automated report generation - PDF generation complex, Excel/CSV export sufficient
- API endpoints for programmatic access - out of scope for v1, manual file uploads only
- Payment/billing integration - out of scope for v1, free tier only
- Advanced statistical tests - overkill for target users, simple metrics only
- Natural language query interface - too complex for MVP, standard form-based UI
- Scheduled batch processing - out of scope for v1, manual triggers only
- Data sharing between users - out of scope for v1, per-user isolation
- ML model persistence - not needed for simple clustering, re-run clustering each time
- Custom algorithm parameters - overwhelms non-expert users, sensible defaults only

## Architecture Overview

**System Architecture:**

```
Client Browser (Next.js + React + Tailwind)
    ↓ HTTP/HTTPS (REST API)
    ↓ JWT Bearer Tokens (httpOnly cookies)
Docker Container Network
    ├─ Frontend (Next.js:3000)
    ├─ Backend (FastAPI:8000)
    └─ MySQL Database (3306)
```

**Component Boundaries:**
- Frontend Container: User interface, client-side state, visualization rendering, communicates with Backend API via HTTP
- Backend Container: API endpoints, authentication, data processing, clustering operations, communicates with MySQL and Frontend
- Database Container: Persistent storage, user data isolation, transaction management, communicates with Backend

**Key Integration Points:**

1. Authentication Flow: Next.js stores JWT in httpOnly cookies, FastAPI issues/validates tokens, middleware validates on protected routes
2. File Upload: Frontend FormData → FastAPI UploadFile → Pandas parsing → MySQL storage → Frontend preview
3. User Data Isolation: MySQL foreign keys enforce ownership, FastAPI queries filter by user_id from JWT, Next.js routes scoped to current user
4. Clustering Operation: Frontend triggers → FastAPI background task → Scikit-Learn KMeans++ → MySQL results → Frontend polling
5. Visualization: Backend aggregates cluster statistics → JSON response → Frontend renders with Recharts (distribution charts, scatter plots, radar charts)
6. React-Python Communication: REST API endpoints (/api/auth/*, /api/projects/*, /api/tasks/*), Axios client with interceptors, standardized error handling

**Data Flow:**
User Action → Frontend State → Backend API → MySQL/Processing → Frontend Update → User Feedback

**Database Schema Pattern:**
- Users table (id, email, password_hash, created_at)
- Projects table (user_id foreign key, name, status, created_at) - ON DELETE CASCADE
- Uploads table (project_id foreign key, file_name, file_size, total_rows, status)
- Raw data table (upload_id foreign key, row_index, data JSON)
- Cluster results table (project_id foreign key, k_value, model_params JSON, metrics JSON)
- Cluster assignments table (cluster_result_id foreign key, row_index, cluster_id)

**Patterns to Follow:**
- Repository Pattern for database access (abstract queries into repository classes)
- Service Layer for business logic (separate from API endpoints)
- React Context for global state (authentication, theme, notifications)
- Error Boundary for React (graceful error handling in production)

**Anti-Patterns to Avoid:**
- Storing JWT in localStorage (vulnerable to XSS attacks, use httpOnly cookies)
- Monolithic frontend components (hard to test/maintain, break into smaller focused components)
- Direct SQL queries in API endpoints (violates separation of concerns, use SQLAlchemy ORM)
- Synchronous long-running operations (blocks request handling, use background tasks)
- Mixing data and UI concerns (format in backend, frontend only renders)

## Critical Pitfalls

### Must Address Immediately

**1. Insecure Session Management with JWT Tokens**
- Store JWT tokens in HTTP-only, Secure, SameSite cookies (NOT localStorage)
- Implement short-lived access tokens (15-30 minutes) with refresh tokens
- Include user ID and expiration in token payload
- Validate token on every protected route
- Implement token blacklist or rotation for logout
- Phase: Authentication System (AUTH)

**2. Missing Database Connection Pooling**
- Use SQLAlchemy with connection pooling (create_engine with pool_size, max_overflow)
- Configure appropriate pool size based on expected concurrent users
- Implement connection timeout and recycle settings
- Use async database drivers (aiomysql) with async FastAPI
- Phase: Infrastructure Foundation (INFRA)

**3. Memory Exhaustion from Large File Processing**
- Implement file size validation before processing (reject files > reasonable limit)
- Use chunked reading with pandas `chunksize` parameter for large files
- Process data in batches and release memory between operations
- Implement queue system for heavy processing tasks (Celery/Redis optional for v2)
- Set strict memory limits per request
- Phase: Data Pipeline (PIPE-02 to PIPE-04)

**4. N+1 Query Problem in Database Operations**
- Use `select_related()` for foreign key relationships (SQL joins)
- Use `prefetch_related()` for many-to-many relationships
- Implement query counting in development to detect N+1 issues
- Use database indexes on frequently queried fields
- Phase: Dashboard (DASH-01, DASH-02)

**5. Inadequate User Data Isolation**
- Implement user ID in all database queries (automatic filtering)
- Use dependency injection for user context in FastAPI
- Add authorization middleware to enforce user-scoped queries
- Implement row-level security in database where possible
- Test with multiple user accounts to verify isolation
- Phase: Authentication System (AUTH), Data Management (DATA-03)

**6. Blocking Operations in Async FastAPI**
- Use async database drivers (aiomysql)
- Offload CPU-intensive operations to background tasks (FastAPI BackgroundTasks)
- Implement proper async/await patterns throughout
- Use run_in_executor for blocking operations that can't be asynced
- Set reasonable timeouts for external operations
- Phase: Data Pipeline (PIPE-09, PIPE-10)

### Address Before Phase N

**7. CORS Misconfiguration**
- Use fastapi.middleware.cors.CORSMiddleware with explicit origins list
- Configure allow_origins to specific production domain only
- Enable credentials for cookie-based authentication
- Use environment variables for CORS configuration
- Phase: Infrastructure Foundation (INFRA)

**8. Insufficient Input Validation and Sanitization**
- Use Pydantic models for all input validation (FastAPI native)
- Validate file types, sizes, and content before processing
- Sanitize user-generated content before storage/display
- Implement whitelist validation (allow known good) instead of blacklist
- Validate numerical ranges for cluster parameters
- Phase: Data Pipeline (PIPE-03, PIPE-04)

**9. Missing Progress Tracking for Long Operations**
- Implement WebSocket or Server-Sent Events for real-time progress
- Use background task system with task state tracking
- Provide progress bars for file uploads and clustering operations
- Implement clear status messages at each stage
- Store task state in database for recovery after refresh
- Phase: Data Pipeline (PIPE-09)

**10. Poor Error Handling for Data Processing Failures**
- Implement specific exception handling for each failure mode
- Provide actionable error messages to users
- Log detailed error context for debugging
- Implement error tracking (Sentry, Rollbar) for production issues
- Create error classification system (user error vs system error)
- Phase: Data Pipeline (PIPE-03, PIPE-09)

**11. Over-Engineering Architecture**
- Start with monolithic architecture for MVP
- Split services only when clear need emerges
- Keep infrastructure simple (Docker Compose over Kubernetes initially)
- Prioritize feature delivery over architectural perfection
- Phase: Infrastructure Foundation (INFRA)

**12. Missing Database Indexes**
- Add indexes to foreign keys and frequently queried fields
- Analyze query patterns in development
- Use EXPLAIN to identify slow queries
- Monitor database performance in production
- Add composite indexes for multi-column queries
- Phase: Data Management (DATA-01 to DATA-04)

**13. Missing Data Validation Before Clustering**
- Implement comprehensive data validation before clustering
- Check for missing values and suggest imputation
- Validate numerical ranges and outliers
- Provide clear feedback about data quality issues
- Offer automatic data cleaning options with transparency
- Phase: Data Pipeline (PIPE-03, PIPE-05)

**14. Inefficient K-Means Implementation**
- Use K-Means++ initialization (Scikit-Learn default, but verify)
- Implement mini-batch K-Means for large datasets
- Consider dimensionality reduction for high-dimensional data
- Cache intermediate results where possible
- Implement early stopping for convergence
- Phase: Data Pipeline (PIPE-09)

## Recommended Phase Structure

| Phase | Focus | Dependencies |
|-------|-------|--------------|
| 1 | Infrastructure Foundation | None (start here) |
| 2 | Authentication System | Phase 1 (database) |
| 3 | Dashboard & Project Management | Phase 2 (auth) |
| 4 | Data Pipeline - Upload & Cleaning | Phase 2 (auth), Phase 3 (projects) |
| 5 | Clustering Engine | Phase 4 (data cleaned) |
| 6 | Visualization | Phase 5 (clustering results) |
| 7 | Export & Security | Phase 6 (results ready) |

**Build Order Rationale:**

Phase 1 (Infrastructure Foundation) starts with database schema and models because user data isolation via foreign keys is the foundation for all multi-tenant security. MySQL with connection pooling must be configured before any API endpoints can reliably handle concurrent requests. Docker setup establishes the container network and environment variable management needed for all subsequent services.

Phase 2 (Authentication System) builds on the database foundation by implementing JWT token generation/validation in FastAPI, login/logout/refresh endpoints, httpOnly cookie setup, auth context in Next.js, and protected route middleware. Authentication must complete before any protected features (dashboard, data pipeline, visualization) can be implemented, as user context is required for all database queries and security boundaries.

Phase 3 (Dashboard & Project Management) provides the user interface entry point and core CRUD operations. Project CRUD API and dashboard UI require authentication for user-scoped data access. This phase delivers the basic navigation structure and project listing functionality that users interact with before performing any data operations.

Phase 4 (Data Pipeline - Upload & Cleaning) implements file upload with validation, Excel/CSV parsing, schema validation service, data preview UI, cleaning options form, and automatic cleaning service. Upload must complete before cleaning (cannot clean what hasn't been uploaded), and cleaning must complete before clustering (K-Means cannot handle null values, standardization affects results).

Phase 5 (Clustering Engine) delivers the core product value through K-Means++ clustering with Scikit-Learn. Background task system handles long-running operations without blocking requests. Clustering service layer encapsulates algorithm logic, and clustering UI provides K value selection and progress indication. This phase requires cleaned data from Phase 4.

Phase 6 (Visualization) renders cluster results using Recharts for client-side visualization. Backend aggregates cluster statistics, calculates dimensionality reduction (PCA), and prepares feature analysis data. Frontend components render distribution charts, profile comparisons, and 2D scatter plots. This phase requires clustering results from Phase 5.

Phase 7 (Export & Security) provides data portability and security hardening. Export functionality generates Excel/CSV from results with streaming downloads. Security hardening implements HTTPS, input validation on all endpoints, rate limiting, and SQL injection prevention. Right to be forgotten implements user deletion cascade for GDPR/privacy compliance.

## Open Questions

1. **Performance under load:** Specific performance characteristics of this exact stack (Next.js + FastAPI + MySQL + Pandas) under production load should be validated through load testing before scaling beyond 100 concurrent users

2. **Optimal polling frequency for background task progress:** Requires empirical testing to balance real-time user feedback with database load (recommend testing 1-2 second intervals initially)

3. **Visualization rendering performance with large cluster results:** Best practices for interactive visualizations with 5,000 data points require empirical testing; may need server-side aggregation or data sampling for initial rendering

4. **Celery vs FastAPI BackgroundTasks for production scale:** Current MVP uses BackgroundTasks; migration to Celery + Redis recommended at ~10K users or when background task queueing becomes a bottleneck

5. **Optimal database indexing for cluster query patterns:** Requires analyzing actual query patterns from Phase 5 and 6 implementation; indexes on foreign keys and frequently queried fields are baseline

6. **Production secrets management approach:** MVP uses environment variables; recommend AWS Secrets Manager or equivalent for production deployment

7. **Migration timing from Docker Compose to Kubernetes:** Depends on operational requirements; monolithic Docker Compose should scale to ~100 users before orchestration becomes necessary

---
*Summary synthesized from 4 research dimensions: STACK, FEATURES, ARCHITECTURE, PITFALLS*
