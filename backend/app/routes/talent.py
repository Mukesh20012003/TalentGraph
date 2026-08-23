from fastapi import APIRouter, HTTPException, Query
from app.db import db
from typing import Optional

router = APIRouter(prefix="/api/talent", tags=["Talent & Graph Queries"])

@router.get("/search")
def search_talent(
    skill: Optional[str] = Query(None, description="Filter by skill name (e.g. 'Rust', 'PyTorch')"),
    company: Optional[str] = Query(None, description="Filter by company worked at (e.g. 'OpenAI', 'Wexa AI')"),
    min_experience: int = Query(0, description="Minimum years of experience"),
    limit: int = Query(20, le=50)
):
    """
    Searches for talent filtered by skill, past company, and experience.
    Returns candidate profile along with their skills and career history.
    """
    cypher = """
        MATCH (p:Person)
        WHERE p.years_experience >= $min_experience
          AND ($skill IS NULL OR EXISTS {
              MATCH (p)-[:HAS_SKILL]->(s:Skill)
              WHERE toLower(s.name) = toLower($skill)
          })
          AND ($company IS NULL OR EXISTS {
              MATCH (p)-[:WORKED_AT]->(c:Company)
              WHERE toLower(c.name) = toLower($company)
          })
        OPTIONAL MATCH (p)-[hs:HAS_SKILL]->(s:Skill)
        OPTIONAL MATCH (p)-[w:WORKED_AT]->(c:Company)
        RETURN p.name AS name,
               p.title AS title,
               p.location AS location,
               p.years_experience AS years_experience,
               p.email AS email,
               collect(DISTINCT {name: s.name, level: hs.level, category: s.category}) AS skills,
               collect(DISTINCT {name: c.name, role: w.role, start: w.start_year, end: w.end_year}) AS companies
        ORDER BY p.years_experience DESC
        LIMIT $limit
    """
    
    with db.get_session() as session:
        result = session.run(cypher, {
            "skill": skill,
            "company": company,
            "min_experience": min_experience,
            "limit": limit
        })
        records = [record.data() for record in result]
    return {"count": len(records), "results": records}


@router.get("/warm-introductions")
def get_warm_introductions(
    referrer: str = Query(..., description="Name of the person requesting introductions (e.g. 'Aria Chen')"),
    target_skill: str = Query(..., description="Skill needed (e.g. 'Rust', 'RAG Systems')"),
    max_hops: int = Query(2, ge=1, le=3, description="Maximum degrees of separation")
):
    """
    MULTI-HOP GRAPH TRAVERSAL (Requirement 5.1):
    Finds candidates who have target_skill and are 1 to 2 hops away in the network from the referrer.
    Returns the exact connection path (e.g. Aria Chen -> Marcus Vance -> Target Candidate).
    """
    cypher = """
        MATCH (me:Person)
        WHERE toLower(me.name) = toLower($referrer)
        
        MATCH path = (me)-[:KNOWS*1..2]-(candidate:Person)-[hs:HAS_SKILL]->(s:Skill)
        WHERE me <> candidate
          AND toLower(s.name) = toLower($target_skill)
        
        WITH candidate, hs, s, path, length(path) AS degree
        ORDER BY degree ASC, candidate.years_experience DESC
        
        RETURN candidate.name AS candidate_name,
               candidate.title AS title,
               candidate.location AS location,
               candidate.years_experience AS years_experience,
               candidate.email AS email,
               hs.level AS skill_level,
               s.name AS matched_skill,
               degree AS degrees_of_separation,
               [n IN nodes(path) | n.name] AS connection_path
        LIMIT 25
    """

    with db.get_session() as session:
        result = session.run(cypher, {
            "referrer": referrer,
            "target_skill": target_skill
        })
        records = [record.data() for record in result]

    # Group or de-duplicate candidates while keeping shortest path
    unique_candidates = {}
    for r in records:
        cname = r["candidate_name"]
        if cname not in unique_candidates:
            unique_candidates[cname] = r

    return {
        "referrer": referrer,
        "target_skill": target_skill,
        "total_matches": len(unique_candidates),
        "candidates": list(unique_candidates.values())
    }


@router.get("/project-matchmaker")
def match_team_for_project(
    project_name: str = Query(..., description="Target Project (e.g. 'Agentic RAG Engine')")
):
    """
    AWKWARD IN SQL QUERY (Requirement 5.1):
    Matches candidates to a project based on overlapping skills,
    calculates compatibility percentage, AND reveals if the candidate
    has previously worked with existing project contributors.
    """
    cypher = """
        MATCH (proj:Project)
        WHERE toLower(proj.name) = toLower($project_name)
        MATCH (proj)-[:USES]->(reqSkill:Skill)
        WITH proj, collect(reqSkill) AS requiredSkills, count(reqSkill) AS totalSkillsRequired
        
        MATCH (candidate:Person)-[hs:HAS_SKILL]->(matchingSkill:Skill)
        WHERE matchingSkill IN requiredSkills
        
        WITH proj, candidate, totalSkillsRequired, 
             count(matchingSkill) AS matchCount, 
             collect({skill: matchingSkill.name, level: hs.level}) AS matchedSkills
        
        // Find if candidate knows anyone who built this project
        OPTIONAL MATCH (candidate)-[:KNOWS]-(colleague:Person)-[:BUILT]->(proj)
        
        RETURN candidate.name AS name,
               candidate.title AS title,
               candidate.location AS location,
               candidate.years_experience AS years_experience,
               candidate.email AS email,
               matchCount,
               totalSkillsRequired,
               round((toFloat(matchCount) / totalSkillsRequired) * 100) AS match_percentage,
               matchedSkills,
               collect(DISTINCT colleague.name) AS team_connections
        ORDER BY matchCount DESC, size(team_connections) DESC, candidate.years_experience DESC
        LIMIT 20
    """

    with db.get_session() as session:
        result = session.run(cypher, {"project_name": project_name})
        records = [record.data() for record in result]

    return {
        "project": project_name,
        "total_evaluated": len(records),
        "top_candidates": records
    }


@router.get("/alumni-network")
def company_alumni_network(
    company_name: str = Query(..., description="Company name (e.g. 'OpenAI', 'Anthropic')")
):
    """
    Explores the alumni diaspora of a company: what skills they carry and where they moved.
    """
    cypher = """
        MATCH (c:Company)
        WHERE toLower(c.name) = toLower($company_name)
        MATCH (p:Person)-[w:WORKED_AT]->(c)
        OPTIONAL MATCH (p)-[hs:HAS_SKILL]->(s:Skill)
        OPTIONAL MATCH (p)-[w2:WORKED_AT]->(other:Company) WHERE other <> c
        RETURN p.name AS name,
               p.title AS title,
               w.role AS role_at_company,
               w.start_year AS start_year,
               w.end_year AS end_year,
               collect(DISTINCT s.name)[0..5] AS top_skills,
               collect(DISTINCT other.name) AS other_companies
        ORDER BY w.end_year DESC, p.years_experience DESC
        LIMIT 25
    """

    with db.get_session() as session:
        result = session.run(cypher, {"company_name": company_name})
        records = [record.data() for record in result]

    return {
        "company": company_name,
        "alumni_count": len(records),
        "alumni": records
    }