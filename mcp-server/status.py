"""Application status look-up for the LoanDesk MCP server.

A customer must give both the application number and the contact e-mail address on the application. When
either is wrong the answer is the same "no match", so guessing numbers reveals nothing. The answer holds the
status, the date it last changed and the next step only: no score, amount, decision reason or name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

APPLICATION_NUMBER = re.compile(r"^LDK-\d{6}$")
_EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,255}$")

# Choice values of ldk_Applicationstatus in solution LoanDesk.
STATUS_LABELS = {
    852190000: "Submitted",
    852190001: "Under review",
    852190002: "Approved",
    852190003: "Rejected",
    852190004: "Needs information",
}

NEXT_STEPS = {
    "Submitted": "A credit officer will review it and decide within 5 business days after all required "
    "documents arrive.",
    "Under review": "A credit officer is reviewing it.",
    "Approved": "The Lending Centre will contact you about the next steps.",
    "Rejected": "The Lending Centre will contact you with the reason. You can ask for a review.",
    "Needs information": "The Lending Centre will tell you exactly what is needed.",
}

NO_MATCH = (
    "No application matches that application number and e-mail address. Check both, or contact the "
    "Lending Centre."
)
BAD_NUMBER = "An application number looks like LDK-000001."
BAD_EMAIL = "Give the contact e-mail address used on the application."
UNAVAILABLE = "The status service is not available right now. Please try again later or contact the Lending Centre."


@dataclass(frozen=True)
class Application:
    number: str
    contact_email: str
    status_code: int | None
    modified_on: str


class ApplicationStore(Protocol):
    def find_by_number(self, number: str) -> Application | None: ...


def _not_found(message: str) -> dict[str, object]:
    return {"found": False, "message": message}


def normalise_number(raw: object) -> str | None:
    value = str(raw or "").strip().upper()
    return value if APPLICATION_NUMBER.fullmatch(value) else None


def look_up_status(store: ApplicationStore, raw_number: object, raw_email: object) -> dict[str, object]:
    """Return the status of one application, or a "not found" answer that does not say why."""
    number = normalise_number(raw_number)
    if number is None:
        return _not_found(BAD_NUMBER)

    email = str(raw_email or "").strip()
    if not _EMAIL.fullmatch(email):
        return _not_found(BAD_EMAIL)

    application = store.find_by_number(number)
    if application is None or application.contact_email.strip().casefold() != email.casefold():
        return _not_found(NO_MATCH)

    status = STATUS_LABELS.get(application.status_code or -1, "Unknown")
    return {
        "found": True,
        "applicationNumber": application.number,
        "status": status,
        "lastUpdated": application.modified_on[:10],
        "nextStep": NEXT_STEPS.get(status, "Contact the Lending Centre for details."),
    }
