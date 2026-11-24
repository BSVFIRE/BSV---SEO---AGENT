#!/usr/bin/env python3
"""Bygger undersidene til BSV Fire som statiske HTML-filer i site/.

Header, footer, ring-bar og cookie-banner hentes fra site/index.html, slik at
alt holdes likt. Kjør:  python3 tools/build_pages.py
Resultatet er vanlig HTML du kan redigere direkte, og du trenger ikke kjøre dette for å drifte siden.
"""
import html, json, os, re
from datetime import date

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
BASE = "https://www.bsvfire.no"
PHONE_TXT, PHONE = "+47 900 46 600", "+4790046600"

idx = open(os.path.join(ROOT, "index.html"), encoding="utf8").read()
HEAD_SCRIPT = re.search(r'<script>try\{var t=.*?</script>', idx, re.S).group(0)
HEADER = re.search(r'<header class="site-header">.*?</header>', idx, re.S).group(0).replace('class="site-header"', 'class="site-header" data-solid', 1)
FOOTER = re.search(r'<footer>.*?</footer>', idx, re.S).group(0)
TAIL = re.search(r'<div class="callbar">.*?</div>\s*<div class="cookie".*?</div>\s*', idx, re.S).group(0)
FORM_OPTS = re.search(r'<select name="tjeneste" required>(.*?)</select>', idx, re.S).group(1)

e = html.escape


def form(service=""):
    opts = FORM_OPTS
    if service:
        opts = opts.replace("<option>%s</option>" % service, "<option selected>%s</option>" % service)
    return f'''<form class="quote" novalidate>
      <label>Navn<input name="navn" required autocomplete="name"></label>
      <label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label>
      <label>Tjeneste<select name="tjeneste" required>{opts}</select></label>
      <label>Adresse<input name="adresse" autocomplete="street-address"></label>
      <label>Melding<textarea name="melding" rows="3"></textarea></label>
      <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
      <button class="btn btn-primary" type="submit">Send forespørsel</button>
      <p class="form-note">Vi bruker opplysningene kun til å svare på henvendelsen. <a href="/personvern/">Personvern</a></p>
      <p class="form-ok" role="status">Takk! Vi tar kontakt så snart som mulig.</p>
    </form>'''


