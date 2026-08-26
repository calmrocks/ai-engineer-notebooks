# Case study A — Customer-support assistant, scoping to deployed (and the 2am page)

> **Reading, not an exercise.** This is a worked narrative that threads the whole
> repo together on one realistic scenario. The runnable code for each phase lives
> in the section it links to. Read it as the shape of the [capstone](../../12-capstone/README.md)
> — and of the "walk me through a project you built" interview round.

---

## The ask (what you actually get handed)

You're an FDE at a vendor. A mid-size SaaS company, **Northwind**, signs on. The
first call, their VP of Support says:

> *"Our team is drowning. Tickets are up 3x since we launched the new product and
> we can't hire fast enough. Can you AI something so customers get answers
> faster?"*

That's it. No spec, no dataset, no success metric. **This vagueness is the job**,
not a failure of the customer — and the gap between this sentence and a deployed
system is the entire case study.

> **🚩 Common mistake —** hearing "AI something" and immediately reaching for a
> framework and a vector DB. You don't yet know what "faster answers" means, what
> counts as *right*, or what it's worth. Build order is: scope → measure → build
> → serve → operate. Reaching for code first is how you ship the wrong thing fast.

---

## Phase 1 — Scope the fuzzy ask → [11 Customer craft](../../11-customer-craft/01-scoping-and-discovery.ipynb)

Before any code, run the discovery questions from section 11 and turn "AI
something" into a scoped, *evaluable* system.

Questions that change the design:
- **Who's the user — the customer, or the support agent?** Northwind's answer:
  *the agent*. This is a decision, not a detail — an agent-facing "draft a reply"
  tool has a human in the loop (lower risk, section 07) and a different UX than a
  customer-facing bot. You scope the agent-assist version.
- **Answers *from what*?** Their help center (≈1,200 articles) + past resolved
  tickets. That's your corpus — **real and messy** (duplicate articles, outdated
  ones, tribal knowledge only in tickets).
- **What's "right"?** Not "sounds good" — *the answer a senior agent would send,
  grounded in a real article*. That definition becomes your eval.
- **What's it worth?** Their number: cut median handle-time, deflect the top-20
  repetitive questions. That gives you a target and a budget.

