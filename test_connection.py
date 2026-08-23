import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER", "cognodb")
PASSWORD = os.getenv("COGNODB_PASSWORD")

def test_conn():
    print(f"Connecting to {URI}...")
    with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            result = session.run("RETURN 'CognoDB connection successful!' AS message, datetime() AS time")
            record = result.single()
            print(f"✅ Success: {record['message']}")
            print(f"🕒 Server Time: {record['time']}")

def create_constraints():
    with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
        with driver.session() as session:
            constraints = [
                "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
                "CREATE CONSTRAINT company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT project_name IF NOT EXISTS FOR (pr:Project) REQUIRE pr.name IS UNIQUE",
            ]
            for c in constraints:
                session.run(c)
            print("✅ Constraints created successfully!")       

if __name__ == "__main__":
    test_conn()
    create_constraints()