def page(path, title, desc, body, schema=None, og_image="og-bsv-fire.jpg", noindex=False):
    url = f"{BASE}/{path}" if path else f"{BASE}/"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in (schema or []))
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    out = f'''<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0d1114">
<meta property="og:type" content="website">
<meta property="og:locale" content="nb_NO">
<meta property="og:site_name" content="BSV Fire">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/{og_image}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{HEAD_SCRIPT}
<link rel="stylesheet" href="/assets/css/style.css">
{ld}</head>
<body>
<a class="skip" href="#innhold">Hopp til innhold</a>
{HEADER}
<main id="innhold">
{body}
</main>
{FOOTER}
{TAIL}<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf8").write(out)


def crumbs(items):
    """items: [(navn, url-sti)] etter Forside."""
    html_ = '<nav class="crumbs" aria-label="Brødsmulesti"><a href="/">Forside</a>' + "".join(
        f' / <a href="/{u}">{e(n)}</a>' if u else f' / {e(n)}' for n, u in items) + "</nav>"
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement":
          [{"@type": "ListItem", "position": 1, "name": "Forside", "item": BASE + "/"}] +
          [{"@type": "ListItem", "position": i + 2, "name": n, "item": f"{BASE}/{u}" if u else None} for i, (n, u) in enumerate(items)]}
    for it in ld["itemListElement"]:
        if it["item"] is None:
            del it["item"]
    return html_, ld


# ------------------------------------------------------------------ TJENESTER
SERVICES = [
 dict(slug="brannalarm", name="Brannalarm", select="Brannalarm",
  title="Brannalarm Bergen og Vestland – service og FG-kontroll | BSV Fire",
  desc="Brannalarm i Bergen og Vestland: nytt anlegg, oppgradering, service og årlig FG-kontroll etter FG790 og NS 3960. Be om tilbud fra FG-sertifisert firma.",
  h1="Brannalarm i Bergen og Vestland",
  lead="Nytt anlegg, oppgradering, service og årlig FG-kontroll. Uansett leverandør, uansett system.",
  img="tjeneste-brannalarm.jpg", alt="Servicetekniker kontrollerer brannalarmsentral i et næringsbygg i Bergen",
  what="Et brannalarmanlegg oppdager brann tidlig og varsler alle i bygget, slik at liv reddes og skader begrenses. Det kan også varsle alarmsentral og styre andre systemer, som røykventilasjon og branndører.",
  law=["Eier skal sørge for at branntekniske installasjoner alltid fungerer som forutsatt (forskrift om brannforebygging § 4-2).",
       "For FG-godkjente anlegg gjelder årlig kontroll etter FG790 og NS 3960, utført av FG-sertifisert firma.",
       "Kontroller og avvik skal dokumenteres og kunne vises ved tilsyn."],
  does=[("Nytt anlegg","Rådgivning, installasjon og idriftsettelse."),("Oppgradering","Nye sentraler og detektorer i eksisterende bygg."),
        ("Service og årlig kontroll","Kontroll etter FG790 og NS 3960 med full rapport."),("Akutt feilretting","Når anlegget gir feil eller må repareres.")],
  faq=[("Når er det krav om brannalarmanlegg?","Det følger av brann- og eksplosjonsvernloven, forskrift om brannforebygging og byggteknisk forskrift (TEK17). Kravet avhenger av byggets bruk, størrelse og risiko. Ta kontakt, så vurderer vi bygget ditt."),
       ("Må brannalarmanlegget kontrolleres hvert år?","Ja. Eier har ansvar for at anlegget fungerer, og FG-godkjente anlegg skal ha årlig kontroll etter FG790 og NS 3960."),
       ("Kan dere ta service på anlegg fra andre leverandører?","Ja. Vi leverer service uansett leverandør og system."),
       ("Hvilke typer brannalarmanlegg finnes?","Konvensjonelle, adresserbare og trådløse anlegg. Riktig valg avhenger av byggets størrelse og bruk.")],
  related=["boligalarm","dokumentasjon-fg-kontroll","nodlys"]),
 dict(slug="boligalarm", name="Boligalarm", select="Boligalarm",
  title="Boligalarm Bergen – Ajax brann- og innbruddsalarm | BSV Fire",
  desc="Boligalarm og Ajax brannalarm i Bergen og Vestland. Prosjektering, programmering, idriftsettelse og service for bolig, borettslag og sameier. Be om tilbud.",
  h1="Boligalarm i Bergen og Vestland",
  lead="Trygghet hjemme. Riktig valgt, programmert og vedlikeholdt, med Ajax Systems.",
  img="tjeneste-boligalarm.jpg", alt="Trådløs boligalarm montert i en bolig i Bergen",
  what="En boligalarm gir tidlig varsling ved brann og innbrudd. Den fungerer best når den er riktig valgt, programmert og fulgt opp over tid. Ajax-systemene er trådløse og finnes i utgaver for både bolig og næringsbygg.",
  law=["Alle boliger skal ha røykvarsler i hver etasje, plassert slik at alarmen høres tydelig på soverom (forskrift om brannforebygging).",
       "I større boligbygg, sameier og borettslag kan det være krav om automatisk brannalarmanlegg etter NS 3960.",
       "Krav i nye bygg følger TEK17."],
  does=[("Valg av løsning","Vi hjelper deg å velge riktig system for boligen."),("Programmering og idriftsettelse","Alt settes opp og testes før overlevering."),
        ("Service og oppfølging","Kontroll slik at alarmen virker når den trengs."),("Borettslag og sameier","Løsninger og avtaler for fellesarealer.")],
  faq=[("Hva er en Ajax-alarm?","Et trådløst alarmsystem fra Ajax Systems for brann og innbrudd. Det styres fra en app og kan utvides senere."),
       ("Hvor skal røykvarslerne henge?","Minst én i hver etasje, slik at alarmen høres på soverom. Montér i taket, vekk fra vegg og hjørner."),
       ("Trenger borettslaget brannalarmanlegg?","Det kan være krav i større boligbygg. Vi vurderer bygget og sier hva som gjelder."),
       ("Kan dere ta service på eksisterende alarm?","Ja. Ta kontakt, så ser vi på anlegget ditt.")],
  related=["brannalarm","brannslokkeutstyr","lovpalagte-krav"]),
 dict(slug="sprinkler-vanntaake", name="Sprinkler og vanntåke", select="Sprinkler og vanntåke",
  title="Sprinkleranlegg og vanntåke Bergen – kontroll og service | BSV Fire",
  desc="Kontroll og service av sprinkleranlegg og vanntåkeanlegg i Bergen og Vestland. Årlige hovedkontroller, testing av pumper og tanker og full dokumentasjon.",
  h1="Sprinkler og vanntåke i Bergen og Vestland",
  lead="Automatisk slokking som fungerer når det gjelder, med riktig kontroll og dokumentasjon.",
  img="tjeneste-sprinkler.jpg", alt="Sprinklerhoder i taket i et moderne næringsbygg",
  film=("sprinkler.mp4", "sprinkler-poster.jpg", "Sprinklerkontroll."),
  what="Et sprinkleranlegg slokker eller holder en brann nede automatisk, før brannvesenet kommer. Våtanlegg, tørranlegg, deluge og pre-action brukes etter byggets behov. Vanntåke er en annen løsning for automatisk slokking.",
  law=["Eier har ansvar for at slokkeanlegg fungerer som forutsatt, og at kontroller dokumenteres.",
       "Sprinkleranlegg prosjekteres og kontrolleres etter NS-EN 12845.",
       "Anlegget skal være koblet riktig mot brannalarmanlegget."],
  does=[("Kontroll og service","Ukentlige og månedlige rutiner og årlig hovedkontroll."),("Pumper og vanntanker","Testing av pumper, ventiler og tanker."),
        ("Koordinering","Vi samkjører med brannalarm og leverandører."),("Dokumentasjon","Rapport etter hver kontroll.")],
  faq=[("Hva er forskjellen på våt- og tørranlegg?","Våtanlegg har vann i rørene hele tiden. Tørranlegg har trykkluft eller nitrogen og passer i uoppvarmede områder."),
       ("Hvor ofte må sprinkleranlegget kontrolleres?","Med faste rutiner gjennom året og en årlig hovedkontroll. Vi setter opp en plan for anlegget ditt."),
       ("Tar dere service på alle typer?","Vi tar service på sprinkler- og vanntåkeanlegg i samarbeid med sertifiserte leverandører."),
       ("Får vi dokumentasjon?","Ja. Du får rapport som kan vises ved tilsyn.")],
  related=["brannalarm","brannslokkeutstyr","dokumentasjon-fg-kontroll"]),
 dict(slug="nodlys", name="Nødlys", select="Nødlys",
  title="Nødlys og nødbelysning Bergen – kontroll og service | BSV Fire",
  desc="Kontroll, service og idriftsettelse av nødlys og ledesystem i Bergen og Vestland. Månedlige funksjonstester, årlige durasjonstester og dokumentasjon.",
  h1="Nødlys i Bergen og Vestland",
  lead="Rømningsveier som lyser når strømmen går. Kontroll, service og dokumentasjon.",
  img="tjeneste-nodlys.jpg", alt="Nødlys lyser opp en rømningsvei i et moderne bygg",
  film=("nodlys.mp4", "nodlys-poster.jpg", "Nødlys som tennes."),
  what="Nødlys og ledesystem lyser opp rømningsveiene ved strømbrudd eller brann, slik at alle finner trygt ut. Anlegget må testes jevnlig for å fungere når det trengs.",
  law=["Eier skal sørge for at nødlys fungerer og kontrolleres jevnlig.",
       "Kravene følger TEK17 og standardene NS-EN 1838 og NS-EN 50172.",
       "Funksjonstester og durasjonstester skal dokumenteres."],
  does=[("Funksjonstest","Månedlige tester."),("Durasjonstest","Årlig test av batteridrift."),
        ("Batteri og lyskilder","Utskifting og reparasjon."),("Dokumentasjon","Logg og rapport klar til tilsyn.")],
  faq=[("Hvor lenge skal nødlys lyse?","Det avhenger av byggets bruk og rømningstid. Vanligvis minst 1 time, og lenger i bygg som sykehus og hoteller. Vi vurderer kravet for ditt bygg."),
       ("Hvor ofte må nødlys kontrolleres?","Månedlig funksjonstest og årlig durasjonstest er vanlig praksis, etter NS-EN 50172."),
       ("Hva er forskjellen på nødlys og ledelys?","Nødlys lyser opp rømningsveien. Ledelys viser retningen ut."),
       ("Kan dere ta over service på eksisterende anlegg?","Ja, uansett leverandør.")],
  related=["brannalarm","roykventilasjon","dokumentasjon-fg-kontroll"]),
 dict(slug="roykventilasjon", name="Røykventilasjon", select="Røykventilasjon",
  title="Røykventilasjon og røykluker Bergen – service og kontroll | BSV Fire",
  desc="Service og kontroll av røykventilasjon, røykluker og trykksetting av trapperom i Bergen og Vestland. Funksjonstester, kapasitetstester og full dokumentasjon.",
  h1="Røykventilasjon i Bergen og Vestland",
  lead="Rømningsveier som holdes fri for røyk. Kontroll og service med dokumentasjon.",
  img="tjeneste-roykventilasjon.jpg", alt="Røykventilasjon i trapperom i et moderne bygg",
  what="Røykventilasjon leder røyk og varme ut av bygget og holder trapperom og rømningsveier fri for røyk. Det kan være naturlig ventilasjon med røykluker, mekaniske vifter eller trykksetting av trapperom.",
  law=["Eier skal sørge for at røykventilasjon fungerer som forutsatt.",
       "Kravet til anlegg følger byggets brannkonsept og TEK17. Standardene NS-EN 12101 og NS 3901 gjelder.",
       "Tester og kontroller skal dokumenteres."],
  does=[("Funksjonstest","Månedlige tester av luker og styring."),("Kapasitetstest","Årlig test av vifter og systemer."),
        ("Kontroll av sensorer","Kalibrering av sensorer og styringer."),("Rapport","Komplett dokumentasjon.")],
  faq=[("Hva er røykluker, og hvorfor trengs de?","Røykluker åpnes automatisk ved brann og slipper røyk og varme ut, slik at rømningsveien holdes fri."),
       ("Når er det krav om røykventilasjon?","Det følger av byggets brannkonsept og TEK17. Vi hjelper deg å se hva som gjelder for bygget ditt."),
       ("Hvor ofte må røykventilasjon kontrolleres?","Vi anbefaler jevnlige funksjonstester og en årlig kapasitetstest, med dokumentasjon."),
       ("Kobles det mot brannalarmen?","Ja. Røykventilasjon styres vanligvis av brannalarmanlegget.")],
  related=["brannalarm","nodlys","dokumentasjon-fg-kontroll"]),
 dict(slug="brannslokkeutstyr", name="Brannslokkeutstyr", select="Brannslokkeutstyr",
  title="Brannslokkeutstyr Bergen – kontroll av slokkere og slanger | BSV Fire",
  desc="Kontroll og service av brannslokkeutstyr i Bergen og Vestland: håndslokkere, brannslanger og trykktest. Uavhengig av leverandør. Be om tilbud.",
  h1="Brannslokkeutstyr i Bergen og Vestland",
  lead="Kontroll og service av håndslokkere og brannslanger, uansett leverandør.",
  img="tjeneste-brannslokkeutstyr.jpg", alt="Tekniker kontrollerer brannslokkeutstyr og brannslange",
  what="Brannslokkeutstyr er første linje når en brann oppstår: håndslokkere og brannslanger. Utstyret må være riktig plassert, av riktig type for risikoen og i forsvarlig stand.",
  law=["Eier skal sørge for at brannslokkeutstyr fungerer og kontrolleres regelmessig.",
       "Kontrollen skal dokumenteres og merkes på utstyret.",
       "Brannslanger og håndslokkere kontrolleres årlig."],
  does=[("Håndslokkere","Årlig kontroll, service og utskifting."),("Brannslanger","Funksjonskontroll og trykktest."),
        ("Riktig utstyr","Vi hjelper med type og plassering."),("Merking og rapport","Dokumentasjon etter kontroll.")],
  faq=[("Hvor ofte må brannslokkeutstyr kontrolleres?","Håndslokkere og brannslanger kontrolleres årlig i næringsbygg. For privatbolig er det 5-årskontroll av slokkere."),
       ("Hvordan velger jeg riktig brannslokkeutstyr?","Det avhenger av hva som kan brenne. Vi hjelper deg med type og plassering."),
       ("Hva er trykktest av brannslanger?","En test som viser at slangen tåler trykk og fungerer når den trengs."),
       ("Tar dere også slokkere fra andre leverandører?","Ja. Vi utfører kontroll uavhengig av leverandør.")],
  related=["brannalarm","sprinkler-vanntaake","dokumentasjon-fg-kontroll"]),
 dict(slug="dokumentasjon-fg-kontroll", name="Dokumentasjon og FG-kontroll", select="Dokumentasjon / FG-kontroll",
  title="Brannteknisk dokumentasjon og FG-kontroll Bergen | BSV Fire",
  desc="O-planer, rømningsplaner, FDV-dokumentasjon og årlig FG-kontroll i Bergen og Vestland. Dokumentasjon som tåler tilsyn. Be om tilbud fra FG-sertifisert firma.",
  h1="Dokumentasjon og FG-kontroll i Bergen og Vestland",
  lead="Dokumentasjon som tåler tilsyn, og årlig FG-kontroll av brannalarmanlegget.",
  img="tjeneste-dokumentasjon.jpg", alt="Tekniker fyller ut kontrollrapport i et næringsbygg",
  what="Brannteknisk dokumentasjon viser hva som er installert, hvordan det skal driftes og at det er kontrollert. Den trengs ved nye anlegg, endringer i bygget og i oppfølgingen av internkontrollen.",
  law=["All dokumentasjon fra installasjoner, kontroller og service skal oppbevares og kunne vises til brannmyndighetene.",
       "Årlig kontroll av brannalarmanlegg skal utføres av FG-sertifisert firma etter FG790 og NS 3960.",
       "Manglende dokumentasjon kan få følger for forsikringsdekningen."],
  does=[("O-planer","Oversikt over detektorer, sentraler og anlegg."),("Rømningsplaner","Tydelige planer per etasje."),
        ("FDV-dokumentasjon","Drift, vedlikehold og instrukser."),("FG-kontroll","Årlig kontroll med rapport.")],
  faq=[("Hvilken dokumentasjon kreves for brannsikkerhet?","Blant annet kontrollrapporter, O-planer, rømningsplaner og FDV-dokumentasjon. Omfanget avhenger av bygget."),
       ("Hva er en O-plan?","Et oversiktskart over brannalarmanleggets detektorer, sentral og soner."),
       ("Hva skjer hvis dokumentasjonen ikke er i orden?","Det kan gi pålegg fra brannvesenet og kan påvirke forsikringen. Vi hjelper deg å få orden."),
       ("Kan dere lage dokumentasjon til eksisterende bygg?","Ja. Vi utarbeider og kvalitetssikrer dokumentasjon for nye og eksisterende anlegg.")],
  related=["brannalarm","lovpalagte-krav","nodlys"]),
]
BY_SLUG = {s["slug"]: s for s in SERVICES}
BY_SLUG["lovpalagte-krav"] = {"name": "Lovpålagte krav"}


def service_page(s):
    cr_html, cr_ld = crumbs([(s["name"], None)])
    film = ""
    if s.get("film"):
        f, poster, label = s["film"]
        film = f'''<section class="film" aria-label="Film: {e(label)}" style="min-height:55vh">
  <video data-autoplay muted loop playsinline preload="none" poster="/assets/img/{poster}" aria-hidden="true"><source src="/assets/video/{f}" type="video/mp4"></video>
  <div class="wrap"><span class="eyebrow">{e(s["name"])}</span><h2>{e(label)}</h2><a class="btn btn-primary" href="tel:{PHONE}">Ring oss</a></div>
