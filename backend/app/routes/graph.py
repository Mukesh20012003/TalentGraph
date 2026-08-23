from fastapi import APIRouter, Query
from app.db import db

router = APIRouter(prefix="/api/graph", tags=["Graph Visualizer & Subgraphs"])

@router.get("/snapshot")
def get_graph_snapshot(limit: int = Query(100, le=300)):
    """
    Returns nodes and edges formatted for D3/ForceGraph.
    """
    cypher = """
        MATCH (n)
        WITH n LIMIT $limit
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, labels(n) AS n_labels, r, type(r) AS rel_type, m, labels(m) AS m_labels
    """
    nodes_map = {}
    links = []

    with db.get_session() as session:
        result = session.run(cypher, {"limit": limit})
        for record in result:
            n = record["n"]
            n_label = record["n_labels"][0] if record["n_labels"] else "Unknown"
            n_id = f"{n_label}:{n.get('name', id(n))}"

            if n_id not in nodes_map:
                nodes_map[n_id] = {
                    "id": n_id,
                    "name": n.get("name", "Unnamed"),
                    "group": n_label,
                    "properties": dict(n)
                }

            m = record["m"]
            r = record["r"]
            if m and r:
                m_label = record["m_labels"][0] if record["m_labels"] else "Unknown"
                m_id = f"{m_label}:{m.get('name', id(m))}"

                if m_id not in nodes_map:
                    nodes_map[m_id] = {
                        "id": m_id,
                        "name": m.get("name", "Unnamed"),
                        "group": m_label,
                        "properties": dict(m)
                    }

                links.append({
                    "source": n_id,
                    "target": m_id,
                    "type": record["rel_type"],
                    "properties": dict(r)
                })

    return {
        "nodes": list(nodes_map.values()),
        "links": links
    }


@router.get("/node-neighborhood")
def get_node_neighborhood(node_name: str = Query(..., description="Node name to explore")):
    """
    Fetches the 1-hop and 2-hop neighborhood surrounding a single node.
    """
    cypher = """
        MATCH (center)
        WHERE toLower(center.name) = toLower($node_name)
        OPTIONAL MATCH (center)-[r]-(neighbor)
        RETURN center, labels(center) AS center_labels,
               r, type(r) AS rel_type,
               neighbor, labels(neighbor) AS neighbor_labels
        LIMIT 60
    """
    nodes_map = {}
    links = []

    with db.get_session() as session:
        result = session.run(cypher, {"node_name": node_name})
        for record in result:
            c = record["center"]
            if not c:
                continue
            c_label = record["center_labels"][0] if record["center_labels"] else "Node"
            c_id = f"{c_label}:{c.get('name', id(c))}"

            if c_id not in nodes_map:
                nodes_map[c_id] = {
                    "id": c_id,
                    "name": c.get("name", "Unnamed"),
                    "group": c_label,
                    "isCenter": True,
                    "properties": dict(c)
                }

            n = record["neighbor"]
            r = record["r"]
            if n and r:
                n_label = record["neighbor_labels"][0] if record["neighbor_labels"] else "Node"
                n_id = f"{n_label}:{n.get('name', id(n))}"

                if n_id not in nodes_map:
                    nodes_map[n_id] = {
                        "id": n_id,
                        "name": n.get("name", "Unnamed"),
                        "group": n_label,
                        "isCenter": False,
                        "properties": dict(n)
                    }

                links.append({
                    "source": c_id,
                    "target": n_id,
                    "type": record["rel_type"],
                    "properties": dict(r)
                })

    return {
        "center": node_name,
        "nodes": list(nodes_map.values()),
        "links": links
    }


@router.get("/metadata")
def get_metadata():
    """
    Returns dropdown choices for persons, skills, companies, and projects.
    """
    cypher = """
        CALL { MATCH (p:Person) RETURN collect(p.name) AS persons }
        CALL { MATCH (s:Skill) RETURN collect(s.name) AS skills }
        CALL { MATCH (c:Company) RETURN collect(c.name) AS companies }
        CALL { MATCH (pr:Project) RETURN collect(pr.name) AS projects }
        RETURN persons, skills, companies, projects
    """
    with db.get_session() as session:
        result = session.run(cypher).single()
        return {
            "persons": sorted(result["persons"]) if result else [],
            "skills": sorted(result["skills"]) if result else [],
            "companies": sorted(result["companies"]) if result else [],
            "projects": sorted(result["projects"]) if result else []
        }