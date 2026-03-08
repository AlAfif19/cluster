# Technology Stack

**Project:** KMeans Engine
**Researched:** March 7, 2026
**Confidence:** MEDIUM (unable to verify with live sources due to tool limitations)

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Next.js | 15.x | Frontend framework | Built-in API routes, server components, excellent performance, strong TypeScript support |
| FastAPI | 0.115.x | Backend framework | Async support, automatic OpenAPI docs, type hints, excellent for ML APIs |
| React | 18.x | UI library | Required by Next.js, component-based architecture |
| TypeScript | 5.x | Type safety | Prevents runtime errors, better DX, especially for ML data structures |

### Data Processing & Machine Learning

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| pandas | 2.2.x | Data manipulation | Industry standard for CSV/Excel processing, robust data cleaning capabilities |
| numpy | 2.0.x | Numerical computing | Required by pandas and scikit-learn, efficient array operations |
| scikit-learn | 1.5.x | K-Means clustering | Stable, well-documented KMeans++ implementation, widely used |
| openpyxl | 3.1.x | Excel file parsing | Reliable .xlsx reader, supports modern Excel formats |
| python-multipart | 0.0.9 | File upload handling | Required by FastAPI for form/multipart file uploads |

### Database

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| MySQL | 8.0+ | Primary database | Relational, ACID compliant, excellent for user/project isolation |
| SQLAlchemy | 2.0.x | Python ORM | Async support, type-safe queries, industry standard |
| PyMySQL | 1.1.x | MySQL driver | Pure Python driver, compatible with SQLAlchemy async |
| mysql-connector-python | 9.0.x | Alternative driver | Official MySQL driver, good fallback option |
| Alembic | 1.13.x | Database migrations | Version control for schema changes, essential for SaaS |

### Authentication & Security

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| passlib | 1.7.x | Password hashing | Secure password hashing (bcrypt), battle-tested |
| bcrypt | 4.2.x | Hash algorithm | Strong password hashing, industry standard |
| PyJWT | 2.8.x | JWT token handling | Stateless authentication, works with Next.js and FastAPI |
| python-jose | 3.3.x | JWT verification | Fast JWT validation, supports RS256 for production |
| httpx | 0.27.x | Async HTTP client | For Next.js to FastAPI API calls, better than requests |
| aiosmtplib | 3.0.x | Email sending (optional) | For user verification emails if needed |

### Data Visualization

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| recharts | 2.12.x | React charts | Declarative, composable, excellent TypeScript support |
| d3-scale | 4.0.x | Data scaling | For custom visualizations, works with React |
| lucide-react | 0.400.x | Icons | Modern icon library, matches project design system |
| @radix-ui/react-* | Latest | UI primitives | Required by Shadcn UI, accessible components |

### Progress Tracking

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| WebSocket (FastAPI) | Built-in | Real-time progress | Built-in WebSocket support in FastAPI for live updates |
| @tanstack/react-query | 5.x | Data fetching | Handles caching, background updates, loading states |
| socket.io-client | 4.x | WebSocket client | For Next.js to connect to FastAPI WebSocket |

### File Processing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| chardet | 5.2.x | Encoding detection | Auto-detect CSV encoding (UTF-8 vs others) |
| xlrd | 2.0.x | Legacy Excel | Fallback for older .xls files if needed |
| xlsxwriter | 3.1.x | Excel export | Generate clean .xlsx files for results download |
| csv | Built-in | CSV parsing | Python built-in, for basic CSV operations |

### Infrastructure

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Docker | 24.x+ | Containerization | Consistent environments, deployment isolation |
| Docker Compose | 2.24.x | Multi-container | Orchestrate Next.js + FastAPI + MySQL |
| nginx | 1.25.x | Reverse proxy | SSL termination, routing, static files |
| uvicorn | 0.30.x | ASGI server | Fast ASGI server for FastAPI |

## Supporting Libraries

### Python Backend
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | 1.0.x | Environment variables | Load .env files, required for security |
| pydantic | 2.7.x | Data validation | Request/response validation, FastAPI integration |
| pydantic-settings | 2.x | Settings management | Type-safe configuration management |
| celery | 5.3.x | Task queue | For background clustering jobs (optional) |
| redis | 5.0.x | Cache/queue | Required if using Celery, job persistence |
| pytest | 8.1.x | Testing | Unit and integration testing |
| pytest-asyncio | 0.23.x | Async testing | Test FastAPI async endpoints |
| httpx | 0.27.x | HTTP client | Test FastAPI endpoints |

