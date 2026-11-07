"""Read-only access to the Loan Application table through the Dataverse Web API.

The function app signs in with its managed identity, which is an application user in the environment with a
security role that can only read Loan Application rows.
"""

from __future__ import annotations

import json
from typing import Protocol
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from status import APPLICATION_NUMBER, Application

ENTITY_SET = "ldk_loanapplications"
COLUMNS = "ldk_applicationnumber,ldk_contactemail,ldk_applicationstatus,modifiedon"
STATUS_LABEL = "ldk_applicationstatus@OData.Community.Display.V1.FormattedValue"


class TokenCredential(Protocol):
    def get_token(self, *scopes: str): ...  # noqa: ANN201 - azure.core AccessToken


class DataverseStore:
    def __init__(self, environment_url: str, credential: TokenCredential, timeout: float = 10.0) -> None:
        self._base = environment_url.rstrip("/")
        self._credential = credential
        self._timeout = timeout

    def find_by_number(self, number: str) -> Application | None:
        # The number is checked against a strict pattern first, so it cannot change the filter.
        if not APPLICATION_NUMBER.fullmatch(number):
            return None

        query = urlencode(
            {
                "$select": COLUMNS,
                "$filter": f"ldk_applicationnumber eq '{number}'",
                "$top": "2",
            },
            quote_via=quote,
        )
        token = self._credential.get_token(f"{self._base}/.default").token
        request = Request(
            f"{self._base}/api/data/v9.2/{ENTITY_SET}?{query}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "OData-MaxVersion": "4.0",
                "OData-Version": "4.0",
                "Prefer": 'odata.include-annotations="OData.Community.Display.V1.FormattedValue"',
            },
        )
        with urlopen(request, timeout=self._timeout) as response:  # noqa: S310 - https URL from settings
            rows = json.load(response).get("value", [])

        if len(rows) != 1:
            return None
        row = rows[0]
        return Application(
            number=row.get("ldk_applicationnumber") or number,
            contact_email=row.get("ldk_contactemail") or "",
            status=row.get(STATUS_LABEL) or "",
            modified_on=row.get("modifiedon") or "",
        )