</section>'''
    does = "".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in s["does"])
    law = "".join(f"<li>{e(x)}</li>" for x in s["law"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in s["faq"])
    related = "".join(f'<a href="/{r}/">{e(BY_SLUG[r]["name"])}</a>' for r in s["related"])
    body = f'''<section class="page-hero"><div class="wrap grid">
  <div>{cr_html}
    <span class="eyebrow">Bergen og Vestland</span>
    <h1>{e(s["h1"])}</h1>
    <p class="lead">{e(s["lead"])}</p>
    <div class="btn-row"><a class="btn btn-primary" href="tel:{PHONE}">Ring oss</a><a class="btn btn-outline" href="#tilbud">Be om tilbud</a></div>
  </div>
  <div class="shot"><img src="/assets/img/{s["img"]}" alt="{e(s["alt"])}" width="800" height="1000" onerror="this.remove()"></div>
</div></section>

<section class="sec-tight alt"><div class="wrap two">
  <div><h2>Hva er {e(s["name"].lower())}?</h2><p class="lead">{e(s["what"])}</p></div>
  <div class="law"><h3>Lovkrav kort forklart</h3><ul class="checks">{law}</ul>
    <p class="form-note" style="margin-top:1rem"><a href="/lovpalagte-krav/">Les mer om lovpålagte krav</a></p></div>
