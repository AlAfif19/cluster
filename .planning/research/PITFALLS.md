# Domain Pitfalls

**Domain:** KMeans Engine SaaS Platform
**Researched:** March 7, 2026
**Overall confidence:** MEDIUM

## Executive Summary

Building a KMeans Engine SaaS platform with Next.js + FastAPI + MySQL involves managing complex interactions between frontend and backend, handling data-intensive operations, and ensuring security across multiple layers. The most critical risks are in authentication/identity management, data processing memory handling, and database query optimization. While the technology stack is well-established and mature, the combination of Python data processing with React frontend and MySQL database introduces specific integration challenges that require careful attention.

## Critical Pitfalls

### Pitfall 1: Insecure Session Management with JWT Tokens

**What goes wrong:** JWT tokens stored improperly, leading to session hijacking, token theft, or unauthorized access. Common issues include storing tokens in localStorage (vulnerable to XSS), not implementing proper token expiration, or missing token revocation mechanisms.

**Why it happens:** Developers often follow simple JWT tutorials without understanding the security implications of token storage and lifecycle management. The convenience of localStorage outweighs security concerns during initial implementation.

**Consequences:** Attackers can steal tokens via XSS attacks, use tokens indefinitely if not expired, or access other users' data if tokens aren't properly scoped to individual users.

**Prevention:**
1. Store JWT tokens in HTTP-only, Secure, SameSite cookies to prevent XSS access
2. Implement short-lived access tokens (15-30 minutes) with refresh tokens
3. Include user ID and expiration in token payload
4. Validate token on every protected route
5. Implement token blacklist or rotation for logout

**Detection:**
- Login persists after logout (no session invalidation)
- Token works indefinitely without re-authentication
- Same token works across different browsers/devices unexpectedly
- Access tokens visible in browser storage (localStorage/sessionStorage)

**Phase:** Phase 02 - Authentication System (AUTH)

**Sources:**
- FastAPI Security Documentation (HIGH confidence) - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- OWASP JWT Security Best Practices (HIGH confidence)

---

### Pitfall 2: Missing Database Connection Pooling

**What goes wrong:** FastAPI opens new MySQL connections for every request, leading to connection exhaustion, performance degradation, and eventual database server crashes under load.

**Why it happens:** Default database connection libraries create new connections unless explicitly configured with pooling. Developers often don't realize the overhead until load testing or production issues arise.

**Consequences:** Database becomes unresponsive, requests timeout, application crashes under concurrent user load, poor user experience during peak usage.

**Prevention:**
1. Use SQLAlchemy with connection pooling (create_engine with pool_size, max_overflow)
2. Configure appropriate pool size based on expected concurrent users
3. Implement connection timeout and recycle settings
4. Monitor connection pool metrics in production
5. Use async database drivers (aiomysql) with async FastAPI

**Detection:**
- Database connection count grows indefinitely under load
- Slow database response times during concurrent requests
- "Too many connections" database errors
- Memory usage increases with request volume

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- SQLAlchemy Connection Pooling Documentation (HIGH confidence)
- FastAPI Database Best Practices (MEDIUM confidence)

---

### Pitfall 3: Memory Exhaustion from Large File Processing

**What goes wrong:** Loading entire Excel/CSV files into Pandas DataFrames causes memory exhaustion when processing large datasets, especially when multiple users upload simultaneously. Even with 5,000 row limit, naive implementations can cause issues.

**Why it happens:** Pandas' convenient `read_excel()` and `read_csv()` load entire files into memory. Without chunking or streaming, memory usage scales linearly with file size and concurrent processing.

**Consequences:** Server crashes, slow processing, inability to handle concurrent uploads, poor user experience, potential data loss.

**Prevention:**
1. Implement file size validation before processing (reject files > reasonable limit)
2. Use chunked reading with pandas `chunksize` parameter for large files
3. Process data in batches and release memory between operations
4. Implement queue system for heavy processing tasks (Celery/Redis)
5. Use generators instead of loading full DataFrames where possible
6. Set strict memory limits per request

**Detection:**
- Server memory usage spikes during file uploads
- Processing slows down with concurrent uploads
- Python MemoryError exceptions in logs
- System becomes unresponsive after multiple uploads

