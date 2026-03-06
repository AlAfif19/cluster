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

### Must-Have (Phase 1-8)

#### Authentication System
- [ ] User registration with email and password
- [ ] User login with credential verification
- [ ] Secure session management with automatic expiration
- [ ] Password hashing (unreadable format)
- [ ] Logout functionality

#### Main Dashboard
- [ ] Collapsible sidebar navigation
- [ ] List of previously created projects
- [ ] System health indicators
- [ ] Responsive design (desktop & tablet)

#### Data Understanding (Stage 2)
- [ ] File upload (Excel .xlsx, CSV UTF-8)
- [ ] Server-side validation of file format and row limit (5,000 rows)
- [ ] Data type validation
- [ ] Required field validation
- [ ] Initial data preview
- [ ] Progress feedback ("Uploading", "Processing")

#### Data Preparation (Stage 3)
- [ ] Automatic detection of null values
- [ ] Automatic detection of duplicates
- [ ] Automatic data cleaning option
- [ ] Manual data cleaning option
- [ ] Numerical data standardization
- [ ] Clear feedback on cleaning actions

#### Modeling (Stage 4)
- [ ] User interface for determining number of clusters (K)
- [ ] K-Means++ algorithm execution
- [ ] Real-time progress indicator during clustering
- [ ] Process status feedback

#### Evaluation & Deployment (Stage 5)
- [ ] Cluster distribution visualization
- [ ] Model evaluation metrics display
- [ ] Download results in Excel format
- [ ] Download results in CSV format

#### Visualization
- [ ] Convert numerical data to graphs and charts
- [ ] Clean, professional visualization design
- [ ] Interactive visualizations for cluster exploration
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
- [ ] HTTPS in production (HTTP local)
- [ ] Data isolation per user in database
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

---
*Extracted from PROJECT.md and specification*
*Last updated: March 4, 2026*
