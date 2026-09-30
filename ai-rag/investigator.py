"""Gemini + RAG investigation reports for CloudShield findings."""

import json
from typing import Any

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, KNOWLEDGE_DIR, LOGGER

REPORT_FIELDS = (
    "root_cause",
    "potential_attack_scenario",
    "evidence_to_check",
    "related_security_controls",
    "remediation",
)
LIST_FIELDS = ("evidence_to_check", "related_security_controls")


def retrieve_knowledge(rule_id: str) -> str:
    """Return the knowledge doc for a rule, or an empty string if there is none."""
    path = KNOWLEDGE_DIR / f"{rule_id}.md"
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _build_prompt(finding: dict[str, Any], knowledge: str) -> str:
    return (
        "You are a cloud security analyst. Investigate this AWS finding.\n"
        f"Finding:\n{json.dumps(finding, indent=2, default=str)}\n\n"
        f"Reference knowledge:\n{knowledge or 'None available for this rule.'}\n\n"
        f"Reply with a JSON object with the keys {', '.join(REPORT_FIELDS)}. "
        f"{' and '.join(LIST_FIELDS)} are lists of strings; the others are strings."
    )


def _parse_report(text: str) -> dict[str, Any]:
    try:
        report = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"Gemini returned invalid JSON: {error}") from error
    missing = [field for field in REPORT_FIELDS if field not in report]
    if missing:
        raise ValueError(f"Gemini report is missing fields: {', '.join(missing)}")
    return report


def investigate_finding(finding: dict[str, Any]) -> dict[str, Any]:
    """Return an investigation report for a backend finding dict."""
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key unavailable; set GEMINI_API_KEY")
    knowledge = retrieve_knowledge(finding["rule_id"])
    if not knowledge:
        LOGGER.warning("No knowledge doc for rule %s", finding["rule_id"])
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=_build_prompt(finding, knowledge),
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    report = _parse_report(response.text)
    return {
        "severity": finding["severity"],
        **{field: report[field] for field in REPORT_FIELDS},
        "generated_by": "gemini",
        "model": GEMINI_MODEL,
    }