**Phase:** Phase 04 - Data Pipeline (PIPE-02 to PIPE-04)

**Sources:**
- Pandas Documentation on Memory Management (HIGH confidence)
- Scikit-Learn Large Dataset Recommendations (HIGH confidence)

---

### Pitfall 4: N+1 Query Problem in Database Operations

**What goes wrong:** Fetching related data (user projects, data points, cluster results) triggers multiple database queries instead of optimized joins, leading to severe performance degradation as data volume grows.

**Why it happens:** ORM patterns (SQLAlchemy) make it easy to iterate over relationships without explicit join optimization. Developers focus on functionality over query efficiency during initial development.

**Consequences:** Dashboard loads become increasingly slow, database CPU usage spikes, poor user experience, scalability bottlenecks.

**Prevention:**
1. Use `select_related()` for foreign key relationships (SQL joins)
2. Use `prefetch_related()` for many-to-many relationships (separate queries, optimized)
3. Implement query counting in development to detect N+1 issues
4. Use database indexes on frequently queried fields
5. Analyze query plans for complex operations
6. Consider denormalization for read-heavy data

**Detection:**
- Number of database queries grows linearly with number of records displayed
- Dashboard loading time increases with more projects/data
- Database query logs show repeated similar queries
- Slow page loads on data-rich pages

**Phase:** Phase 03 - Dashboard (DASH-01, DASH-02)

**Sources:**
- Django ORM Query Optimization Documentation (HIGH confidence) - https://docs.djangoproject.com/en/stable/topics/db/queries/
- SQLAlchemy Performance Best Practices (MEDIUM confidence)

---

### Pitfall 5: Inadequate User Data Isolation

**What goes wrong:** User can access or modify another user's data through URL manipulation, API endpoint abuse, or missing authorization checks. This violates the "right to be forgotten" requirement and creates serious privacy/legal issues.

**Why it happens:** Authorization logic is often forgotten after authentication is implemented. Developers assume authentication implies authorization, or implement checks inconsistently across endpoints.

**Consequences:** Data privacy breaches, legal liability (GDPR/CCPA violations), user trust loss, potential regulatory fines, competitive intelligence leaks.

**Prevention:**
1. Implement user ID in all database queries (automatic filtering)
2. Use dependency injection for user context in FastAPI
3. Add authorization middleware to enforce user-scoped queries
4. Implement row-level security in database where possible
5. Audit all endpoints for missing user scoping
6. Test with multiple user accounts to verify isolation

**Detection:**
- User can access another user's project by changing project ID in URL
- API returns data not owned by authenticated user
- Deleting projects affects other users' data
- Querying with different user IDs returns unexpected results

**Phase:** Phase 02 - Authentication System (AUTH), Phase 05 - Data Management (DATA-03)

**Sources:**
- FastAPI Security Documentation (HIGH confidence)
- OWASP Authorization Cheat Sheet (HIGH confidence)

---

### Pitfall 6: Blocking Operations in Async FastAPI

**What goes wrong:** Long-running operations (K-Means clustering, file processing, database queries) block the event loop, making the entire application unresponsive to other users during processing.

**Why it happens:** Mixing synchronous libraries (standard Pandas, some database drivers) with async FastAPI without proper async/await patterns. Developers don't understand the blocking nature of certain operations.

**Consequences:** Application freezes during processing, poor user experience, inability to handle concurrent requests, timeouts, cascading failures.

**Prevention:**
1. Use async database drivers (aiomysql, asyncpg)
2. Offload CPU-intensive operations to background tasks (Celery, FastAPI BackgroundTasks)
3. Implement proper async/await patterns throughout
4. Use run_in_executor for blocking operations that can't be asynced
5. Set reasonable timeouts for external operations
6. Monitor event loop blocking metrics

**Detection:**
- Application becomes unresponsive during data processing
- Other users experience slow responses when one user uploads large file
- Logs show event loop warnings or blocking indicators
- Request times increase with concurrent operations

**Phase:** Phase 04 - Data Pipeline (PIPE-09, PIPE-10)

