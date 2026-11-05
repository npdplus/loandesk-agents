# Solution

The **LoanDesk** Power Platform solution, version 0.1.0.0, publisher *NPD PLUS Labs* (`npdpluslabs`, prefix
`ldk`). Exported **unmanaged** from `LoanDesk-Dev` on 2026-11-05 (Solutions → Export solution) and unzipped
here. Line endings were normalised to LF, trailing spaces and one byte-order mark were removed; nothing else
was changed.

| Path | What it is |
|---|---|
| `solution.xml`, `customizations.xml`, `[Content_Types].xml` | Solution manifest and customisations |
| `bots/<agent>/bot.xml`, `configuration.json` | The two agents: name, model (`claude-sonnet-5-5`), instructions, web search off |
| `botcomponents/*.tool.Azure-FoundryIQ-*` | The Foundry IQ MCP tool of each agent, with its knowledge base name (`kb-loan-policy-public` or `kb-loan-policy-staff`) |
| `botcomponents/*.iqCapability.*` | Work IQ capability components (calendar, files, mail, people, sites, teams); see below |
| `botcomponents/Default_FeedbackCollectionBotSettings_*` | Feedback settings |
| `Assets/botcomponent_connectionreferenceset.xml` | Links each tool to its connection reference |
| `environmentvariabledefinitions/` | `ldk_SearchIndexPublic`, `ldk_SearchIndexStaff` |

## What is not here

- **No secrets.** A connection reference names a connection; the Azure AI Search query key stays in the
  connection in the environment. Importing the solution elsewhere asks for a new connection.
- No tenant ID, environment URL or person's e-mail address (checked before committing).

## Known items

- The agents and their tool connection references use the prefix `cr8c5_` of the environment's default
  publisher, because they were created before they joined the solution.
- Each agent carries six Work IQ capability components with `access: Write`, although Work IQ is not among
  the agents' tools and `WorkIqAddedByDefault` is `false`. A Preview test showed no Work IQ call; they are to
  be removed before v0.2.0 (decision D10 in [../docs/decisions.md](../docs/decisions.md)).

## Next exports

With the Power Platform CLI, the same can be done from the command line; the exported `.zip` goes to `out/`,
which Git ignores:

```text
pac solution export --name LoanDesk --path ../out/LoanDesk.zip
pac solution unpack --zipfile ../out/LoanDesk.zip --folder .
```

`pac solution unpack` uses a different file layout from a plain unzip; switch in one commit if it is used.
