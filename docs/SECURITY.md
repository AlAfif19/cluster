# Security Documentation

## User Data Isolation

### Principle
Each user's data is logically isolated from other users in the database. This is enforced at the application layer.

### Implementation
1. **Database Schema**: All user-specific tables include `user_id` foreign key
2. **Query Filtering**: All queries filter by `user_id` from authenticated user
3. **Ownership Validation**: Endpoints validate ownership before returning/modifying data
4. **Dependency Injection**: Use `require_user_ownership` dependency for automatic validation

### Patterns

#### Filter Pattern
```python
@router.get("/projects")
def get_user_projects(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Always filter by current_user.id
    return db.query(Project).filter(Project.user_id == current_user.id).all()
```

#### Ownership Validation
```python
@router.get("/projects/{project_id}")
def get_project(
    project_id: str,
    current_user: User = Depends(require_user_ownership(project_id)),
    db: Session = Depends(get_db)
):
    return db.query(Project).filter(Project.id == project_id).first()
```

See `backend/app/core/isolation.py` for complete patterns.

## Authentication

### Password Security
- Passwords hashed with bcrypt
- Minimum 8 characters
- No plain text storage

### Session Management
- JWT tokens for authentication
- Token expiration: 30 minutes (development), 15 minutes (production)
- Token blacklist for logout
- httpOnly cookies recommended for production (v2)

## Token Storage

### Current Implementation (v1)
- Tokens stored in localStorage
- Client-side logout clears token
- Server-side token blacklist

### Production Recommendation (v2+)
- Use httpOnly cookies for token storage
- Secure flag: true
- SameSite: strict
- CSRF protection for form submissions

## Data Security

- All user data isolated by user_id
- Server-side validation for all inputs
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via React and FastAPI defaults

## Compliance

- GDPR: Data isolation enables right to be forgotten
- SOC 2: Audit logging recommended (v2)
- HIPAA: Not applicable (not healthcare data)