**Sources:**
- FastAPI Async Documentation (HIGH confidence)
- Python Asyncio Best Practices (MEDIUM confidence)

---

### Pitfall 7: CORS Misconfiguration

**What goes wrong:** Overly permissive CORS settings allow unauthorized domains to access API, or overly restrictive settings break legitimate frontend-backend communication in production.

**Why it happens:** During development, developers set CORS to allow all origins for convenience, then forget to tighten for production. Or they misconfigure CORS headers for specific domains.

**Consequences:** Security vulnerabilities (CSRF attacks), broken production deployment, API abuse, unauthorized data access.

**Prevention:**
1. Use fastapi.middleware.cors.CORSMiddleware with explicit origins list
2. Configure allow_origins to specific production domain only
3. Enable credentials for cookie-based authentication
4. Use environment variables for CORS configuration
5. Test CORS in development and production environments
6. Implement rate limiting alongside CORS

**Detection:**
- Frontend can't make API requests in production (blocked by CORS)
- Browser console shows CORS errors
- API requests succeed from unexpected domains
- Network inspection shows CORS headers

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- FastAPI CORS Documentation (HIGH confidence)
- MDN CORS Security Guide (HIGH confidence)

---

### Pitfall 8: Insufficient Input Validation and Sanitization

**What goes wrong:** User input (file uploads, cluster parameters, project names) is not properly validated, allowing malicious uploads, injection attacks, or data corruption.

**Why it happens:** Validation logic is often scattered or incomplete. Developers focus on happy path validation and miss edge cases or malicious inputs.

**Consequences:** Security vulnerabilities (path traversal, injection), data corruption, application crashes, unexpected behavior, poor user experience.

**Prevention:**
1. Use Pydantic models for all input validation (FastAPI native)
2. Validate file types, sizes, and content before processing
3. Sanitize user-generated content before storage/display
4. Implement whitelist validation (allow known good) instead of blacklist
5. Validate numerical ranges for cluster parameters
6. Log and alert on validation failures

**Detection:**
- Application crashes on unexpected input
- Malicious files accepted by upload system
- Invalid cluster parameters cause processing errors
- User input affects other users' data

**Phase:** Phase 04 - Data Pipeline (PIPE-03, PIPE-04)

**Sources:**
- FastAPI Request Body Documentation (HIGH confidence)
- OWASP Input Validation Cheat Sheet (HIGH confidence)

---

### Pitfall 9: Missing Progress Tracking for Long Operations

**What goes wrong:** Users have no visibility into long-running operations (file upload, clustering, data processing), leading to poor UX, user abandonment, and support burden.

**Why it happens:** Progress tracking requires additional complexity (websockets, polling, background task management). Developers prioritize functionality over UX polish.

**Consequences:** Users think application is broken, repeated uploads causing server load, support tickets, poor user experience, abandoned workflows.

**Prevention:**
1. Implement WebSocket or Server-Sent Events for real-time progress
2. Use background task system (Celery) with task state tracking
3. Provide progress bars for file uploads and clustering operations
4. Implement clear status messages at each stage
5. Handle task cancellation gracefully
6. Store task state in database for recovery after refresh

**Detection:**
- Users complain about "broken" uploads that are actually processing
- No indication of progress during long operations
- Users repeat operations unnecessarily
- Support tickets about stuck operations

**Phase:** Phase 04 - Data Pipeline (PIPE-09)

**Sources:**
- FastAPI Websocket Documentation (HIGH confidence)
- Celery Task State Tracking (MEDIUM confidence)

---

### Pitfall 10: Poor Error Handling for Data Processing Failures

**What goes wrong:** Data processing errors (invalid file formats, clustering failures, data validation issues) result in generic error messages, making debugging difficult and user experience poor.

**Why it happens:** Error handling is treated as an afterthought. Developers use broad exception catching without proper logging or user-friendly messages.

**Consequences:** Users can't resolve issues on their own, debugging is difficult, support burden increases, user trust erodes, application appears unreliable.

**Prevention:**
1. Implement specific exception handling for each failure mode
2. Provide actionable error messages to users
3. Log detailed error context for debugging
4. Implement error tracking (Sentry, Rollbar) for production issues
5. Create error classification system (user error vs system error)
6. Implement graceful degradation for non-critical failures

