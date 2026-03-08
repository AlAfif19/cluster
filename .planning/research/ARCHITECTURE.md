# Architecture Patterns

**Domain:** KMeans Engine SaaS Platform
**Researched:** March 7, 2026

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                            │
│                    (Next.js + React + Tailwind)                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP/HTTPS (REST API)
                             │ JWT Bearer Tokens
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Container Network                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │  Frontend (Next) │  │  Backend (Fast)  │  │   MySQL (DB)    │ │
│  │  :3000           │  │  :8000           │  │   :3306         │ │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With | Technology |
|-----------|---------------|-------------------|------------|
| **Frontend Container** | User interface, client-side state, visualization rendering | Backend API via HTTP | Next.js 14+, React, Tailwind CSS, Shadcn UI |
| **Backend Container** | API endpoints, authentication, data processing, clustering operations | MySQL database, Frontend | FastAPI, Pandas, Scikit-Learn |
| **Database Container** | Persistent storage, user data isolation, transaction management | Backend API | MySQL 8.0+ |

### Data Flow

```
User Action → Frontend State → Backend API → MySQL/Processing → Frontend Update → User Feedback
```

## Integration Points

### 1. Authentication Flow

**Technology Stack Integration:**
- Next.js stores JWT tokens in httpOnly cookies (secure, XSS-resistant)
- FastAPI issues JWT tokens using python-jose or PyJWT
- Middleware validates tokens on protected routes

**Flow:**
```
1. User submits credentials → POST /api/auth/login
2. FastAPI validates credentials against MySQL users table
3. FastAPI generates JWT token (payload: user_id, email, expires)
4. Backend returns token in httpOnly cookie (Secure, HttpOnly, SameSite=Strict)
5. Next.js receives cookie, browser stores it automatically
6. Subsequent requests include cookie automatically
7. FastAPI middleware validates token before protected endpoints
8. Token refresh: POST /api/auth/refresh with short-lived access + long-lived refresh tokens
```

**New Components:**
- `frontend/lib/auth.ts` - Auth state management (React Context or Zustand)
- `backend/app/api/auth/endpoints.py` - Login, logout, refresh endpoints
- `backend/app/api/auth/security.py` - JWT token generation/validation
- `backend/app/api/auth/middleware.py` - Token validation middleware
- `backend/app/db/models/user.py` - User model with password hashing (bcrypt)

**Data Format:**
```typescript
// Login Request
interface LoginRequest {
  email: string;
  password: string;
}

// Login Response (token in httpOnly cookie)
interface LoginResponse {
  success: boolean;
  user: {
    id: number;
    email: string;
  };
}
```

**Build Order Priority:** **1** (Foundation for all protected features)

---

### 2. File Upload Pipeline

**Technology Stack Integration:**
- Frontend uses FormData API for multipart uploads
- FastAPI uses UploadFile with streaming for large files
- Pandas reads Excel/CSV directly from file-like objects

**Flow:**
```
1. User selects file → React File Input component
2. Frontend validates file size (< 5MB client-side check) and extension (.xlsx, .csv)
3. Next.js creates FormData with file and metadata
4. POST /api/projects/{project_id}/upload with FormData
5. FastAPI receives UploadFile, validates file size server-side
6. Stream file to temporary storage (in-memory or tmpfs for < 5MB)
7. Pandas reads file (pd.read_excel() or pd.read_csv())
8. Validate schema (required columns, data types)
9. Store raw data in MySQL (temporary table or staging)
10. Return preview data to frontend
```

**New Components:**
- `frontend/components/upload/FileUploadForm.tsx` - Upload UI with progress
- `frontend/lib/api/upload.ts` - Upload API client
- `backend/app/api/upload/endpoints.py` - Upload endpoint with validation
- `backend/app/services/data_parser.py` - Excel/CSV parsing service
- `backend/app/services/data_validator.py` - Schema validation service
- `backend/app/db/models/upload.py` - Upload tracking model

