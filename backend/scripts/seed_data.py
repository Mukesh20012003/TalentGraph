import os
import sys
import random
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load env variables
load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER", "cognodb")
PASSWORD = os.getenv("COGNODB_PASSWORD")

if not URI or not PASSWORD:
    print("❌ Error: COGNODB_URI or COGNODB_PASSWORD not found in environment.")
    sys.exit(1)

# -------------------------------------------------------------
# 1. Curated Realistic Data Definition
# -------------------------------------------------------------

SKILLS = [
    # AI / ML
    {"name": "PyTorch", "category": "AI/ML"},
    {"name": "LangChain", "category": "AI/ML"},
    {"name": "LlamaIndex", "category": "AI/ML"},
    {"name": "Hugging Face", "category": "AI/ML"},
    {"name": "TensorFlow", "category": "AI/ML"},
    {"name": "vLLM", "category": "AI/ML"},
    {"name": "Ray", "category": "AI/ML"},
    {"name": "RAG Systems", "category": "AI/ML"},
    # Languages
    {"name": "Python", "category": "Language"},
    {"name": "Rust", "category": "Language"},
    {"name": "TypeScript", "category": "Language"},
    {"name": "Go", "category": "Language"},
    {"name": "C++", "category": "Language"},
    {"name": "SQL", "category": "Language"},
    # Databases & Graphs
    {"name": "CognoDB", "category": "Database"},
    {"name": "Neo4j", "category": "Database"},
    {"name": "PostgreSQL", "category": "Database"},
    {"name": "Redis", "category": "Database"},
    {"name": "Qdrant", "category": "Database"},
    {"name": "Milvus", "category": "Database"},
    # Cloud & Infra
    {"name": "Kubernetes", "category": "Cloud/Infra"},
    {"name": "Docker", "category": "Cloud/Infra"},
    {"name": "AWS", "category": "Cloud/Infra"},
    {"name": "GCP", "category": "Cloud/Infra"},
    {"name": "Terraform", "category": "Cloud/Infra"},
    {"name": "Kafka", "category": "Cloud/Infra"},
    # Frontend & Frameworks
    {"name": "React", "category": "Frontend"},
    {"name": "Next.js", "category": "Frontend"},
    {"name": "FastAPI", "category": "Backend"},
    {"name": "GraphQL", "category": "Backend"},
    {"name": "gRPC", "category": "Backend"},
    {"name": "Tailwind CSS", "category": "Frontend"},
]

COMPANIES = [
    {"name": "Wexa AI", "industry": "AI/ML", "size": "Startup", "location": "San Francisco, CA"},
    {"name": "Anthropic", "industry": "AI/ML", "size": "Scaleup", "location": "San Francisco, CA"},
    {"name": "OpenAI", "industry": "AI/ML", "size": "Enterprise", "location": "San Francisco, CA"},
    {"name": "Stripe", "industry": "Fintech", "size": "Enterprise", "location": "South San Francisco, CA"},
    {"name": "Databricks", "industry": "Data/AI", "size": "Enterprise", "location": "San Francisco, CA"},
    {"name": "Scale AI", "industry": "AI/ML", "size": "Scaleup", "location": "San Francisco, CA"},
    {"name": "Figma", "industry": "Design/SaaS", "size": "Scaleup", "location": "San Francisco, CA"},
    {"name": "Cohere", "industry": "AI/ML", "size": "Scaleup", "location": "Toronto, Canada"},
    {"name": "Vercel", "industry": "DevTools", "size": "Scaleup", "location": "Remote"},
    {"name": "Supabase", "industry": "DevTools", "size": "Startup", "location": "Remote"},
    {"name": "Snowflake", "industry": "Data/Cloud", "size": "Enterprise", "location": "Bozeman, MT"},
    {"name": "DeepMind", "industry": "AI Research", "size": "Enterprise", "location": "London, UK"},
    {"name": "Mistral AI", "industry": "AI/ML", "size": "Startup", "location": "Paris, France"},
    {"name": "Hugging Face", "industry": "AI/ML", "size": "Scaleup", "location": "New York, NY"},
    {"name": "Linear", "industry": "Productivity", "size": "Startup", "location": "Remote"},
    {"name": "Pinecone", "industry": "Database/AI", "size": "Startup", "location": "New York, NY"},
]