**Detection:**
- Generic error messages for all failure types
- Users unable to self-diagnose issues
- Logs lack context for production debugging
- High support ticket volume

**Phase:** Phase 04 - Data Pipeline (PIPE-03, PIPE-09)

**Sources:**
- FastAPI Exception Handling Documentation (HIGH confidence)
- Python Error Handling Best Practices (MEDIUM confidence)

---

## Moderate Pitfalls

### Pitfall 11: Over-Engineering Architecture

**What goes wrong:** Prematurely splitting into microservices, complex message queues, or over-abstraction adds complexity without benefit, slowing development and introducing bugs.

**Why it happens:** Developers apply "best practices" for large-scale systems to a small MVP, prioritizing architectural purity over shipping features.

**Consequences:** Slower development, harder debugging, unnecessary infrastructure complexity, increased operational overhead, delayed time-to-market.

**Prevention:**
1. Start with monolithic architecture for MVP
2. Split services only when clear need emerges (team scaling, performance)
3. Keep infrastructure simple (Docker Compose over Kubernetes initially)
4. Prioritize feature delivery over architectural perfection
5. Re-evaluate architecture at major milestones

**Detection:**
- Development slows due to architectural complexity
- Simple features require changes across multiple services
- Infrastructure complexity exceeds business complexity
- Team spends more time on infrastructure than features

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- Martin Fowler Microservices Prerequisites (HIGH confidence)
- Startup Architecture Best Practices (MEDIUM confidence)

---

### Pitfall 12: Missing Database Indexes

**What goes wrong:** Critical queries (user lookups, project lists, data filtering) become slow as data volume grows due to missing database indexes.

**Why it happens:** Indexes aren't added until performance issues emerge. Developers don't analyze query patterns during initial development.

**Consequences:** Slow page loads, poor user experience, database performance degradation, scalability issues.

**Prevention:**
1. Add indexes to foreign keys and frequently queried fields
2. Analyze query patterns in development
3. Use EXPLAIN to identify slow queries
4. Monitor database performance in production
5. Add composite indexes for multi-column queries

**Detection:**
- Page loads slow down with more data
- Database query times increase with data volume
- EXPLAIN shows table scans on filtered queries
- Production database performance degradation

**Phase:** Phase 05 - Data Management (DATA-01 to DATA-04)

**Sources:**
- MySQL Index Best Practices (HIGH confidence)
- Database Performance Monitoring Guide (MEDIUM confidence)

---

### Pitfall 13: Improper Docker Resource Limits

**What goes wrong:** Docker containers lack memory/CPU limits, allowing runaway processes to consume host resources and crash the entire application.

**Why it happens:** Docker defaults provide no resource limits. Developers don't test resource exhaustion scenarios.

**Consequences:** Container crashes affect other containers, host system becomes unstable, cascading failures, poor isolation.

**Prevention:**
1. Set memory limits in docker-compose.yml
2. Set CPU limits for CPU-intensive operations
3. Implement health checks for container monitoring
4. Test resource exhaustion scenarios
5. Use container orchestration with resource policies

**Detection:**
- One container crash affects others
- Host system becomes unresponsive
- Memory usage grows indefinitely
- Container restarts due to OOM killer

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- Docker Resource Constraints Documentation (HIGH confidence)
- Docker Compose Best Practices (MEDIUM confidence)

---

### Pitfall 14: Missing Data Validation Before Clustering

**What goes wrong:** Invalid or malformed data (missing values, wrong types, outliers) causes K-Means clustering to fail or produce meaningless results without proper user feedback.

**Why it happens:** Data validation is complex and easy to overlook. Developers focus on the clustering algorithm rather than data quality.

**Consequences:** Users get confusing results, clustering fails silently, poor trust in the system, wasted compute resources.

**Prevention:**
1. Implement comprehensive data validation before clustering
2. Check for missing values and suggest imputation
3. Validate numerical ranges and outliers
4. Provide clear feedback about data quality issues
5. Offer automatic data cleaning options with transparency

**Detection:**
- Clustering produces unexpected or meaningless results
- Users report "broken" clustering results
- Processing fails without clear error messages
- High rate of clustering failures

