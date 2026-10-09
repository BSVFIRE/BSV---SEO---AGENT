import pathlib
import pytest
from seo_agent.guardrails import safe_request, assert_gaql_readonly, ReadOnlyViolation, READONLY_SCOPES


def test_blocks_writes():
    for m in ("POST", "PUT", "DELETE", "PATCH"):
        with pytest.raises(ReadOnlyViolation):
            safe_request(m, "https://www.bsvfire.no/")


def test_gaql_select_only():
    assert_gaql_readonly("SELECT campaign.name FROM campaign")
    with pytest.raises(ReadOnlyViolation):
        assert_gaql_readonly("mutate")


def test_scopes_readonly():
    assert all(s.endswith(".readonly") for s in READONLY_SCOPES)


def test_no_mutation_calls_in_source():
    src = "".join(p.read_text() for p in pathlib.Path("seo_agent").rglob("*.py") if p.name != "guardrails.py")
    for bad in ("mutate", ".post(", "requests.put", "requests.delete", "requests.patch"):
        assert bad not in src.replace('requests.post("https://api.openai', "").replace('requests.post("https://api.perplexity', "")
