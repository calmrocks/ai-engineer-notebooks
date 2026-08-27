# Contributing

Thanks for stopping by — feedback and contributions are welcome, and they're
what keep these notebooks working against a moving target (models and libraries
drift constantly).

## The most useful things you can do

- **Ran a notebook? Say so.** Open a [Discussion](https://github.com/calmrocks/ai-engineer-notebooks/discussions)
  and tell us which section, and whether it ran clean — especially the GPU
  appendices (06 LoRA, 09 serving), which depend on fast-moving libraries.
- **Hit an error or API drift?** Open a [Bug / API drift issue](../../issues/new?template=bug-or-api-drift.md).
  Include the library version — that's the single most useful detail, since these
  run against live APIs.
- **Want a topic covered?** Open a [Notebook / topic request](../../issues/new?template=notebook-request.md).

## Scope

This repo teaches the **applied-LLM stack an AI Engineer / FDE is hired and
interviewed on**, deliberately **framework-free** (raw APIs first), with **evals
as the spine**. Contributions that fit that thesis are the easiest to merge;
proposals to wrap everything in a framework are (politely) out of scope — the
point is to understand the layer under the frameworks. See the
[curriculum plan](docs/curriculum-plan.md) for the design rationale.

## Notebook conventions

- **Self-contained**: first cell installs, then `from aien import setup;
  client, MODEL = setup()`. No hidden state between notebooks.
- **Runs on the free Groq API**; GPU-only topics (LoRA, self-hosted serving) are
  concept-first with an optional, clearly fenced Colab-GPU appendix.
- **Ends with exercises.** Callouts follow the emoji-blockquote convention in
  [docs/theming.md](docs/theming.md).

If you're opening a PR, keep the diff focused and mention which notebook(s) you
ran it against.