**Phase:** Phase 04 - Data Pipeline (PIPE-03, PIPE-05)

**Sources:**
- Scikit-Learn Data Validation Guide (HIGH confidence)
- Pandas Data Quality Checking (HIGH confidence)

---

### Pitfall 15: Inefficient K-Means Implementation

**What goes wrong:** Naive K-Means implementation doesn't use optimized algorithms (K-Means++, mini-batch) or caching, leading to poor performance even on moderate datasets.

**Why it happens:** Developers use default Scikit-Learn K-Means without understanding optimization options or dataset-specific tuning.

**Consequences:** Slow clustering times, poor user experience, inability to handle larger datasets, wasted server resources.

**Prevention:**
1. Use K-Means++ initialization (Scikit-Learn default, but verify)
2. Implement mini-batch K-Means for large datasets
3. Consider dimensionality reduction for high-dimensional data
4. Cache intermediate results where possible
5. Implement early stopping for convergence

**Detection:**
- Clustering times are slow relative to dataset size
- CPU usage spikes during clustering
- Users complain about long processing times
- Server becomes unresponsive during clustering

**Phase:** Phase 04 - Data Pipeline (PIPE-09)

**Sources:**
- Scikit-Learn K-Means Documentation (HIGH confidence)
- Clustering Performance Optimization Guide (MEDIUM confidence)

---

## Minor Pitfalls

### Pitfall 16: Poor Visualization Performance

**What goes wrong:** Visualizations render slowly or become unresponsive with large datasets, especially when using heavy charting libraries or client-side processing.

**Why it happens:** Visualization libraries are chosen for aesthetics over performance, and data is sent entirely to frontend for client-side processing.

**Consequences:** Slow page loads, browser hangs, poor user experience, limited interactivity.

**Prevention:**
1. Use lightweight charting libraries (Recharts, Chart.js over D3.js)
2. Implement server-side aggregation for large datasets
3. Use data sampling for initial visualization
4. Implement progressive rendering for complex charts
5. Cache visualization data where possible

**Detection:**
- Visualization pages load slowly
- Browser becomes unresponsive during rendering
- Memory usage spikes in browser
- Poor interactivity on large datasets

**Phase:** Phase 06 - Visualization (VIS-01, VIS-02)

**Sources:**
- React Visualization Performance Guide (MEDIUM confidence)
- Charting Library Comparison (LOW confidence)

---

### Pitfall 17: Missing Accessibility in Visualizations

**What goes wrong:** Visualizations lack proper ARIA labels, keyboard navigation, or screen reader support, making the application inaccessible to users with disabilities.

**Why it happens:** Accessibility is often overlooked in data visualization. Developers focus on visual appeal rather than inclusive design.

**Consequences:** Excludes users with disabilities, legal compliance issues (ADA), poor user experience, limited market reach.

**Prevention:**
1. Use accessible charting libraries with ARIA support
2. Provide text-based alternatives for visualizations
3. Ensure keyboard navigation for interactive elements
4. Test with screen readers
5. Follow WCAG guidelines for data visualization

**Detection:**
- Screen readers can't interpret visualizations
- Keyboard users can't interact with charts
- Accessibility audits fail
- Users with disabilities report issues

**Phase:** Phase 06 - Visualization (VIS-03)

**Sources:**
- WCAG Data Visualization Guidelines (HIGH confidence)
- React Accessibility Best Practices (MEDIUM confidence)

---

### Pitfall 18: Inadequate Logging and Monitoring

**What goes wrong:** Insufficient logging makes debugging production issues difficult, and lack of monitoring prevents proactive issue detection.

**Why it happens:** Logging and monitoring are treated as nice-to-have rather than essential. Basic console logging suffices during development.

**Consequences:** Difficult debugging, slow issue resolution, reactive rather than proactive operations, poor system visibility.

**Prevention:**
1. Implement structured logging (JSON format)
2. Add correlation IDs for request tracing
3. Monitor key metrics (response times, error rates, resource usage)
4. Set up alerts for critical issues
5. Log business events (user actions, data processing)