### Next.js Frontend
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| axios | 1.6.x | HTTP client | API calls to FastAPI backend |
| react-hook-form | 7.51.x | Form handling | File upload forms, user registration |
| zod | 3.22.x | Schema validation | Client-side validation, matches Pydantic |
| react-dropzone | 14.2.x | File upload | Drag-and-drop file upload UI |
| @tanstack/react-query | 5.x | Data fetching | Cache API responses, handle loading states |
| date-fns | 3.3.x | Date formatting | Display creation dates, timestamps |
| clsx | 2.1.x | Class utilities | Conditional CSS classes with Tailwind |
| tailwind-merge | 2.2.x | Merge Tailwind | Prevent class conflicts |

## Integration Points

### Next.js ↔ FastAPI Communication

```
Next.js Frontend (localhost:3000)
    ↓ HTTPS
FastAPI Backend (localhost:8000)
    ↓ SQLAlchemy Async
MySQL Database (localhost:3306)
```

**Authentication Flow:**
1. Next.js sends credentials to FastAPI `/api/auth/login`
2. FastAPI validates with database, returns JWT token
3. Next.js stores token in httpOnly cookie or localStorage
4. All subsequent requests include JWT in Authorization header
5. FastAPI middleware validates JWT on protected routes

**File Upload Flow:**
1. User drags file to Next.js dropzone
2. Next.js validates client-side (size, type)
3. Next.js sends to FastAPI `/api/upload` via FormData
4. FastAPI validates server-side (5,000 rows, format)
5. FastAPI processes with pandas, stores in MySQL
6. Returns job ID to Next.js
7. WebSocket updates progress to frontend

**Clustering Flow:**
1. User selects K value in Next.js
2. Next.js sends request to FastAPI `/api/cluster`
3. FastAPI loads data, executes KMeans++ with scikit-learn
4. WebSocket sends progress (0-100%) to Next.js
5. FastAPI stores results, returns to Next.js
6. Next.js visualizes with Recharts

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| ML Library | scikit-learn | PyTorch/TensorFlow | Overkill for KMeans, steeper learning curve |
| Database | MySQL | PostgreSQL | Both excellent, MySQL specified in project requirements |
| ORM | SQLAlchemy | Django ORM | FastAPI doesn't require Django, SQLAlchemy is framework-agnostic |
| Charts | Recharts | Chart.js | Recharts has better TypeScript and React integration |
| Auth | JWT + passlib | OAuth2/OIDC | MVP doesn't need external providers, simpler to implement |
| File Upload | python-multipart | Django Storage | Not using Django, FastAPI has built-in multipart support |
| Progress | WebSocket | Server-Sent Events | WebSocket is bidirectional, better for interactive updates |

## Docker Configuration

### docker-compose.yml Structure

```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on: [backend]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=mysql+aiomysql://user:pass@db:3306/kmeans
      - JWT_SECRET=${JWT_SECRET}
    depends_on: [db]
    volumes:
      - ./uploads:/app/uploads

  db:
    image: mysql:8.0
    ports: ["3306:3306"]
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
      - MYSQL_DATABASE=kmeans
    volumes:
      - mysql_data:/var/lib/mysql

  nginx:
    image: nginx:1.25
    ports: ["443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on: [frontend, backend]

volumes:
  mysql_data:
```

## Installation

### Python Backend

```bash
# Core ML and data processing
pip install pandas==2.2.2
pip install numpy==2.0.0
pip install scikit-learn==1.5.0
pip install openpyxl==3.1.2

# Database
pip install sqlalchemy==2.0.30
pip install aiomysql==0.2.0
pip install pymysql==1.1.0
pip install alembic==1.13.1

# FastAPI and web
pip install fastapi==0.115.0
pip install uvicorn[standard]==0.30.0
pip install python-multipart==0.0.9
pip install httpx==0.27.0
pip install websockets==12.0

# Authentication and security
pip install passlib==1.7.4
pip install bcrypt==4.2.0
pip install PyJWT==2.8.0
pip install python-jose[cryptography]==3.3.0

# Utilities
pip install python-dotenv==1.0.1
pip install pydantic==2.7.1
pip install pydantic-settings==2.2.1
pip install chardet==5.2.0
pip install xlsxwriter==3.1.9

# Testing (optional)
pip install pytest==8.1.1
pip install pytest-asyncio==0.23.5
```