**Data Format:**
```typescript
// Upload Request (FormData)
FormData.append('file', fileBlob);
FormData.append('project_id', '123');

// Upload Response
interface UploadResponse {
  success: boolean;
  upload_id: string;
  preview: {
    rows: any[];
    total_rows: number;
    columns: string[];
    detected_types: Record<string, string>;
  };
  issues: {
    missing_columns: string[];
    invalid_types: string[];
    null_values: number;
    duplicates: number;
  };
}
```

**Key Integration Points:**
- Frontend handles progress events (onUploadProgress in Axios)
- Backend returns streaming responses for large previews
- MySQL stores file metadata and processing status

**Build Order Priority:** **3** (Requires authentication, precedes clustering)

---

### 3. User Data Isolation

**Technology Stack Integration:**
- MySQL foreign keys enforce user ownership
- FastAPI queries filter by user_id from JWT token
- Next.js routes scoped to current user

**Database Schema Pattern:**
```sql
-- Users table
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table (user-scoped)
CREATE TABLE projects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  status ENUM('upload', 'validation', 'cleaning', 'clustering', 'complete') DEFAULT 'upload',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Data uploads (project-scoped)
CREATE TABLE uploads (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_id INT NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_size INT NOT NULL,
  total_rows INT NOT NULL,
  status ENUM('processing', 'validated', 'cleaned') DEFAULT 'processing',
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Raw data storage (project-scoped)
CREATE TABLE raw_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  upload_id INT NOT NULL,
  row_index INT NOT NULL,
  data JSON NOT NULL,
  FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE CASCADE,
  INDEX idx_upload_row (upload_id, row_index)
);

-- Cluster results (project-scoped)
CREATE TABLE cluster_results (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_id INT NOT NULL,
  k_value INT NOT NULL,
  model_params JSON,
  metrics JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Cluster assignments (project-scoped)
CREATE TABLE cluster_assignments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cluster_result_id INT NOT NULL,
  row_index INT NOT NULL,
  cluster_id INT NOT NULL,
  FOREIGN KEY (cluster_result_id) REFERENCES cluster_results(id) ON DELETE CASCADE,
  INDEX idx_cluster_row (cluster_result_id, row_index)
);
```

**Backend Query Pattern:**
```python
# All queries automatically filter by current user
def get_user_projects(user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project_data(project_id: int, user_id: int):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id
    ).first()
    if not project:
        raise HTTPException(404, "Project not found")
    return project
```

**New Components:**
- `backend/app/db/models/` - All data models with user_id foreign keys
- `backend/app/db/session.py` - Database session with user context
- `backend/app/services/user_isolation.py` - Helper functions for user-scoped queries
- `backend/app/middleware/user_context.py` - Extract user_id from JWT for DB queries

**Build Order Priority:** **2** (Database foundation, required for all features)

---

### 4. K-Means Clustering Operation

**Technology Stack Integration:**
- FastAPI BackgroundTasks for async processing
- Scikit-Learn KMeans algorithm
- MySQL stores intermediate results and final cluster assignments

**Flow:**
```
1. User selects K value and clicks "Cluster" → POST /api/projects/{id}/cluster
2. FastAPI validates project status (data must be cleaned)
3. Backend creates background task:
   a. Load cleaned data from MySQL
   b. Standardize features (StandardScaler)
   c. Fit KMeans++ model
   d. Predict cluster assignments
   e. Calculate metrics (inertia, silhouette score)
4. Return task_id to frontend for polling
5. Frontend polls GET /api/tasks/{task_id} for progress
6. Backend updates task status in MySQL (processing, completed, failed)
7. On completion, store cluster results and assignments in MySQL
8. Frontend receives completion, fetches visualization data
```

**New Components:**
- `backend/app/api/clustering/endpoints.py` - Cluster trigger endpoint
- `backend/app/services/clustering/` - Clustering service layer
  - `kmeans_service.py` - KMeans execution
  - `data_preprocessor.py` - Feature standardization
  - `metrics_calculator.py` - Cluster evaluation metrics
- `backend/app/tasks/background_tasks.py` - Celery or BackgroundTasks wrapper
- `backend/app/db/models/task.py` - Task tracking model
- `frontend/components/clustering/ClusterProgress.tsx` - Progress UI
- `frontend/lib/api/clustering.ts` - Clustering API client