</div></section>

<section class="sec-tight"><div class="wrap">
  <h2>Hva vi gjør</h2>
  <div class="cards">{does}</div>
  <p style="margin-top:1.6rem" class="form-note">FG-sertifisert (FG750, FG760, FG790). Sertifikatnr. FG-760-8016. Vi dekker Bergen og Vestland.</p>
</div></section>
{film}
<section class="sec-tight alt"><div class="wrap" style="max-width:860px">
  <h2>Ofte stilte spørsmål</h2>
  <div class="faq">{faq}</div>
  <div class="related" aria-label="Relaterte tjenester">{related}</div>
</div></section>

<section class="contact" id="tilbud"><div class="wrap contact-grid">
  <div><span class="eyebrow">Tilbud</span><h2>Be om tilbud på {e(s["name"].lower())}</h2>
  <p class="lead">Fortell kort hva du trenger, så tar vi kontakt.</p>
  <address><strong>Brannteknisk Service og Vedlikehold AS</strong><br>Sælenveien 44, 5151 Straumsgrend<br>
  <a href="tel:{PHONE}">{PHONE_TXT}</a><br><a href="mailto:mail@bsvfire.no">mail@bsvfire.no</a></address></div>
  {form(s["select"])}
</div></section>'''
    url = f'{BASE}/{s["slug"]}/'
    svc = {"@context": "https://schema.org", "@type": "Service", "name": s["name"] + " i Bergen og Vestland",
           "serviceType": s["name"], "description": s["desc"], "url": url,
           "provider": {"@type": "LocalBusiness", "@id": BASE + "/#org", "name": "Brannteknisk Service og Vedlikehold AS"},
           "areaServed": [{"@type": "City", "name": "Bergen"}, {"@type": "AdministrativeArea", "name": "Vestland"}]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity":
              [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]}
    page(s["slug"] + "/", s["title"], s["desc"], body, [svc, faq_ld, cr_ld], og_image="og-bsv-fire.jpg")


for s in SERVICES:
    service_page(s)

# ------------------------------------------------------------------ LOVKRAV
cr_html, cr_ld = crumbs([("Lovpålagte krav", None)])
duties = [("Årlig kontroll", "Eier er ansvarlig for at brannalarmanlegget kontrolleres årlig av et FG-sertifisert firma (FG790 og NS 3960)."),
          ("Dokumentasjon", "All dokumentasjon fra installasjon, kontroll og service skal oppbevares og kunne vises til brannmyndighetene."),
          ("Vedlikehold", "Brannsikkerhetsutstyr skal fungere til enhver tid. Feil og mangler utbedres umiddelbart."),
          ("Varsling ved endringer", "Endringer i bygget som kan påvirke brannsikkerheten må meldes, og dokumentasjonen oppdateres."),
          ("Opplæring og informasjon", "Beboere og brukere skal få nødvendig informasjon om brannsikkerhetsutstyret."),
          ("Forsikring", "Manglende vedlikehold og kontroll kan gjøre at forsikringsselskapet nekter erstatning ved brann.")]
board = ["Sørge for årlig kontroll av brannalarmanlegg", "Inngå serviceavtale med FG-sertifisert firma", "Budsjettere for vedlikehold og oppgraderinger",
         "Oppbevare all dokumentasjon forsvarlig", "Informere beboere om brannsikkerhet", "Følge opp avvik og mangler umiddelbart",
         "Gjennomføre brannøvelser etter behov", "Sikre at rømningsveier er frie"]
body = f'''<section class="page-hero"><div class="wrap" style="max-width:900px">{cr_html}
  <span class="eyebrow">For eiere og styrer</span><h1>Lovpålagte krav til brannsikkerhet</h1>
  <p class="lead">Som eier eller styremedlem har du et lovpålagt ansvar for brannsikkerheten. Her er det viktigste, enkelt forklart.</p>
  <div class="btn-row"><a class="btn btn-primary" href="tel:{PHONE}">Ring oss</a><a class="btn btn-outline" href="#tilbud">Be om tilbud</a></div></div></section>
