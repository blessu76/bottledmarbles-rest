(function () {
  "use strict";
  var KEY = "ipe_lang";
  var DEFAULT = "en";
  var LANGS = ["en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"];
  var BOT = /bot|crawl|spider|slurp|lighthouse/i;

  function split(tag) {
    return String(tag || "").trim().toLowerCase().split(/[-_]/).filter(Boolean);
  }

  // One browser language tag -> a site language, or null when the site has none for it.
  function match(tag) {
    var p = split(tag);
    if (!p.length) return null;
    var code = p[0] === "in" ? "id" : p[0];
    if (code === "zh") return "zh-Hant";
    if (code === "pt") return "pt-BR";
    for (var i = 0; i < LANGS.length; i++) {
      if (LANGS[i].toLowerCase() === code) return LANGS[i];
    }
    return null;
  }

  function detect(list) {
    for (var i = 0; i < (list || []).length; i++) {
      var m = match(list[i]);
      if (m) return m;
    }
    return DEFAULT;
  }

  function saved() {
    try {
      var v = localStorage.getItem(KEY);
      return LANGS.indexOf(v) >= 0 ? v : null;
    } catch (e) {
      return null;
    }
  }

  function save(lang) {
    try {
      localStorage.setItem(KEY, lang);
    } catch (e) { /* storage blocked: the link still works */ }
  }

  // Only the language-less x-default URLs may redirect: "/" and "/journal/...". "/ko/..." etc. are never touched.
  function rootPath(path) {
    if (path === "/" || path === "/index.html") return "/";
    if (path === "/journal" || path.indexOf("/journal/") === 0) return path;
    return null;
  }

  var api = { match: match, detect: detect, rootPath: rootPath, LANGS: LANGS };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document === "undefined") return;

  var sel = document.querySelector("select[data-langsel]");
  if (sel) {
    sel.addEventListener("change", function () {
      var o = sel.options[sel.selectedIndex];
      save(o.getAttribute("lang"));
      location.href = o.value;
    });
  }

  var path = rootPath(location.pathname);
  if (path === null) return;
  if (BOT.test(navigator.userAgent || "")) return;
  var pick = saved() || detect(navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language]);
  if (pick !== DEFAULT) location.replace("/" + pick + path.replace("/index.html", "/") + location.search + location.hash);
})();
