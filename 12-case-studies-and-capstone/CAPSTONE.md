# Capstone: the deployed project

The notebooks teach the skills; this project is what goes on your resume.
It is deliberately **not** a notebook: a notebook project signals
"weekend hacker" in a loop that screens for production judgment. Build it
as a real repo, deployed, that you can hand an interviewer a link to.

Full requirements and anti-patterns:
[Guide: Building a Real LLM Project for Your Resume](https://www.calm.rocks/resources/career-development/real-llm-project/).

**See it done first:** [Case study A](01-customer-support-assistant.ipynb) walks
one project (a customer-support assistant) from a vague ask all the way to
deployed and then *debugged in production*, with runnable code at each phase.
It's the shape of what you're about to build; read (and run) it before you start.

## Non-negotiables

- **Real data** — a messy corpus or workflow, not a toy dataset.
- **A real user who isn't you** — a friend's business, a team at work, an
  open community. The interview probes how you translated their fuzzy need
  into a system (section 11).
- **A serving component** — an API or app, deployed and linkable, that you
  can reason about under load (sections 09–10).
- **An eval methodology** — a written eval report, tracked over time; "it
  works" is not one (sections 02, 04, 08).
- **A write-up** — the user's problem, the system, the eval results, what
  you'd do next. You should survive 15 minutes of hostile questioning on it.

## Use the modern stack, don't reinvent it

The teaching notebooks were framework-free *on purpose*: you built the agent
loop, RAG, and evals from raw parts so you understand what every library is
doing. **The capstone is where you flip that** — assemble the real stack, and
be ready to explain, for each tool, *what it does and why you chose it*. That
"I built it by hand first, then reached for the framework" arc is itself a
strong interview answer.

A mainstream, resume-legible stack (pick what your project needs, not all of it):

| Layer | Reach for | Taught in |
|---|---|---|
| **RAG / orchestration** | LangChain, LlamaIndex, or LangGraph | 03 (+ bridge), 05 |
| **Serving / inference** | vLLM or TGI (self-host); a managed API to start | 09/01 |
| **Inference performance** | continuous batching, quantization, KV-cache sizing | 09/02 |
| **Fine-tuning (if it earns it)** | LoRA / QLoRA via PEFT | 06 |
| **Experiment tracking & registry** | MLflow: track every eval run, register the shipped model | 08/03 |
| **Observability** | tracing, safe logging, cost/latency metrics | 08/01 |

> You are **not** on an algorithms track; no one expects novel modeling. The
> hire signal is **AI distributed-systems / application engineering**: wiring a
> modern stack into a deployed, evaluated, operable system, and making the
> cost/latency/quality trade-offs consciously.

## Strong shapes

1. **RAG over a real messy corpus** — served behind an API (vLLM or a managed
   endpoint), with an MLflow-tracked eval report showing what you measured and
   what you changed because of it.
2. **An agent automating a real multi-step workflow** — guardrails, a cost
   budget, orchestrated with LangGraph, traced end to end.
3. **An internal AI tool at your current job** — adoption numbers beat
   architecture diagrams.

## Show the systems thinking (sections 09–10)

This is the layer that separates "called an API" from "owns the serving layer."
Put a short **system-design section** in your write-up:

- **Sizing** — the back-of-envelope from 10/01: expected QPS, tokens/request,
  therefore GPUs (or the managed-endpoint cost), and where it breaks at 10×.
- **Performance** — one lever you actually pulled and its measured effect
  (batching throughput, a quantization quality/latency trade, a prompt cache),
  tied to a number.
- **Reliability & cost** — retries/timeouts/fallbacks (08/02) and the monthly
  cost with the knob you'd turn to cut it.

Interviewers press on numbers. "≈40 peak QPS, ~2 GPUs at 70% util, ~$3k/mo,
halve it by quantizing" is a passing answer; "it's deployed on the cloud" is not.

## Simulate the team: roles, Agile/Scrum, and the resume story

This experience is meant to read on your resume as **an internship-grade project**,
which means it needs a *working-process* story, not just an artifact. Interviewers
ask "what was your role? how did the team work? how did you handle changing
requirements?" So build (or role-play with your mentor) a realistic delivery
process and know where you sat in it.

**Run it as sprints.** Two-week sprints with a backlog, sprint planning, a
standup cadence, and a retro. Track work as tickets (GitHub Issues/Projects is
fine). Even solo, narrate it as sprints; it's how the work actually gets
discussed in the interview.

**Know the roles, even if you wore several hats.** On a real team this project
would spread across:

| Role | Owns | In this project |
|---|---|---|
| **Product Manager** | the user problem, priorities, acceptance criteria | the scoping doc (section 11); what "good" means |
| **Tech Lead / EM** | architecture, breakdown, review | the system design (10); splitting work into tickets |
| **AI/ML Engineer** | prompts, RAG, agent, fine-tune, evals | most of 01–06; the eval harness |
| **Platform / MLOps** | serving, deploy, CI, tracking, registry | 08–09; MLflow, the deployment |
| **SRE / On-call** | reliability, monitoring, incident response | 08/02; the runbook |
| **QA / Eval owner** | the golden set, regression gate, sign-off | 02, 04; "is it safe to ship?" |

Pick the role you'll **claim** on the resume (usually AI/ML Engineer or a
blended AI-systems role), own it deeply, and be able to speak to how you handed
off to and depended on the others: that's the collaboration question.

> **Mentor role-play (recommended).** Have your mentor act as PM/stakeholder:
> hand you a vague ask, change a requirement mid-sprint, push back on a demo,
> and ask "why this architecture?" in a mock review. Rehearsing the *process*
> questions is as important as the technical ones; most candidates can describe
> the system but freeze on "how did the team decide that?"

**Put it on the resume as process + impact**, e.g.:
*"Built and deployed a RAG assistant over [real corpus] for [real user];
owned the AI/eval layer across 2-week sprints, served on vLLM with an
MLflow-tracked eval gate; cut answer cost 40% via retrieval tuning and
quantization, validated against a 50-case golden set."*

## Before you ship

Walk the [best practices & anti-patterns cheat sheet](../docs/best-practices-and-anti-patterns.md):
the do/don't for the whole stack in one place. It's also the answer sheet
for the "what would you watch out for building this?" interview question. Make
sure your project is on the ✅ side of each row before you call it done.

## The interview readiness check

Before you call the capstone done, make sure you can answer each of these cold.
They are the rounds the whole repo has been preparing you for:

- **Scoping** — "how did you turn the user's vague ask into this system?" (11)
- **Technical deep-dive** — "walk me through retrieval / the agent loop / your
  evals" and *why* each choice (03–06)
- **System design** — "how would you scale this to 100k users?" (09–10)
- **Operations** — "how do you know it's still working in production?" (08)
- **Security** — "what happens when a user pastes a prompt injection?" (07)
- **Collaboration / process** — "what was your role, and how did the team
  ship it?" (this page)

If any answer is shaky, that section's notebooks are where you go back.