<section class="sec-tight alt"><div class="wrap"><h2>Eiers plikter</h2>
  <div class="cards">{"".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in duties)}</div></div></section>
<section class="sec-tight"><div class="wrap two">
  <div><h2>Styrets ansvar i borettslag og sameier</h2><p class="lead">Styret har et særskilt ansvar for brannsikkerheten i fellesarealene.</p>
  <ul class="checks">{"".join(f"<li>{e(x)}</li>" for x in board)}</ul></div>
  <div class="law"><h3>Personlig ansvar</h3><p>Styremedlemmer kan holdes personlig ansvarlige hvis de:</p>
  <ul class="checks"><li>unnlater å følge opp lovpålagte krav</li><li>ikke budsjetterer for nødvendig vedlikehold</li><li>ignorerer kjente feil og mangler</li><li>ikke følger opp pålegg fra brannvesenet</li></ul>
  <p class="form-note">Styret bør tegne styreansvarsforsikring som dekker brannsikkerhetsansvar.</p></div>
</div></section>
<section class="sec-tight alt"><div class="wrap" style="max-width:860px"><h2>Egenkontroll</h2>
  <p class="lead">Eier og styre skal gjennomføre systematisk egenkontroll av brannsikkerheten, med rutiner som sikrer at kravene overholdes. Dokumentasjonen skal kunne vises ved inspeksjon.</p>
  <h3 style="margin-top:2rem">Se kravene per tjeneste</h3>
  <div class="related">{"".join(f'<a href="/{x["slug"]}/">{e(x["name"])}</a>' for x in SERVICES)}</div></div></section>
