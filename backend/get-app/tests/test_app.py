import platform
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app


def test_health():
    resp = app.test_client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


@pytest.mark.skipif(platform.system() != "Linux", reason="needs Linux ps")
def test_get_procs():
    resp = app.test_client().get("/getProcs")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)