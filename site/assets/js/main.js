/* BSV Fire – konfigurasjon. Fyll inn ID-er her; ingenting sporer før samtykke. */
window.BSV_CONFIG = {
  GA4_ID: "",            // f.eks. "G-XXXXXXXXXX"
  ADS_ID: "",            // f.eks. "AW-XXXXXXXXX"
  ADS_LABEL_FORM: "",    // konverteringsetikett «skjema sendt»
  ADS_LABEL_CALL: "",    // konverteringsetikett «telefonklikk»
  FORM_ENDPOINT: ""      // f.eks. Formspree-URL. Tom = åpner e-post i stedet
};

(function () {
  var C = window.BSV_CONFIG;
  var KEY = "bsv_consent_v1";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- Samtykke + tagger (Consent Mode v2, standard = avslått) ---- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("consent", "default", { ad_storage: "denied", analytics_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });

  var tagLoaded = false;
  function loadTags() {
    if (tagLoaded || !(C.GA4_ID || C.ADS_ID)) return;
    tagLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + (C.GA4_ID || C.ADS_ID);
    document.head.appendChild(s);
    gtag("js", new Date());
    if (C.GA4_ID) gtag("config", C.GA4_ID);
    if (C.ADS_ID) gtag("config", C.ADS_ID);
  }
  function getConsent() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function applyConsent(v) {
    if (v === "all") {
      gtag("consent", "update", { analytics_storage: "granted", ad_storage: "granted", ad_user_data: "granted", ad_personalization: "granted" });
      loadTags();
    }
  }
  var banner = $("#cookie");
  var saved = getConsent();
  if (saved) applyConsent(saved); else if (banner) banner.classList.add("show");
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-consent");
      setConsent(v); applyConsent(v); if (banner) banner.classList.remove("show");
    });
  });
  $$("[data-cookie-settings]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); if (banner) banner.classList.add("show"); });
  });

  /* ---- Konverteringer ---- */
  function convert(kind) {
    if (typeof gtag !== "function") return;
    gtag("event", kind === "call" ? "phone_click" : "generate_lead");
    var label = kind === "call" ? C.ADS_LABEL_CALL : C.ADS_LABEL_FORM;
    if (C.ADS_ID && label) gtag("event", "conversion", { send_to: C.ADS_ID + "/" + label });
  }
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener("click", function () { convert("call"); }); });

  /* ---- Skjema ---- */
  $$("form.quote").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (f.querySelector(".hp input").value) return;
      var d = {}; new FormData(f).forEach(function (v, k) { d[k] = v; });
      var ok = f.querySelector(".form-ok");
      function done() { convert("form"); f.reset(); if (ok) ok.style.display = "block"; }
      if (C.FORM_ENDPOINT) {
        fetch(C.FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(d) })
          .then(function (r) { if (r.ok) done(); else throw 0; })
          .catch(function () { alert("Noe gikk galt. Ring oss på +47 900 46 600."); });
      } else {
        var body = "Navn: " + d.navn + "\nTelefon: " + d.telefon + "\nTjeneste: " + d.tjeneste + "\nAdresse: " + d.adresse + "\n\n" + (d.melding || "");
        location.href = "mailto:mail@bsvfire.no?subject=" + encodeURIComponent("Tilbud: " + d.tjeneste) + "&body=" + encodeURIComponent(body);
        done();
      }
    });
  });

  /* ---- UI ---- */
  var header = $(".site-header");
  function onScroll() { if (header) header.classList.toggle("solid", window.scrollY > 40 || header.hasAttribute("data-solid")); }
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  var tb = $(".theme-btn");
  if (tb) tb.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    var nxt = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", nxt);
    try { localStorage.setItem("bsv_theme", nxt); } catch (e) {}
  });
  var mb = $(".menu-btn"), nav = $(".nav");
  if (mb) mb.addEventListener("click", function () { var o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o); if (o) header.setAttribute("data-solid", ""); else header.removeAttribute("data-solid"); onScroll(); });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { threshold: .12 });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("in"); }); }

  /* Film: spill kun når synlig, aldri ved redusert bevegelse */
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  $$("video[data-autoplay]").forEach(function (v) {
    if (reduce) { v.removeAttribute("autoplay"); v.pause(); return; }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) v.play().catch(function () {}); else v.pause(); }); }, { threshold: .25 }).observe(v);
    }
  });
})();
