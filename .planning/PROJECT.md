# KMeans Engine

## What This Is

KMeans Engine is a web-based SaaS platform that helps companies automatically segment customers using the K-Means Clustering algorithm. The product transforms historical customer data into actionable business insights without requiring in-depth data science expertise from users.

## Core Value

Provide accurate, reliable customer segmentation through automated K-Means clustering with intuitive visualization and clear results.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **AUTH-01**: User can create account with email and password
- [ ] **AUTH-02**: User can log in and stay logged in across sessions
- [ ] **AUTH-03**: User can log out from any page
- [ ] **AUTH-04**: Passwords are stored with secure hash encryption
- [ ] **AUTH-05**: Login sessions have automatic expiration

- [ ] **DASH-01**: User can view main dashboard with collapsible sidebar
- [ ] **DASH-02**: User can see list of previously created projects
- [ ] **DASH-03**: User can view system health indicators

- [ ] **PIPE-01**: User can access educational page about clustering benefits (Stage 1: Business Understanding)
- [ ] **PIPE-02**: User can upload customer data files (Excel .xlsx or CSV UTF-8) (Stage 2: Data Understanding)
- [ ] **PIPE-03**: System validates data types and required fields automatically
- [ ] **PIPE-04**: User can preview initial data after upload
- [ ] **PIPE-05**: System detects null values and duplicates (Stage 3: Data Preparation)
- [ ] **PIPE-06**: User can choose automatic or manual data cleaning options
- [ ] **PIPE-07**: System standardizes numerical data automatically
- [ ] **PIPE-08**: User can determine number of clusters (K) (Stage 4: Modeling)
- [ ] **PIPE-09**: System executes K-Means++ algorithm with progress indicator
- [ ] **PIPE-10**: User can view cluster distribution visualization (Stage 5: Evaluation & Deployment)
- [ ] **PIPE-11**: User can view model evaluation metrics
- [ ] **PIPE-12**: User can download results in Excel/CSV format

- [ ] **DATA-01**: System validates file size and rejects files exceeding 5,000 rows
- [ ] **DATA-02**: System processes and stores customer data securely
- [ ] **DATA-03**: System isolates each user's data in database
- [ ] **DATA-04**: User can delete their project data manually

- [ ] **VIS-01**: System converts numerical data into understandable graphs and charts
- [ ] **VIS-02**: Visualizations use clean, professional design
- [ ] **VIS-03**: User can interact with visualizations to explore cluster results

- [ ] **UI-01**: Interface uses minimalist modern design with white background and high-contrast text
- [ ] **UI-02**: Interface uses Inter font for maximum readability
- [ ] **UI-03**: Interface has smooth transitions and responsive animations
- [ ] **UI-04**: Interface is responsive for desktop and tablet screens

- [ ] **SEC-01**: All communication uses secure protocol (HTTPS in production)
- [ ] **SEC-02**: Each user's data is logically isolated from other users
- [ ] **SEC-03**: System validates upload limits server-side
- [ ] **SEC-04**: Database structure supports right to be forgotten

### Out of Scope

- **Payment integration** — Defer to v2 (monthly/annual subscriptions)
- **Advanced analysis algorithms** — Defer to v2 (beyond K-Means, e.g., Hierarchical Clustering)
- **Team collaboration** — Defer to v2 (multi-user within single company account)
- **Public API** — Defer to v2 (automated data connections without manual uploads)
- **PDF reports** — Defer to v2 (automated presentation format reports)

## Context

**Target Users:** SMEs and medium-sized companies who want to make data-driven decisions without hiring data scientists.

**Problem Solved:** Companies have customer data but lack expertise and tools to segment customers effectively for marketing, retention, and product decisions.

**Current State:** Project ready to enter Phase 3 (Development - Sprint 1), starting with basic infrastructure (Docker, Database, Hello World).

**Sample Data:** User has sample Excel files (`exported_data.xlsx`, `exported_data_mutasi.xlsx`) representing typical customer datasets to test against.

## Constraints

- **Row Limit**: 5,000 rows maximum per upload — Ensures server memory stability while accommodating realistic datasets
- **File Format**: Excel (.xlsx) and CSV (UTF-8) only — Simplifies parsing and validation
- **User Model**: One account per user — No collaborative team features in v1
- **Storage**: Project data stored for account lifetime — Manual delete option provided
- **Tech Stack** (from specification):
  - Frontend: Next.js (React) with Tailwind CSS, Shadcn UI, Acernity UI, Radix UI
  - Backend: Python FastAPI with Pandas, Scikit-Learn
  - Database: MySQL
  - Infrastructure: Docker & Docker Compose with start.bat script

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Row limit: 5,000 | User specified based on sample data with growth buffer | — Pending |
| Tech stack: Next.js + FastAPI | Balance performance, scalability, and UX quality | — Pending |
| Database: MySQL | Relational, stable, easy to manage for structured data | — Pending |
| Design: Minimalist Modern | Clean, professional impression, focus on data | — Pending |

---
*Last updated: March 3, 2026 after project initialization*
