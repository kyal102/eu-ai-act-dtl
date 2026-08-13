# EcoKure DTL capability register

This register prevents the public package from presenting every capability as
equally mature. â€œEvidence pathâ€ points to the implementation area in the
source product; the public EU AI Act verifier is intentionally smaller.

| Capability | Status | Evidence path | Boundary |
|---|---|---|---|
| Probabilistic-to-deterministic transition | Reference architecture and implementation | `modules/dtl_registry/probabilistic_transition.py` | Candidate interpretation remains probabilistic; acceptance is lane-bound |
| DTL lane schema and conformance | Open standard/reference implementation | `dtl/SPEC.md`, `dtl/schema/`, `dtl/conformance/` | Registry records gates; domain owners close them |
| Multi-tenant DTL Registry | Technical platform support | `modules/dtl_registry/registry.py` | Identity, storage, retention and deployment security are required |
| Specialist gate catalog and partner boundary | Product/API implementation | `modules/dtl_registry/apigate.py` | Gate maturity, availability and domain limits are explicit |
| Exact mathematics | Deterministic gate | `modules/dtl_registry/supermath_lab.py` | Calculation result is not a universal proof of external truth |
| Dimensional and chemistry checks | Deterministic gates | `unitgate_lab.py`, `elementgate_lab.py` | Curated rule domains |
| Claim extraction and wording lint | Deterministic/structured assistance | `claimgate_lab.py`, `claimlint_lab.py` | Unverifiable claims remain unresolved |
| EvidencePack | Technical implementation | `claim_infra/core/evidence/`, `evidencepack_lab.py` | Preserves tested state; does not establish truth |
| ReplayGate | Technical implementation | `claim_infra/core/replay/`, `replaygate_lab.py` | External dependencies must be pinned or controlled |
| Signed attestation | Technical implementation | `modules/dtl_registry/attestation.py` | Signatures prove issuer/integrity, not correctness |
| Application sink guard | Technical implementation | `modules/dtl_registry/dtl_app_guard.py` | Coverage and integration must be maintained |
| Security taxonomy | Deterministic/guarded verification | `security_taxonomy.py`, `security_synthesizer.py` | Not a complete security programme |
| Clinical rule evaluation | Controlled partner/technical evaluation | `medical_taxonomy.py`, `medgate_*` | Not a registered medical device or clinical decision |
| Hardware/RTL safety preview | Preview | `chipgate_lab.py`, `chipgate_api.py` | Not physical safety or silicon readiness |
| Orbital verification | Research preview | `domains/avionics_seu_sim.py`, OrbitGate catalog | Not flight software or certification |
| Biology/discovery lanes | Research demonstration | `domains/foldgate.py`, `bindgate.py`, `mutationgate.py` | Not a biomedical conclusion |
| Research taxonomy bundle | Research | `modules/dtl_registry/domains/` | Domain validation is still required |
| EU AI Act readiness mapping | Public application pack | `modules/eu_ai_act_readiness.py`, `eu_ai_act_dtl/` | Readiness evidence only; no legal classification or certification |
| Enterprise workspace/control plane | Product architecture | `financegate_control_plane_v2.py`, governance modules | Customer deployment, identity and operating controls are required |

The register is a product-disclosure document, not a warranty. Status changes
must be reviewed, tested and released with the relevant implementation.