**Data Format:**
```typescript
// Cluster Request
interface ClusterRequest {
  k: number; // Number of clusters
  features: string[]; // Selected features for clustering
}

// Cluster Response (immediate)
interface ClusterResponse {
  success: boolean;
  task_id: string;
  estimated_time: number; // seconds
}

// Task Status Poll
interface TaskStatus {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number; // 0-100
  current_step: string;
  error?: string;
}

// Cluster Results (when completed)
interface ClusterResults {
  cluster_id: string;
  k: number;
  metrics: {
    inertia: number;
    silhouette_score: number;
    davies_bouldin_score: number;
  };
  clusters: {
    cluster_id: number;
    count: number;
    centroid: Record<string, number>;
    characteristics: string;
  }[];
  assignments: {
    row_index: number;
    cluster_id: number;
    distance_to_centroid: number;
  }[];
}
```

**Progress Tracking Strategy:**
- Use MySQL task table for status updates (works across container restarts)
- Backend updates progress percentage every 10-20% of rows processed
- Frontend polls every 1-2 seconds until completion

**Build Order Priority:** **4** (Requires data pipeline complete)

---

### 5. Visualization Rendering

**Technology Stack Integration:**
- Frontend: Recharts or Chart.js for client-side rendering
- Backend: Aggregates data, calculates statistics, sends JSON payload
- Real-time: Server-sent events or polling for updates

**Flow:**
```
1. User views cluster results → GET /api/projects/{id}/visualization
2. Backend aggregates cluster statistics from MySQL:
   - Cluster sizes and proportions
   - Centroid values for radar/spider plots
   - 2D/3D scatter plot coordinates (PCA or t-SNE)
   - Feature distributions per cluster
3. Backend returns JSON with visualization data
4. Frontend renders charts using Recharts:
   - Pie chart: Cluster distribution
   - Bar chart: Feature means per cluster
   - Scatter plot: 2D projection with cluster colors
   - Radar chart: Cluster profiles
5. User interactions (hover, click) handled client-side
```

**New Components:**
- `backend/app/api/visualization/endpoints.py` - Visualization data endpoints
- `backend/app/services/visualization/` - Visualization data preparation
  - `cluster_stats.py` - Calculate cluster statistics
  - `dimensionality_reduction.py` - PCA/t-SNE for 2D plots
  - `feature_analysis.py` - Feature distributions per cluster
- `frontend/components/visualization/` - Visualization components
  - `ClusterDistribution.tsx` - Pie chart
  - `ClusterProfiles.tsx` - Bar/Radar charts
  - `ClusterScatter.tsx` - 2D scatter plot
  - `FeatureComparison.tsx` - Side-by-side feature distributions
- `frontend/lib/api/visualization.ts` - Visualization API client

**Data Format:**
```typescript
// Visualization Data Response
interface VisualizationData {
  cluster_distribution: {
    cluster_id: number;
    count: number;
    percentage: number;
  }[];
  cluster_profiles: {
    cluster_id: number;
    feature_means: Record<string, number>;
  }[];
  scatter_plot: {
    points: {
      row_index: number;
      x: number;
      y: number;
      cluster_id: number;
    }[];
    feature_names: [string, string]; // Which features are plotted
  };
  feature_distributions: {
    feature_name: string;
    clusters: {
      cluster_id: number;
      min: number;
      max: number;
      mean: number;
      std: number;
      median: number;
    }[];
  }[];
}
```

**Rendering Strategy:**
- Use Recharts for React integration with Tailwind styling
- Responsive design: Charts resize with viewport
- Interactive: Hover tooltips, click to filter cluster data
- Export: Download charts as PNG using html2canvas

**Build Order Priority:** **5** (Requires clustering results)

---

### 6. React-Python Communication

