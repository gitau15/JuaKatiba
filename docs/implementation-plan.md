# JuaKatiba Implementation Plan

## Build Milestones

### Milestone 0: Repo Bootstrapping (Week 1)
- Create monorepo structure:
  - `services/ingestion`
  - `services/retrieval`
  - `services/generation`
  - `apps/public-web`
  - `apps/enterprise-api`
  - `infra/`
- Add formatting, linting, test, and CI baselines.

### Milestone 1: Ingestion MVP (Weeks 1-2)
- Implement PDF classifier + dual-path extraction.
- Add notice segmentation + metadata parser.
- Add OCR fallback and deduplication.
- Deliver reproducible test corpus for Kenya Gazette docs.

### Milestone 2: Retrieval MVP (Week 3)
- Provision Qdrant collections.
- Add dense + sparse indexing pipeline.
- Implement payload filter query API and hybrid retrieval tests.

### Milestone 3: Generation MVP (Week 4)
- Add constrained prompt templates and abstention behavior.
- Integrate citation validator + grounding self-check.
- Expose one public endpoint and one enterprise policy endpoint.

### Milestone 4: Product Surface (Weeks 5-6)
- Public web UX for civic Q&A.
- Enterprise API with structured response envelope and audit logging.
- Observability: retrieval hit rates, abstention rates, latency budgets.

## Definition of Done (MVP)
- End-to-end query returns sourced answer or `INSUFFICIENT_CONTEXT`.
- Hallucinated citation block is covered by automated tests.
- Gazette ingestion supports incremental runs and skips duplicates.
- Core pipelines run in Docker Compose locally.
