# Notebook theming & callout conventions

How these notebooks align with the [calm.rocks](https://www.calm.rocks) visual
system, and the constraints that shape what's possible.

## The hard constraint

A `.ipynb` is rendered by **Colab** and **GitHub**, and both control their own
CSS — they strip `<style>` blocks and `class` attributes from markdown cells.
So the website's actual theme (paper/ink palette, Inter + JetBrains Mono, the
walkthrough **teal** per-format accent) **cannot** apply to a raw notebook.
Those only render if a notebook is exported to HTML and served on calm.rocks
with `global.css` attached (see "Hosting, later").

What *does* travel across viewers: **content structure** and **callouts**.

## Callouts — dual format (GitHub alert + emoji label)

The site themes the five GitHub-alert roles with fixed meanings. GitHub renders
`[!NOTE]` etc. as colored boxes that already match the site; **Colab does not**
(it shows the literal `[!NOTE]` text). Since these notebooks open mainly via the
Colab badge, we author callouts in a **dual format**: the alert keyword (for
GitHub + future hosting) *plus* an emoji-labelled bold lead (so the role still
reads clearly on Colab).

```markdown
> [!WARNING]
> **⚠️ Production reality —** the usage chunk arrives last; drop it and you lose the bill.
```

Role → emoji → meaning (matches the site's `--role-*` colors):

| Alert | Site color | Emoji | Use it for |
|---|---|---|---|
| `[!IMPORTANT]` | purple | ⭐ | **Key takeaway** — the one thing to remember |
| `[!TIP]` | green | 💡 | **Why** — the good reason / positive |
| `[!NOTE]` | blue | 🔵 | **Interview signal / info** |
| `[!WARNING]` | amber | ⚠️ | **Production reality** — what bites in prod |
| `[!CAUTION]` | red | 🚩 | **Common mistake / anti-pattern** |

Rules:
- Keep callouts **rare** — 1–3 per notebook. They lose force if every paragraph is boxed.
- Lead line is always `**<emoji> <Label> —** <text>` so Colab readers get the role even without color.
- Don't repurpose a role's meaning (the site enforces this too).

## Content structure — the walkthrough shape

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

Deferred by decision — markdown-first now; revisit hosting if the notebooks
should become first-class pages on the site.
