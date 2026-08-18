# AI Engineer Notebooks

Runnable Colab notebooks for learning the **AI Engineer / Forward Deployed
Engineer (FDE)** skill set: building working systems on top of foundation
models — model APIs, RAG, evals, agents, and when to adapt the model itself —
using raw APIs, not frameworks.

Everything runs on the **free [Groq](https://console.groq.com/) API** (Llama
models, no credit card required), so you can work through the whole thing
without a paid account. The patterns — tool calling, structured output,
streaming, the agent loop — use the OpenAI-compatible interface Groq exposes,
which transfers directly to OpenAI and (with small shape changes) to
Anthropic. (One exception: the optional LoRA fine-tuning appendix in section
06 needs a free Colab GPU runtime and a training stack, since Groq is
inference-only — it's clearly fenced and skippable.)

Built as the hands-on companion to
[Plan: Transitioning to Forward Deployed Engineer / AI Engineer](https://www.calm.rocks/resources/career-development/transition-fde-ai-engineer/).
The plan explains what to learn and why; these notebooks are where you run it.

## Who this is for

Backend or full-stack engineers moving into AI Engineer, FDE, Applied AI,
or Solutions Engineer (AI) roles — different titles, largely the same job.
You can ship production code; you want the applied-model layer on top.

## Learning order

Work top to bottom. Each notebook is self-contained (installs its own
dependencies, reads API keys from Colab secrets) and ends with exercises.

### 00 — Setup

| Notebook | What you'll learn |
|---|---|
| [Environment & cost hygiene](00-setup/00-environment.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/00-setup/00-environment.ipynb) | API keys via Colab secrets, spend guards, model picking |

### 01 — Model APIs

| Notebook | What you'll learn |
|---|---|
| [Structured output](01-model-apis/01-structured-output.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/01-model-apis/01-structured-output.ipynb) | Getting reliable JSON out of a model, and where it breaks |
| [Tool calling](01-model-apis/02-tool-calling.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/01-model-apis/02-tool-calling.ipynb) | Function/tool calling end to end, error paths included |
| [Streaming](01-model-apis/03-streaming.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/01-model-apis/03-streaming.ipynb) | Streaming responses and what UIs need from them |
| [Context & caching](01-model-apis/04-context-and-caching.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/01-model-apis/04-context-and-caching.ipynb) | Context-window budgeting, prompt caching, batch vs real-time pricing |

### 02 — Evals I: measuring outputs

| Notebook | What you'll learn |
|---|---|
| [Measuring outputs](02-evals-basics/01-measuring-outputs.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/02-evals-basics/01-measuring-outputs.ipynb) | Golden sets and metrics on the section-01 task — install the "measure before you tune" habit *before* building anything you'd need to tune. Evals is the spine; it returns in every section after this |

### 03 — RAG

| Notebook | What you'll learn |
|---|---|
| [What is RAG?](03-rag/00-what-is-rag.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/03-rag/00-what-is-rag.ipynb) | The retrieve → augment → generate loop, why RAG beats a plain LLM, and why RAG isn't the same as embeddings — with a 15-line working demo |
| [Embeddings & retrieval](03-rag/01-embeddings-retrieval.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/03-rag/01-embeddings-retrieval.ipynb) | Embedding choice, vector search, similarity pitfalls — get retrieval working first |
| [Hybrid & reranking](03-rag/02-hybrid-and-reranking.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/03-rag/02-hybrid-and-reranking.ipynb) | Keyword + vector hybrid retrieval, rerankers, when each earns its cost |
| [Chunking](03-rag/03-chunking.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/03-rag/03-chunking.ipynb) | Chunking strategies on a real messy corpus — revisited last, once you can judge them against retrieval |
| [Why RAG fails](03-rag/04-why-rag-fails.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/03-rag/04-why-rag-fails.ipynb) | Diagnosing bad answers: retrieval quality, not generation, is usually the bottleneck |

### 04 — Evals II: the differentiator

| Notebook | What you'll learn |
|---|---|
| [Golden sets](04-evals/01-golden-sets.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/04-evals/01-golden-sets.ipynb) | Building a golden set for the RAG system from section 03 |
| [LLM as judge](04-evals/02-llm-as-judge.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/04-evals/02-llm-as-judge.ipynb) | Judge prompts, agreement with humans, and the judge's own failure modes |
| [Regression evals](04-evals/03-regression-evals.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/04-evals/03-regression-evals.ipynb) | Evals as CI: catching quality regressions when you change a prompt or model |

### 05 — Agents

| Notebook | What you'll learn |
|---|---|
| [Agent loop from scratch](05-agents/01-agent-loop-from-scratch.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/05-agents/01-agent-loop-from-scratch.ipynb) | A working agent loop in raw API calls — no framework |
| [Tool design](05-agents/02-tool-design.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/05-agents/02-tool-design.ipynb) | Designing tools the model can actually use well |
| [Guardrails & budgets](05-agents/03-guardrails-and-budgets.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/05-agents/03-guardrails-and-budgets.ipynb) | Stopping conditions, cost/latency budgets, when a pipeline beats an agent |
| [MCP & the tool ecosystem](05-agents/04-mcp-and-the-tool-ecosystem.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/05-agents/04-mcp-and-the-tool-ecosystem.ipynb) | Concept: what the Model Context Protocol standardizes, how it maps to the raw tool loop, and when to reach for it |

### 06 — Adapting the model

| Notebook | What you'll learn |
|---|---|
| [Fine-tune vs RAG vs prompt](06-adaptation/01-fine-tune-vs-rag-vs-prompt.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/06-adaptation/01-fine-tune-vs-rag-vs-prompt.ipynb) | When to change the model's weights vs its inputs; what LoRA/QLoRA are and cost; the argument you'll have in the room — plus an optional real LoRA fine-tune on a free GPU |

### 07 — Security

| Notebook | What you'll learn |
|---|---|
| [Prompt injection & the trust boundary](07-security/01-prompt-injection-and-trust.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/07-security/01-prompt-injection-and-trust.ipynb) | Direct & indirect prompt injection, output handling, PII, excessive agency — the OWASP LLM Top 10 risks, failing live then defended |

### 08 — Operations

| Notebook | What you'll learn |
|---|---|
| [Observability & LLMOps](08-operations/01-observability-and-llmops.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/08-operations/01-observability-and-llmops.ipynb) | Tracing every call, safe prompt logging, cost/latency/error metrics, drift detection, and the observe→eval feedback loop |
| [Reliability & fallbacks](08-operations/02-reliability-and-fallbacks.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/08-operations/02-reliability-and-fallbacks.ipynb) | Retries with backoff, timeouts, fallback models, output validation, circuit breakers, graceful degradation |

### 09 — Customer craft (the FDE differentiator)

| Notebook | What you'll learn |
|---|---|
| [Scoping & discovery](09-customer-craft/01-scoping-and-discovery.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/09-customer-craft/01-scoping-and-discovery.ipynb) | Turn a vague customer ask into a scoped, evaluable system: discovery questions, a one-page scoping doc, the demo discipline — the customer-scenario interview round most engineers can't evidence |

### 10 — Capstone

Not a notebook. [The brief](10-capstone/README.md) for the deployed
project that goes on your resume — built as a real repo with a serving
component and an eval report. Notebooks are for learning; the capstone is
for hiring.

## Conventions

- **Raw model APIs, no frameworks.** Patterns are durable; wrappers churn.
- **One shared corpus** (`data/`) across RAG and eval sections, so evals
  measure the retrieval you actually built.
- **Self-contained notebooks.** First cell installs, second cell calls
  `from aien import setup; client, MODEL = setup()` to load your key from
  Colab secrets (or a local env var). No hidden state between notebooks.
  `aien` is the tiny shared-setup package in this repo — one place to change
  credential loading — installed automatically by the first cell.
- **Every notebook ends with exercises** — do them before moving on.

## Setup

1. Get a free API key at [console.groq.com](https://console.groq.com/) — no
   credit card required.
2. In Colab: the key icon in the left sidebar → add `GROQ_API_KEY` as a secret,
   and toggle notebook access on.
3. Open any notebook via its badge and run top to bottom.

Running locally instead: `pip install -r requirements.txt && pip install -e .`
(the second installs the `aien` setup helper), `export GROQ_API_KEY=...`,
open with Jupyter.

## Related reading

- [Plan: Transitioning to FDE / AI Engineer](https://www.calm.rocks/resources/career-development/transition-fde-ai-engineer/) — the roadmap these notebooks implement
- [Guide: Building a Real LLM Project for Your Resume](https://www.calm.rocks/resources/career-development/real-llm-project/) — the capstone's requirements bar
- [Walkthrough: Designing a RAG System](https://www.calm.rocks/resources/prepare-interview/system-design/rag-system-walkthrough/) — the systems view of section 03
- [Walkthrough: Designing an AI Agent Orchestration System](https://www.calm.rocks/resources/prepare-interview/system-design/agent-orchestration-walkthrough/) — the systems view of section 05