PROJECTS = [
    {"name": "Agentic RAG Engine", "description": "Autonomous multi-agent orchestration framework for hybrid retrieval", "status": "Active"},
    {"name": "Distributed Vector Indexer", "description": "High-throughput HNSW index clustering in Rust", "status": "Active"},
    {"name": "Graph-Augmented LLM Search", "description": "Knowledge graph semantic layer for contextual query rewriting", "status": "Active"},
    {"name": "Sub-millisecond Model Gateway", "description": "gRPC inference proxy with speculative decoding caching", "status": "Completed"},
    {"name": "Autonomous Code Reviewer", "description": "AST-aware multi-file diff reasoning agent", "status": "Active"},
    {"name": "Real-time Telemetry Pipeline", "description": "Distributed log streaming over Kafka and ClickHouse", "status": "Completed"},
    {"name": "Synthetic Data Synthesizer", "description": "Diffusion-based tabular and graph data generator for privacy", "status": "Active"},
    {"name": "Cloud-Native Observability Mesh", "description": "eBPF zero-instrumentation metric collector", "status": "Active"},
    {"name": "Multi-Modal Embedding Pipeline", "description": "Unified text-vision-audio vectorization backend", "status": "Completed"},
    {"name": "Enterprise Graph Sync", "description": "CDC connector syncing Postgres write streams to CognoDB", "status": "Active"},
    {"name": "Edge AI Inference Runtime", "description": "Quantized INT4 ONNX runtime optimized for Apple Silicon", "status": "Completed"},
    {"name": "Collaborative Canvas UI", "description": "Real-time CRDT-backed interactive workflow editor", "status": "Active"},
    {"name": "Federated Learning Hub", "description": "Privacy-preserving model aggregator with differential privacy", "status": "Archived"},
    {"name": "Zero-Trust Service Mesh", "description": "Mutual TLS identity proxy for microservices", "status": "Completed"},
    {"name": "AI Evaluation Benchmarker", "description": "Automated hallucination and bias test runner for LLMs", "status": "Active"},
]

NAMES = [
    ("Aria Chen", "Principal AI Architect", "San Francisco, CA", 10),
    ("Marcus Vance", "Staff Rust Systems Engineer", "Seattle, WA", 8),
    ("Elena Rostova", "Senior ML Infrastructure Engineer", "New York, NY", 7),
    ("Kaito Tanaka", "Lead Graph Database Researcher", "Tokyo, Japan", 9),
    ("Sarah Jenkins", "Fullstack AI Engineer", "Austin, TX", 5),
    ("Devon Brooks", "Distributed Systems Engineer", "San Francisco, CA", 6),
    ("Priya Sharma", "Director of Machine Learning", "San Francisco, CA", 12),
    ("Mateo Alvarez", "Backend Platform Engineer", "Remote", 4),
    ("Chloe Dupont", "AI Research Scientist", "Paris, France", 8),
    ("Liam O'Connor", "DevOps & Cloud Architect", "London, UK", 11),
    ("Zhenya Petrov", "High Performance Computing Lead", "Berlin, Germany", 10),
    ("Ananya Patel", "Staff Prompt Engineer & Evaluator", "Bengaluru, India", 6),
    ("Lucas Silva", "Senior Frontend Engineer", "Remote", 5),
    ("Maya Lin", "Applied AI Specialist", "San Francisco, CA", 4),
    ("Gabriel Santos", "Database Internals Engineer", "Remote", 7),
    ("Nora Al-Mansoor", "VP of Engineering", "New York, NY", 14),
    ("Jonas Becker", "Systems Programmer", "Munich, Germany", 6),
    ("Tara Campbell", "Machine Learning Platform Engineer", "Seattle, WA", 5),
    ("Kenji Sato", "Senior Vector Search Engineer", "Tokyo, Japan", 8),
    ("Fatima Zahra", "Senior Data Engineer", "Toronto, Canada", 7),
    ("David Kim", "Principal Security Engineer", "San Francisco, CA", 11),
    ("Olivia Taylor", "Product-Focused AI Engineer", "New York, NY", 5),
    ("Samir Qureshi", "Compiler & Kernel Engineer", "Austin, TX", 9),
    ("Isabella Rossi", "Graph Analytics Lead", "Milan, Italy", 8),
    ("Alexander Wright", "MLOps Engineer", "London, UK", 6),
    ("Grace Hopper-Li", "Chief Scientist", "San Francisco, CA", 15),
    ("Ethan Hunt", "Site Reliability Engineer", "Remote", 7),
    ("Yuki Takahashi", "Frontier Model Researcher", "Tokyo, Japan", 6),
    ("Camila Fernandez", "Fullstack Developer", "Buenos Aires, Argentina", 4),
    ("Victor Vance", "Low Latency Engineer", "Chicago, IL", 10),
    ("Hannah Abbott", "NLP Specialist", "Boston, MA", 5),
    ("Felix Mueller", "Cloud Native Architect", "Zurich, Switzerland", 9),
    ("Siddharth Menon", "AI Workflow Orchestration Lead", "Bengaluru, India", 7),
    ("Rachel Green", "Technical Product Manager", "San Francisco, CA", 8),
    ("Tariq Al-Fassi", "Distributed Data Engineer", "Dubai, UAE", 6),
    ("Megan Ross", "Frontend Engineer", "New York, NY", 4),
    ("Arjun Reddy", "Principal Distributed Systems Engineer", "San Francisco, CA", 11),
    ("Sophie Martin", "Computer Vision Scientist", "Paris, France", 7),
    ("Hassan El-Sayed", "Platform Engineer", "Cairo, Egypt", 5),
    ("Zoe Kravitz-Lin", "Senior AI Applications Engineer", "San Francisco, CA", 6),
]

