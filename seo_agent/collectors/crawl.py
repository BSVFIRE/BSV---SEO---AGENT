"""Teknisk/innholdsrevisjon av egen side og konkurrenter (kun GET)."""
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from ..guardrails import safe_request


def sitemap_urls(sitemap_url, limit=200):
    try:
        r = safe_request("GET", sitemap_url)
        urls = re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text)
    except Exception:
        return []
    out = []
    for u in urls:
        if u.endswith(".xml") and len(out) < limit:
            out += sitemap_urls(u, limit)
        else:
            out.append(u)
    return out[:limit]


def audit_page(url):
    try:
        r = safe_request("GET", url)
    except Exception as e:
        return {"url": url, "error": str(e)}
    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text(" ", strip=True)
    schema_types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string or "")
            for item in (d if isinstance(d, list) else d.get("@graph", [d])):
                schema_types.append(item.get("@type"))
        except Exception:
            pass
    imgs = soup.find_all("img")
    return {
        "url": url,
        "status": r.status_code,
        "title": (soup.title.string.strip() if soup.title and soup.title.string else None),
        "meta_description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content"),
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(strip=True) for h in soup.find_all("h2")][:12],
        "canonical": (soup.find("link", rel="canonical") or {}).get("href"),
        "noindex": bool(soup.find("meta", attrs={"name": "robots", "content": re.compile("noindex", re.I)})),
        "words": len(text.split()),
        "images_without_alt": sum(1 for i in imgs if not i.get("alt")),
        "schema_types": schema_types,
        "internal_links": len({urljoin(url, a["href"]) for a in soup.find_all("a", href=True)
                               if urlparse(urljoin(url, a["href"])).netloc == urlparse(url).netloc}),
        "has_phone_or_address": bool(re.search(r"\+47|\b\d{2}\s?\d{2}\s?\d{2}\s?\d{2}\b", text)),
        "mentions_bergen": "bergen" in text.lower(),
    }


def site_files(base):
    res = {}
    for name in ("robots.txt", "llms.txt"):
        try:
            r = safe_request("GET", urljoin(base, name))
            res[name] = r.text[:2000] if r.status_code == 200 else f"HTTP {r.status_code}"
        except Exception as e:
            res[name] = f"feil: {e}"
    return res


def collect(cfg):
    site = cfg["site"]
    urls = sitemap_urls(site["sitemap"]) or [site["url"]]
    try:  # annonse-landingssider revideres alltid, også om de ikke er i sitemap
        from ..ads_structure import landing_pages
        ad_urls = list(dict.fromkeys(r["url"] for r in landing_pages()))
    except Exception:
        ad_urls = []
    urls = ad_urls + [u for u in urls if u not in ad_urls]
    return {
        "site_files": site_files(site["url"]),
        "ad_landing_urls": ad_urls,
        "pages": [audit_page(u) for u in urls[:60]],
        "competitors": [audit_page(c if c.startswith("http") else f"https://{c}/") for c in cfg.get("competitors", [])],
    }
