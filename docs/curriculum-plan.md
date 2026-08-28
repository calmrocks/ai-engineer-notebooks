# Curriculum plan & design log

Working notes on the structure of this repo: why the sections are what they
are, what was researched, what was decided (and rejected), and what's still
open. Kept so the reasoning survives even if the conversation context is lost.

Last updated: 2026-08-17.

## What this repo is

Runnable Colab notebooks teaching the **FDE / AI Engineer** applied-LLM stack,
framework-free, on the **free Groq API**. Hands-on companion to the
[transition plan](https://www.calm.rocks/resources/career-development/transition-fde-ai-engineer/).
Shared `aien` package (repo root) handles setup; one shared RFC corpus runs
through RAG + evals so evals measure the retrieval you actually built.

## Current structure (13 sections)

```
00 Setup            environment, keys, cost hygiene, spend guard
01 Model APIs       prompting fundamentals, structured output, tool calling, streaming, context/caching+batch
02 Evals I          NEW — "measure before you tune" on the 01 extraction task (no RAG dep)
03 RAG              what-is-rag → embeddings → hybrid/rerank → chunking → why-rag-fails
04 Evals II         golden sets, LLM-as-judge, regression-as-CI (coupled to RAG)
05 Agents           loop from scratch, tool design, guardrails/budgets, MCP, skills, harness engineering
06 Adaptation       fine-tune vs RAG vs prompt; LoRA/QLoRA; optional GPU LoRA appendix
07 Security         prompt injection (direct+indirect), OWASP LLM Top 10, trust boundary
08 Operations       observability/LLMOps; reliability/fallbacks; experiment tracking & registry (MLflow)
09 Serving & perf   NEW — serving frameworks (vLLM/TGI/Triton/TensorRT-LLM); inference performance; concept + GPU appendix
10 ML system design NEW — designing an inference service (QPS/VRAM/latency/cost, scaling, SLAs); concept, no code
11 Customer craft   scoping/discovery, scoping-doc template, demo discipline (was 09)
12 Capstone         deployed project brief (not a notebook) (was 10)
```

RAG internal order is deliberate (**retrieval before chunking**): you can't
judge a chunking strategy until you've seen retrieval succeed/fail on it, and
an RFC (~40k tokens) can't be embedded whole (model window ~256 tokens), so
chunking's *necessity* is shown in 03/embeddings, its *craft* deferred to
03/chunking.

## AI-systems track added (2026-08-25): sections 09 & 10, 08/03

Driven by a goal shift: package a resume-ready **AI distributed-systems /
application** internship experience: modern stack (RAG+LLM, LangChain,
vLLM/Triton/TensorRT, MLflow, LoRA), *use frameworks* rather than implement from
scratch, with **ML system design + performance** added; student is not on an
algorithms track, so no modeling depth.

Tension resolved by **layering, not reversing** the framework-free rule (which
still governs the teaching notebooks 00–08, and is itself the strongest
interview answer: "hand-wrote the loop to understand it, *then* reached for the
framework knowing what it buys"):

- **08/03 Experiment tracking & registry (MLflow)** — runnable; logs the
  section-04 eval harness's runs/params/metrics, registers + stage-promotes a
  model. Turns "I ran an eval" into a tracked workflow. [candidate 4]
- **09 Serving & inference performance** — NEW section. 09/01 *Serving
  frameworks* (vLLM/TGI/Triton/TensorRT-LLM: what each optimizes, maps onto the
  OpenAI-compatible seam, when to pick which); 09/02 *Inference performance*
  (continuous batching, KV cache, quantization, throughput-vs-latency, sizing
  math). Concept-first + **optional fenced Colab-T4 vLLM appendix** (same fence
  discipline as the 06 LoRA appendix; Groq is inference-only, can't self-host).
  [candidate 1]
- **10 ML system design & performance** — NEW section. 10/01 *Designing an
  inference service*, the ML-system-design interview worked end to end
  (QPS/VRAM/latency/cost estimation, replica scaling, queueing, caching, SLAs).
  Concept, no runnable code (fence like 05/04 MCP). [candidate 2]
- **Framework-bridge concept beats** (candidate 3) — DONE. A "Where the
  frameworks come in" markdown cell appended before Exercises in **03/04**
  (LangChain & LlamaIndex: RAG is a pattern not a library; every 03 failure mode
  happens inside the framework too) and **05/06** (LangChain & LangGraph, where the
  AgentExecutor/state-graph IS the loop you hand-built; LangGraph = persist the
  harness). Continues the repo's "what frameworks add" pattern (04/03, 05/01);
  gives resume keywords without reversing framework-free. No new notebooks.
- Candidates 5–7 (Agile/Scrum role-play doc, capstone rewrite for the framework
  stack, interview-acceptance rubric) deferred by user. **5 & 7 dropped, 6
  (capstone rewrite) still wanted** but not in this batch.

**AI-systems track build: COMPLETE** (2026-08-25). Shipped: 08/03 (MLflow, ran
green on 3.1.4), 09/01 + 09/02 (serving + perf, concept + GPU appendix), 10/01
(system design, concept), framework-bridge cells in 03/04 + 05/06, and the
**capstone (12) rewrite** — added a "use the modern stack" table (LangChain/
LlamaIndex/LangGraph, vLLM/TGI, LoRA, MLflow) mapped to teaching sections, a
systems-thinking section (09–10 sizing/perf numbers), reliability/cost, and a
**team/Agile-Scrum + roles** section (PM/EM/AIML/Platform/SRE/QA role table,
mentor role-play, resume process+impact bullet, interview-readiness checklist).
This delivers candidate 6 and the original goal's role-narrative ask. Candidates
5 & 7 remain dropped. **No open work on this track.**

Full-repo check after the track (2026-08-25): all 30 notebooks parse + every
code cell compiles; badge URLs match paths; all internal cross-links + README
links resolve; no residual 09-customer-craft/10-capstone refs. Renumbering
verified clean.

09/01 vLLM appendix HARDENED (2026-08-26) after a real Colab-T4 run surfaced
three real serving-stack failures, now handled in the notebook itself: (1)
vLLM upgrades torch → Colab's stale `torchaudio` has a mismatched CUDA version
and crashes the server at import (transformers imports it unconditionally); fix
= uninstall torchaudio. (2) A leftover EngineCore from a failed attempt holds
the whole GPU → "Free memory … less than desired GPU memory utilization"; fix =
kill stale procs / restart runtime + `--gpu-memory-utilization 0.85`. (3) Server
launched with logs to DEVNULL → blind timeouts; fix = log to a file + print the
tail on exit, `--enforce-eager`. Added an explicit cleanup cell (`server`
terminate + pkill + nvidia-smi). Confirmed end-to-end: TinyLlama served on a T4,
same OpenAI client returned a completion. These gotchas are framed as the
section-09 lesson (self-hosting = dependency + resource management), not hidden.

Renumbering: Customer craft 09→**11**, Capstone 10→**12** (only 3 refs updated:
README ×2 + the moved notebook's own badge; no other cross-links pointed at
them). New sections slot in after Operations because serving/perf/design are
"make it real" concerns, same rationale that put security/ops late.

Build status (2026-08-25): skeleton + **09/01 built and validated** (14 cells,
compiles, links resolve except the forward ref to 10/01). Still to build: 09/02,
10/01, 08/03, the framework-bridge beats, capstone rewrite.

## Research consulted

- **OWASP LLM Top 10 (2025)** — prompt injection is #1; drove section 07.
- **MCP** (modelcontextprotocol.io) — now a standard (Claude/OpenAI/VS Code/
  Cursor); folded into agents as concept-only (repo avoids frameworks).
- **PEFT / LoRA / QLoRA** (HuggingFace) — mainstream, runs on free Colab T4.
- **RAG canon** — Lewis et al. 2020, AWS, Pinecone, Prompting Guide. Settled
  that RAG ≠ embeddings (retrieval can be vector/BM25/hybrid/SQL/API).
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
   appendix, matching the plan ("conceptually only") without ignoring LoRA's rise.
6. **Security after agents; ops after security** — cross-cutting "make it real"
   concerns need a real system to be meaningful. Both evaluators endorsed.

## Explicitly rejected

- Multimodal / multi-agent as hands-on core modules (see #3).
- Standalone prompt-engineering *hero module* (both evaluators warned it breeds
  cargo-cult tricks). BUT an audit (2026-08-20) found the intended "woven in"
  fold-in never actually happened: prompting was *used* everywhere, *taught*
  nowhere. Fixed by adding `01-model-apis/00-prompting-basics` (fundamentals as
  the on-ramp to structured output: clear instructions, few-shot, format specs,
  CoT, tied to the eval habit, anti-cargo-cult). Not a hero module; a short
  front-of-section fold-in, which is what the plan intended all along.
- Fine-tuning internals / RLHF / classical ML / agent-framework deep-dives
  (plan says skip).
- Data-pipeline / deploy-infra notebooks (that's the capstone's job).

## Phase 2: DONE (2026-08-17)

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

## Harness-engineering notebook added (2026-08-25)

- New **05/06-harness-engineering** (runnable; reuses section 01's FS/tools/loop
  on Groq). Names the third axis alongside prompt-engineering (the message) and
  model-adaptation (the weights): **harness engineering = the scaffold around the
  call**. Framed as a *synthesis* closer: an explicit table reframes 01–05 as
  harness components (loop / tool-input / bounds / external-tools / packaged
  know-how), then teaches the three levers the section left implicit: **(1)
  context assembly & compaction** (window = per-turn budget you rebuild; keep
  task+recent+commitments, summarize the middle), **(2) tool-result shaping** (the
  *return* side of nb-02: truncate blobs head+tail, make errors actionable, wired
  via a `shape_result` seam added to the compact loop), **(3) verification loops**
  (harness computes ground truth in code and loops on failure; nb-03's
  trajectory-eval pointed at the output). Closes with an ASCII harness diagram
  ("model is fixed; everything else is code you own") and the rule *fix the
  harness before reaching for a bigger model / fine-tune (§06)*. Does NOT reopen
  decision #3: single-agent context/scaffold engineering, not orchestration.
  README + best-practices 05 table + this log updated; all internal links
  verified. Static-only per standing caveat (not executed, no key here); the new
  verification-loop cell makes real model calls, so flag it in the Colab pass.

## Skills notebook added (2026-08-23)

- New **05/05-skills-and-progressive-disclosure** (concept-only, no runnable code,
  same fence as MCP: Skills live in an agent host, not a raw Groq
  `chat.completions` call). Closes a real gap: the repo taught tools, the agent
  loop, and MCP, but not how to *package reusable know-how* an agent loads on
  demand. Framed **pattern-first** (progressive disclosure / "context is a
  budget") with Anthropic's `SKILL.md` as the concrete instance. This was
  deliberate, because the format is now an **open standard** (agentskills.io) adopted across
  vendors (OpenAI Codex, Gemini CLI, editors), so it's a durable pattern, not a
  vendor feature. Spine is the trio **Tools *act* / MCP *connects* / Skills
  *package***. Cross-linked from 04-mcp; README + this doc updated. Details
  verified against live Anthropic/agentskills docs 2026-08-23: 6-field portable
  frontmatter (`name`, `description` required; no `version`), 3-level
  progressive disclosure (~100 tok metadata → <5k body → bundled files/scripts,
  scripts run via bash so only output enters context). This does NOT reverse
  decision #3 (multi-agent/multimodal stay off-spine): Skills is a
  single-agent context-management concept, not orchestration.

## Adaptation: FFT-vs-LoRA second axis (added 2026-08-23)

- Added a **"full fine-tuning vs LoRA"** cell to 06 (after "What LoRA is",
  before the provider paths): the umbrella framing (fine-tuning = category; FFT
  + LoRA = two methods), a comparison table (trainable params, VRAM, artifact
  size, catastrophic forgetting), and **why LoRA dominates** — multi-tenant
  serving (one frozen base + hot-swapped adapters) and accessibility (single
  GPU). Two AWS citations verified against live posts 2026-08-23: multi-LoRA
  vLLM serving on SageMaker/Bedrock (confirms swap-adapters-per-request; qual.
  "5×10%-GPU → 1 GPU"), and Bedrock Custom Model Import GA (confirms full/merged
  Safetensors only, so a LoRA must be merged in first, consistent with the
  existing cell-9 Bedrock note). Two new exercises (FFT-vs-LoRA judgment; design
  the multi-adapter serving story). Deliberately kept decision-framed, not an
  internals deep-dive: no optimizer/gradient math. Doubles down on the
  taxonomy precision from the [reframe below]; best-practices 06 table updated.

## Adaptation notebook reframe (added 2026-08-22)

- **06/fine-tune-vs-rag-vs-prompt** reframed around a *degree-of-model-modification*
  spectrum (prompt → RAG │ LoRA → full fine-tune; inputs vs weights) instead of
  popularity, plus a "pendulum" cell (fine-tune was the early default → field swung
  to prompt/RAG → fine-tuning specialized to style-at-scale + small-model
  distillation). Taxonomy precision added: LoRA is a *kind* of fine-tuning, not a
  peer. Hosted reference code expanded to a verified 3-tier split: **abstracted**
  (OpenAI, Bedrock: no LoRA knob) vs **explicit-LoRA** (Together, Fireworks:
  `lora=True`/`--lora-rank`) vs self-train (`peft`). All snippets reference-only.
  Provider APIs verified against live docs 2026-08-22; corrected a prior wrong
  claim that Bedrock yields a "LoRA endpoint" (Bedrock has no LoRA surface;
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

## Case-study backlog (planned 2026-08-26, not built yet)

Add end-to-end **case studies** — worked real-world narratives (concept-forward,
like 10/01), organized on TWO axes so they cover different *application types*,
not three variations of RAG-QA:
- **Axis 1 — use case** (customer support, document processing, security/eval, …)
- **Axis 2 — application type / technique** (RAG+agent build, pipeline decision,
  adversarial benchmark harness, classifier, semantic recommender, …)

Home decided (2026-08-26): section **12 renamed "Case Studies & Capstone"** (dir
`12-case-studies-and-capstone/`). Cases and the capstone brief now live together:
cases are the worked examples, the capstone is "now build your own." By case
nature: **narrative-heavy full-stack cases could be docs, but per user request A
is a RUNNABLE notebook**; self-contained cases (C, D) are runnable notebooks too.
The capstone brief stays docs (`CAPSTONE.md`): a notebook project signals
"weekend hacker"; a case study can be a notebook because it's a worked example,
the student's capstone must be a real deployed repo.

**Status:** A BUILT + RUNNABLE (2026-08-26) as
`12-case-studies-and-capstone/01-customer-support-assistant.ipynb` (28 cells,
needs a Groq key). Narrative preserved from the original draft, plus minimal
runnable code per phase on a 6-article corpus + 5-question golden set. The
Phase-8 regression is REAL: `index_corpus()` seam left stale after a corpus
migration → eval score drops → re-index → recovers. Section `README.md` (cases
then capstone) + `CAPSTONE.md` (renamed from the old capstone README). Old
`docs/case-studies/` removed; drafts deleted. All links verified. Static-only
here (no key); run in Colab to confirm like 06/09.

**C and D BUILT + RUNNABLE (2026-08-26)** as `02-...pipeline-vs-agent.ipynb` and
`03-red-team-robustness-benchmark.ipynb`. NOTE: case-study *letters* renumbered to
match file order: A (customer support), **B = contract extraction pipeline-vs-agent**
(was "C"), **C = red-team benchmark** (was "D"). B builds the same extraction task
as both an agent and a pipeline and proves with accuracy + token count that the
pipeline wins when steps are known (05/03's thesis, measured). C is a NEW system
type: an attacker→target→judge PAIR loop reporting ASR (generalized from the
user's résumé jailbreaker project); framed DEFENSIVELY on a harmless proxy task
("never reveal a secret passphrase"), with no real harmful content or transferable
jailbreaks. All three cases now listed in section README + main README; all
compile + links + badges verified. Case-study backlog COMPLETE (E/F still
deferred). All static-only (need Groq key); run in Colab to confirm.

**Locked into backlog (user picked A+C+D):**
- **A — Customer-support assistant, scoping → deployed** (flagship, DONE). Build angle;
  RAG + agent. Threads 11 scoping → 03 RAG → 02/04 evals → 05 agent (order
  lookup) → 07 injection defense (tickets are an attack surface) → 09 serving →
  08 observability → 11 demo. **Ends with a "two weeks later, answer quality
  collapsed, diagnose it" act** (the old "3am incident" idea folded in as A's
  final scene, using 08 tracing + 04 regression eval): covers build→debug in one
  arc. The living exemplar for the capstone.
- **C — Contract extraction: pipeline vs agent** (decision angle, lighter). The
  interview judgment call: the tempting agent vs the correct pipeline when steps
  are known; argue it with eval + cost numbers. Completes 05's
  "pipeline-beats-agent" thesis as a full worked case.
- **D — Red-team robustness benchmark** (adversarial harness / benchmark; a NEW
  application type for the repo: build a harness to *evaluate/attack* models, not
  serve one). Generalized from the user's real résumé project (a PAIR-loop
  jailbreaker: attack model → target → Llama-Guard judge, ~68% ASR). Composes 05
  loop + 04 LLM-as-judge + 07 security + 02 evals (ASR metric). Runnable on Groq
  (attack/target/judge all have Groq models incl. Llama Guard).

**Considered, deferred (E/F):** E, AI-generated-text / clickbait detection (LLM
classifier + eval; text version is on-thesis, image detection is multimodal =
off-thesis). F, semantic recommender + explanation (embedding retrieval + LLM
rerank; only on-thesis if framed as LLM/embedding recsys, not classical CF).

## Standing caveats

- **Most notebooks verified statically only** (JSON structure, code compiles,
  badges/cross-refs consistent), not executed here (no API key). Before treating
  any as final, run top-to-bottom in Colab. **Exceptions now verified live on a
  Colab T4 (2026-08-26): 06 LoRA appendix and 09/01+09/02 vLLM appendices**: see
  the [[colab-gpu-vllm-gotchas]] memory for the fixes applied. 08/03 MLflow ran
  green locally. Remaining highest risk: the live-call key-path notebooks (00–05,
  07, 08/01-02, 11) never executed end-to-end.
- **Models:** repo uses `openai/gpt-oss-120b` / `-20b` (current Groq production).
  Re-verify against Groq's model list if calls 404.
- **Colab has no repo checkout** → notebooks install `aien` via
  `pip install "git+https://github.com/calmrocks/ai-engineer-notebooks.git"`,
  pulling from `main` (latest). Breaking `aien` changes hit published notebooks.
