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
| SEC-02 | 2 | Pending |
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
