"""Enable the Activity protocol on a Microsoft Foundry agent, so Copilot Studio can call it.

The Foundry portal cannot do this yet; it takes one PATCH to the agent's endpoint configuration
(Microsoft Learn: "Connect a Microsoft Foundry agent", "Configure and share your agent").

The script reads the agent first and keeps every protocol and authorization scheme it already has,
because the PATCH replaces those lists. It only adds what is missing:

- the protocol ``activity``;
- the authorization scheme ``BotServiceRbac``.

Run it from Azure Cloud Shell, signed in as a user with the Foundry User role on the resource:

    python3 activity_endpoint.py <project-endpoint> <agent-name>            # show only
    python3 activity_endpoint.py <project-endpoint> <agent-name> --apply    # change

The project endpoint is on the project's Overview page and looks like
``https://<resource>.services.ai.azure.com/api/projects/<project>``. The agent name is the name
shown in the Agents list (not the agent ID). The access token is taken from the Azure CLI and is
never printed.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_VERSION = "v1"
TOKEN_RESOURCE = "https://ai.azure.com"
FEATURE_HEADER = ("Foundry-Features", "AgentEndpoints=V1Preview")
ACTIVITY = "activity"
BOT_SERVICE = "BotServiceRbac"


def agent_url(project_endpoint: str, agent_name: str) -> str:
    """URL of one agent in a project, with the API version."""
    if not project_endpoint.startswith("https://"):
        raise ValueError("The project endpoint must start with https://")
    base = project_endpoint.rstrip("/")
    name = urllib.parse.quote(agent_name, safe="")
    return f"{base}/agents/{name}?api-version={API_VERSION}"


def with_activity(endpoint: dict[str, Any] | None) -> dict[str, Any]:
    """Return a copy of ``agent_endpoint`` with the Activity protocol and BotServiceRbac added.

    Two shapes are in use. Older previews list protocols in ``protocols``; the current one keys them
    in ``protocol_configuration``. Whatever is already there is kept.
    """
    result = copy.deepcopy(endpoint) if endpoint else {}

    if isinstance(result.get("protocols"), list):
        if ACTIVITY not in result["protocols"]:
            result["protocols"].append(ACTIVITY)
    else:
        config = result.get("protocol_configuration")
        if not isinstance(config, dict) or not config:
            # Nothing configured yet: keep the default Responses protocol next to Activity.
            config = {"responses": {}}
        config.setdefault(ACTIVITY, {})
        result["protocol_configuration"] = config

    schemes = result.get("authorization_schemes")
    if not isinstance(schemes, list) or not schemes:
        # The portal and SDK use Azure RBAC (Entra) by default; keep it.
        schemes = [{"type": "AzureRbac"}]
    if not any(isinstance(s, dict) and s.get("type") == BOT_SERVICE for s in schemes):
        schemes.append({"type": BOT_SERVICE})
    result["authorization_schemes"] = schemes
    return result


def has_activity(endpoint: dict[str, Any] | None) -> bool:
    """True when the Activity protocol and BotServiceRbac are both configured."""
    if not endpoint:
        return False
    protocols = endpoint.get("protocols")
    config = endpoint.get("protocol_configuration")
    protocol_on = (isinstance(protocols, list) and ACTIVITY in protocols) or (
        isinstance(config, dict) and ACTIVITY in config
    )
    schemes = endpoint.get("authorization_schemes") or []
    scheme_on = any(isinstance(s, dict) and s.get("type") == BOT_SERVICE for s in schemes)
    return protocol_on and scheme_on


def get_token() -> str:
    """Access token for Microsoft Foundry from the signed-in Azure CLI."""
    completed = subprocess.run(
        [
            "az", "account", "get-access-token",
            "--resource", TOKEN_RESOURCE,
            "--query", "accessToken",
            "--output", "tsv",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("az account get-access-token failed; run 'az login' first")
    return completed.stdout.strip()


def call(method: str, url: str, token: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    """Send one request and return the JSON reply. Errors show the status and the service message."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header(*FEATURE_HEADER)
    request.add_header(
        "Content-Type",
        "application/merge-patch+json" if method == "PATCH" else "application/json",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"{method} returned HTTP {error.code}: {detail}") from None


def show(label: str, endpoint: dict[str, Any] | None) -> None:
    print(f"{label}:")
    print(json.dumps(endpoint or {}, indent=2))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project_endpoint")
    parser.add_argument("agent_name")
    parser.add_argument("--apply", action="store_true", help="send the PATCH (default: show only)")
    args = parser.parse_args(argv)

    url = agent_url(args.project_endpoint, args.agent_name)
    token = get_token()

    current = call("GET", url, token).get("agent_endpoint")
    show("Current agent_endpoint", current)
    if has_activity(current):
        print("Activity protocol and BotServiceRbac are already on. Nothing to do.")
        return 0

    wanted = with_activity(current)
    show("agent_endpoint to send", wanted)
    if not args.apply:
        print("Show only. Run again with --apply to send it.")
        return 0

    call("PATCH", url, token, {"agent_endpoint": wanted})
    after = call("GET", url, token).get("agent_endpoint")
    show("agent_endpoint after the change", after)
    if has_activity(after):
        print("Done: the Activity protocol is on.")
        return 0
    print("The change was sent, but the agent does not show the Activity protocol yet.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)
