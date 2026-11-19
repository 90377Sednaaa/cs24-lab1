"""
CS24/L Juice Shop Lab - automated submission checker.

This validates that a student's submission is COMPLETE and WELL-FORMED.
It does NOT prove the app was actually exploited - screenshots + instructor
spot-check do that. Run locally with:  pytest -q
"""
import csv
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "findings.csv")
SHOTS_DIR = os.path.join(ROOT, "screenshots")

REQUIRED_IDS = ["JUICE-001", "JUICE-002", "JUICE-003", "JUICE-004"]

REQUIRED_COLUMNS = [
    "finding_id", "title", "vuln_type", "url_or_endpoint", "severity",
    "owasp", "mitre_attack", "payload_used", "impact", "remediation",
    "screenshot",
]

ALLOWED_VULN_TYPES = {"SQL Injection", "XSS - Reflected", "XSS - Stored"}
ALLOWED_SEVERITIES = {"Low", "Medium", "High", "Critical"}

# Per-finding the expected category, so students can't mislabel the type.
EXPECTED_TYPE = {
    "JUICE-001": {"SQL Injection"},
    "JUICE-002": {"SQL Injection"},
    "JUICE-003": {"XSS - Reflected"},
    "JUICE-004": {"XSS - Stored"},
}

IMAGE_EXTS = (".png", ".jpg", ".jpeg")


def load_rows():
    assert os.path.exists(CSV_PATH), "findings.csv not found at repo root."
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def test_csv_exists_and_has_header():
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        header = next(csv.reader(fh))
    for col in REQUIRED_COLUMNS:
        assert col in header, f"Missing required column: '{col}'"


def test_exactly_four_required_findings():
    rows = load_rows()
    ids = [r["finding_id"].strip() for r in rows if r.get("finding_id", "").strip()]
    assert ids == REQUIRED_IDS, (
        f"findings.csv must contain exactly these IDs in order: {REQUIRED_IDS}. "
        f"Got: {ids}"
    )


@pytest.mark.parametrize("fid", REQUIRED_IDS)
def test_all_cells_filled(fid):
    rows = {r["finding_id"].strip(): r for r in load_rows()}
    row = rows[fid]
    for col in REQUIRED_COLUMNS:
        val = (row.get(col) or "").strip()
        assert val, f"{fid}: column '{col}' is empty - fill it in."


@pytest.mark.parametrize("fid", REQUIRED_IDS)
def test_vuln_type_valid_and_correct(fid):
    rows = {r["finding_id"].strip(): r for r in load_rows()}
    vtype = rows[fid]["vuln_type"].strip()
    assert vtype in ALLOWED_VULN_TYPES, (
        f"{fid}: vuln_type '{vtype}' not allowed. Use one of {sorted(ALLOWED_VULN_TYPES)}."
    )
    assert vtype in EXPECTED_TYPE[fid], (
        f"{fid}: expected a {EXPECTED_TYPE[fid]} finding but got '{vtype}'."
    )


@pytest.mark.parametrize("fid", REQUIRED_IDS)
def test_severity_valid(fid):
    rows = {r["finding_id"].strip(): r for r in load_rows()}
    sev = rows[fid]["severity"].strip()
    assert sev in ALLOWED_SEVERITIES, (
        f"{fid}: severity '{sev}' not allowed. Use one of {sorted(ALLOWED_SEVERITIES)}."
    )


@pytest.mark.parametrize("fid", REQUIRED_IDS)
def test_screenshot_exists(fid):
    rows = {r["finding_id"].strip(): r for r in load_rows()}
    shot = rows[fid]["screenshot"].strip()
    assert shot.lower().endswith(IMAGE_EXTS), (
        f"{fid}: screenshot '{shot}' must be a .png/.jpg/.jpeg file."
    )
    path = os.path.join(SHOTS_DIR, shot)
    assert os.path.exists(path), (
        f"{fid}: screenshot file '{shot}' not found in screenshots/. "
        f"Add your evidence image."
    )
