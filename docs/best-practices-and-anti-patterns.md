# Best practices & anti-patterns

The do/don't for the whole applied-LLM stack, in one place — harvested from the
notebooks and organized by section. Two uses:

- **Pre-interview review.** "What would you watch out for building this?" is a
  real system-design / customer-scenario question. This is the answer sheet.
- **Pre-capstone checklist.** Before you ship the resume project (section 10),
  walk this and make sure you're on the ✅ side of each row.

Anti-patterns sit next to the practice they violate on purpose — the mistake is
the fastest way to remember the rule. Each section links to where it's taught.

---

## 00 — Setup & the non-determinism mindset

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Treat the model as **probabilistic** — same input can give different output | Assume "it worked once" means it works; eyeball-and-ship |
| Keep keys in Colab Secrets / env vars | Paste an API key into a cell (it gets committed/screenshotted) |
| Wrap calls in a spend guard; know your per-token cost | Run unbounded loops against a paid key and find out via the invoice |
| Default to the largest model while iterating; drop to a small one for bulk | Use the biggest model for everything "to be safe" |

## 01 — Model APIs

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Force **tool/function calling** for structured output — schema as code | "Just ask for JSON" and hope; parse prose with regex forever |
| Validate business rules in your code, retry with the error fed back | Trust `strict:true` (uneven support) as your only guard |
| Write tool **descriptions** that state *when* to call — they're prompts | Vague descriptions ("does math"); the model under/over-triggers |
| Stream for UX; always capture the final usage/`x_groq.usage` chunk | Drop the tail chunk and lose the billing record |
| Reserve output headroom; budget the four context lines | Fill the context window "because it fits"; pay for cost creep |

## 02 / 04 — Evals (the spine)

