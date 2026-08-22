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
01 Model APIs       prompting fundamentals, structured output, tool calling, streaming, context/caching+batch
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
- Standalone prompt-engineering *hero module* (both evaluators warned it breeds
  cargo-cult tricks). BUT — an audit (2026-08-20) found the intended "woven in"
  fold-in never actually happened: prompting was *used* everywhere, *taught*
  nowhere. Fixed by adding `01-model-apis/00-prompting-basics` (fundamentals as
  the on-ramp to structured output: clear instructions, few-shot, format specs,
  CoT — tied to the eval habit, anti-cargo-cult). Not a hero module; a short
  front-of-section fold-in, which is what the plan intended all along.
- Fine-tuning internals / RLHF / classical ML / agent-framework deep-dives
  (plan says skip).
- Data-pipeline / deploy-infra notebooks (that's the capstone's job).

## Phase 2 — DONE (2026-08-17)

All four evaluator-recommended polish items shipped:

1. **Eval spine cross-linked** — 00 setup "shock" motivates it; 03/RAG intro
   calls back to the section-02 habit; a **trajectory-eval** touchpoint added
   after agents (05/guardrails) so evals visibly *return*.
2. **Non-determinism "shock" cell** in 00 Setup (same prompt ×5 varies; a strict
   output contract breaks intermittently).
3. **Workflows-before-autonomy** caution at the front of 05/agent-loop
   ("reach for the loop last; pipeline if the steps are known").
4. **Cross-provider reference code** (non-runnable markdown snippets, verified
   against current provider docs): Anthropic `cache_control` + OpenAI Batch
   submit/poll in 01/context-caching; OpenAI `fine_tuning.jobs` + Bedrock note
   in 06/adaptation. Kept as fenced markdown so they can't break a Groq run.

No open structural work remains. Any future work is content refinement or
the still-pending end-to-end Colab execution pass (see caveats).

## Best practices & anti-patterns (added 2026-08-18)

- **`docs/best-practices-and-anti-patterns.md`** — consolidated ✅ do / ❌ don't
  for the whole stack, section by section, ending with "the five that matter
  most." Doubles as a pre-interview review sheet and pre-capstone checklist;
  linked from the capstone README ("Before you ship").
- **Per-notebook closing beat** — a uniform `## Practices & anti-patterns`
  table added before Exercises in the 6 notebooks that lacked one
  (02-tool-calling, 03-hybrid, 03-chunking, 04-regression, 05-mcp,
  08-observability). The other notebooks already carried equivalent content
  (ladders, checklists, "when a pipeline beats an agent", diagnosis cards) and
  were left as-is to avoid redundancy.

## Adaptation notebook reframe (added 2026-08-22)

- **06/fine-tune-vs-rag-vs-prompt** reframed around a *degree-of-model-modification*
  spectrum (prompt → RAG │ LoRA → full fine-tune; inputs vs weights) instead of
  popularity, plus a "pendulum" cell (fine-tune was the early default → field swung
  to prompt/RAG → fine-tuning specialized to style-at-scale + small-model
  distillation). Taxonomy precision added: LoRA is a *kind* of fine-tuning, not a
  peer. Hosted reference code expanded to a verified 3-tier split — **abstracted**
  (OpenAI, Bedrock: no LoRA knob) vs **explicit-LoRA** (Together, Fireworks:
  `lora=True`/`--lora-rank`) vs self-train (`peft`). All snippets reference-only.
  Provider APIs verified against live docs 2026-08-22; corrected a prior wrong
  claim that Bedrock yields a "LoRA endpoint" (Bedrock has no LoRA surface —
  explicit LoRA on AWS is SageMaker).

## Callout theming (added 2026-08-18)

Site-brand callouts, within the constraint that Colab/GitHub notebook
renderers strip CSS and don't support the `[!NOTE]` alert extension (verified:
literal text on both). Convention in `docs/theming.md`:

- **Emoji-labelled blockquotes** — `> **⭐ Key takeaway —** …`. Roles map to
  the site's `--role-*` colors via emoji: ⭐ key takeaway, 💡 why, 🔵 signal,
  ⚠️ production reality, 🚩 common mistake. Clean and identical in Colab + GitHub.
- Applied **1–2 per notebook** to the single strongest takeaway/mistake, only
  where the insight was buried in prose. Notebooks that already carry a
  practices table or checklist (tool-calling, llm-judge) were left alone.
- Real colored boxes would need inline-HTML `<div style=…>` (chosen against,
  for clean source) or the deferred HTML-hosting route (the only path to the
  walkthrough teal).

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
