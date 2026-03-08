# KMeans Engine Requirements

## Overview
KMeans Engine is a web-based SaaS platform for customer segmentation using K-Means clustering. It transforms historical customer data into actionable business insights without requiring data science expertise.

## Tech Stack (Locked Decisions)
- **Frontend:** Next.js (React), Tailwind CSS, Shadcn UI, Acernity UI, Radix UI, Motion Dev & Magic UI
- **Backend:** Python FastAPI with Pandas, Scikit-Learn
- **Database:** MySQL
- **Infrastructure:** Docker & Docker Compose with start.bat script

## Constraints
- **Row Limit:** 5,000 rows maximum per upload
- **File Format:** Excel (.xlsx) and CSV (UTF-8) only
- **User Model:** One account per user (no team collaboration in v1)
- **Storage:** Project data stored for account lifetime with manual delete option

## v1.0 Requirements

### Must-Have (Phase 1-7)

#### Infrastructure
- [ ] INFRA-01: Docker setup for database
- [ ] INFRA-02: Docker setup for backend
- [ ] INFRA-03: Docker setup for frontend
- [ ] INFRA-04: Docker Compose orchestration
- [ ] INFRA-05: start.bat script for local development
- [ ] INFRA-06: Environment configuration (local vs production)
- [ ] INFRA-07: Git-based version control

#### Authentication System
- [ ] AUTH-01: User can create account with email and password
- [ ] AUTH-02: User can log in and stay logged in across sessions
- [ ] AUTH-03: User can log out from any page
- [ ] AUTH-04: Passwords are stored with secure hash encryption
- [ ] AUTH-05: Login sessions have automatic expiration

#### Main Dashboard
- [ ] DASH-01: User can view main dashboard with collapsible sidebar
- [ ] DASH-02: User can see list of previously created projects
- [ ] DASH-03: User can view system health indicators

#### UI/UX Design
- [ ] UI-01: Interface uses minimalist modern design with white background and high-contrast text
- [ ] UI-02: Interface uses Inter font for maximum readability
- [ ] UI-03: Interface has smooth transitions and responsive animations
- [ ] UI-04: Interface is responsive for desktop and tablet screens

#### Data Understanding (Stage 2)
- [ ] PIPE-02: User can upload customer data files (Excel .xlsx or CSV UTF-8)
- [ ] PIPE-03: System validates data types and required fields automatically
- [ ] PIPE-04: User can preview initial data after upload
- [ ] DATA-01: System validates file size and rejects files exceeding 5,000 rows
- [ ] DATA-02: System processes and stores customer data securely
- [ ] DATA-03: System isolates each user's data in database
- [ ] SEC-03: System validates upload limits server-side
- [ ] Progress feedback ("Uploading", "Processing")

#### Data Preparation (Stage 3)
- [ ] PIPE-05: System detects null values and duplicates
- [ ] PIPE-06: User can choose automatic or manual data cleaning options
- [ ] PIPE-07: System standardizes numerical data automatically
- [ ] DATA-04: User can delete their project data manually
- [ ] Clear feedback on cleaning actions

#### Modeling (Stage 4)
- [ ] PIPE-08: User can determine number of clusters (K)
- [ ] PIPE-09: System executes K-Means++ algorithm with progress indicator
- [ ] Real-time progress indicator during clustering
- [ ] Process status feedback

#### Evaluation & Deployment (Stage 5)
- [ ] PIPE-10: User can view cluster distribution visualization
- [ ] PIPE-11: User can view model evaluation metrics
- [ ] PIPE-12: User can download results in Excel/CSV format

#### Business Understanding (Stage 1)
- [ ] PIPE-01: User can access educational page about clustering benefits
- [ ] Clear explanation of K-Means for businesses
- [ ] Use case examples

#### Visualization
- [ ] VIS-01: System converts numerical data into understandable graphs and charts
- [ ] VIS-02: Visualizations use clean, professional design
- [ ] VIS-03: User can interact with visualizations to explore cluster results
- [ ] High contrast, readable charts

#### UI/UX Design
- [ ] Minimalist modern design (white background, high contrast text)
- [ ] Inter font family
- [ ] Smooth page transitions
- [ ] Responsive loading animations
- [ ] Clear error messages in human language
- [ ] Tooltips and help text per step
- [ ] Empty states handled gracefully

#### Security & Privacy
- [ ] SEC-01: All communication uses secure protocol (HTTPS in production)
- [ ] SEC-02: Each user's data is logically isolated from other users
- [ ] Server-side upload validation
- [ ] Session token expiration
- [ ] Database schema supports right to be forgotten
- [ ] Password encryption

