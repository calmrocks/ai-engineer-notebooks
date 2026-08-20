"""Shared setup for ai-engineer-notebooks.

One job: load the Groq API key (Colab Secrets or env var) and hand back a
ready client plus the default model. This is the block every notebook used
to inline — centralized so a change lands in one place.

Deliberately tiny. The notebooks teach the raw API; this only removes the
copy-pasted credential boilerplate, not any concept worth learning. See
00-setup/00-environment.ipynb for the unabstracted version.
"""

DEFAULT_MODEL = "openai/gpt-oss-120b"

__all__ = ["setup", "load_key", "DEFAULT_MODEL"]


def load_key():
    """Ensure GROQ_API_KEY is set in the environment.

    In Colab, read it from Secrets (key icon, left sidebar). Running locally,
    expect it as an environment variable. Raises a clear, actionable error
    when it's missing rather than failing later inside the client.
    """
    import os

    try:
        from google.colab import userdata  # only importable inside Colab
    except ImportError:
        # Not in Colab — expect the key in the environment.
        if not os.environ.get("GROQ_API_KEY"):
            raise RuntimeError(
                "GROQ_API_KEY is not set. Run `export GROQ_API_KEY=...` in your "
                "shell before launching Jupyter, or set it in os.environ."
            )
        return

    # In Colab: pull from Secrets, with a message that names the exact fix.
    try:
        os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
    except Exception as e:
        raise RuntimeError(
            "Couldn't read GROQ_API_KEY from Colab Secrets. Click the key icon "
            "in the left sidebar, add a secret named exactly GROQ_API_KEY, and "
            "flip 'Notebook access' on for this notebook, then re-run this cell."
        ) from e


def setup(model=DEFAULT_MODEL, quiet=False, max_retries=8):
    """Load the key and return a ready (client, model) pair.

    Usage in a notebook:

        from aien import setup
        client, MODEL = setup()

    Pass `model=` to override the default (e.g. a smaller model for bulk work).
    If a call later fails with a 404, list available models — see
    00-setup/00-environment.ipynb.

    `max_retries` (default 8, vs the SDK's 2): the free Groq tier has a low
    tokens-per-minute cap, so a notebook that fires several calls in a burst
    can hit HTTP 429. The SDK retries 429s automatically with backoff and
    honors the server's `retry-after` hint; a higher ceiling just lets those
    short waits resolve transparently instead of surfacing as an error. Costs
    nothing when you're under the limit.
    """
    load_key()
    from groq import Groq  # imported lazily so `import aien` works without groq

    client = Groq(max_retries=max_retries)
    if not quiet:
        print(f"Groq client ready. MODEL = {model}")
    return client, model
