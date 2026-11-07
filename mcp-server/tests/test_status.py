"""Tests for the Application Status MCP server. Run from the mcp-server folder:
python -m unittest discover -s tests"""

from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dataverse  # noqa: E402
import function_app  # noqa: E402
import status  # noqa: E402

APP = status.Application(
    number="LDK-000004",
    contact_email="Owner@Contoso-Coffee.example",
    status_code=852190002,
    modified_on="2026-11-06T04:24:10Z",
)


class FakeStore:
    def __init__(self, application: status.Application | None = APP) -> None:
        self.application = application
        self.calls: list[str] = []

    def find_by_number(self, number: str) -> status.Application | None:
        self.calls.append(number)
        return self.application if self.application and self.application.number == number else None


class LookUpTests(unittest.TestCase):
    def test_match_returns_status_only(self) -> None:
        result = status.look_up_status(FakeStore(), " ldk-000004 ", "owner@contoso-coffee.example")
        self.assertEqual(
            result,
            {
                "found": True,
                "applicationNumber": "LDK-000004",
                "status": "Approved",
                "lastUpdated": "2026-11-06",
                "nextStep": status.NEXT_STEPS["Approved"],
            },
        )

    def test_wrong_email_and_unknown_number_look_the_same(self) -> None:
        wrong_email = status.look_up_status(FakeStore(), "LDK-000004", "someone@else.example")
        unknown = status.look_up_status(FakeStore(), "LDK-000099", "owner@contoso-coffee.example")
        self.assertEqual(wrong_email, unknown)
        self.assertEqual(wrong_email, {"found": False, "message": status.NO_MATCH})

    def test_bad_input_never_reaches_the_store(self) -> None:
        store = FakeStore()
        for number, email in (("LDK-1", "a@b.example"), ("LDK-000004' or 1 eq 1", "a@b.example"),
                              (None, "a@b.example"), ("LDK-000004", "not-an-email"), ("LDK-000004", None)):
            with self.subTest(number=number, email=email):
                self.assertFalse(status.look_up_status(store, number, email)["found"])
        self.assertEqual(store.calls, [])

    def test_every_status_has_a_label_and_next_step(self) -> None:
        for code, label in status.STATUS_LABELS.items():
            result = status.look_up_status(
                FakeStore(status.Application("LDK-000001", "a@b.example", code, "2026-11-01T00:00:00Z")),
                "LDK-000001",
                "a@b.example",
            )
            self.assertEqual(result["status"], label)
            self.assertEqual(result["nextStep"], status.NEXT_STEPS[label])


class DataverseStoreTests(unittest.TestCase):
    def _store(self) -> dataverse.DataverseStore:
        credential = mock.Mock()
        credential.get_token.return_value = SimpleNamespace(token="t0ken")
        return dataverse.DataverseStore("https://org.example.crm5.dynamics.com/", credential)

    def test_builds_a_read_only_filtered_query(self) -> None:
        body = io.BytesIO(json.dumps({"value": [{
            "ldk_applicationnumber": "LDK-000004", "ldk_contactemail": "x@y.example",
            "ldk_applicationstatus": 852190000, "modifiedon": "2026-11-05T01:02:03Z"}]}).encode())
        with mock.patch.object(dataverse, "urlopen", return_value=body) as opened:
            found = self._store().find_by_number("LDK-000004")
        request = opened.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        url = unquote(request.full_url)
        self.assertTrue(url.startswith("https://org.example.crm5.dynamics.com/api/data/v9.2/ldk_loanapplications?"))
        self.assertIn("$filter=ldk_applicationnumber eq 'LDK-000004'", url)
        self.assertEqual(request.get_header("Authorization"), "Bearer t0ken")
        self.assertEqual(found, status.Application("LDK-000004", "x@y.example", 852190000, "2026-11-05T01:02:03Z"))

    def test_no_row_or_bad_number_is_none(self) -> None:
        with mock.patch.object(dataverse, "urlopen", return_value=io.BytesIO(b'{"value": []}')):
            self.assertIsNone(self._store().find_by_number("LDK-000004"))
        with mock.patch.object(dataverse, "urlopen") as opened:
            self.assertIsNone(self._store().find_by_number("LDK-0' or ''='"))
        opened.assert_not_called()


class ToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handler = function_app.get_application_status.build().get_user_function()

    def test_tool_is_registered(self) -> None:
        trigger = function_app.get_application_status.build().get_trigger()
        self.assertEqual(trigger.get_binding_name(), "mcpToolTrigger")
        payload = trigger.get_dict_repr()
        self.assertEqual(payload["toolName"], "get_application_status")
        names = [p["propertyName"] for p in json.loads(payload["toolProperties"])]
        self.assertEqual(names, ["applicationNumber", "contactEmail"])

    def test_handler_reads_arguments(self) -> None:
        context = json.dumps({"arguments": {"applicationNumber": "LDK-000004",
                                            "contactEmail": "owner@contoso-coffee.example"}})
        with mock.patch.object(function_app, "_store", return_value=FakeStore()):
            result = json.loads(self.handler(context))
        self.assertTrue(result["found"])
        self.assertEqual(result["status"], "Approved")

    def test_failure_gives_a_safe_answer(self) -> None:
        context = json.dumps({"arguments": {"applicationNumber": "LDK-000004", "contactEmail": "a@b.example"}})
        with mock.patch.object(function_app, "_store", side_effect=KeyError("DATAVERSE_URL")), \
                self.assertLogs(level="ERROR") as logs:
            result = json.loads(self.handler(context))
        self.assertEqual(result, {"found": False, "message": status.UNAVAILABLE})
        self.assertNotIn("a@b.example", "".join(logs.output))
        self.assertNotIn("LDK-000004", "".join(logs.output))


if __name__ == "__main__":
    unittest.main()
