# Notebook theming & callout conventions

How these notebooks align with the [calm.rocks](https://www.calm.rocks) visual
system, and the constraints that shape what's possible.

## The hard constraint

A `.ipynb` is rendered by **Colab** and **GitHub**, and both control their own
CSS: they strip `<style>` blocks and `class` attributes from markdown cells.
So the website's actual theme (paper/ink palette, Inter + JetBrains Mono, the
walkthrough **teal** per-format accent) **cannot** apply to a raw notebook.
Those only render if a notebook is exported to HTML and served on calm.rocks
with `global.css` attached (see "Hosting, later").

What *does* travel across viewers: **content structure** and **callouts**.

## Callouts: emoji-labelled blockquotes (no `[!ALERT]` syntax)

Important gotcha, learned the hard way: **GitHub's notebook (`.ipynb`) renderer
is NOT its markdown-file renderer.** The `[!NOTE]`/`[!WARNING]` alert extension
works in `.md` files, issues, and READMEs, but **not** inside a rendered
notebook, and **not** in Colab either. In both notebook viewers, `[!NOTE]`
shows as literal text on a plain blockquote. So we do **not** use it.

Instead: a plain blockquote led by an **emoji + bold label**. Clean and
identical in Colab and GitHub; the emoji carries the role even without color.

```markdown
> **⚠️ Production reality —** the usage chunk arrives last; drop it and you lose the bill.
```

Role → emoji → meaning (emoji stands in for the site's `--role-*` colors):

| Role (site color) | Emoji | Use it for |
|---|---|---|
| Key takeaway (purple) | ⭐ | the one thing to remember |
| Why (green) | 💡 | the good reason / positive |
| Interview signal (blue) | 🔵 | info the loop rewards |
| Production reality (amber) | ⚠️ | what bites in prod |
| Common mistake (red) | 🚩 | anti-pattern / danger |

Rules:
- Keep callouts **rare**, 1–3 per notebook. They lose force if every paragraph is boxed.
- Always `> **<emoji> <Label> —** <text>`.
- Don't repurpose a role's emoji/meaning.

**The only way to get real colored boxes in a raw notebook** is inline HTML with
inline `style=` (a `<div style="border-left:4px solid #d1242f;…">`) using the
site hexes. It renders in both viewers but puts raw HTML in the cells. We chose
*not* to, favoring clean source; revisit if colored boxes become worth it.
When the notebooks are hosted as HTML (below), the emoji-labelled blockquotes
can be upgraded to the site's real colored callouts via `global.css`.

## Diagrams: code-fenced box-art, NOT Mermaid

Same trap as `[!NOTE]`, same reason. **Mermaid does not render in either target
viewer:** GitHub's `.ipynb` renderer is not its markdown-file renderer (Mermaid
works in `.md`/issues/PRs, *not* in a rendered notebook), and Colab has never
rendered Mermaid in a markdown cell. A ```` ```mermaid ```` block shows as **raw
source in both**, strictly worse than plain text. So we don't use it.

What renders as a real diagram, statically, in *both* Colab and GitHub:

- ✅ **ASCII / Unicode box-art in a fenced block** — the default. Zero
  dependencies, editable as text, diffs cleanly. Box-drawing glyphs
  (`┌ │ └ ─ ▶ ·`) are fine; they render width-1 in the monospace font both
  viewers use for code fences (this is the repo's existing idiom).
- ✅ **A committed image** (`![](…/foo.svg)`) or a **`mermaid.ink` image URL** —
  portable, but adds an asset / external dependency and stops being editable in
  place. Reach for these only when box-art genuinely can't express the shape.

Rules for box-art:
- **Align to a fixed interior width.** Pad every interior line to the same width
  so both walls and all four corners land on the same columns. Generate it with
  a tiny script rather than eyeballing; see how `05/06-harness-engineering` was
  built. Verify the left/right border columns match on *every* line, corners
  included.
- **Avoid ambiguous-width glyphs** where alignment matters: circled digits
  (`①②③`) and many emoji can render 2-wide and silently break the grid. Prefer
  `(1) (2) (3)`. Box-drawing and arrow glyphs are safe.
- If a diagram ever looks misaligned in Colab specifically, fall back to the
  **pure-ASCII** variant (`+---+`, `-->`, `[1]`): zero ambiguous-width glyphs.

## Content structure: the walkthrough shape

Mirror the site's walkthrough progression so a reader always knows where they are:

1. **What it is** — the concept and the concrete scenario, before any code.
2. **How it works** — the mechanism / the "ladder" or pipeline, often an at-a-glance table.
3. **Details** — the depth: each stage, its failure modes, demonstrated live.
4. **Practices & anti-patterns** — the ✅/❌ recap table (see best-practices doc).
5. **Exercises** — do-them-before-moving-on.

## Hosting, later (the only way to get the teal)

To get the walkthrough teal accent + clean colored callouts in *every* viewer,
export to HTML and serve on the site:

1. `jupyter nbconvert --to html --template lab <nb>.ipynb`
2. Inject `calm.rocks/src/styles/global.css`; wrap the body in
   `<article class="prose-article doc-format-walkthrough">` so the teal
   `--doc-accent` and themed tables apply.
3. Publish under an Astro route like `/notebooks/<section>/<name>`.
4. Keep the Colab badge pointing at the `.ipynb` for the runnable copy.

Deferred by decision: markdown-first now; revisit hosting if the notebooks
should become first-class pages on the site.
