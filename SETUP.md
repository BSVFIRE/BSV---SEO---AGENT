# Oppsett – steg for steg (ca. 45–60 min, én gang)

Alt legges inn som **GitHub Secrets**: repoet → *Settings* → *Secrets and variables* → *Actions* → *New repository secret*. Navnet må være nøyaktig som under. Ingenting skrives i filer.

Hopp over det du ikke har: agenten hopper over kilder uten nøkler og skriver i rapporten hva som mangler. Start gjerne med steg 1–2, så får du en første rapport raskt.

## 0. Aktiver kjøringen
Den ukentlige kjøringen virker bare fra repoets **hovedgren (main)**. Koden ligger nå på en arbeidsgren, så den må flettes til main først (be Claude lage en pull request).

## 1. Claude (påkrevd)
1. Gå til console.anthropic.com → *API keys* → *Create key*.
2. Secret: `ANTHROPIC_API_KEY`.
(Krever betalingskort. Én ukerapport koster typisk noen kroner.)

## 2. Google Search Console + GA4 (anbefalt først)
1. console.cloud.google.com → lag et prosjekt «BSV SEO-agent».
2. *APIs & Services* → *Library*: aktiver **Google Search Console API** og **Google Analytics Data API**.
3. *IAM & Admin* → *Service accounts* → *Create*. Gi den et navn, hopp over rollene.
4. Åpne kontoen → *Keys* → *Add key* → *JSON*. En fil lastes ned.
5. Secret `GOOGLE_SERVICE_ACCOUNT_JSON`: lim inn **hele innholdet** i JSON-filen.
6. Kopier e-postadressen til service account (slutter på `iam.gserviceaccount.com`):
   - **Search Console** → *Innstillinger* → *Brukere og tillatelser* → *Legg til bruker* → tillatelse **Begrenset**.
   - **GA4** → *Admin* → *Tilgangsstyring for eiendom* → legg til med rolle **Seer (Viewer)**.
7. Secret `GSC_SITE_URL`: `sc-domain:bsvfire.no` hvis Search Console er satt opp som domene, ellers `https://www.bsvfire.no/` (se hvordan eiendommen heter øverst i Search Console).
8. Secret `GA4_PROPERTY_ID`: GA4 → *Admin* → *Eiendomsinformasjon* → tallet «Eiendoms-ID».

## 3. Google Ads
Du trenger en **manager-konto (MCC)** for developer token. Har dere ikke det, opprett en gratis på ads.google.com/home/tools/manager-accounts og koble den til kontoen.
1. **Customer ID:** 10-sifret kontonummer øverst i Google Ads, **uten bindestreker** → Secret `GOOGLE_ADS_CUSTOMER_ID`. Bruker du manager-konto: dens nummer → `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.
2. **Developer token:** i manager-kontoen → *Verktøy* → *API-senter* → søk om tilgang (*Basic access*). Godkjenning kan ta noen dager. Secret `GOOGLE_ADS_DEVELOPER_TOKEN`.
3. **Egen leser-bruker (viktig for «aldri endre»):** i Google Ads → *Administrator* → *Tilgang og sikkerhet* → inviter en Google-bruker (f.eks. en ny Gmail) med tilgangsnivå **Skrivebeskyttet (Read only)**. Godta invitasjonen.
4. I Google Cloud-prosjektet: aktiver **Google Ads API**. Under *Credentials* → *Create credentials* → *OAuth client ID* → type *Desktop app*. (Første gang må du fylle ut «OAuth consent screen» som *External* og legge leser-brukeren inn som testbruker.)
   Secrets: `GOOGLE_ADS_CLIENT_ID` og `GOOGLE_ADS_CLIENT_SECRET`.
5. **Refresh token:** på en PC med Python: `pip install google-auth-oauthlib`, så
   `python scripts/get_refresh_token.py <CLIENT_ID> <CLIENT_SECRET>`.
   Logg inn med **leser-brukeren** fra punkt 3. Kopier verdien som skrives ut → Secret `GOOGLE_ADS_REFRESH_TOKEN`.

> Merk: Google har ikke et «kun lese»-scope for Ads-API-et. Det er **leser-brukeren** i punkt 3 som gjør at agenten teknisk ikke kan endre noe, og i tillegg sender koden bare GAQL-`SELECT`.

## 4. Valgfritt
- `OPENAI_API_KEY` (platform.openai.com) og `PERPLEXITY_API_KEY` (perplexity.ai/settings/api): gir AI-synlighetstesten. Uten dem hoppes den over.
- E-post: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `REPORT_TO` (mottaker). Uten dette ligger rapporten bare i `reports/`.

## 5. Første kjøring
GitHub → *Actions* → *Ukentlig SEO-rapport* → *Run workflow*. Rapporten dukker opp i `reports/` (og på e-post). Deretter kjører den automatisk hver mandag.
