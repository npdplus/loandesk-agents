"""LoanDesk Application Status MCP server (Azure Functions MCP extension, Python v2 model).

One read-only tool, get_application_status. The extension serves it over Streamable HTTP at
/runtime/webhooks/mcp; callers send the mcp_extension system key in the x-functions-key header.

Settings (app settings, never in the repository):
- DATAVERSE_URL: the environment URL, for example https://<org>.crm5.dynamics.com
- DATAVERSE_CLIENT_ID: client ID of the user-assigned managed identity that is the Dataverse application user
"""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache

import azure.functions as func

from dataverse import DataverseStore
from status import UNAVAILABLE, ApplicationStore, look_up_status

app = func.FunctionApp()

TOOL_PROPERTIES = json.dumps(
    [
        {
            "propertyName": "applicationNumber",
            "propertyType": "string",
            "description": "The application number the customer received, for example LDK-000001.",
            "isRequired": True,
        },
        {
            "propertyName": "contactEmail",
            "propertyType": "string",
            "description": "The contact e-mail address the customer gave on the application.",
            "isRequired": True,
        },
    ]
)

DESCRIPTION = (
    "Gets the status of a LoanDesk loan application. Needs both the application number and the contact "
    "e-mail address from the application; ask the customer for both. Returns the status, the date it last "
    "changed and the next step, or found=false when they do not match."
)


@lru_cache(maxsize=1)
def _store() -> ApplicationStore:
    from azure.identity import ManagedIdentityCredential

    credential = ManagedIdentityCredential(client_id=os.environ["DATAVERSE_CLIENT_ID"])
    return DataverseStore(os.environ["DATAVERSE_URL"], credential)


def _arguments(context: object) -> dict[str, object]:
    content = json.loads(context) if isinstance(context, (str, bytes)) else context
    if not isinstance(content, dict):
        return {}
    arguments = content.get("arguments") or {}
    return arguments if isinstance(arguments, dict) else {}


@app.mcp_tool_trigger(
    arg_name="context",
    tool_name="get_application_status",
    description=DESCRIPTION,
    tool_properties=TOOL_PROPERTIES,
)
def get_application_status(context: str) -> str:
    arguments = _arguments(context)
    try:
        result = look_up_status(_store(), arguments.get("applicationNumber"), arguments.get("contactEmail"))
    except Exception as exc:  # noqa: BLE001 - any failure gives the customer the same safe answer
        # Log the error type only: no application number, e-mail address or token.
        logging.error("get_application_status failed: %s", type(exc).__name__)
        result = {"found": False, "message": UNAVAILABLE}
    return json.dumps(result)