### Next.js Frontend

```bash
# Core
npm install next@15 react@18 react-dom@18 typescript@5

# Data visualization
npm install recharts@2.12 d3-scale@4

# UI and design
npm install @radix-ui/react-*@latest
npm install lucide-react@0.400.0
npm install tailwindcss@3
npm install clsx@2.1.0
npm install tailwind-merge@2.2.0

# Data fetching and forms
npm install @tanstack/react-query@5
npm install axios@1.6.7
npm install react-hook-form@7.51.0
npm install zod@3.22.4
npm install react-dropzone@14.2.3

# WebSocket
npm install socket.io-client@4

# Utilities
npm install date-fns@3.3.0
```

## Dependencies to Avoid

### Don't Add
| Library | Why Avoid |
|---------|-----------|
| Django | Not using Django framework, FastAPI is async-first |
| Flask | FastAPI is modern async replacement |
| Requests | Use httpx for async compatibility |
| TensorFlow/PyTorch | Overkill for KMeans, unnecessary bloat |
| Chart.js | Recharts has better React/TypeScript support |
| Redux | Not needed for MVP, React Query handles state |
| MongoDB | Project requires MySQL for relational data |

### Defer to v2
| Library | Why Defer |
|---------|-----------|
| Celery + Redis | Background jobs not needed for MVP clustering |
| Stripe SDK | Payment integration deferred |
| Socket.IO Server | WebSocket built into FastAPI |
| PostgreSQL | MySQL is project requirement |
| GraphQL | REST is sufficient for MVP |

## Compatibility Considerations

### React ↔ Python Communication
- **JSON serialization:** FastAPI's Pydantic models match React interfaces via TypeScript
- **Date handling:** ISO 8601 strings in JSON, parsed with date-fns in React
- **File uploads:** FormData from React, parsed with python-multipart in FastAPI
- **Error handling:** HTTP status codes + JSON response body on both sides
- **CORS:** FastAPI CORS middleware configured for Next.js origin

### Database Schema Considerations
- **User isolation:** All tables require `user_id` foreign key
- **Cascade delete:** `ON DELETE CASCADE` for data cleanup
- **Right to forget:** User deletion must cascade to all user data
- **Timestamps:** UTC timezone for all datetime fields
- **Soft delete:** Optional `deleted_at` for audit trail

### Performance Considerations
- **5,000 row limit:** Fits comfortably in memory for KMeans clustering
- **Batch processing:** Process in chunks if needed for larger datasets
- **Connection pooling:** SQLAlchemy async pool for database efficiency
- **Caching:** React Query for frontend, consider Redis for backend in v2
- **WebSocket overhead:** Only during clustering operation, minimal impact

## Security Configuration

### Password Hashing
```python
# FastAPI backend
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(plain_password)
```

### JWT Configuration
```python
# FastAPI backend
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### HTTPS Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:3000;
    }
}
```

## Version Compatibility Matrix

| Component | Min Version | Recommended | Tested Together |
|-----------|-------------|-------------|-----------------|
| Python | 3.10+ | 3.12 | ✅ |
| Node.js | 18+ | 20 LTS | ✅ |
| Next.js | 14+ | 15 | ✅ |
| FastAPI | 0.100+ | 0.115 | ✅ |
| MySQL | 8.0+ | 8.0 | ✅ |
| Docker | 20+ | 24 | ✅ |

## Sources

**Confidence Level:** MEDIUM (unable to verify with live sources due to tool limitations. Versions and recommendations based on training data up to August 2025. Recommend verifying with official documentation before implementation.)

### Official Documentation (to verify)
- scikit-learn: https://scikit-learn.org/
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- pandas: https://pandas.pydata.org/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Recharts: https://recharts.org/

### Recommended Verification Before Implementation
1. Check latest stable versions on PyPI and npm
2. Verify compatibility matrix with official docs
3. Test Docker multi-container setup locally
4. Validate WebSocket connection between Next.js and FastAPI
5. Confirm JWT implementation matches current best practices
