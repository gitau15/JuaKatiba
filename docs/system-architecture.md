# JuaKatiba System Architecture & Technical Specification

## 1) Data Ingestion Pipeline (Extraction Layer)

### 1.1 Classification & Extraction
- Classify PDF pages by text density.
- Route digital pages to `pdfplumber` to preserve multi-column structure and tables.
- Use page-level OCR fallback (`pdf2image` + `pytesseract`) when digital extraction appears sparse (e.g., `<50` chars).
- Route scanned pages through OCR preprocessing (grayscale + sharpen) before Tesseract.
- Keep AWS Textract as an enterprise upgrade path for mission-critical extraction reliability.

### 1.2 Segmentation & Metadata Extraction
- Split text by notice-aware regex (`GAZETTE NOTICE NO. XXXX`).
- Extract `ministry`, `notice_type`, and `date` into metadata.
- If regex fails, send only the missing fields to a low-cost LLM fallback and enforce strict JSON output.

### 1.3 Cleaning & NER (GraphRAG Lite)
- Normalize whitespace and line breaks.
- Remove headers/footers and short artifacts (`<80` chars).
- Run spaCy (`en_core_web_sm`) for `PERSON`, `ORG`, `LOC` payload tags.

### 1.4 Chunking & Validation
- Use notice-aware recursive chunking (`chunk_size=400`, `overlap=50`).
- Preserve notice headers in each chunk for traceability.
- Validate chunk quality (length, noise ratio, required metadata).
- Deduplicate using SHA-256 hash over cleaned text.

## 2) Retrieval Layer (R in RAG)

### 2.1 Vector Database
- Self-hosted Qdrant for hybrid retrieval, payload filtering, and data sovereignty.

### 2.2 Hybrid Search
- Dense vectors:
  - Public: `text-embedding-3-small` (OpenAI)
  - Enterprise: `embed-multilingual-v3.0` (Cohere)
- Sparse vectors: SPLADE via `fastembed`.
- Rank fusion: Qdrant RRF.

### 2.3 Payload Filtering
- Store NER tags and metadata in payloads.
- Support pre-filtered retrieval (e.g., `ORG=Safaricom`, `date>2020`) before semantic ranking.

## 3) Generation & Anti-Hallucination Layer (G in RAG)

### 3.1 Model Tiering
- Public MVP: `mistral-small-latest` (API)
- Public Scale: self-hosted Mistral 7B Instruct (`Q4_K_M`) via Ollama.
- Enterprise: self-hosted Llama 3.1 8B (`Q4_K_M`) via Ollama/llama.cpp in private VPC/on-prem.

### 3.2 Prompt Controls
- Temperature fixed at `0.0`.
- Force source-tagged context blocks.
- Hard abstention token: `INSUFFICIENT_CONTEXT`.
- Dynamic tone template:
  - Public: plain language
  - Enterprise: formal legal precision

### 3.3 Guardrails
- Secondary self-check pass to verify claims are grounded in retrieved context.
- Regex validator to ensure cited Gazette notice IDs exist in retrieved chunks.
- If hallucinated citation detected:
  - block response,
  - return safe abstention,
  - flag for review,
  - persist immutable audit log in enterprise tier.

## 4) Deployment Roadmap

### Phase 1 (MVP)
- Local/Docker Qdrant.
- Python backend.
- Mistral API.
- Minimal web or WhatsApp interface.

### Phase 2 (Public Scale)
- Qdrant on VPS.
- GPU inference node via Vast.ai/RunPod + Ollama Mistral 7B.
- Optional freemium auth/identity (Persona).

### Phase 3 (Enterprise)
- Kubernetes Helm deploy in client private cloud/on-prem.
- Full offline/air-gapped capability.
- Signed tarball update protocol for model/prompt/schema updates.