#### Infrastructure
- [ ] Docker setup for database
- [ ] Docker setup for backend
- [ ] Docker setup for frontend
- [ ] Docker Compose orchestration
- [ ] start.bat script for local development
- [ ] Environment configuration (local vs production)
- [ ] Git-based version control

#### Business Understanding (Stage 1)
- [ ] Educational page about clustering benefits
- [ ] Clear explanation of K-Means for businesses
- [ ] Use case examples

### Should-Have (if time/resources allow)

- [ ] Data quality score before processing
- [ ] Recommended K value suggestion
- [ ] Cluster profiles/insights auto-generation
- [ ] Multiple projects per user
- [ ] Project duplication for testing
- [ ] Data export before cleaning
- [ ] Dark mode toggle
- [ ] Tutorial/onboarding for new users

### Won't-Have (v2+)

- Payment integration (subscriptions)
- Advanced algorithms (Hierarchical Clustering, DBSCAN)
- Team collaboration (multi-user accounts)
- Public API (automated data connections)
- PDF report generation

## Non-Functional Requirements

### Performance
- Responsive UI even at 5,000 row limit
- Clustering completes in reasonable time for 5,000 rows
- Fast page transitions and loading states

### Reliability
- System remains stable under load
- Graceful error handling without crashes
- Data integrity throughout analysis pipeline

### Security
- All sensitive data encrypted at rest and in transit
- User data isolation enforced
- Session management prevents unauthorized access

### Usability
- No technical expertise required for analysis
- Clear, actionable error messages
- Intuitive 5-stage pipeline flow

## Success Criteria

### Primary
- **Analysis Accuracy:** K-Means clustering produces meaningful, actionable customer segments

### Secondary
- User can complete full 5-stage analysis pipeline without technical support
- System handles 5,000-row datasets reliably
- Visualizations are clear and interpretable by business users

## Requirements Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | 1 | Pending |
| INFRA-02 | 1 | Pending |
| INFRA-03 | 1 | Pending |
| INFRA-04 | 1 | Pending |
| INFRA-05 | 1 | Pending |
| INFRA-06 | 1 | Pending |
| INFRA-07 | 1 | Pending |
| AUTH-01 | 2 | Complete |
| AUTH-02 | 2 | Complete |
| AUTH-03 | 2 | Complete |
| AUTH-04 | 2 | Complete |
| AUTH-05 | 2 | Complete |
| SEC-01 | 2 | Complete |
| SEC-02 | 2 | Complete |
| DASH-01 | 3 | Pending |
| DASH-02 | 3 | Pending |
| DASH-03 | 3 | Pending |
| UI-01 | 3 | Pending |
| UI-02 | 3 | Pending |
| UI-03 | 3 | Pending |
| UI-04 | 3 | Pending |
| PIPE-01 | 7 | Pending |
| PIPE-02 | 4 | Pending |
| PIPE-03 | 4 | Pending |
| PIPE-04 | 4 | Pending |
| PIPE-05 | 5 | Pending |
| PIPE-06 | 5 | Pending |
| PIPE-07 | 5 | Pending |
| PIPE-08 | 6 | Pending |
| PIPE-09 | 6 | Pending |
| PIPE-10 | 7 | Pending |
| PIPE-11 | 7 | Pending |
| PIPE-12 | 7 | Pending |
| DATA-01 | 4 | Pending |
| DATA-02 | 4 | Pending |
| DATA-03 | 4 | Pending |
| DATA-04 | 5 | Pending |
| SEC-03 | 4 | Pending |
| VIS-01 | 7 | Pending |
| VIS-02 | 7 | Pending |
| VIS-03 | 7 | Pending |

**Total v1 Requirements: 45**
**Coverage: 45/45 (100%)**

---
*Extracted from PROJECT.md and specification*
*Last updated: March 6, 2026*
# Requirements: KMeans Engine

**Defined:** March 7, 2026
**Core Value:** Provide accurate, reliable customer segmentation through automated K-Means clustering with intuitive visualization and clear results.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Authentication

- [ ] **AUTH-01**: User can create account with email and password
- [ ] **AUTH-02**: User can log in and stay logged in across sessions
- [ ] **AUTH-03**: User can log out from any page
- [ ] **AUTH-04**: Passwords are stored with secure hash encryption
- [ ] **AUTH-05**: Login sessions have automatic expiration

### Dashboard

- [ ] **DASH-01**: User can view main dashboard with collapsible sidebar
- [ ] **DASH-02**: User can see list of previously created projects
- [ ] **DASH-03**: User can view system health indicators

### Data Pipeline

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

### Data Management