**Detection:**
- Production issues take long to debug
- No visibility into system health
- Issues discovered by users before operations team
- No historical data for analysis

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- Python Logging Best Practices (HIGH confidence)
- Application Monitoring Guide (MEDIUM confidence)

---

### Pitfall 19: Weak Password Policies

**What goes wrong:** Password requirements are too weak or not enforced, allowing users to choose easily guessable passwords.

**Why it happens:** Developers prioritize user convenience over security, or don't implement proper password validation.

**Consequences:** Account compromise via credential stuffing or brute force, security breaches, user trust loss.

**Prevention:**
1. Implement minimum length requirements (12+ characters)
2. Require complexity (mix of character types)
3. Check against common password lists
4. Implement rate limiting on login attempts
5. Encourage password managers with no maximum length

**Detection:**
- Users can set weak passwords
- High rate of successful brute force attempts
- Account compromise reports
- Security audit failures

**Phase:** Phase 02 - Authentication System (AUTH-04)

**Sources:**
- OWASP Password Storage Cheat Sheet (HIGH confidence)
- NIST Password Guidelines (HIGH confidence)

---

### Pitfall 20: Missing Environment Configuration Validation

**What goes wrong:** Missing or invalid environment variables cause application crashes or security misconfigurations, especially in production deployments.

**Why it happens:** Environment variables are assumed to be present. Startup configuration lacks validation, leading to runtime failures.

**Consequences:** Application crashes on startup, security misconfigurations, difficult deployment issues, production outages.

**Prevention:**
1. Validate all required environment variables on startup
2. Provide clear error messages for missing configuration
3. Use type-safe configuration loading (Pydantic Settings)
4. Document all required environment variables
5. Implement default values where appropriate

**Detection:**
- Application crashes on missing environment variables
- Security issues from misconfigured settings
- Deployment failures due to configuration
- Runtime errors from invalid configuration

**Phase:** Phase 01 - Infrastructure Foundation (INFRA)

**Sources:**
- FastAPI Settings Documentation (HIGH confidence)
- Python Configuration Management (MEDIUM confidence)

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|------------|---------------|-----------|
| Phase 01: Infrastructure | Missing connection pooling, Docker resource limits, CORS misconfiguration | Configure SQLAlchemy pooling, set Docker resource limits, explicit CORS origins |
| Phase 02: Authentication | Insecure token storage, missing authorization, weak passwords | Use HTTP-only cookies, implement user-scoped queries, enforce password complexity |
| Phase 03: Dashboard | N+1 query problem, missing indexes | Use select_related/prefetch_related, add database indexes |
| Phase 04: Data Pipeline | Memory exhaustion, blocking operations, poor error handling | Implement file size limits, use background tasks, specific exception handling |
| Phase 05: Data Management | Inadequate data isolation, missing right to be forgotten | User-scoped queries on all data, implement cascading deletes |
| Phase 06: Visualization | Poor performance, missing accessibility | Use lightweight libraries, implement ARIA labels, keyboard navigation |
| Phase 07: Security | SQL injection vulnerabilities, XSS risks | Use parameterized queries, React sanitization, content security policy |

---

## Integration Pitfalls (Cross-Tech Boundary)

### Pitfall 21: Next.js FastAPI Type Mismatches

**What goes wrong:** TypeScript types in Next.js don't match Pydantic models in FastAPI, leading to runtime errors and difficult debugging.

**Why it happens:** Type definitions are maintained separately without a shared schema or automatic generation from API documentation.

**Prevention:**
1. Use FastAPI automatic OpenAPI documentation
2. Generate TypeScript types from OpenAPI spec
3. Maintain shared type definitions or schema
4. Implement runtime validation on both sides
5. Use tools like openapi-typescript

**Detection:**
- Runtime type errors in API calls
- TypeScript types don't match API responses
- Difficult debugging of type-related bugs
- Frequent API integration issues

**Phase:** Phase 02 onwards (all API integration)

**Sources:**
- FastAPI OpenAPI Documentation (HIGH confidence)
- TypeScript Integration Best Practices (MEDIUM confidence)

---

### Pitfall 22: Data Serialization/Deserialization Issues

