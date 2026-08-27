# Case Studies & Capstone

The teaching notebooks (00–11) each cover one skill. This final section is where
they come together into **projects** — first by watching a worked one, then by
building your own.

## Case studies — see it done, end to end

A **case study** takes one realistic scenario all the way through: a vague
customer ask, scoped, measured, built, served, and then **debugged in
production**. They're runnable where it teaches something a description can't —
so you can watch a quality score drop when an index goes stale, and recover when
you re-index.

| Case | Use case | Application type | The angle it teaches |
|---|---|---|---|
| [01 — Customer-support assistant](01-customer-support-assistant.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calmrocks/ai-engineer-notebooks/blob/main/12-case-studies-and-capstone/01-customer-support-assistant.ipynb) | Customer support | RAG + agent, **build → debug** | Scoping a fuzzy ask into a deployed, evaluated system — then diagnosing it when quality collapses after launch |
| C — Contract extraction *(planned)* | Document processing | **Pipeline vs agent** | The judgment call: when a pipeline beats an agent, argued with eval + cost |
| D — Red-team benchmark *(planned)* | Security / evaluation | **Adversarial harness** | Building a harness to *evaluate and attack* models, not serve one |

> **⭐ Key takeaway —** interviews and real work never hand you "implement a RAG
> pipeline." They hand you "our support team is drowning — help." The gap between
> those two sentences is the job. Case studies live in that gap.

## Capstone — now build your own

The case studies show *a* project. The **[capstone](CAPSTONE.md)** is *yours* —
the deployed repo that goes on your resume. It is deliberately **not** a
notebook: a notebook project signals "weekend hacker" in a loop that screens for
production judgment. A case study can be a notebook because it's a worked
example; your capstone must be a real, deployed repo.

**→ [Read the capstone brief](CAPSTONE.md)** for the non-negotiables, the modern
stack to reach for, the systems-thinking numbers to show, the Agile/Scrum role
story, and the interview-readiness checklist.
