"""LoanDesk mock Credit Score API (Azure Functions, Python v2 programming model).

GET /api/credit-score?businessId=BIZ-100001 returns a made-up score. Callers authenticate with a function
key in the x-functions-key header. Nothing is logged except what the Functions host logs by default; the
business ID is not written to the log.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import azure.functions as func

from scoring import SCORE_MAX, SCORE_MIN, InvalidBusinessId, look_up

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

SOURCE = "LoanDesk mock credit bureau"


def _json(body: dict[str, object], status_code: int) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body),
        status_code=status_code,
        mimetype="application/json",
        headers={"Cache-Control": "no-store"},
    )


def _error(code: str, message: str, status_code: int) -> func.HttpResponse:
    return _json({"error": {"code": code, "message": message}}, status_code)


@app.route(route="credit-score", methods=["GET"])
def credit_score(req: func.HttpRequest) -> func.HttpResponse:
    try:
        result = look_up(req.params.get("businessId"))
    except InvalidBusinessId as exc:
        return _error("InvalidBusinessId", str(exc), 400)

    if result is None:
        return _error("NoCreditFile", "The credit bureau has no file for this business ID.", 404)

    return _json(
        {
            "businessId": result.business_id,
            "score": result.score,
            "scoreMin": SCORE_MIN,
            "scoreMax": SCORE_MAX,
            "checkedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": SOURCE,
            "mock": True,
        },
        200,
    )
