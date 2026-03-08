"""
User Data Isolation Patterns

This module demonstrates how to enforce user data isolation in KMeans Engine.
All user-specific data must include user_id foreign key and be filtered by current user.

Usage Examples:

1. Filter queries by user_id:
    @router.get("/projects")
    def get_user_projects(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        projects = db.query(Project).filter(Project.user_id == current_user.id).all()
        return projects

2. Validate ownership for single resource access:
    @router.get("/projects/{project_id}")
    def get_project(
        project_id: str,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Validate ownership
        if project.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        return project

3. Use ownership dependency (recommended):
    @router.get("/projects/{project_id}")
    def get_project(
        project_id: str,
        current_user: User = Depends(require_user_ownership(project_id)),
        db: Session = Depends(get_db)
    ):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

4. Create resources with user_id:
    @router.post("/projects")
    def create_project(
        project_data: ProjectCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        project = Project(
            **project_data.dict(),
            user_id=current_user.id  # Always set user_id from current user
        )
        db.add(project)
        db.commit()
        return project

5. Update resources with ownership validation:
    @router.put("/projects/{project_id}")
    def update_project(
        project_id: str,
        project_update: ProjectUpdate,
        current_user: User = Depends(require_user_ownership(project_id)),
        db: Session = Depends(get_db)
    ):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Only owner can update (enforced by require_user_ownership)
        for field, value in project_update.dict(exclude_unset=True).items():
            setattr(project, field, value)

        db.commit()
        return project

6. Delete resources with ownership validation:
    @router.delete("/projects/{project_id}")
    def delete_project(
        project_id: str,
        current_user: User = Depends(require_user_ownership(project_id)),
        db: Session = Depends(get_db)
    ):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Only owner can delete (enforced by require_user_ownership)
        db.delete(project)
        db.commit()
        return {"message": "Project deleted"}
"""

from backend.app.core.deps import get_current_user, get_current_active_user
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def validate_user_ownership(resource_user_id: str, current_user_id: str) -> bool:
    """
    Validate that current_user_id owns the resource.

    Args:
        resource_user_id: The user_id of the resource being accessed
        current_user_id: The user_id of the authenticated user

    Returns:
        True if ownership is valid, False otherwise

    Raises:
        HTTPException with 403 status if ownership is invalid
    """
    if resource_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    return True

# Common isolation patterns for different resource types
ISOLATION_PATTERNS = {
    # Filter pattern: Always filter by user_id in queries
    "filter": "db.query(Model).filter(Model.user_id == current_user.id).all()",

    # Ownership validation: Check user_id before access
    "validate": "if resource.user_id != current_user.id: raise HTTPException(403)",

    # Create pattern: Always set user_id from current user
    "create": "Model(**data, user_id=current_user.id)",

    # Update pattern: Validate ownership before update
    "update": "require_user_ownership(resource_user_id) as dependency",

    # Delete pattern: Validate ownership before delete
    "delete": "require_user_ownership(resource_user_id) as dependency",
}