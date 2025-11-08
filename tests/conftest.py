import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # корень репозитория
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ruff: noqa: E402
import pytest

# ruff: noqa: E402
from task_app.Database.db import init


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init()