**What goes wrong:** Python data structures (Pandas DataFrames, numpy arrays) don't serialize cleanly to JSON for API responses, causing data loss or errors.

**Why it happens:** Complex data types need explicit serialization. Default JSON encoders fail on numpy types or datetime objects.

**Prevention:**
1. Implement custom JSON encoders for numpy/pandas types
2. Use Pydantic models with custom validators
3. Convert complex types to simple JSON-serializable formats
4. Test serialization/deserialization roundtrip
5. Document data format contracts

**Detection:**
- JSON serialization errors in API responses
- Data loss during API calls
- Type mismatches between frontend and backend
- Unexpected null values in responses

**Phase:** Phase 04 - Data Pipeline (PIPE-11, PIPE-12)

**Sources:**
- Pydantic Custom Types Documentation (HIGH confidence)
- FastAPI Response Model Documentation (HIGH confidence)

---

### Pitfall 23: Timezone Handling Inconsistencies

**What goes wrong:** Timezone handling differs between Next.js (browser local time), FastAPI (server time), and MySQL (database time), causing incorrect timestamps and confusion.

**Why it happens:** Timezone handling is complex and often defaulted. Each layer uses different defaults or lacks explicit timezone specification.

**Prevention:**
1. Store all times in UTC in database
2. Convert to user's timezone for display in frontend
3. Use timezone-aware datetime objects throughout
4. Include timezone information in API responses
5. Test across different timezone contexts

**Detection:**
- Timestamps display incorrectly for users in different timezones
- Scheduling or time-based logic fails
- Inconsistent time displays across components
- User reports of incorrect times

**Phase:** Phase 02 onwards (all timestamp handling)

**Sources:**
- Python Datetime Best Practices (HIGH confidence)
- Timezone Handling in JavaScript (HIGH confidence)

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Authentication & Security | HIGH | FastAPI official documentation provides comprehensive security guidance. OWASP best practices well-established. |
| Data Processing | HIGH | Pandas and Scikit-Learn documentation is extensive. Memory and performance patterns well-documented. |
| Architecture | MEDIUM | Architecture patterns depend on specific use case. Some recommendations based on general best practices rather than this specific tech stack. |
| Performance | MEDIUM | Performance optimization often requires empirical testing. Recommendations are based on common patterns but may vary with specific implementation. |
| Database | HIGH | MySQL, SQLAlchemy, and Django ORM documentation provide strong guidance on query optimization and connection management. |
| User Experience | MEDIUM | UX pitfalls are often discovered through user testing rather than documented best practices. |
| Integration | MEDIUM | Cross-tech integration issues vary based on specific implementation details. Some recommendations based on general patterns. |

## Gaps to Address

- **Performance under load:** Specific performance characteristics of this exact stack (Next.js + FastAPI + MySQL + Pandas) under production load should be validated through load testing
- **Scalability thresholds:** At what user count/data volume does monolithic architecture need to split? This depends on specific usage patterns
- **Visualization optimization:** Best practices for interactive visualizations with this specific stack require empirical testing
- **Container orchestration:** When and how to migrate from Docker Compose to Kubernetes or other orchestration depends on operational requirements not yet defined

## Sources

**HIGH Confidence (Official Documentation):**
- FastAPI Security Documentation - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- FastAPI Tutorial - https://fastapi.tiangolo.com/tutorial/
- Django ORM Query Optimization - https://docs.djangoproject.com/en/stable/topics/db/queries/
- Scikit-Learn Clustering Documentation - https://scikit-learn.org/stable/modules/clustering.html
- Pandas Documentation - https://pandas.pydata.org/docs/
- OWASP Security Cheat Sheets - https://cheatsheetseries.owasp.org/
- NIST Digital Identity Guidelines

**MEDIUM Confidence (Well-established practices, multiple sources):**
- SQLAlchemy Connection Pooling Best Practices
- React Performance Optimization Guides
- Python Asyncio Best Practices
- Docker Resource Constraints
- Database Performance Monitoring

**LOW Confidence (General best practices, needs validation):**
- Specific performance characteristics of this exact stack
- Visualization library comparisons
- Microservices vs Monolith decision points for this use case
- Container orchestration migration timing
