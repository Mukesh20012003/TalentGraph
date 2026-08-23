import logging
from contextlib import contextmanager
from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError
from app.config import settings

logger = logging.getLogger("talent_graph.db")

class Database:
    def __init__(self):
        self._driver: Driver | None = None

    def connect(self):
        """Initializes and verifies the Neo4j driver connection."""
        if not settings.COGNODB_URI or not settings.COGNODB_PASSWORD:
            logger.warning("⚠️ COGNODB credentials not fully set.")
            return

        try:
            self._driver = GraphDatabase.driver(
                settings.COGNODB_URI,
                auth=(settings.COGNODB_USER, settings.COGNODB_PASSWORD),
                max_connection_lifetime=30 * 60,
                max_connection_pool_size=50,
                connection_acquisition_timeout=10.0,
            )
            self._driver.verify_connectivity()
            logger.info("✅ Connected to CognoDB successfully.")
        except AuthError as e:
            logger.error(f"❌ CognoDB Authentication failed: {e}")
            self._driver = None
        except ServiceUnavailable as e:
            logger.error(f"❌ CognoDB is unreachable at {settings.COGNODB_URI}: {e}")
            self._driver = None
        except Exception as e:
            logger.error(f"❌ Unexpected DB connection error: {e}")
            self._driver = None

    def close(self):
        """Closes driver connection pool."""
        if self._driver:
            self._driver.close()
            logger.info("Database driver connection closed.")

    def is_connected(self) -> bool:
        """Returns True if the database is currently reachable."""
        if not self._driver:
            return False
        try:
            self._driver.verify_connectivity()
            return True
        except Exception:
            return False

    @contextmanager
    def get_session(self, database: str | None = None):
        """Context manager yielding a Neo4j session with error handling."""
        if not self._driver:
            raise ServiceUnavailable("Database driver is not initialized or unreachable.")
        session: Session = self._driver.session(database=database)
        try:
            yield session
        finally:
            session.close()

db = Database()