# Solution

The **LoanDesk** Power Platform solution (publisher prefix `ldk`), unpacked as source with the Power Platform
CLI:

```text
pac solution export --name LoanDesk --path ../out/LoanDesk.zip
pac solution unpack --zipfile ../out/LoanDesk.zip --folder .
```

The exported `.zip` goes to `out/`, which Git ignores. Before committing, check the unpacked files for
secrets, tenant IDs and environment URLs.

Built in v0.1.0.