**API Endpoint Structure:**
```
/api/auth/*           - Authentication (login, logout, refresh)
/api/users/*          - User management
/api/projects/*       - Project CRUD
/api/projects/:id/upload    - File upload
/api/projects/:id/validate   - Data validation
/api/projects/:id/clean      - Data cleaning
/api/projects/:id/cluster    - K-Means clustering
/api/projects/:id/results    - Cluster results
/api/projects/:id/visualization  - Visualization data
/api/projects/:id/download   - Download results (Excel/CSV)
/api/tasks/:id/status       - Background task polling
```

**HTTP Client Pattern (Frontend):**
```typescript
// frontend/lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true, // Include httpOnly cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth if needed)
apiClient.interceptors.request.use((config) => {
  // Cookies automatically included
  return config;
});

// Response interceptor (handle errors, token refresh)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

**API Error Handling Pattern:**
```typescript
// Backend (FastAPI)
from fastapi import HTTPException

@app.post("/api/projects/{id}/cluster")
async def create_cluster(project_id: int, request: ClusterRequest):
    project = get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail={"error": "Project not found", "code": "PROJECT_NOT_FOUND"}
        )
    if project.status != 'cleaned':
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Data must be cleaned before clustering",
                "code": "INVALID_PROJECT_STATUS"
            }
        )

// Frontend (React)
try {
  const response = await apiClient.post(`/api/projects/${projectId}/cluster`, data);
  // Handle success
} catch (error) {
  if (error.response?.status === 400) {
    const errorCode = error.response.data.code;
    // Show specific error message based on error code
  } else {
    // Generic error handling
  }
}
```

**Data Format Conventions:**
- All responses: `{ success: boolean, data?: any, error?: string }`
- Lists: `{ items: T[], total: number, page: number, per_page: number }`
- Errors: `{ success: false, error: string, code?: string, details?: any }`
- Dates: ISO 8601 strings

---

### 7. Docker Container Structure

**Docker Compose Services:**
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NODE_ENV=development
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:pass@db:3306/kmeans_db
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app
      - /app/__pycache__

  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=kmeans_db
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

**Container Communication:**
- Frontend → Backend: HTTP to `http://backend:8000` (internal) or `http://localhost:8000` (external)
- Backend → MySQL: MySQL protocol to `db:3306`
- All containers share Docker network for inter-container communication

**Volume Strategy:**
- `mysql-data`: Persistent MySQL data (survives container restart)
- Code mounting: Development mode (hot reload enabled)
- Production: Build images without mounting, use read-only volumes

---

### 8. Environment Variable Configuration

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=KMeans Engine
NODE_ENV=development
```

**Backend (.env):**
```bash
# Database
DATABASE_URL=mysql+pymysql://user:pass@db:3306/kmeans_db
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_DATABASE=kmeans_db
MYSQL_USER=kmeans_user
MYSQL_PASSWORD=${MYSQL_PASSWORD}

# Security
SECRET_KEY=${SECRET_KEY}
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# Application
ENVIRONMENT=development
MAX_FILE_SIZE_MB=5
MAX_ROWS_PER_FILE=5000
UPLOAD_DIR=/tmp/uploads

