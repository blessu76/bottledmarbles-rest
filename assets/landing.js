(function () {
  "use strict";
  var KEY = "bm-lang";
  var DEFAULT = "en";
  var links = Array.prototype.slice.call(document.querySelectorAll(".langs a[hreflang]"));
  var supported = links.map(function (a) { return a.getAttribute("hreflang"); });

  function split(tag) {
    return String(tag || "").trim().toLowerCase().split(/[-_]/).filter(Boolean);
  }

  function resolve(tag) {
    var p = split(tag);
    if (!p.length) return DEFAULT;
    var code = p[0] === "in" ? "id" : p[0];
    var rest = p.slice(1);
    if (code === "zh") {
      var script = rest.filter(function (x) { return x.length === 4 && /^[a-z]+$/.test(x); })[0];
      var region = rest.filter(function (x) { return x.length === 2 && /^[a-z]+$/.test(x); })[0];
      var hant = script === "hant" || (script === undefined && ["tw", "hk", "mo"].indexOf(region) >= 0);
      return hant ? "zh-Hant" : DEFAULT;
    }
    if (code === "pt") return "pt-BR";
    for (var i = 0; i < supported.length; i++) {
      if (supported[i].toLowerCase() === code) return supported[i];
    }
    return DEFAULT;
  }

  function saved() {
    try {
      var v = localStorage.getItem(KEY);
      return supported.indexOf(v) >= 0 ? v : null;
    } catch (e) {
      return null;
    }
  }

  function save(lang) {
    try {
      localStorage.setItem(KEY, lang);
    } catch (e) { /* storage blocked: the link still works */ }
  }

  links.forEach(function (a) {
    a.addEventListener("click", function () { save(a.getAttribute("hreflang")); });
  });

  if (location.pathname === "/" || location.pathname === "/index.html") {
    var pick = saved() || resolve(navigator.language);
    if (pick !== DEFAULT) location.replace("/" + pick + "/");
  }
})();
