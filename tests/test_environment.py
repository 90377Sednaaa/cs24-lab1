"""
CS24/L Juice Shop Lab - environment smoke test (optional).

This checks that the Juice Shop target is actually up on port 3000, so you can
verify your setup before starting. It is SEPARATE from the submission grader
(test_findings.py) and is NOT run by the auto-grading GitHub Action - the grader
must work without Docker.

Run it yourself AFTER `docker compose up -d` (give Juice Shop ~30-60s to boot):

    pytest tests/test_environment.py -q

If it passes, your lab environment is ready.
"""
import urllib.request
import urllib.error

import pytest

URL = "http://localhost:3000"


def test_juice_shop_is_up():
    try:
        with urllib.request.urlopen(URL, timeout=5) as resp:
            status = resp.status
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        pytest.skip(
            f"Juice Shop not reachable at {URL} ({e}). "
            f"Run 'docker compose up -d' and wait ~30-60s for it to boot, "
            f"then try again."
        )
    assert status == 200, f"Expected HTTP 200 from Juice Shop, got {status}."