# Logging
LOG_LEVEL=debug
```

**Configuration Management:**
- Frontend: Vars prefixed with `NEXT_PUBLIC_` exposed to browser
- Backend: All vars server-side only, never exposed to client
- Docker Compose: Pass env vars from host to containers
- Production: Use secrets management (e.g., AWS Secrets Manager)

---

## Patterns to Follow

### Pattern 1: Repository Pattern for Database Access

**What:** Abstract database queries into repository classes
**When:** For complex data access, maintaining separation of concerns
**Example:**
```python
# backend/app/db/repositories/project_repository.py
from sqlalchemy.orm import Session
from app.db.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_projects(self, user_id: int):
        return self.db.query(Project).filter(Project.user_id == user_id).all()

    def get_by_id(self, project_id: int, user_id: int):
        return self.db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id
        ).first()

    def create(self, project_data: dict, user_id: int):
        project = Project(**project_data, user_id=user_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
```

---

### Pattern 2: Service Layer for Business Logic

**What:** Separate business logic from API endpoints
**When:** For complex operations like clustering, data cleaning
**Example:**
```python
# backend/app/services/clustering/kmeans_service.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

class KMeansService:
    def execute_clustering(self, data: pd.DataFrame, k: int):
        # Standardize features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)

        # Fit KMeans
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
        clusters = kmeans.fit_predict(scaled_data)

        # Calculate metrics
        inertia = kmeans.inertia_
        silhouette = silhouette_score(scaled_data, clusters)

        return {
            'clusters': clusters,
            'centroids': scaler.inverse_transform(kmeans.cluster_centers_),
            'inertia': inertia,
            'silhouette_score': silhouette
        }
```

---

### Pattern 3: React Context for Global State

**What:** Share authentication and UI state across components
**When:** For user auth, theme, notifications
**Example:**
```typescript
// frontend/contexts/AuthContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/login', { email, password });
    setUser(response.data.user);
  };

  const logout = async () => {
    await apiClient.post('/api/auth/logout');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

---

### Pattern 4: Error Boundary for React

**What:** Catch JavaScript errors in component tree
**When:** For graceful error handling in production
**Example:**
```typescript
// frontend/components/ErrorBoundary.tsx
import React from 'react';

export class ErrorBoundary extends React.Component<{ children: React.ReactNode }> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: any) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 text-center">
          <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
          <p className="text-gray-600 mb-4">An unexpected error occurred.</p>
          <button onClick={() => window.location.reload()}>Reload Page</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Storing JWT in localStorage

**What:** Storing JWT tokens in localStorage or sessionStorage
**Why bad:** Vulnerable to XSS attacks, tokens can be stolen by malicious scripts
**Instead:** Use httpOnly cookies for token storage (Set-Cookie header from backend)

---

### Anti-Pattern 2: Monolithic Frontend Components

**What:** Building massive components with mixed concerns
**Why bad:** Hard to test, maintain, and reuse
**Instead:** Break into smaller, focused components with clear responsibilities

---

### Anti-Pattern 3: Direct SQL Queries in API Endpoints

**What:** Writing raw SQL queries directly in FastAPI endpoints
**Why bad:** Violates separation of concerns, hard to test, SQL injection risk
**Instead:** Use SQLAlchemy ORM or repository pattern for database access

---

### Anti-Pattern 4: Synchronous Long-Running Operations

**What:** Running clustering synchronously in HTTP request
**Why bad:** Blocks request handling, timeouts, poor UX
**Instead:** Use background tasks (FastAPI BackgroundTasks or Celery) with progress tracking

---

### Anti-Pattern 5: Mixing Data and UI Concerns

**What:** Formatting dates, numbers, or calculating statistics in React components
**Why bad:** Business logic scattered in UI, hard to test
**Instead:** Prepare data in backend services, frontend only renders

---

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| **Database** | Single MySQL instance sufficient | Add read replicas | Sharding + connection pooling |
| **Backend** | Single container sufficient | Horizontal scaling (multiple containers) | Load balancer + auto-scaling |
| **Clustering** | Background tasks per request | Queue system (Celery + Redis) | Dedicated clustering workers |
| **File Storage** | Local filesystem | Cloud storage (S3) | CDN + multi-region storage |
| **Frontend** | Static hosting | CDN caching | Edge computing (Cloudflare Workers) |

**Current MVP Scope:**
- Single MySQL instance (Docker volume)
- Single backend container (handles ~10 concurrent clustering ops)
- Frontend static assets served by Next.js
- File processing in memory (< 5MB files)
- Background tasks using FastAPI BackgroundTasks

---

## Data Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE DATA PIPELINE                          │
└─────────────────────────────────────────────────────────────────────────┘

Stage 1: Upload
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌─────────────┐
│  User    │───▶│ Next.js   │───▶│ FastAPI   │───▶│ MySQL       │
│ Browser  │    │ FormData  │    │ UploadFile│    │ uploads table│
└──────────┘    └───────────┘    └───────────┘    └─────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │ Pandas parses   │
                                         │ Excel/CSV       │
                                         └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │ Validation Check│
                                         │ (schema, types) │
                                         └─────────────────┘
                                                  │
                                         Valid? ├──▶ Yes ──▶ Preview Data
                                                  │
                                                  ▼
                                                No ───▶ Error Response

Stage 2: Clean
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌─────────────┐
│  User    │───▶│ Next.js   │───▶│ FastAPI   │───▶│ Pandas      │
│  Selects │    │   UI      │    │ Clean API │    │ Processing  │
│ Options  │    └───────────┘    └───────────┘    └─────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Handle nulls    │
                                        │ Remove duplicates│
                                        │ Standardize data│
                                        └─────────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Store cleaned   │
                                        │ data in MySQL   │
                                        └─────────────────┘

Stage 3: Cluster
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌─────────────┐
│  User    │───▶│ Next.js   │───▶│ FastAPI   │───▶│ Background  │
│  Sets K  │    │   UI      │    │ Cluster   │    │ Task        │
│          │    └───────────┘    └───────────┘    └─────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Scikit-Learn    │
                                        │ KMeans++        │
                                        └─────────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Calculate       │
                                        │ Metrics         │
                                        └─────────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Store results   │
                                        │ in MySQL       │
                                        └─────────────────┘

Stage 4: Visualize
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌─────────────┐
│  User    │───▶│ Next.js   │───▶│ FastAPI   │───▶│ Recharts    │
│  Views   │    │   UI      │    │ Results   │    │ Rendering   │
│ Results  │    └───────────┘    └───────────┘    └─────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Aggregated stats│
                                        │ from MySQL      │
                                        └─────────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ 2D projections   │
                                        │ (PCA)           │
                                        └─────────────────┘

Stage 5: Download
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌─────────────┐
│  User    │───▶│ Next.js   │───▶│ FastAPI   │───▶│ Pandas      │
│  Exports │    │   UI      │    │ Export    │    │ to Excel/CSV│
└──────────┘    └───────────┘    └───────────┘    └─────────────┘
```

---

## Suggested Build Order

Based on dependencies and integration complexity:

### Phase 1: Foundation (Weeks 1-2)
**Priority: HIGH** - Prerequisites for everything else

1. **Database Schema & Models** (Week 1)
   - Create MySQL schema with all tables
   - Build SQLAlchemy models (user, project, upload, etc.)
   - Implement user isolation via foreign keys
   - **Integration Point:** Backend ↔ MySQL

2. **Authentication System** (Week 1-2)
   - JWT token generation/validation in FastAPI
   - Login/logout/refresh endpoints
   - httpOnly cookie setup
   - Auth context in Next.js
   - Protected route middleware
   - **Integration Point:** Frontend ↔ Backend ↔ MySQL

### Phase 2: Project Management (Weeks 2-3)
**Priority: HIGH** - Core CRUD before data features

3. **Project CRUD API** (Week 2)
   - Create/read/update/delete projects
   - User-scoped project listing
   - Project status tracking
   - **Integration Point:** Frontend ↔ Backend ↔ MySQL

4. **Dashboard UI** (Week 2-3)
   - Project list display
   - Health indicators
   - Sidebar navigation
   - **Integration Point:** Next.js components + API client

### Phase 3: Data Pipeline - Upload (Weeks 3-4)
**Priority: HIGH** - Core data ingestion

5. **File Upload System** (Week 3)
   - Frontend upload form with progress
   - FastAPI upload endpoint with validation
   - Excel/CSV parsing with Pandas
   - Schema validation service
   - **Integration Point:** Frontend → Backend → MySQL

6. **Data Preview UI** (Week 3-4)
   - Data table display
   - Issue reporting (nulls, duplicates)
   - Column type detection
   - **Integration Point:** Backend aggregation → Frontend rendering

### Phase 4: Data Pipeline - Cleaning (Weeks 4-5)
**Priority: MEDIUM** - Data quality before clustering

7. **Data Cleaning Service** (Week 4)
   - Automatic cleaning options
   - Null handling strategies
   - Duplicate removal
   - Feature standardization
   - **Integration Point:** Pandas processing → MySQL storage

8. **Cleaning UI** (Week 4-5)
   - Cleaning options form
   - Before/after comparison
   - Cleaning summary display
   - **Integration Point:** Frontend state → Backend API

### Phase 5: Clustering Engine (Weeks 5-6)
**Priority: HIGH** - Core value proposition

9. **Background Task System** (Week 5)
   - Task tracking model
   - Background task execution
   - Progress polling mechanism
   - **Integration Point:** Frontend polling → Backend status → MySQL

10. **K-Means Clustering Service** (Week 5-6)
    - Scikit-Learn KMeans++ integration
    - Feature preprocessing
    - Metrics calculation (inertia, silhouette)
    - Result storage
    - **Integration Point:** Pandas → Scikit-Learn → MySQL

11. **Clustering UI** (Week 6)
    - K value selector
    - Progress indicator
    - Clustering trigger
    - **Integration Point:** Frontend → Background Task API

### Phase 6: Visualization (Weeks 6-7)
**Priority: MEDIUM** - User experience enhancement

12. **Visualization Data Service** (Week 6-7)
    - Cluster statistics aggregation
    - Dimensionality reduction (PCA)
    - Feature analysis per cluster
    - **Integration Point:** MySQL aggregation → JSON response

13. **Visualization Components** (Week 7)
    - Cluster distribution chart
    - Profile comparison charts
    - 2D scatter plot
    - Interactive tooltips
    - **Integration Point:** Recharts → Frontend

### Phase 7: Export & Security (Weeks 7-8)
**Priority: MEDIUM** - Final polish

14. **Export Functionality** (Week 7)
    - Excel/CSV generation from results
    - Download endpoint with streaming
    - **Integration Point:** Pandas → FastAPI FileResponse

15. **Security Hardening** (Week 7-8)
    - HTTPS configuration
    - Input validation all endpoints
    - Rate limiting
    - SQL injection prevention
    - **Integration Point:** All API endpoints

16. **Right to Be Forgotten** (Week 8)
    - User deletion cascade
    - Data purging service
    - **Integration Point:** MySQL cascade deletes + manual cleanup

---

## Integration Testing Strategy

### Critical Integration Points to Test

1. **Auth Flow**
   - Test: Login → Token → Protected API → Logout
   - Verify: JWT validation, cookie handling, token expiration

2. **Data Isolation**
   - Test: User A creates project → User B cannot access
   - Verify: Foreign key constraints, user-scoped queries

3. **Upload → Clean → Cluster Pipeline**
   - Test: Upload file → Clean data → Cluster → View results
   - Verify: Data integrity, status transitions, error handling

4. **Background Task Execution**
   - Test: Trigger cluster → Poll progress → Complete
   - Verify: Task state updates, progress tracking, error recovery

5. **Visualization Data Flow**
   - Test: Fetch results → Render charts → Interact
   - Verify: Data aggregation, chart rendering, user interaction

---

## Migration Path for v2

When scaling beyond MVP:

1. **Queue System:** Replace BackgroundTasks with Celery + Redis
2. **Object Storage:** Move file uploads to S3 or Azure Blob
3. **Database Scaling:** Add read replicas, consider sharding
4. **API Gateway:** Implement rate limiting, caching
5. **Monitoring:** Add Prometheus, Grafana, distributed tracing
6. **CI/CD:** Automated testing, deployment pipelines

---

## Sources

**MEDIUM Confidence (Based on established patterns and technology capabilities):**
- Next.js + FastAPI integration patterns (well-documented common architecture)
- JWT authentication with httpOnly cookies (security best practice)
- FastAPI BackgroundTasks documentation (official FastAPI docs)
- MySQL foreign key relationships (relational database fundamentals)
- Scikit-Learn KMeans API (official scikit-learn documentation)
- React Context API (official React docs)
- Recharts visualization library (official Recharts docs)
- Docker Compose multi-service setup (official Docker docs)

**LOW Confidence (Requires validation):**
- Specific performance characteristics with 5,000-row datasets
- Optimal polling frequency for background task progress
- Visualization rendering performance with large cluster results

**Gaps requiring phase-specific research:**
- Celery vs BackgroundTasks for production scale (v2 planning)
- Optimal database indexing for cluster query patterns
- CDN strategy for frontend asset delivery
- Production secrets management approach

---

*Last updated: March 7, 2026*
