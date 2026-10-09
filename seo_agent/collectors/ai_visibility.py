"""Sjekker om BSV nevnes/siteres når kunder spør AI-assistenter."""
import os
import re
import requests
from urllib.parse import urlparse


def _mentions(text, brands, domain, competitors):
    low = text.lower()
    return {
        "mentioned": any(b.lower() in low for b in brands) or domain in low,
        "competitors_mentioned": [c for c in competitors if urlparse(c if "//" in c else "//" + c).netloc.replace("www.", "").split(".")[0].lower() in low],
        "urls": re.findall(r"https?://[^\s)\]]+", text)[:10],
    }


def _openai(prompt):
    r = requests.post("https://api.openai.com/v1/chat/completions", timeout=60,
                      headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                      json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]})
    return r.json()["choices"][0]["message"]["content"]


def _perplexity(prompt):
    r = requests.post("https://api.perplexity.ai/chat/completions", timeout=60,
                      headers={"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"},
                      json={"model": "sonar", "messages": [{"role": "user", "content": prompt}]})
    j = r.json()
    return j["choices"][0]["message"]["content"] + "\n" + "\n".join(j.get("citations", []))


def collect(cfg):
    engines = {}
    if os.getenv("OPENAI_API_KEY"):
        engines["chatgpt"] = _openai
    if os.getenv("PERPLEXITY_API_KEY"):
        engines["perplexity"] = _perplexity
    if not engines:
        return {"skipped": "Ingen AI-nøkler satt (OPENAI_API_KEY / PERPLEXITY_API_KEY)"}
    out = []
    for p in cfg["ai_prompts"]:
        for name, fn in engines.items():
            try:
                ans = fn(p)
                out.append({"engine": name, "prompt": p, "answer": ans[:1200],
                            **_mentions(ans, cfg["brand_names"], cfg["site"]["domain"], cfg.get("competitors", []))})
            except Exception as e:
                out.append({"engine": name, "prompt": p, "error": str(e)})
    return out
