from fastapi import APIRouter, HTTPException, status
from app.db import db

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health")
def health_check():
    """Checks FastAPI server status and CognoDB connectivity."""
    db_ok = db.is_connected()
    
    if not db_ok:
        return {
            "status": "degraded",
            "backend": "online",
            "database": "unreachable",
            "message": "Backend is running, but cannot reach CognoDB instance."
        }

    # Fetch stats if connected
    try:
        with db.get_session() as session:
            result = session.run("""
                CALL {
                    MATCH (p:Person) RETURN count(p) AS persons
                }
                CALL {
                    MATCH (s:Skill) RETURN count(s) AS skills
                }
                CALL {
                    MATCH (c:Company) RETURN count(c) AS companies
                }
                CALL {
                    MATCH (pr:Project) RETURN count(pr) AS projects
                }
                RETURN persons, skills, companies, projects
            """).single()

            stats = {
                "persons": result["persons"] if result else 0,
                "skills": result["skills"] if result else 0,
                "companies": result["companies"] if result else 0,
                "projects": result["projects"] if result else 0
            }
    except Exception as e:
        stats = {"error": str(e)}

    return {
        "status": "healthy",
        "backend": "online",
        "database": "connected",
        "counts": stats
    }