<section class="contact" id="tilbud"><div class="wrap contact-grid">
  <div><span class="eyebrow">Usikker på hva som gjelder?</span><h2>Vi hjelper deg å få orden.</h2><p class="lead">Fortell oss om bygget, så sier vi hva som må kontrolleres.</p></div>{form()}</div></section>'''
page("lovpalagte-krav/", "Lovpålagte brannkrav for eiere og styrer i Bergen | BSV Fire",
     "Enkelt forklart: eiers og styrets plikter for brannsikkerhet, årlig FG-kontroll, dokumentasjon og egenkontroll. Hjelp fra FG-sertifisert firma i Bergen og Vestland.",
     body, [cr_ld])

# ------------------------------------------------------------------ MILJØ
cr_html, cr_ld = crumbs([("Miljø og bærekraft", None)])
practice = [("Lengre levetid", "Riktig kontroll, vedlikehold og reparasjon forlenger levetiden på eksisterende branntekniske installasjoner og reduserer unødvendig utskifting."),
            ("Energieffektivitet", "Vi velger intelligente systemer som bruker mindre energi og færre ressurser."),
            ("Avfall og resirkulering", "Vi minimerer avfall og resirkulerer materialer der det er mulig."),
            ("Mindre transport", "Vi arbeider systematisk med å redusere transport og utslipp."),
            ("Samarbeid", "Vi samarbeider med partnere og leverandører som deler vår bærekraftsvisjon, blant annet Miljønorge og Bergen Batteri Service."),
            ("Kompetanse", "Våre ansatte er opplært i bærekraftige arbeidsmåter og leter hele tiden etter forbedringer.")]
body = f'''<section class="page-hero green-sec"><div class="wrap grid">
  <div>{cr_html}<span class="cert-badge">✓ Miljøfyrtårn-sertifisert</span>
  <h1>Miljøfyrtårn-sertifisert brannsikkerhet</h1>
  <p class="lead">Vi leverer branntekniske tjenester med minst mulig belastning på miljø og klima. Sertifisert første gang i 2023 og resertifisert i 2026.</p>
  <div class="btn-row"><a class="btn btn-dark" href="#dokumenter">Last ned dokumenter</a><a class="btn btn-outline" href="#tilbud">Be om tilbud</a></div></div>
  <div class="shot"><img src="/assets/img/miljo-elbil.jpg" alt="Elektrisk servicebil med fjell og natur ved Bergen i bakgrunnen" width="800" height="1000" onerror="this.remove()"></div>
</div></section>
<section class="sec-tight"><div class="wrap two"><div><h2>Vår miljøpolicy</h2>
  <p class="lead">BSV Fire har som mål å levere branntekniske tjenester med minst mulig belastning på miljø og klima.</p></div>
  <div><p>Vi arbeider systematisk med å redusere ressursbruk, transport, utslipp og avfall, og velger miljøvennlige løsninger der det er praktisk og faglig forsvarlig.</p>
  <p>Gjennom riktig kontroll, vedlikehold og reparasjon forlenger vi levetiden på eksisterende installasjoner. Vi arbeider kontinuerlig med å forbedre miljøprestasjonen.</p>
  <p><a class="btn btn-outline" href="/dokumenter/bsv-fire-miljopolicy-2026.pdf">Les hele miljøpolicyen (PDF, 2026)</a></p></div></div></section>
<section class="sec-tight alt"><div class="wrap"><h2>Dette gjør vi i praksis</h2>
  <div class="cards">{"".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in practice)}</div></div></section>
<section class="sec-tight"><div class="wrap two"><div><h2>Om Miljøfyrtårn</h2></div>
  <div><p>Miljøfyrtårn-sertifiseringen hjelper oss å systematisere, dokumentere og synliggjøre arbeidet med å redusere miljøbelastningen. Den gir et tydelig rammeverk for blant annet transport, energibruk, avfall, innkjøp, arbeidsmiljø og ressursbruk.</p>
  <p>BSV Fire ble første gang Miljøfyrtårn-sertifisert i 2023 og resertifisert i 2026.</p></div></div></section>
<section class="sec-tight alt" id="dokumenter"><div class="wrap" style="max-width:860px"><h2>Rapporter og dokumenter</h2>
  <div class="docs">
   <a class="doc" href="/dokumenter/bsv-fire-miljopolicy-2026.pdf"><span><strong>Miljøpolicy 2026</strong><small>PDF</small></span><span class="dl">Last ned ↓</span></a>
   <a class="doc" href="/dokumenter/bsv-fire-aktsomhetsvurderinger-2026.pdf"><span><strong>Redegjørelse for aktsomhetsvurderinger 2026 (åpenhetsloven)</strong><small>PDF</small></span><span class="dl">Last ned ↓</span></a>
   <!-- Legg til flere dokumenter her: Miljøfyrtårn-sertifikat, miljørapport osv. Kopier en av <a class="doc"> over. -->
  </div></div></section>