- [ ] **DATA-01**: System validates file size and rejects files exceeding 5,000 rows
- [ ] **DATA-02**: System processes and stores customer data securely
- [ ] **DATA-03**: System isolates each user's data in database
- [ ] **DATA-04**: User can delete their project data manually

### Visualization

- [ ] **VIS-01**: System converts numerical data into understandable graphs and charts
- [ ] **VIS-02**: Visualizations use clean, professional design
- [ ] **VIS-03**: User can interact with visualizations to explore cluster results

### UI Design

- [ ] **UI-01**: Interface uses minimalist modern design with white background and high-contrast text
- [ ] **UI-02**: Interface uses Inter font for maximum readability
- [ ] **UI-03**: Interface has smooth transitions and responsive animations
- [ ] **UI-04**: Interface is responsive for desktop and tablet screens

### Security

- [ ] **SEC-01**: All communication uses secure protocol (HTTPS in production)
- [ ] **SEC-02**: Each user's data is logically isolated from other users
- [ ] **SEC-03**: System validates upload limits server-side
- [ ] **SEC-04**: Database structure supports right to be forgotten

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Payment Integration

- **PAYM-01**: User can subscribe to monthly/annual plans
- **PAYM-02**: User can manage subscription and billing
- **PAYM-03**: System processes payments securely

### Advanced Analysis

- **ADVN-01**: User can choose hierarchical clustering algorithm
- **ADVN-02**: User can choose DBSCAN clustering algorithm
- **ADVN-03**: System provides advanced statistical tests

### Team Collaboration

- **TEAM-01**: Multiple users can access same company account
- **TEAM-02**: Users have role-based permissions (admin, member)
- **TEAM-03**: System tracks user activity in shared projects

### Public API

- **API-01**: Users can programmatically upload data
- **API-02**: Users can trigger clustering via API
- **API-03**: Users can retrieve results via API

### PDF Reports

- **PDF-01**: User can generate PDF summary reports
- **PDF-02**: PDF includes visualizations and insights
- **PDF-03**: User can customize report layout

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Social login (Google, Facebook) | Not MVP need, adds complexity |
| Real-time collaborative editing | Out of scope for v1, single user per account |
| Advanced clustering beyond K-Means | Complexity explosion, K-Means is sufficient for MVP |
| Automated PDF report generation | Excel/CSV export sufficient, PDF too complex for v1 |
| Public API endpoints for programmatic access | Out of scope for v1, manual file uploads only |
| Payment/billing integration | Out of scope for v1, free tier only |
| Scheduled batch processing | Out of scope for v1, manual triggers only |
| Data sharing between users | Out of scope for v1, per-user isolation required |
| Natural language query interface | Too complex for MVP, form-based UI sufficient |
| Advanced statistical tests | Overkill for target users, simple metrics only |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 2 | Pending |
| AUTH-03 | Phase 2 | Pending |
| AUTH-04 | Phase 2 | Pending |
| AUTH-05 | Phase 2 | Pending |
| DASH-01 | Phase 3 | Pending |
| DASH-02 | Phase 3 | Pending |
| DASH-03 | Phase 3 | Pending |
| PIPE-01 | Phase 4 | Pending |
| PIPE-02 | Phase 4 | Pending |
| PIPE-03 | Phase 4 | Pending |
| PIPE-04 | Phase 4 | Pending |
| PIPE-05 | Phase 4 | Pending |
| PIPE-06 | Phase 4 | Pending |
| PIPE-07 | Phase 4 | Pending |
| PIPE-08 | Phase 5 | Pending |
| PIPE-09 | Phase 5 | Pending |
| PIPE-10 | Phase 6 | Pending |
| PIPE-11 | Phase 6 | Pending |
| PIPE-12 | Phase 7 | Pending |
| DATA-01 | Phase 4 | Pending |
| DATA-02 | Phase 4 | Pending |
| DATA-03 | Phase 7 | Pending |
| DATA-04 | Phase 3 | Pending |
| VIS-01 | Phase 6 | Pending |
| VIS-02 | Phase 6 | Pending |
| VIS-03 | Phase 6 | Pending |
| UI-01 | Phase 6 | Pending |
| UI-02 | Phase 6 | Pending |
| UI-03 | Phase 6 | Pending |
| UI-04 | Phase 6 | Pending |
| SEC-01 | Phase 7 | Pending |
| SEC-02 | Phase 7 | Pending |
| SEC-03 | Phase 7 | Pending |
| SEC-04 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 35 total
- Mapped to phases: 35 (after roadmap creation)
- Unmapped: 0 ✓

---
*Requirements defined: March 7, 2026*
*Last updated: March 7, 2026 after initial definition*
