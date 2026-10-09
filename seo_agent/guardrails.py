"""Agenten er KUN lesende. Dette er de harde sperrene.

- Google OAuth-scopes er kun *readonly*.
- Google Ads: kun GoogleAdsService.search/search_stream (GAQL). Ingen mutate.
- HTTP mot bsvfire.no: kun GET/HEAD.
- Eneste skriving: rapportfiler i reports/ (og valgfri e-post).
"""
import requests

READONLY_SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]
ALLOWED_METHODS = {"GET", "HEAD"}


class ReadOnlyViolation(RuntimeError):
    pass


def safe_request(method: str, url: str, **kw):
    if method.upper() not in ALLOWED_METHODS:
        raise ReadOnlyViolation(f"{method} er ikke tillatt (kun lesing)")
    kw.setdefault("timeout", 20)
    kw.setdefault("headers", {"User-Agent": "BSV-SEO-Agent/1.0 (read-only)"})
    return requests.request(method, url, **kw)


def assert_gaql_readonly(query: str):
    q = query.strip().lower()
    if not q.startswith("select"):
        raise ReadOnlyViolation("Kun GAQL SELECT er tillatt")