<section class="contact" id="tilbud"><div class="wrap contact-grid">
  <div><span class="eyebrow">Kontakt</span><h2>Spørsmål om miljøarbeidet?</h2><p class="lead">Ring eller send oss en melding.</p>
  <address><a href="tel:{PHONE}">{PHONE_TXT}</a><br><a href="mailto:mail@bsvfire.no">mail@bsvfire.no</a></address></div>{form()}</div></section>'''
page("miljo-og-barekraft/", "Miljøfyrtårn-sertifisert brannsikkerhet i Bergen – miljø | BSV Fire",
     "BSV Fire er Miljøfyrtårn-sertifisert. Les miljøpolicyen, se hva vi gjør i praksis og last ned dokumenter. Grønn brannsikkerhet i Bergen og Vestland.",
     body, [cr_ld])

# ------------------------------------------------------------------ OM OSS
cr_html, cr_ld = crumbs([("Om oss", None)])
values = [("Sikkerhet først", "Kundens sikkerhet er alltid vår høyeste prioritet."), ("Kvalitet og pålitelighet", "Jobben skal gjøres riktig første gang."),
          ("Partnerskap", "Langsiktige relasjoner basert på tillit, åpenhet og respekt."), ("Innovasjon", "Vi holder oss oppdatert på nye teknologier og metoder.")]
body = f'''<section class="page-hero"><div class="wrap" style="max-width:900px">{cr_html}
  <span class="eyebrow">Om oss</span><h1>Din pålitelige partner innen brannsikkerhet siden 2018</h1>
  <p class="lead">Brannteknisk Service og Vedlikehold AS ble etablert i 2018 av Erik Sebastian Skille, som daglig leder og grunnlegger.</p>
  <div class="btn-row"><a class="btn btn-primary" href="tel:{PHONE}">Ring oss</a><a class="btn btn-outline" href="/kontakt/">Kontakt oss</a></div></div></section>
<section class="sec-tight alt"><div class="wrap two"><div><h2>Én kontaktperson</h2></div>
  <div><p class="lead">Vi vil være totalleverandør innen brannsikkerhet: dokumentasjon, prosjektering og teknikk. Du får ett firma å forholde seg til for nødlys, slokkeutstyr, sprinkler, dokumentasjon og brannvarsling.</p>
  <p>Mangler vi kompetanse på et fagfelt, bruker vi gode samarbeidspartnere og stiller krav til dem om kompetanse, godkjenninger, dokumentasjon og rapportering. Det merker du ikke som kunde.</p></div></div></section>
<section class="sec-tight"><div class="wrap"><h2>Våre verdier</h2>
  <div class="cards">{"".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in values)}</div></div></section>
<section class="sec-tight alt"><div class="wrap two"><div><h2>Sertifisert og lokal</h2></div>
  <div><p>Vi er sertifisert FG750, FG760 og FG790 (FG-760-8016) og Miljøfyrtårn-sertifisert. Kontoret ligger i Straumsgrend, og vi dekker Bergen og Vestland.</p>
  <p><a href="/miljo-og-barekraft/">Les om miljøarbeidet</a> · <a href="/referanser/">Se referanser</a></p></div></div></section>
<section class="contact" id="tilbud"><div class="wrap contact-grid"><div><span class="eyebrow">Kontakt</span><h2>La oss ta en prat.</h2><p class="lead">Uforpliktende samtale om dine behov.</p></div>{form()}</div></section>'''
page("om-oss/", "Om BSV Fire – FG-sertifisert brannteknisk firma i Bergen",
     "Brannteknisk Service og Vedlikehold AS, etablert 2018. FG-sertifisert og Miljøfyrtårn-sertifisert, med kontor i Straumsgrend. Service i Bergen og Vestland.",
     body, [cr_ld])

# ------------------------------------------------------------------ REFERANSER
cr_html, cr_ld = crumbs([("Referanser", None)])
body = f'''<section class="page-hero"><div class="wrap" style="max-width:900px">{cr_html}
  <span class="eyebrow">Referanser</span><h1>Referanser og prosjekter</h1>
  <p class="lead">Utvalgte kunder og prosjekter i Bergen og Vestland.</p></div></section>
<section class="sec-tight alt"><div class="wrap">
  <!-- LEGG INN REFERANSER HER. Kopier kortet under for hver referanse (kun godkjente kunder og tall).
  <div class="card"><h3>Kundenavn</h3><p>Kort om oppdraget · Sted</p></div> -->
  <div class="note"><strong>Referanser legges inn her.</strong> Send kundenavn, sted og en linje om oppdraget (og bilder med tillatelse), så publiserer vi dem.</div>
  <div class="cards"></div></div></section>
