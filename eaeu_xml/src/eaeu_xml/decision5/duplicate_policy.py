from typing import Protocol


class DuplicatePolicy(Protocol):
    """Process-specific duplicate detection boundary required by paragraph 101."""

    def is_duplicate(self, payload: object) -> bool: ...