The one-page **scoping doc** (section 11's artifact) comes out of this: user,
problem, in/out of scope, success metric, the demo you'll show in two weeks.

> **🔵 Interview signal —** leading with "who's the user and what counts as a
> correct answer?" before any architecture is the senior tell. It's also what
> makes everything downstream measurable.

---

## Phase 2 — Install the metric *before* building → [02 Evals I](../../02-evals-basics/01-measuring-outputs.ipynb)

Section 02's whole thesis: **put a number on "is it good" before you build the
thing you'd tune.** So the very next step — before retrieval, before any
model call — is a tiny **golden set**.

You sit with two senior agents for an afternoon and write down **40 real
questions** paired with the answer they'd actually send and the article it comes
from. That's the golden set. It is boring, manual, and the highest-leverage hour
of the project: every later decision (which retriever, which chunk size, whether
to ship) is now **a measurement, not an argument**.

> **⚠️ Production reality —** teams skip this because it feels like not-building.
> Then they "improve" the prompt for a week with no idea if it got better. The
> golden set is what turns that week into a graph.

---

## Phase 3 — Build retrieval, and watch it fail → [03 RAG](../../03-rag/00-what-is-rag.ipynb)

Now the RAG system, in the deliberate order section 03 teaches.

1. **Retrieve first** ([03/01](../../03-rag/01-embeddings-retrieval.ipynb)):
   embed the 1,200 articles, do vector search. It works on clean questions and
   **fails on Northwind's actual tickets** — customers paste error codes and
   product-specific jargon that embeddings miss (the vocabulary-mismatch pitfall).
2. **Add hybrid + rerank** ([03/02](../../03-rag/02-hybrid-and-reranking.ipynb)):
   BM25 catches the exact error codes vector search missed; a reranker fixes
   ordering. Your golden-set retrieval score jumps — *measured*, not assumed.
3. **Fix chunking last** ([03/03](../../03-rag/03-chunking.ipynb)): the help
   articles have long troubleshooting sections; naive chunking split a fix from
   its heading. You revisit chunk boundaries *now that you can see* which
   golden-set cases it breaks.

> **🚩 Common mistake —** treating "bad answers" as a generation problem and
> reaching for a bigger model. Section [03/04 (why RAG fails)](../../03-rag/04-why-rag-fails.ipynb)
> is explicit: it's almost always **retrieval**. Your golden set tells you which
> — a wrong answer whose right article never got retrieved is a retrieval bug, not
> a model one.

---

## Phase 4 — Make it an assistant, not just search → [05 Agents](../../05-agents/01-agent-loop-from-scratch.ipynb)

Retrieval finds articles; the agent *does something* with them. Northwind's
tickets often need a lookup ("is order #4021 shipped?"), so you give the model a
tool and a bounded loop.

- **The loop + a tool** ([05/01](../../05-agents/01-agent-loop-from-scratch.ipynb),
  [05/02](../../05-agents/02-tool-design.ipynb)): retrieve-article + an
  `order_status(order_id)` tool, wired into the raw loop.
- **Guardrails and a budget** ([05/03](../../05-agents/03-guardrails-and-budgets.ipynb)):
  max turns, a cost ceiling, and a **human gate** — this drafts a reply for the
  agent to approve, it does not send. That's the scoping decision from Phase 1
  paying off as a safety property.

> **💡 Why not a bigger agent —** most of Northwind's questions are "find the
> article and phrase the answer." That's barely an agent. You keep the loop small
> and reach for a tool only where the task genuinely branches (the order lookup).
> Section [05/03](../../05-agents/03-guardrails-and-budgets.ipynb)'s
> pipeline-beats-agent caution applies even inside this build. *(Case study C
> takes that judgment call all the way — when to drop the agent entirely.)*

---

## Phase 5 — The differentiator: rich evals → [04 Evals II](../../04-evals/01-golden-sets.ipynb)

Phase 2's golden set measured retrieval. Now you measure **answer quality**, the
thing Northwind actually pays for.

- **Grow the golden set** ([04/01](../../04-evals/01-golden-sets.ipynb)) to cover
  the top-20 question types + known hard cases.
- **LLM-as-judge** ([04/02](../../04-evals/02-llm-as-judge.ipynb)): "is this
  answer grounded in the retrieved article and does it match the senior-agent
  reply?" — with the judge's own failure modes (verbosity bias, self-preference)
  kept in mind, and spot-checked against human labels.
- **Regression eval as a gate** ([04/03](../../04-evals/03-regression-evals.ipynb)):
  wire it into CI so a prompt or model change that drops quality **fails the
  build**. This is the piece that will save you in Phase 8.

> **🔵 Interview signal —** "we had an LLM-judge eval gate in CI, spot-checked
> against human labels" is the line that separates an engineer who *built a demo*
> from one who *shipped a system*. It's also the honest answer to "how did you
> know it was good?"

---

## Phase 6 — Serve it → [09 Serving](../../09-serving-inference/01-serving-frameworks.ipynb) + [10 System design](../../10-ml-system-design/01-designing-an-inference-service.ipynb)

Northwind has ~200 agents, bursty during business hours. You size it with the
section-10 method:

- **Managed endpoint or self-host?** At this volume a **managed API** (the Groq/
  OpenAI-compatible seam the whole repo uses) is cheaper and less work than
  standing up GPUs — [09/01](../../09-serving-inference/01-serving-frameworks.ipynb)'s
  default. You note the self-host-on-vLLM path for when volume justifies it.
- **Sizing the numbers** ([10/01](../../10-ml-system-design/01-designing-an-inference-service.ipynb)):
  peak concurrent agents → QPS → tokens/s → cost/month, with a prompt cache for
  the repeated system preamble and article context.

> **⚠️ Production reality —** the interviewer will push "what at 10x?" Because you
> sized it (Phase 6) you answer with a lever, not a redesign: more replicas, or
> self-host on vLLM when the managed bill crosses the GPU break-even.

---

## Phase 7 — Ship the demo → back to [11 Customer craft](../../11-customer-craft/01-scoping-and-discovery.ipynb)

Two weeks in, you demo to Northwind — **on their real tickets, live**, not a
cherry-picked script (section 11's demo discipline). You show the eval numbers,
not just vibes: "on 60 real questions, 82% matched a senior-agent reply, grounded
in a real article; here are the 11 it got wrong and why." Honest failure cases
build more trust than a flawless scripted run.

You wire in **observability** ([08/01](../../08-operations/01-observability-and-llmops.ipynb))
at launch: trace every call, log prompts safely (no customer PII — ties to
[07](../../07-security/01-prompt-injection-and-trust.ipynb)), track cost/latency/
error rate. It goes live to a pilot group of 20 agents.

---

## Phase 8 — Two weeks later, the 2am page (build → **debug**)

The system was working. Now the pilot agents report: **"the answers went weird."**
Quality is down, nobody deployed a model change, and the eval gate in CI is
green. This is the other half of the job — **diagnosing a live regression** — and
it's where the observability and evals you built earn back their cost.

**The diagnosis, as a decision tree** (this is the reusable skill, not the
specific bug):

1. **Reproduce it with a number, not a vibe.** Run the [04 regression eval](../../04-evals/03-regression-evals.ipynb)
   against *production* — not the frozen CI copy. Quality score has dropped from
   82% to 61%. Real, and now measured.
2. **Retrieval or generation?** ([03/04 lens](../../03-rag/04-why-rag-fails.ipynb))
   Pull traces ([08/01](../../08-operations/01-observability-and-llmops.ipynb))
   for the failing cases. The model's answers are fine *given* what it retrieved
   — but the retrieved articles are wrong/empty. **It's retrieval**, not the model.
3. **What changed, if not the code?** The system is identical. What changed is the
   **data**: Northwind's team did a big help-center cleanup — re-titled and merged
   articles. The embeddings index is now **stale**: it points at article chunks
   that were rewritten, so retrieval returns near-misses.
4. **The root cause:** nobody re-indexed after the content migration. The RAG
   system has a **data freshness dependency** no one owned.

**The fix, and the lesson:**
- Immediate: re-embed the updated corpus; the eval score recovers.
- Durable: add a **re-index step** to the content-publishing workflow, and a
  cheap **canary eval** that runs the golden set against production daily — so the
  next drift pages you at a *dashboard*, not from a frustrated pilot agent. This
  closes section [08/01](../../08-operations/01-observability-and-llmops.ipynb)'s
  observe → eval loop for real.

> **🚩 Common mistake —** assuming a quality regression means "the model got
> worse" or "someone changed the prompt." In a RAG system the most common cause is
> **the data moved and the index didn't** — a green CI gate can't catch drift it
> never sees. The build skill is wiring it; the debug skill is knowing to suspect
> the data boundary first.

> **🔵 Interview signal —** "our CI eval was green but production quality dropped,
> because the corpus was re-indexed upstream and our vectors went stale — we added
> a production canary eval" is a *senior* war story. It shows you distinguish
> offline eval from production monitoring, and that you think in terms of data
> dependencies, not just code.

---

## What this case exercised

One scenario, most of the repo — and both halves of the job:

| Phase | Section | Skill |
|---|---|---|
| Scope the ask | [11](../../11-customer-craft/01-scoping-and-discovery.ipynb) | discovery, the scoping doc |
| Metric first | [02](../../02-evals-basics/01-measuring-outputs.ipynb) | golden set before building |
| Retrieval | [03](../../03-rag/00-what-is-rag.ipynb) | RAG, hybrid, chunking, failure diagnosis |
| Assistant | [05](../../05-agents/01-agent-loop-from-scratch.ipynb) | agent loop, tools, guardrails |
| Quality gate | [04](../../04-evals/01-golden-sets.ipynb) | LLM-judge, regression-as-CI |
| Serve & size | [09](../../09-serving-inference/01-serving-frameworks.ipynb), [10](../../10-ml-system-design/01-designing-an-inference-service.ipynb) | managed vs self-host, sizing math |
| Security | [07](../../07-security/01-prompt-injection-and-trust.ipynb) | untrusted tickets, safe logging, human gate |
| Launch + demo | [11](../../11-customer-craft/01-scoping-and-discovery.ipynb), [08](../../08-operations/01-observability-and-llmops.ipynb) | honest demo, tracing |
| **The 2am page** | [08](../../08-operations/01-observability-and-llmops.ipynb), [04](../../04-evals/03-regression-evals.ipynb), [03/04](../../03-rag/04-why-rag-fails.ipynb) | **diagnosing a live regression** |

> **⭐ Key takeaway —** you were never missing the pieces; you built them across
> sections 00–11. A real project is where you *compose* them under a customer's
> constraints, ship honestly, and — the half most portfolios skip — **keep it
> working after launch.** That arc, told clearly, is the strongest thing you can
> bring to an interview. Now go build your own: the [capstone](../../12-capstone/README.md).
