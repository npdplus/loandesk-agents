# Microsoft Foundry: LoanDesk Document Agent

v0.3.0 step 3. A Foundry prompt agent that tells a business which documents it still needs, connected to
the Front Desk (the Apply Agent) in Copilot Studio as a Foundry agent (preview).

## The agent

Built in the new Foundry portal: project `proj-loandesk` → **Agents** → **New agent** → **Build an agent**.

| Setting | Value |
|---|---|
| Agent name | `loandesk-document-agent` (cannot be changed later; the script below uses it) |
| Interaction mode | Text |
| Microsoft Copilot harness | Off |
| Model | `gpt-4.1-mini` (Global Standard deployment) |
| Tools | **File search** only, over [`knowledge/required-documents.md`](../knowledge/required-documents.md). The portal adds **Web search** to a new agent; it was removed |
| Instructions | [`document-agent-instructions.md`](document-agent-instructions.md) |

No customer files are uploaded; the only file is the public checklist.

## Enable the Activity protocol

Copilot Studio talks to a Foundry agent over the Activity protocol, which a new agent does not have (it
exposes Responses and A2A). Without it the call fails with HTTP 400: *endpoint does not support activity*.
The portal cannot turn it on, and after it is on, the portal still lists only Responses and A2A.

[`activity_endpoint.py`](activity_endpoint.py) reads the agent, keeps every protocol and authorization
scheme it has, and adds `activity` and `BotServiceRbac`. It needs only the Python standard library and the
Azure CLI, so it runs in Azure Cloud Shell as is:

```bash
python3 activity_endpoint.py "<project endpoint>" loandesk-document-agent           # show only
python3 activity_endpoint.py "<project endpoint>" loandesk-document-agent --apply   # change
```

The project endpoint is on the project's overview page
(`https://<resource>.services.ai.azure.com/api/projects/<project>`). The signed-in user needs the
**Foundry User** role. The access token comes from `az account get-access-token` and is never printed.

Tests: `python3 -m pytest foundry/tests`.
