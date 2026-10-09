# BSV Fire – SEO-agent

Ukentlig, **kun-lesende** rådgiver for bsvfire.no (Bergen/Vestland). Den endrer aldri nettside, annonser eller kontoer – den leverer bare en rapport (`reports/ÅÅÅÅ-MM-DD.md`, valgfritt på e-post).

## Hva den gjør hver uke
1. **Nettside**: crawler sitemap (title, meta, H1/H2, schema, alt-tekst, lokale signaler, robots/llms.txt).
2. **Google Search Console + GA4**: søkeord, posisjoner, CTR, landingssider, konvertering.
3. **Google Ads** (GAQL, kun SELECT): søketermer, søkeord, kvalitetsscore, landingssider, kostnad/konvertering.
4. **Rød tråd organisk × annonser**: samme tema/intensjon sammenlignes – gap, kannibalisering, annonse→side uten matchende innhold.
5. **Konkurrenter** i Bergen/Vestland: samme sideaudit.
6. **AI-synlighet**: stiller kundespørsmål til ChatGPT/Perplexity og sjekker om BSV nevnes/siteres.
7. **Claude** skriver rapporten: prioriterte tiltak (eier: Mint Media / BSV / annonsør), nye sider med H1/H2-utkast og faglig tekst, annonseforslag, endringer siden sist.

## Sikkerhet (aldri endre)
- Search Console og GA4: kun `*.readonly`-scopes. Google Ads har ikke readonly-scope, så agenten kobles til med en bruker som har «Read only»-rolle (se SETUP.md).
- HTTP kun GET/HEAD (`seo_agent/guardrails.py`), GAQL kun `SELECT`. Tester i `tests/` feiler hvis mutasjonskall legges til.

## Oppsett
1. `cp .env.example .env` og fyll inn (ellers hoppes kilden over og rapporten sier hva som mangler).
2. Rediger `config/config.yaml`: tjenester, konkurrentdomener, søkeord, AI-spørsmål.
3. `pip install -r requirements.txt && python -m seo_agent.main` (`--no-llm` = kun rådata).
4. Automatisk: legg verdiene som GitHub Secrets; `.github/workflows/weekly-report.yml` kjører mandager.

Oppsett steg for steg: se [SETUP.md](SETUP.md).
