"""Kjør: python -m seo_agent.main [--no-llm]  → reports/YYYY-MM-DD.md"""
import argparse
import glob
import json
import os
import smtplib
from datetime import date
from email.message import EmailMessage
import yaml
from .collectors import crawl, google, ai_visibility


def safe(fn, *a):
    try:
        return fn(*a)
    except Exception as e:  # én kilde som feiler skal ikke stoppe rapporten
        return {"error": f"{type(e).__name__}: {e}"}


def collect(cfg):
    return {
        "date": str(date.today()),
        "config": {k: cfg[k] for k in ("geo", "services", "seed_keywords", "competitors")},
        "website": safe(crawl.collect, cfg),
        "search_console": safe(google.search_console),
        "analytics": safe(google.ga4),
        "google_ads": safe(google.google_ads),
        "ai_visibility": safe(ai_visibility.collect, cfg),
    }


def email(subject, body):
    if not (os.getenv("SMTP_HOST") and os.getenv("REPORT_TO")):
        return
    m = EmailMessage()
    m["Subject"], m["From"], m["To"] = subject, os.environ["SMTP_USER"], os.environ["REPORT_TO"]
    m.set_content(body)
    with smtplib.SMTP_SSL(os.environ["SMTP_HOST"], 465) as s:
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        s.send_message(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/config.yaml")
    ap.add_argument("--no-llm", action="store_true", help="kun innsamling (rådata til reports/)")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    data = collect(cfg)
    os.makedirs("reports", exist_ok=True)
    today = str(date.today())
    json.dump(data, open(f"reports/{today}.data.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    if a.no_llm:
        return
    from . import analyze
    prev = sorted(glob.glob("reports/*.md"))
    previous = open(prev[-1], encoding="utf-8").read() if prev else None
    report = analyze.run(data, previous)
    open(f"reports/{today}.md", "w", encoding="utf-8").write(report)
    email(f"SEO-ukesrapport BSV Fire {today}", report)
    print(f"Skrev reports/{today}.md")


if __name__ == "__main__":
    main()
