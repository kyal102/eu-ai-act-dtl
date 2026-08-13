# GitHub profile and public-positioning audit

Audit date: 13 August 2026
Audited account: `kyal102`
Primary product: JARVI3 / DTL

## Current state observed

- The account has a public profile repository at `kyal102/kyal102` with a
  strong deterministic-verification thesis and links to multiple gate demos.
- The main `kyal102/jarvi3` repository is private and is very large compared
  with the public lite repositories.
- Several public repositories demonstrate individual gates, evidence packs,
  replay, benchmarks and domain examples.
- The public profile README already states an important limitation boundary:
  a passing gate is not automatically scientific truth, clinical safety,
  regulatory compliance or production readiness.

## Strengths

1. The thesis is memorable: â€œAI proposes. Gates verify. Evidence records.
   Replay checks drift.â€
2. The account has a coherent family of public demonstrations rather than one
   unsupported landing page.
3. The public README already separates a measured gate result from a broad
   safety or compliance claim.
4. The EU AI Act DTL project now adds a timely, legally bounded use case to the
   existing ClaimGate/EvidencePack/ReplayGate story.

## Highest-impact weaknesses

1. **Discoverability:** the profile does not yet lead with a single flagship
   EU AI Act DTL demo and one reproducible command.
2. **Repository sprawl:** many small gate repositories can look fragmented to
   a new reviewer. They need a clear â€œstart here / why these repos existâ€ map.
3. **Evidence of maturity:** the public material needs a visible conformance
   matrix, threat model, versioning, source registry and negative test suite.
4. **Legal wording risk:** â€œAI Actâ€ projects can easily overclaim. Every public
   page should say mapping/readiness/evidence layerâ€”not certification.
5. **Profile conversion:** the profile should make the target audience clear:
   technical reviewers, safety/security teams, enterprise pilots and
   researchers.

## 100x profile plan

### Today

- Link this project from the profile README under a â€œCurrent flagshipâ€ section.
- Put the one-line thesis, demo command and BLOCK/ALLOW proof above the fold.
- Keep a short â€œdoes not proveâ€ line beside every benchmark.
- Pin three repositories: the flagship DTL demo, the end-to-end evidence demo,
  and the security benchmark.

### Next 30 days

- Publish a dedicated public repository named `eu-ai-act-dtl` or move this
  self-contained folder into a clean public repository.
- Add GitHub Actions, release tags, a changelog and a versioned evidence schema.
- Invite independent review from one legal/compliance practitioner, one
  security engineer and one academic or standards reviewer.
- Publish four fixed scenarios: Article 50, prohibited-use block,
  high-risk-human-review abstention and stale-evidence replay drift.

### Next 90 days

- Publish latency and replay benchmarks with exact hardware and commit SHA.
- Add signed evidence packs and a verifier that works offline.
- Add a transparent issue tracker for open legal interpretation questions.
- Build a small hosted demo that never accepts personal data by default.
- Create a â€œprovider vs deployer vs downstream providerâ€ integration guide.

### Long-term

- Maintain a dated legal-source registry and change-impact process.
- Seek external assurance rather than self-awarded â€œ100%â€ claims.
- Keep the open reference verifier small and auditable; keep tenant operations,
  billing and product orchestration separate.

## Suggested profile headline

> Building deterministic verification boundaries for probabilistic AI â€”
> canonical tasks, evidence, replay and human review across AI governance,
> science and security.

## Suggested profile call-to-action

> Start with EU AI Act DTL: run one command, watch a 99%-confidence candidate
> fail a missing Article 50 control, then replay the corrected state.
