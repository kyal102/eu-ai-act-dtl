# EU AI Act DTL

## The missing layer between AI generation and accountable acceptance

Large language models are probabilistic. Compliance decisions cannot be
accepted because a model sounded confident, repeated itself, or received a
high score from another model.

**EU AI Act DTL** is a small, dependency-free reference implementation of the
alternative:

```text
AI candidate
    -> operator-defined legal/product profile
    -> canonical task + deterministic lane
    -> required-control verification
    -> replayable evidence hash
    -> ALLOW / BLOCK / ABSTAIN
    -> natural-language rendering
```

The language can vary. The accepted semantic state cannot vary when the task,
evidence, policy and state are identical.

This is an **engineering demonstrator**, not legal advice, a legal classifier,
a conformity assessment, or an EU AI Act compliance certificate. The operator
must determine the applicable role, intended purpose, jurisdiction and
obligations with qualified legal support.

## Why this is different

| Conventional AI compliance | EU AI Act DTL |
|---|---|
| Ask another model whether an answer is safe | Verify structured controls against fixed rules |
| Treat confidence as evidence | Treat evidence as evidence |
| Keep only the final sentence | Keep the canonical task, lane, policy and verdict |
| Silently pick one answer | Detect conflict and block or abstain |
| Produce a checklist | Produce a replayable decision record |

DTL does not make the model deterministic. It makes the **accepted semantic
result** deterministic.

## Read the full design

- [EU AI Act DTL Whitepaper](EU_AI_ACT_DTL_WHITEPAPER.md)
- [Control matrix, research and roadmap](EU_AI_ACT_DTL_WHITEPAPER.md#control-by-control-mapping)
- [Official research sources](RESEARCH_SOURCES.md)
- [Threat model and limitations](EU_AI_ACT_DTL_WHITEPAPER.md#safety-and-threat-model)
- [GitHub profile audit and 100x plan](PROFILE_AUDIT.md)

## Run the demo

```bash
python eu-ai-act-dtl/eu_ai_act_dtl.py eu-ai-act-dtl/example.json
python -m unittest discover -s eu-ai-act-dtl -p "test_*.py"
```

The example deliberately contains a candidate with high confidence but a
missing Article 50 disclosure control. The result is still `BLOCK`.

Change only `candidate.disclosure_applied` to `true` and the same
profile/evidence/policy state produces `ALLOW` for the corrected candidate.

## Input contract

The operator supplies the legal/product profile. DTL does not invent a legal
classification from model confidence.

```json
{
  "task": {"kind": "customer_facing_ai_interaction", "output_type": "text"},
  "profile": {
    "product_role": "provider_and_deployer",
    "user_jurisdiction": "EU",
    "article50_triggered": true,
    "high_risk_use": false,
    "role_declared": true,
    "classification_reviewed": true,
    "ai_literacy_evidence_bound": true,
    "prohibited_practice_screen_passed": true
  },
  "policy": {"version": "eu-ai-act-demo-policy-v1", "fail_closed": true},
  "evidence": {"model_version": "jarvi3-demo-1", "source_state": "sha256:demo"},
  "candidate": {
    "answer": "Here is the requested summary.",
    "confidence": 0.99,
    "disclosure_applied": false
  }
}
```

`confidence` is recorded as metadata and never participates in acceptance.

## Output contract

The verifier emits:

- `canonical_task`
- `input_state_sha256`
- `lane`
- `required_controls`
- `control_results`
- `verification_state`
- `canonical_result`
- `canonical_result_sha256`
- `replay_key`

The result is intentionally boring to explain:

```text
same task + same evidence + same policy/state = same accepted result
```

## Scope

This demonstrator focuses on the probabilistic-to-deterministic transition and
uses Article 50 transparency plus a high-risk human-oversight example lane. It
does not attempt to implement the entire Regulation, replace technical
documentation, risk management, human oversight, incident reporting, or a
conformity assessment.

Primary legal source: [Regulation (EU) 2024/1689 on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en).

Built on the JARVI3 / DTL concept. Patent and licensing claims, if any, must be
reviewed by qualified counsel before public distribution.
