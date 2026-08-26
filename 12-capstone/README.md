# Capstone: the deployed project

The notebooks teach the skills; this project is what goes on your resume.
It is deliberately **not** a notebook — a notebook project signals
"weekend hacker" in a loop that screens for production judgment. Build it
as a real repo.

Full requirements and anti-patterns:
[Guide: Building a Real LLM Project for Your Resume](https://www.calm.rocks/resources/career-development/real-llm-project/).

## Non-negotiables

- **Real data** — a messy corpus or workflow, not a toy dataset.
- **A real user who isn't you** — a friend's business, a team at work, an
  open community. The FDE interview probes how you translated their fuzzy
  need into a system.
- **A serving component** — an API or app, deployed and linkable.
- **An eval methodology** — a written eval report; "it works" is not one.
- **A write-up** — the user's problem, the system, the eval results, what
  you'd do next. You should survive 15 minutes of hostile questioning on it.

## Strong shapes

1. RAG over a real messy corpus, with an eval report showing what you
   measured and what you fixed because of it.
2. An agent automating a real multi-step workflow, with guardrails and a
   cost budget.
3. An internal AI tool at your current job — adoption numbers beat
   architecture diagrams.

## Before you ship

Walk the [best practices & anti-patterns cheat sheet](../docs/best-practices-and-anti-patterns.md)
— the do/don't for the whole stack in one place. It's also the answer sheet
for the "what would you watch out for building this?" interview question. Make
sure your project is on the ✅ side of each row before you call it done.
