import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from activity_endpoint import agent_url, has_activity, with_activity  # noqa: E402

# Shape returned by the service for a new portal agent (2026-11-08), both protocol fields at once.
SERVICE_SHAPE = {
    "version_selector": {
        "version_selection_rules": [
            {"type": "FixedRatio", "agent_version": "@latest", "traffic_percentage": 100}
        ]
    },
    "protocols": ["responses"],
    "protocol_configuration": {"responses": {}},
    "authorization_schemes": [{"type": "Entra", "isolation_key_source": {"kind": "Entra"}}],
    "publish_approval_status": "not_published",
}


def test_agent_url_adds_version_and_quotes_name():
    url = agent_url("https://example.services.ai.azure.com/api/projects/p/", "doc agent")
    assert url == "https://example.services.ai.azure.com/api/projects/p/agents/doc%20agent?api-version=v1"


def test_agent_url_needs_https():
    with pytest.raises(ValueError):
        agent_url("http://example.services.ai.azure.com/api/projects/p", "a")


def test_service_shape_updates_both_protocol_fields_and_sends_nothing_else():
    result = with_activity(SERVICE_SHAPE)
    assert set(result) == {"protocols", "protocol_configuration", "authorization_schemes"}
    assert result["protocols"] == ["responses", "activity"]
    assert result["protocol_configuration"] == {"responses": {}, "activity": {}}
    assert result["authorization_schemes"] == [
        {"type": "Entra", "isolation_key_source": {"kind": "Entra"}},
        {"type": "BotServiceRbac"},
    ]
    assert has_activity(result)
    assert SERVICE_SHAPE["protocols"] == ["responses"]  # input not changed


def test_empty_endpoint_gets_responses_activity_and_both_schemes():
    result = with_activity(None)
    assert "protocols" not in result
    assert result["protocol_configuration"] == {"responses": {}, "activity": {}}
    assert result["authorization_schemes"] == [{"type": "AzureRbac"}, {"type": "BotServiceRbac"}]
    assert has_activity(result)


def test_map_only_shape_keeps_existing_entries():
    current = {
        "protocol_configuration": {"responses": {}, "a2a": {}},
        "authorization_schemes": [{"type": "AzureRbac"}],
    }
    result = with_activity(current)
    assert set(result["protocol_configuration"]) == {"responses", "a2a", "activity"}
    assert result["authorization_schemes"] == [{"type": "AzureRbac"}, {"type": "BotServiceRbac"}]


def test_list_shape_appends_activity_once():
    current = {"protocols": ["responses", "activity"], "authorization_schemes": [{"type": "BotServiceRbac"}]}
    result = with_activity(current)
    assert result["protocols"] == ["responses", "activity"]
    assert result["authorization_schemes"] == [{"type": "BotServiceRbac"}]


def test_has_activity_needs_every_protocol_field_and_the_scheme():
    assert not has_activity(SERVICE_SHAPE)
    half = {
        "protocols": ["responses", "activity"],
        "protocol_configuration": {"responses": {}},
        "authorization_schemes": [{"type": "BotServiceRbac"}],
    }
    assert not has_activity(half)
    assert not has_activity({"protocol_configuration": {"activity": {}}})
    assert not has_activity({"authorization_schemes": [{"type": "BotServiceRbac"}]})
    assert has_activity({"protocols": ["activity"], "authorization_schemes": [{"type": "BotServiceRbac"}]})
