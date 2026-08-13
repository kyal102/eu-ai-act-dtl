import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from eu_ai_act_dtl import verify  # noqa: E402


def document(disclosure: bool = False):
    return {
        "task": {"kind": "customer_facing_ai_interaction", "output_type": "text"},
        "profile": {
            "product_role": "provider_and_deployer",
            "user_jurisdiction": "EU",
            "article50_triggered": True,
            "high_risk_use": False,
            "role_declared": True,
            "classification_reviewed": True,
            "ai_literacy_evidence_bound": True,
            "prohibited_practice_screen_passed": True,
        },
        "policy": {"version": "v1", "fail_closed": True},
        "evidence": {"model_version": "demo-1", "source_state": "fixed"},
        "candidate": {
            "answer": "A natural-language answer.",
            "confidence": 0.99,
            "disclosure_applied": disclosure,
        },
    }


class EUAIActDTLTests(unittest.TestCase):
    def test_confidence_does_not_override_missing_control(self):
        result = verify(document(disclosure=False))
        self.assertEqual(result["canonical_result"]["verdict"], "BLOCK")
        self.assertEqual(result["canonical_result"]["failed_controls"], ["ART-50-DISCLOSURE"])

    def test_verified_control_is_allowed(self):
        result = verify(document(disclosure=True))
        self.assertEqual(result["canonical_result"]["verdict"], "ALLOW")
        self.assertTrue(result["canonical_result"]["accepted_claim"])

    def test_same_state_replays_to_same_semantic_result(self):
        first = verify(document(disclosure=False))
        second = verify(json.loads(json.dumps(document(disclosure=False))))
        self.assertEqual(first["replay_key"], second["replay_key"])
        self.assertEqual(first["canonical_result"], second["canonical_result"])

    def test_confidence_is_metadata_not_a_semantic_input(self):
        first_document = document(disclosure=True)
        second_document = document(disclosure=True)
        second_document["candidate"]["confidence"] = 0.01
        self.assertEqual(verify(first_document)["replay_key"], verify(second_document)["replay_key"])


if __name__ == "__main__":
    unittest.main()
