"""Qt frontend for the EAEU XML application."""


def main(*args, **kwargs):
    """Lazy bootstrap so presentation-only helpers do not require PySide6."""

    from .app import main as run

    return run(*args, **kwargs)


__all__ = ("main",)