<section class="contact" id="tilbud"><div class="wrap contact-grid"><div><span class="eyebrow">Tilbud</span><h2>Vil du bli vår neste kunde?</h2><p class="lead">Ring oss eller be om tilbud.</p>
  <div class="btn-row"><a class="btn btn-primary" href="tel:{PHONE}">Ring oss</a></div></div>{form()}</div></section>'''
page("referanser/", "Referanser og prosjekter – brannsikkerhet i Bergen | BSV Fire",
     "Utvalgte referanser og prosjekter fra BSV Fire. FG-sertifisert brannteknisk service for bedrifter, borettslag og kommuner i Bergen og Vestland.",
     body, [cr_ld], noindex=True)

# ------------------------------------------------------------------ KONTAKT
cr_html, cr_ld = crumbs([("Kontakt", None)])
body = f'''<section class="page-hero"><div class="wrap" style="max-width:900px">{cr_html}
  <span class="eyebrow">Kontakt</span><h1>Kontakt BSV Fire i Bergen</h1>
  <p class="lead">Ring oss, eller be om tilbud. Vi svarer så fort vi kan.</p>
  <div class="btn-row"><a class="btn btn-primary" href="tel:{PHONE}">Ring {PHONE_TXT}</a></div></div></section>
<section class="contact" id="tilbud"><div class="wrap contact-grid">
  <div><h2>Besøk og post</h2>
  <address><strong>Brannteknisk Service og Vedlikehold AS</strong><br>Sælenveien 44<br>5151 Straumsgrend<br>
  <a href="tel:{PHONE}">{PHONE_TXT}</a><br><a href="mailto:mail@bsvfire.no">mail@bsvfire.no</a><br>Org.nr. 921 044 879</address>
  <p><a href="https://www.google.com/maps/search/?api=1&query=S%C3%A6lenveien+44+5151+Straumsgrend" rel="noopener">Vis på kart</a></p>
  <h3 style="margin-top:2rem">Område</h3><p>Vi dekker Bergen og Vestland.</p></div>
  {form()}</div></section>'''
page("kontakt/", "Kontakt BSV Fire – brannsikkerhet i Bergen og Vestland",
     "Ring +47 900 46 600 eller be om tilbud. BSV Fire, Sælenveien 44, Straumsgrend. FG-sertifisert service i Bergen og Vestland.",
     body, [cr_ld])

# ------------------------------------------------------------------ PERSONVERN
cr_html, cr_ld = crumbs([("Personvern", None)])
body = f'''<section class="page-hero"><div class="wrap prose" style="max-width:820px">{cr_html}
  <h1>Personvern og informasjonskapsler</h1>
  <p class="lead">Slik behandler vi opplysninger på bsvfire.no.</p>
  <h2>Behandlingsansvarlig</h2><p>Brannteknisk Service og Vedlikehold AS, org.nr. 921 044 879, Sælenveien 44, 5151 Straumsgrend. E-post: <a href="mailto:mail@bsvfire.no">mail@bsvfire.no</a>.</p>
  <h2>Kontaktskjema</h2><p>Når du sender skjemaet, behandler vi navn, telefon, adresse og meldingen din for å svare på henvendelsen og gi tilbud. Vi lagrer opplysningene så lenge det er nødvendig for oppfølgingen.</p>
  <h2>Informasjonskapsler</h2><p>Vi bruker nødvendige kapsler for å huske valgene dine (samtykke og lys/mørk modus). Hvis du gir samtykke, bruker vi Google Analytics og Google Ads til å forstå bruken av siden og måle annonser. Ingen analyse eller annonsemåling lastes før du har samtykket. Du kan endre valget via «Informasjonskapsler» nederst på siden.</p>
  <h2>Dine rettigheter</h2><p>Du kan be om innsyn, retting eller sletting av opplysninger vi har om deg, og du kan klage til Datatilsynet. Kontakt oss på e-post.</p>
  <p class="form-note">Utkast: bør gjennomgås av BSV før publisering.</p></div></section>'''
page("personvern/", "Personvern og informasjonskapsler | BSV Fire",
     "Slik behandler BSV Fire personopplysninger og informasjonskapsler på bsvfire.no.", body, [cr_ld])

# ------------------------------------------------------------------ 404, sitemap, robots
open(os.path.join(ROOT, "404.html"), "w", encoding="utf8").write(
    open(os.path.join(ROOT, "personvern", "index.html"), encoding="utf8").read()
    .replace("<title>Personvern og informasjonskapsler | BSV Fire</title>", "<title>Siden finnes ikke | BSV Fire</title>")
    .replace('<link rel="canonical" href="https://www.bsvfire.no/personvern/">', '<meta name="robots" content="noindex">')
    .replace("<h1>Personvern og informasjonskapsler</h1>", "<h1>Siden finnes ikke</h1>")
    .replace("Slik behandler vi opplysninger på bsvfire.no.", 'Adressen finnes ikke, eller siden er flyttet. <a href="/">Gå til forsiden</a> eller <a href="/kontakt/">ta kontakt</a>.'))
# 404: fjern personverntekst
t = open(os.path.join(ROOT, "404.html"), encoding="utf8").read()
t = re.sub(r'<h2>Behandlingsansvarlig</h2>.*?<p class="form-note">Utkast.*?</p>', "", t, flags=re.S)
open(os.path.join(ROOT, "404.html"), "w", encoding="utf8").write(t)

paths = ["", "brannalarm/", "boligalarm/", "sprinkler-vanntaake/", "nodlys/", "roykventilasjon/", "brannslokkeutstyr/",
         "dokumentasjon-fg-kontroll/", "lovpalagte-krav/", "miljo-og-barekraft/", "om-oss/", "kontakt/", "personvern/"]
today = date.today().isoformat()
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod></url>\n" for p in paths) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf8").write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {BASE}/sitemap.xml\n")
print("Ferdig:", len(paths), "sider i sitemap")
