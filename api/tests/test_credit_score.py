"""Tests for the mock Credit Score API. Run from the api folder: python -m unittest discover -s tests"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import azure.functions as func  # noqa: E402

import scoring  # noqa: E402
from function_app import credit_score  # noqa: E402

handler = credit_score.build().get_user_function()


def call(params: dict[str, str]) -> func.HttpResponse:
    request = func.HttpRequest(method="GET", url="/api/credit-score", params=params, body=b"")
    return handler(request)


class ScoringTests(unittest.TestCase):
    def test_score_is_stable_and_in_range(self) -> None:
        for business_id in ("BIZ-100001", "BIZ-100002", "ABC", "X" * 20):
            score = scoring.score_for(business_id)
            self.assertEqual(score, scoring.score_for(business_id))
            self.assertGreaterEqual(score, scoring.SCORE_MIN)
            self.assertLessEqual(score, scoring.SCORE_MAX)

    def test_normalise_trims_and_upper_cases(self) -> None:
        self.assertEqual(scoring.normalise_business_id("  biz-100001 "), "BIZ-100001")

    def test_rejects_bad_ids(self) -> None:
        for raw in (None, "", "  ", "AB", "-BIZ1", "BIZ 1001", "BIZ_1001", "X" * 21, "BIZ-1'; drop"):
            with self.subTest(raw=raw), self.assertRaises(scoring.InvalidBusinessId):
                scoring.normalise_business_id(raw)

    def test_no_file_id_returns_none(self) -> None:
        self.assertIsNone(scoring.look_up(scoring.NO_FILE_BUSINESS_ID.lower()))

    def test_scores_spread_across_the_range(self) -> None:
        scores = {scoring.score_for(f"BIZ-{n:06d}") for n in range(100001, 100201)}
        self.assertLess(min(scores), 450)
        self.assertGreater(max(scores), 750)


class FunctionTests(unittest.TestCase):
    def test_returns_score(self) -> None:
        response = call({"businessId": "biz-100001"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        body = json.loads(response.get_body())
        self.assertEqual(body["businessId"], "BIZ-100001")
        self.assertEqual(body["score"], scoring.score_for("BIZ-100001"))
        self.assertEqual((body["scoreMin"], body["scoreMax"]), (300, 900))
        self.assertTrue(body["mock"])
        self.assertRegex(body["checkedAt"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

    def test_missing_id_is_400(self) -> None:
        response = call({})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.get_body())["error"]["code"], "InvalidBusinessId")

    def test_no_credit_file_is_404(self) -> None:
        response = call({"businessId": "BIZ-000000"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.get_body())["error"]["code"], "NoCreditFile")

    def test_route_needs_a_function_key(self) -> None:
        self.assertNotEqual(credit_score.build().get_trigger().auth_level, func.AuthLevel.ANONYMOUS)


if __name__ == "__main__":
    unittest.main()