# -------------------------------------------------------------
# 2. Ingestion Execution
# -------------------------------------------------------------

def seed_database():
    print(f"Connecting to CognoDB instance: {URI}")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    random.seed(42)

    with driver.session() as session:
        print("\n🧹 Step 1: Cleaning previous data...")
        session.run("MATCH (n) DETACH DELETE n")

        print("⚡ Step 2: Creating uniqueness constraints and indexes...")
        constraints = [
            "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT project_name IF NOT EXISTS FOR (pr:Project) REQUIRE pr.name IS UNIQUE",
        ]
        for query in constraints:
            try:
                session.run(query)
            except Exception as e:
                print(f"  Note on constraint: {e}")

        # 1. Insert Skills
        print("🛠️ Step 3: Loading Skills...")
        session.run("""
            UNWIND $skills AS s
            CREATE (:Skill {name: s.name, category: s.category})
        """, {"skills": SKILLS})

        # 2. Insert Companies
        print("🏢 Step 4: Loading Companies...")
        session.run("""
            UNWIND $companies AS c
            CREATE (:Company {name: c.name, industry: c.industry, size: c.size, location: c.location})
        """, {"companies": COMPANIES})

        # 3. Insert Projects
        print("📁 Step 5: Loading Projects...")
        session.run("""
            UNWIND $projects AS pr
            CREATE (:Project {name: pr.name, description: pr.description, status: pr.status})
        """, {"projects": PROJECTS})

        # 4. Insert Persons
        print("👤 Step 6: Loading Persons...")
        persons_payload = []
        for name, title, loc, exp in NAMES:
            clean_name = name.lower().replace(" ", ".").replace("'", "")
            email = clean_name + "@example.com"
            persons_payload.append({
                "name": name,
                "title": title,
                "location": loc,
                "years_experience": exp,
                "email": email
            })

        session.run("""
            UNWIND $persons AS p
            CREATE (:Person {
                name: p.name,
                title: p.title,
                location: p.location,
                years_experience: p.years_experience,
                email: p.email
            })
        """, {"persons": persons_payload})

        # -------------------------------------------------------------
        # Relationship Generation
        # -------------------------------------------------------------
        print("🔗 Step 7: Generating Graph Relationships...")

        skill_names = [s["name"] for s in SKILLS]
        company_names = [c["name"] for c in COMPANIES]
        project_names = [pr["name"] for pr in PROJECTS]

        # A. Project USES Skill
        project_skills_payload = []
        for pr_name in project_names:
            chosen_skills = random.sample(skill_names, random.randint(3, 6))
            for sk in chosen_skills:
                project_skills_payload.append({"project": pr_name, "skill": sk})

        session.run("""
            UNWIND $pairs AS pair
            MATCH (pr:Project {name: pair.project})
            MATCH (s:Skill {name: pair.skill})
            MERGE (pr)-[:USES]->(s)
        """, {"pairs": project_skills_payload})

        # B. Person HAS_SKILL
        proficiency_levels = ["Expert", "Proficient", "Familiar"]
        person_skills_payload = []
        for p in persons_payload:
            count = random.randint(4, 8)
            skills = random.sample(skill_names, count)
            for i, sk in enumerate(skills):
                level = "Expert" if i < 2 else random.choice(proficiency_levels)
                person_skills_payload.append({
                    "person": p["name"],
                    "skill": sk,
                    "level": level
                })

        session.run("""
            UNWIND $pairs AS pair
            MATCH (p:Person {name: pair.person})
            MATCH (s:Skill {name: pair.skill})
            MERGE (p)-[:HAS_SKILL {level: pair.level}]->(s)
        """, {"pairs": person_skills_payload})

        # C. Person WORKED_AT Company
        person_companies_payload = []
        for p in persons_payload:
            num_jobs = random.randint(1, 3)
            comps = random.sample(company_names, num_jobs)
            for i, comp in enumerate(comps):
                start = 2024 - (p["years_experience"] - (i * 2))
                end = 2024 if i == 0 else start + random.randint(1, 3)
                person_companies_payload.append({
                    "person": p["name"],
                    "company": comp,
                    "role": p["title"],
                    "start_year": max(2012, start),
                    "end_year": end
                })

        session.run("""
            UNWIND $pairs AS pair
            MATCH (p:Person {name: pair.person})
            MATCH (c:Company {name: pair.company})
            MERGE (p)-[:WORKED_AT {
                role: pair.role,
                start_year: pair.start_year,
                end_year: pair.end_year
            }]->(c)
        """, {"pairs": person_companies_payload})

        # D. Person BUILT Project
        person_projects_payload = []
        for p in persons_payload:
            projs = random.sample(project_names, random.randint(1, 2))
            for pr in projs:
                roles = ["Core Architect", "Lead Developer", "Contributor", "Maintainer"]
                person_projects_payload.append({
                    "person": p["name"],
                    "project": pr,
                    "role": random.choice(roles)
                })

        session.run("""
            UNWIND $pairs AS pair
            MATCH (p:Person {name: pair.person})
            MATCH (pr:Project {name: pair.project})
            MERGE (p)-[:BUILT {role: pair.role}]->(pr)
        """, {"pairs": person_projects_payload})

        # E. Person KNOWS Person
        # 1) Overlapping colleagues
        session.run("""
            MATCH (p1:Person)-[w1:WORKED_AT]->(c:Company)<-[w2:WORKED_AT]-(p2:Person)
            WHERE id(p1) < id(p2)
              AND w1.start_year <= w2.end_year
              AND w2.start_year <= w1.end_year
            MERGE (p1)-[:KNOWS {
                since_year: CASE WHEN w1.start_year > w2.start_year THEN w1.start_year ELSE w2.start_year END,
                context: "Ex-Colleagues at " + c.name
            }]->(p2)
        """)

        # 2) Project co-contributors
        session.run("""
            MATCH (p1:Person)-[:BUILT]->(pr:Project)<-[:BUILT]-(p2:Person)
            WHERE id(p1) < id(p2)
            MERGE (p1)-[:KNOWS {
                since_year: 2023,
                context: "Collaborated on " + pr.name
            }]->(p2)
        """)

        # Summary of loaded data
        p_count = session.run("MATCH (p:Person) RETURN count(p) AS c").single()["c"]
        s_count = session.run("MATCH (s:Skill) RETURN count(s) AS c").single()["c"]
        c_count = session.run("MATCH (c:Company) RETURN count(c) AS c").single()["c"]
        pr_count = session.run("MATCH (pr:Project) RETURN count(pr) AS c").single()["c"]
        rel_count = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]

        print("\n" + "="*50)
        print("🎉 GRAPH SEEDING COMPLETE!")
        print("="*50)
        print(f"👤 Persons:        {p_count}")
        print(f"🛠️ Skills:         {s_count}")
        print(f"🏢 Companies:      {c_count}")
        print(f"📁 Projects:       {pr_count}")
        print(f"🔗 Relationships:  {rel_count}")
        print("="*50)

    driver.close()

if __name__ == "__main__":
    seed_database()