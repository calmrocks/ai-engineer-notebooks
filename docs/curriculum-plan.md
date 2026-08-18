# Curriculum plan & design log

Working notes on the structure of this repo — why the sections are what they
are, what was researched, what was decided (and rejected), and what's still
open. Kept so the reasoning survives even if the conversation context is lost.

Last updated: 2026-08-17.

## What this repo is

Runnable Colab notebooks teaching the **FDE / AI Engineer** applied-LLM stack,
framework-free, on the **free Groq API**. Hands-on companion to the
[transition plan](https://www.calm.rocks/resources/career-development/transition-fde-ai-engineer/).
Shared `aien` package (repo root) handles setup; one shared RFC corpus runs
through RAG + evals so evals measure the retrieval you actually built.

## Current structure (11 sections)

```
00 Setup            environment, keys, cost hygiene, spend guard
01 Model APIs       structured output, tool calling, streaming, context/caching+batch
02 Evals I          NEW — "measure before you tune" on the 01 extraction task (no RAG dep)
03 RAG              what-is-rag → embeddings → hybrid/rerank → chunking → why-rag-fails
04 Evals II         golden sets, LLM-as-judge, regression-as-CI (coupled to RAG)
05 Agents           loop from scratch, tool design, guardrails/budgets, MCP (concept)
06 Adaptation       fine-tune vs RAG vs prompt; LoRA/QLoRA; optional GPU LoRA appendix
07 Security         prompt injection (direct+indirect), OWASP LLM Top 10, trust boundary
08 Operations       observability/LLMOps; reliability/fallbacks
09 Customer craft   NEW — scoping/discovery, scoping-doc template, demo discipline
10 Capstone         deployed project brief (not a notebook)
```

RAG internal order is deliberate (**retrieval before chunking**): you can't
judge a chunking strategy until you've seen retrieval succeed/fail on it, and
an RFC (~40k tokens) can't be embedded whole (model window ~256 tokens) — so
chunking's *necessity* is shown in 03/embeddings, its *craft* deferred to
03/chunking.

## Research consulted

- **OWASP LLM Top 10 (2025)** — prompt injection is #1; drove section 07.
- **MCP** (modelcontextprotocol.io) — now a standard (Claude/OpenAI/VS Code/
  Cursor); folded into agents as concept-only (repo avoids frameworks).
- **PEFT / LoRA / QLoRA** (HuggingFace) — mainstream, runs on free Colab T4.
- **RAG canon** — Lewis et al. 2020, AWS, Pinecone, Prompting Guide. Settled
  that RAG ≠ embeddings (retrieval is swappable: vector/BM25/hybrid/SQL/API).
- **Groq** — inference-only (no training, no caching/batch API); does support
  multimodal (`qwen`) and LoRA *serving*.
- **Two independent curriculum evaluators** (market-lens + pedagogy-lens), each
  told to design the ideal from first principles. They converged (see below).

## Decisions locked (with rationale)

1. **Evals is the spine, introduced early.** Both evaluators' #1 fix: RAG→Evals
   was backwards (can't tune RAG without a metric). Split into 02 (basics, on
   the extraction task) + 04 (rich, on RAG). Kept the shared-corpus design by
   *splitting* rather than re-pointing the rich eval notebooks off RAG.
2. **Added FDE customer-craft (09).** Both called its absence the single largest
   gap for an "FDE" repo; it's a named interview round.
3. **Multimodal & multi-agent: concept-only / OFF the core spine.** Both
   evaluators independently pushed back on adding them hands-on (multi-agent
   hands-on "rewards exactly the instinct the curriculum should suppress").
   Multimodal's only strong argument was Groq feasibility, which is not a
   plan-priority. → not added as modules.
4. **Priority rule (user):** "does the plan want it" > "does it stay on Groq."
   Groq is a delivery detail; where Groq can't run a plan-named topic, show real
   provider API shapes as reference code instead of watering it down.
5. **Fine-tuning stays late, decision-framed**, with an optional fenced GPU LoRA
   appendix — matches plan ("conceptually only") without ignoring LoRA's rise.
6. **Security after agents; ops after security** — cross-cutting "make it real"
   concerns need a real system to be meaningful. Both evaluators endorsed.

## Explicitly rejected

- Multimodal / multi-agent as hands-on core modules (see #3).
- Standalone prompt-engineering module (woven throughout; plan = baseline).
- Fine-tuning internals / RLHF / classical ML / agent-framework deep-dives
  (plan says skip).
- Data-pipeline / deploy-infra notebooks (that's the capstone's job).

## Open work — Phase 2 (polish the evaluators also recommended)

Not yet done; all lighter-touch than the reorder:

1. **Cross-link the eval spine** — from 02 into 03/RAG's intro; add a short
   **trajectory-eval** touchpoint after agents (evals should visibly *return*).
2. **Non-determinism "shock" cell** in 00 Setup (run same prompt ×5, watch it
   vary / a structured parse fail) — motivation hook for evals.
3. **Workflows-before-autonomy** beat at the front of 05 Agents (pull the "when
   a pipeline beats an agent" intuition earlier).
4. **Cross-provider API reference code** (non-runnable, clearly fenced) where
   Groq can't run a plan-named topic: Anthropic `cache_control`, OpenAI prefix
   caching + Batch submit/poll (in 01/context-caching); OpenAI `fine_tuning.jobs`
   + Bedrock adapter path (in 06/adaptation).

## Standing caveats

- **Notebooks are verified statically only** (JSON structure, code compiles,
  badges/cross-refs consistent) — they have NOT been executed here (no API key,
  no GPU). Before treating any as final, run top-to-bottom in Colab. Highest
  risk: 06 LoRA appendix (peft/trl API drift), 08 reliability (groq typed
  exceptions), the live-call notebooks (02 evals harness, 09 role-play).
- **Models:** repo uses `openai/gpt-oss-120b` / `-20b` (current Groq production).
  Re-verify against Groq's model list if calls 404.
- **Colab has no repo checkout** → notebooks install `aien` via
  `pip install "git+https://github.com/calmrocks/ai-engineer-notebooks.git"`,
  pulling from `main` (latest). Breaking `aien` changes hit published notebooks.
