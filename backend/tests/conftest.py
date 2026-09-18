from collections.abc import Generator
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Finding, Resource


@pytest.fixture
def client(tmp_path) -> Generator[TestClient, None, None]:
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


@pytest.fixture
def finding_payload() -> dict[str, str]:
    return {
        "finding_id": "F-001",
        "resource_id": "sg-001",
        "resource_type": "Security Group",
        "title": "SSH is public",
        "severity": "HIGH",
        "category": "NETWORK_SECURITY",
        "rule_id": "CIS-SG-001",
        "status": "OPEN",
    }
