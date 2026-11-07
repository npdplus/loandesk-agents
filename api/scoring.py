"""Mock credit scoring for the LoanDesk demo.

Every business ID and every score here is made up. The score is derived from the business ID with a hash,
so the same ID always gets the same score and no data is stored anywhere.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

SCORE_MIN = 300
SCORE_MAX = 900

# A business ID with no credit file, so callers can test their "not found" path.
NO_FILE_BUSINESS_ID = "BIZ-000000"

_BUSINESS_ID = re.compile(r"^[A-Z0-9][A-Z0-9-]{2,19}$")


class InvalidBusinessId(ValueError):
    """The business ID is missing or not in an accepted format."""


@dataclass(frozen=True)
class CreditScore:
    business_id: str
    score: int


def normalise_business_id(raw: str | None) -> str:
    """Trim and upper-case a business ID, or raise InvalidBusinessId."""
    value = (raw or "").strip().upper()
    if not _BUSINESS_ID.fullmatch(value):
        raise InvalidBusinessId(
            "businessId must be 3 to 20 letters, digits or hyphens, starting with a letter or digit, "
            "for example BIZ-100001."
        )
    return value


def score_for(business_id: str) -> int:
    """Return a stable mock score between SCORE_MIN and SCORE_MAX for a normalised business ID."""
    digest = hashlib.sha256(business_id.encode("utf-8")).digest()
    span = SCORE_MAX - SCORE_MIN + 1
    return SCORE_MIN + int.from_bytes(digest[:8], "big") % span


def look_up(raw_business_id: str | None) -> CreditScore | None:
    """Score a business ID. Returns None when the business has no credit file."""
    business_id = normalise_business_id(raw_business_id)
    if business_id == NO_FILE_BUSINESS_ID:
        return None
    return CreditScore(business_id=business_id, score=score_for(business_id))
