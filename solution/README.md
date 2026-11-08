# Solution

The **LoanDesk** Power Platform solution, version **0.2.0.1**, publisher *NPD PLUS Labs* (`npdpluslabs`,
prefix `ldk`). Exported **unmanaged** from `LoanDesk-Dev` on 2026-11-08 (Solutions → Export solution) and
unzipped here. Line endings were normalised to LF and one byte-order mark was removed; nothing else was
changed.

Earlier exports: 0.1.0.0 is tagged `v0.1.0`; 0.1.1.0 removed the Work IQ capability components (decision
D10). 0.2.0.0 was exported first for v0.2.0 but missed two agent tools (see *Known items*), so 0.2.0.1 is
the one kept here.

| Path | What it is |
|---|---|
| `solution.xml`, `customizations.xml`, `[Content_Types].xml` | Solution manifest and customisations: table **Loan Application** (`ldk_loanapplication`), security role **LoanDesk Status Reader**, the prompt (AI model) *Explain eligibility result 1* |
| `bots/<agent>/` | The three agents: customer and staff (new experience) and `ldk_applyagent` (standard harness) |
| `botcomponents/<agent>.tool.*` | Agent tools: Foundry IQ MCP (customer, staff), *Get credit score* (staff), *LoanDesk Application Status* MCP (customer) |
| `botcomponents/ldk_applyagent.topic.*` | Apply Agent topics: Apply, Check eligibility, Rates and the system topics |
| `botcomponents/ldk_applyagent.action.*`, `aiplugins/`, `aipluginoperations/` | The REST API tool *Get credit score REST* |
| `botcomponents/mspva_*` | Evaluate test cases (category *Testing*) of the customer and staff agents, v0.1.0 and v0.2.0 sets; the same questions as `evals/import/` |
| `botcomponentcollections/` | Component collection *LoanDesk shared components* (Talk to a person) |
| `Connector/` | Custom connectors *LoanDesk Credit Score*, *LoanDesk Credit Score REST* and *LoanDesk Application Status* (MCP) |
| `Workflows/` | Agent flow **Submit Application** |
| `environmentvariabledefinitions/` | Seven environment variables (definitions only) |
| `Assets/` | Links from agent components to connection references, environment variables, the AI model and the flow |

## What is not here

- **No secrets.** Connections hold the function keys and the Azure AI Search query key; the topic's key is
  in Key Vault behind `ldk_CreditApiKey`. Importing the solution elsewhere asks for new connections.
- **No environment values.** The current values of `ldk_ApproverEmail`, `ldk_NotifyEmail`,
  `ldk_CreditApiHost`, `ldk_CreditApiKey` and `ldk_McpServerHost` have *Export value* set to *No*; an import
  asks for them. The three connectors read their host from `@environmentVariables(...)`.
- No tenant ID, subscription ID, environment URL, function host name, client ID, person's e-mail address or
  Application Insights connection string (checked before committing). The test cases use fictional
  `.example` addresses.

## Known items

- The customer and staff agents and their first tool connection references use the prefix `cr8c5_` of the
  environment's default publisher, because they were created before they joined the solution.
- **0.2.0.0 missed two tools** added after the agents joined the solution (*Get credit score* and the
  Application Status MCP tool). *Add required objects* on both agents fixed it; it also brought in their
  Evaluate test cases and two connection references.
- The security role carries the baseline privileges Dataverse adds to every new role (plug-in and SDK
  message reads, SharePoint data) besides **Read** on Loan Application.
- Connection references left over from flow experiments (Mail/SendGrid, Excel Online, a second Dataverse
  reference) are not used and can be removed from the solution later.

## Next exports

With the Power Platform CLI, the same can be done from the command line; the exported `.zip` goes to `out/`,
which Git ignores:

```text
pac solution export --name LoanDesk --path ../out/LoanDesk.zip
pac solution unpack --zipfile ../out/LoanDesk.zip --folder .
```

`pac solution unpack` uses a different file layout from a plain unzip; switch in one commit if it is used.
