#!/usr/bin/env python3
"""Dependency-free EU AI Act DTL reference verifier.

This is an educational engineering demonstrator.  It does not classify legal
obligations and does not provide legal advice.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


SCHEMA = "eu-ai-act-dtl.reference/v1"
SOURCE = "https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en"
DISCLAIMER = (
    "Engineering demonstrator only; not legal advice, legal classification, "
    "conformity assessment, certification, or a compliance declaration."
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _bool(value: Any) -> bool:
    return value is True


def _control(control_id: str, article: str, source: str, field: str, rule: str) -> dict[str, Any]:
    return {
        "id": control_id,
        "article": article,
        "source": source,
        "field": field,
        "rule": rule,
    }


def build_canonical_task(document: Mapping[str, Any]) -> dict[str, Any]:
    task = document.get("task") or {}
    profile = document.get("profile") or {}
    return {
        "kind": str(task.get("kind") or "unspecified_task"),
        "output_type": str(task.get("output_type") or "text"),
        "jurisdiction": str(profile.get("user_jurisdiction") or "unspecified"),
        "role": str(profile.get("product_role") or "unspecified"),
    }


def select_lane(document: Mapping[str, Any]) -> str:
    task = document.get("task") or {}
    profile = document.get("profile") or {}
    if _bool(profile.get("high_risk_use")):
        return "eu_ai_act.high_risk.human_oversight"
    if _bool(profile.get("article50_triggered")):
        return f"eu_ai_act.article50.{str(task.get('output_type') or 'text')}"
    return "eu_ai_act.general.transparency_review"


def required_controls(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    profile = document.get("profile") or {}
    controls: list[dict[str, Any]] = []

    # These are deliberately operator-supplied facts. DTL does not infer legal
    # role or classification from model output.
    controls.extend([
        _control(
            "PROFILE-ROLE-DECLARED",
            "Articles 2-3",
            "profile",
            "role_declared",
            "profile.role_declared must be true",
        ),
        _control(
            "PROFILE-CLASSIFICATION-REVIEWED",
            "Articles 6-7 / Annex III",
            "profile",
            "classification_reviewed",
            "profile.classification_reviewed must be true",
        ),
        _control(
            "ART-4-AI-LITERACY",
            "Article 4",
            "profile",
            "ai_literacy_evidence_bound",
            "profile.ai_literacy_evidence_bound must be true",
        ),
        _control(
            "ART-5-PROHIBITED-SCREEN",
            "Article 5",
            "profile",
            "prohibited_practice_screen_passed",
            "profile.prohibited_practice_screen_passed must be true",
        ),
    ])
    if _bool(profile.get("article50_triggered")):
        controls.append(_control(
            "ART-50-DISCLOSURE",
            "Article 50",
            "candidate",
            "disclosure_applied",
            "candidate.disclosure_applied must be true",
        ))
    if _bool(profile.get("high_risk_use")):
        controls.extend([
            _control("ART-9-RISK-MANAGEMENT", "Article 9", "profile", "risk_management_bound", "profile.risk_management_bound must be true"),
            _control("ART-10-DATA-GOVERNANCE", "Article 10", "profile", "data_governance_bound", "profile.data_governance_bound must be true"),
            _control("ART-11-TECHNICAL-DOCS", "Article 11", "profile", "technical_documentation_bound", "profile.technical_documentation_bound must be true"),
            _control("ART-12-RECORD-KEEPING", "Article 12", "candidate", "record_keeping_bound", "candidate.record_keeping_bound must be true"),
            _control("ART-13-INSTRUCTIONS", "Article 13", "profile", "instructions_for_use_bound", "profile.instructions_for_use_bound must be true"),
            _control("ART-14-HUMAN-OVERSIGHT", "Article 14", "candidate", "human_oversight_available", "candidate.human_oversight_available must be true"),
            _control("ART-15-ACCURACY-ROBUSTNESS-SECURITY", "Article 15", "profile", "accuracy_robustness_security_tested", "profile.accuracy_robustness_security_tested must be true"),
            _control("ART-17-QUALITY-MANAGEMENT", "Article 17", "profile", "quality_management_bound", "profile.quality_management_bound must be true"),
            _control("ART-26-DEPLOYER-CONTROLS", "Article 26", "profile", "deployer_controls_bound", "profile.deployer_controls_bound must be true"),
            _control("ART-72-POST-MARKET", "Article 72", "profile", "post_market_monitoring_bound", "profile.post_market_monitoring_bound must be true"),
            _control("ART-73-SERIOUS-INCIDENT", "Article 73", "profile", "serious_incident_process_bound", "profile.serious_incident_process_bound must be true"),
        ])
        if _bool(profile.get("fria_required")):
            controls.append(_control(
                "ART-27-FUNDAMENTAL-RIGHTS-ASSESSMENT",
                "Article 27",
                "profile",
                "fundamental_rights_assessment_bound",
                "profile.fundamental_rights_assessment_bound must be true",
            ))
    if _bool(profile.get("gpai_provider")):
        controls.extend([
            _control("GPAI-53-TECHNICAL-DOCS", "Articles 53-54", "profile", "gpai_technical_documentation_bound", "profile.gpai_technical_documentation_bound must be true"),
            _control("GPAI-53-COPYRIGHT", "Article 53", "profile", "gpai_copyright_policy_bound", "profile.gpai_copyright_policy_bound must be true"),
            _control("GPAI-53-TRAINING-SUMMARY", "Article 53", "profile", "gpai_training_summary_bound", "profile.gpai_training_summary_bound must be true"),
        ])
        if _bool(profile.get("gpai_systemic_risk")):
            controls.extend([
                _control("GPAI-55-RISK-MITIGATION", "Article 55", "profile", "gpai_systemic_risk_mitigation_bound", "profile.gpai_systemic_risk_mitigation_bound must be true"),
                _control("GPAI-55-INCIDENT-REPORTING", "Article 55", "profile", "gpai_incident_reporting_bound", "profile.gpai_incident_reporting_bound must be true"),
                _control("GPAI-55-CYBERSECURITY", "Article 55", "profile", "gpai_cybersecurity_bound", "profile.gpai_cybersecurity_bound must be true"),
            ])
    return controls


def _observed_value(document: Mapping[str, Any], control: Mapping[str, Any]) -> Any:
    source = document.get(control["source"]) or {}
    return source.get(control["field"])


def verify(document: Mapping[str, Any]) -> dict[str, Any]:
    """Return the deterministic semantic result for one canonical input state."""
    task = build_canonical_task(document)
    profile = document.get("profile") or {}
    evidence = document.get("evidence") or {}
    policy = document.get("policy") or {}
    candidate = document.get("candidate") or {}
    controls = required_controls(document)
    control_results = []
    for control in controls:
        observed = _observed_value(document, control)
        passed = _bool(observed)
        control_results.append({
            **control,
            "passed": passed,
            "observed": observed,
        })

    # Confidence is intentionally excluded from the semantic state. Changing
    # confidence alone must not change acceptance. The candidate's actual
    # claims/control observations are included so replay cannot accidentally
    # reuse a receipt for a different candidate.
    candidate_state = dict(candidate)
    candidate_state.pop("confidence", None)
    state = {
        "task": task,
        "lane": select_lane(document),
        "profile": profile,
        "evidence": evidence,
        "policy": policy,
        "candidate": candidate_state,
    }
    input_state_hash = sha256(state)
    failed = [item["id"] for item in control_results if not item["passed"]]
    fail_closed = policy.get("fail_closed", True) is True
    if failed and fail_closed:
        verdict = "BLOCK"
        verification_state = "FAIL"
    elif failed:
        verdict = "ABSTAIN"
        verification_state = "INCOMPLETE"
    else:
        verdict = "ALLOW"
        verification_state = "PASS"

    canonical_result = {
        "verdict": verdict,
        "verification_state": verification_state,
        "failed_controls": failed,
        "accepted_claim": verdict == "ALLOW",
    }
    canonical_result_hash = sha256(canonical_result)
    return {
        "schema": SCHEMA,
        "disclaimer": DISCLAIMER,
        "source": SOURCE,
        "canonical_task": task,
        "input_state_sha256": input_state_hash,
        "lane": state["lane"],
        "required_controls": controls,
        "control_results": control_results,
        "candidate_confidence_recorded_only": candidate.get("confidence"),
        "legal_profile_is_operator_input": True,
        "legal_classification_required": True,
        "verification_state": verification_state,
        "canonical_result": canonical_result,
        "canonical_result_sha256": canonical_result_hash,
        "replay_key": f"{input_state_hash}:{canonical_result_hash}",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <document.json>", file=sys.stderr)
        return 2
    document = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(verify(document), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