| ✅ Do | ❌ Anti-pattern |
|---|---|
| **Measure before you tune** — a golden set + a number gate every change | Tune a prompt/chunk-size/model by vibes and one lucky output |
| Pin only machine-checkable fields; cover the cases you *fear* | Golden set of only happy-path cases; brittle exact-string matching |
| Judge with a *different, cheaper* model; anchor scores to a rubric | Let a model grade its own output; unanchored 1–5 (everything's a 3.5) |
| Reasoning-before-score in the judge; calibrate against human labels | Score-first (post-hoc rationalization); ship on an uncalibrated judge |
| Two gate types: budget gates (noisy aggregates) + zero-tolerance (must-never-ship) | One global threshold; block merges on single-case flakiness |
| Every production failure becomes a new golden-set case | Fix the bug, don't capture it; hit it again next month |

## 03 — RAG

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Remember RAG = *retrieve then generate*; retrieval is swappable | Conflate "RAG" with "embeddings/vector DB" — keyword/SQL/API count too |
| When an answer is wrong, **check retrieval first** | Blame the model and start rewriting the prompt |
| Clean the corpus before chunking; junk in → junk embeddings | Embed raw docs with page furniture / boilerplate |
| Prefer structure-aware chunking when the corpus has structure | Fetishize chunk-size tuning before you can measure retrieval |
| Add hybrid/rerank only when an eval says it earns its cost | Stack retrieval stages because each "sounds reasonable" |
| Make the model decline when the corpus doesn't cover the question | Let it answer confidently from pretraining, uncited |

## 05 — Agents

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Reach for a **pipeline** when the steps are known ahead of time | Wrap every task in an autonomous agent (a pipeline in a trench coat) |
| Bound every loop: max_turns, cost, wall-clock, loop detection | Unbounded loop against a paid key; "it usually stops" |
| Human-gate destructive/irreversible actions; deny by default | Let the agent delete/send/pay without confirmation |
| Least privilege per tool; scope tightly, enforce the *user's* perms | A `run_sql`/`run_shell` mega-tool the model can point anywhere |
| Grade the **trajectory** (tool path), not just the final answer | Accept a right-looking answer reached by an insane, costly path |
| Fail loud with a status + partial trace | Silently truncate and return partial work as done |
| Know MCP maps to the raw tool loop; adopt when integrations justify it | Reach for a framework before you understand the loop it wraps |
| Package *occasional, detailed* know-how as a **skill** (loaded on demand); keep always-relevant lines in the prompt | Stuff every playbook into the system prompt and pay for all of it every turn |
| Write the skill **`description`** for the model — what it does *and when to use it* | Vague description, then wonder why the skill never triggers |
| Push fragile logic into a bundled, validated **script** (only its output costs context) | Make the model re-derive the same brittle procedure in-context each time |
| Treat installed skills as trusted code; review third-party ones (see 07) | Install a public skill and assume its body/scripts are safe |

## 06 — Adapting the model

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Order the levers: **prompt → RAG → fine-tune**, advance only on eval failure | Fine-tune first because it "sounds like real ML" |
| Fine-tune for style / format / narrow-task cost — behavior, not facts | Fine-tune to add knowledge (that's RAG's job — stale, uncitable) |
| Default to **LoRA** over full fine-tuning: cheap, single-GPU, swappable adapters, less forgetting | Full-fine-tune by default; reserve it for drastic change (new language, deep reasoning) |
| Serve many variants as one frozen base + hot-swapped adapters | Stand up a separate full model per task and pay for idle GPUs |
| Prove the fine-tune beat prompt+RAG with the same eval harness | Ship a fine-tune because it *feels* better; no before/after number |
| Prefer a hosted fine-tuning API unless you need full control | Stand up a GPU training stack for a decision you'll make twice |

## 07 — Security

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Treat **all** model-visible text as attacker-controllable (incl. RAG/tools) | Trust retrieved docs or tool output as safe |
| Validate/whitelist model **output** before any sink (DB, shell, HTML, send) | Pass raw model output into a consequential action |
| Least privilege + human-in-loop; assume the model *will* be hijacked | Rely on the system prompt as a security boundary (it leaks) |
| Keep secrets/PII out of context; redact before logging | Put keys/other-users' data in the prompt "just in case" |
| Defense in depth — no single failure is catastrophic | Believe any single "prompt-injection fix" makes you safe |

## 08 — Operations

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Trace every call (in/out/tokens/latency/status); sample full payloads | Log nothing, or log raw prompts (a quiet PII spill) |
| Track p50 **and** p95/p99; alert on deltas, not absolutes | Watch only the mean; miss the tail users actually feel |
| Retry transient errors with backoff+jitter; fail fast on 4xx | Retry everything, or nothing; synchronized thundering-herd retries |
| Timeout + fallback model + graceful degradation; emit a `degraded` metric | Let a hung call block a user; return a raw 500/exception |
| Validate output as a reliability check (200 ≠ usable) | Assume HTTP 200 means the response is parseable/usable |
| Feed production failures back into the eval set (the flywheel) | Treat observability as dashboards you look at once |

## 09 — Customer craft (FDE)

| ✅ Do | ❌ Anti-pattern |
|---|---|
| Turn a vague ask into a scoped, *numeric* success metric before building | Start building "AI for X" before you know what success means |
| Ask about the current workflow and where it breaks | Ask "what do you want the AI to do?" and take the fog answer |
| Let the cost-of-being-wrong drive the guardrail/eval depth | Same architecture regardless of stakes |
| Ship the smallest useful slice; name what's out of scope | Boil the ocean; unbounded scope creep |
| In the demo, say clearly what it **can't** do | Over-claim; the impressive-but-brittle demo that dies in prod |

---

## The five that matter most

If you internalize nothing else:

1. **Measure, don't eyeball** — a golden set + a number is what makes everything else safe to change.
2. **Retrieval-first debugging** — bad RAG answers are almost always a retrieval problem.
3. **Pipeline before agent** — autonomy is the expensive last resort, not the default.
4. **Model output is untrusted input** — validate before any consequential sink.
5. **Prompt → RAG → fine-tune** — advance only when the cheaper lever fails an eval.
