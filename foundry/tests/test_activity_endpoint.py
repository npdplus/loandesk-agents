import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from activity_endpoint import agent_url, has_activity, with_activity  # noqa: E402


def test_agent_url_adds_version_and_quotes_name():
    url = agent_url("https://example.services.ai.azure.com/api/projects/p/", "doc agent")
    assert url == "https://example.services.ai.azure.com/api/projects/p/agents/doc%20agent?api-version=v1"


def test_agent_url_needs_https():
    with pytest.raises(ValueError):
        agent_url("http://example.services.ai.azure.com/api/projects/p", "a")


def test_empty_endpoint_gets_responses_activity_and_both_schemes():
    result = with_activity(None)
    assert result["protocol_configuration"] == {"responses": {}, "activity": {}}
    assert result["authorization_schemes"] == [{"type": "AzureRbac"}, {"type": "BotServiceRbac"}]
    assert has_activity(result)


def test_current_shape_keeps_existing_entries():
    current = {
        "version_selector": {"kind": "latest"},
        "protocol_configuration": {"responses": {}, "a2a": {}},
        "authorization_schemes": [{"type": "Entra", "isolation_key_source": {"kind": "Entra"}}],
    }
    result = with_activity(current)
    assert result["version_selector"] == {"kind": "latest"}
    assert set(result["protocol_configuration"]) == {"responses", "a2a", "activity"}
    assert result["authorization_schemes"][0]["type"] == "Entra"
    assert result["authorization_schemes"][-1] == {"type": "BotServiceRbac"}
    assert current["protocol_configuration"] == {"responses": {}, "a2a": {}}  # input not changed


def test_list_shape_appends_activity_once():
    current = {"protocols": ["responses", "activity"], "authorization_schemes": [{"type": "BotServiceRbac"}]}
    result = with_activity(current)
    assert result["protocols"] == ["responses", "activity"]
    assert result["authorization_schemes"] == [{"type": "BotServiceRbac"}]


def test_has_activity_needs_both_protocol_and_scheme():
    assert not has_activity({"protocol_configuration": {"activity": {}}})
    assert not has_activity({"authorization_schemes": [{"type": "BotServiceRbac"}]})
    assert has_activity({"protocols": ["activity"], "authorization_schemes": [{"type": "BotServiceRbac"}]})
