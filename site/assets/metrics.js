/* Public reach, read in the browser: the downloads of every release asset
   and the GitHub stars. The Vercel build already bakes both in
   (scripts/site/apply_metrics.py); this keeps them current between
   deploys. A number shows only when it is known and above zero; an error,
   a rate limit or a partial answer leaves the built page as it is. */
(function () {
  "use strict";
  var API = "https://api.github.com/repos/MAECLY/coverly-roms";
  var KEY = "cr-metrics";
  var es = document.documentElement.lang === "es";
  var WORDS = es ? { downloads: ["descarga", "descargas"], stars: ["estrella", "estrellas"] }
    : { downloads: ["download", "downloads"], stars: ["star", "stars"] };

  function whole(n) { return typeof n === "number" && n >= 0 && n % 1 === 0; }

  function show(m) {
    var list = document.querySelectorAll("[data-metric]");
    for (var i = 0; i < list.length; i++) {
      var el = list[i], name = el.getAttribute("data-metric"), n = m[name];
      if (!WORDS[name] || !whole(n)) continue;
      if (n > 0) {
        el.textContent = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, es ? "." : ",") +
          " " + WORDS[name][n === 1 ? 0 : 1];
      }
      el.hidden = !(n > 0);
    }
  }

  function get(url) {
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 8000);
    return fetch(url, { headers: { Accept: "application/vnd.github+json" }, signal: ctl && ctl.signal })
      .then(function (res) { clearTimeout(timer); return res.ok ? res.json() : Promise.reject(); },
        function (e) { clearTimeout(timer); return Promise.reject(e); });
  }

  /* Every page of releases; past 10 pages the sum would be partial. */
  function downloads(page, sum) {
    return get(API + "/releases?per_page=100&page=" + page).then(function (list) {
      if (!Array.isArray(list)) return Promise.reject();
      for (var i = 0; i < list.length; i++) {
        var assets = (list[i] && list[i].assets) || [];
        for (var j = 0; j < assets.length; j++) {
          if (!assets[j] || !whole(assets[j].download_count)) return Promise.reject();
          sum += assets[j].download_count;
        }
      }
      if (list.length < 100) return sum;
      return page < 10 ? downloads(page + 1, sum) : Promise.reject();
    });
  }

  /* Cached for the tab for 10 minutes, like release.js: unauthenticated,
     GitHub allows 60 requests an hour per address. Only a full answer is
     kept. */
  function load() {
    try {
      var c = JSON.parse(sessionStorage.getItem(KEY));
      if (c && Date.now() - c.t < 6e5) return show(c.m);
    } catch (e) {}
    if (!window.fetch || !window.Promise) return;
    var m = {}, ok = 0;
    Promise.all([
      downloads(1, 0).then(function (n) { m.downloads = n; ok++; }, function () {}),
      get(API).then(function (r) {
        if (r && whole(r.stargazers_count)) { m.stars = r.stargazers_count; ok++; }
      }, function () {})
    ]).then(function () {
      if (ok === 2) try { sessionStorage.setItem(KEY, JSON.stringify({ t: Date.now(), m: m })); } catch (e) {}
      show(m);
    });
  }

  load();
})();
