"""Search Console, GA4 og Google Ads – kun lesing."""
import base64
import json
import os
from datetime import date, timedelta
from ..guardrails import READONLY_SCOPES, assert_gaql_readonly


def _creds():
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        return None
    from google.oauth2 import service_account
    if os.path.exists(raw):
        return service_account.Credentials.from_service_account_file(raw, scopes=READONLY_SCOPES)
    try:
        info = json.loads(raw)
    except json.JSONDecodeError:
        info = json.loads(base64.b64decode(raw))
    return service_account.Credentials.from_service_account_info(info, scopes=READONLY_SCOPES)


def search_console(days=28):
    creds, site = _creds(), os.getenv("GSC_SITE_URL")
    if not creds or not site:
        return {"skipped": "GSC ikke konfigurert"}
    from googleapiclient.discovery import build
    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=days)

    def q(dim, limit=100):
        body = {"startDate": str(start), "endDate": str(end), "dimensions": dim, "rowLimit": limit}
        rows = svc.searchanalytics().query(siteUrl=site, body=body).execute().get("rows", [])
        return [{"keys": r["keys"], "clicks": r["clicks"], "impr": r["impressions"],
                 "ctr": round(r["ctr"], 4), "pos": round(r["position"], 1)} for r in rows]
    return {"queries": q(["query"], 150), "pages": q(["page"], 60), "query_page": q(["query", "page"], 200)}


def ga4(days=28):
    creds, prop = _creds(), os.getenv("GA4_PROPERTY_ID")
    if not creds or not prop:
        return {"skipped": "GA4 ikke konfigurert"}
    from googleapiclient.discovery import build
    svc = build("analyticsdata", "v1beta", credentials=creds, cache_discovery=False)
    body = {"dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "landingPage"}],
            "metrics": [{"name": "sessions"}, {"name": "conversions"}, {"name": "engagementRate"}],
            "limit": 100}
    return svc.properties().runReport(property=f"properties/{prop}", body=body).execute()


def _ads_client():
    from google.ads.googleads.client import GoogleAdsClient
    return GoogleAdsClient.load_from_dict({
        "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID") or None,
        "use_proto_plus": True,
    })


def _gaql(client, cid, query):
    assert_gaql_readonly(query)
    svc = client.get_service("GoogleAdsService")
    return [row for batch in svc.search_stream(customer_id=cid, query=query) for row in batch.results]


def google_ads():
    cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
    if not cid or not os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"):
        return {"skipped": "Google Ads ikke konfigurert"}
    c = _ads_client()
    terms = _gaql(c, cid, """
        SELECT search_term_view.search_term, campaign.name, ad_group.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM search_term_view WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC LIMIT 200""")
    kws = _gaql(c, cid, """
        SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
               campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, ad_group_criterion.quality_info.quality_score
        FROM keyword_view WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC LIMIT 200""")
    lp = _gaql(c, cid, """
        SELECT landing_page_view.unexpanded_final_url, metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM landing_page_view WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC LIMIT 50""")
    m = lambda x: round(x.metrics.cost_micros / 1e6, 2)
    return {
        "search_terms": [{"term": r.search_term_view.search_term, "campaign": r.campaign.name,
                          "impr": r.metrics.impressions, "clicks": r.metrics.clicks,
                          "cost": m(r), "conv": r.metrics.conversions} for r in terms],
        "keywords": [{"kw": r.ad_group_criterion.keyword.text, "campaign": r.campaign.name,
                      "impr": r.metrics.impressions, "clicks": r.metrics.clicks, "cost": m(r),
                      "conv": r.metrics.conversions,
                      "qs": r.ad_group_criterion.quality_info.quality_score} for r in kws],
        "landing_pages": [{"url": r.landing_page_view.unexpanded_final_url, "clicks": r.metrics.clicks,
                           "cost": m(r), "conv": r.metrics.conversions} for r in lp],
    }
