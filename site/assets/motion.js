/* What moves, once, and only towards the finished page the HTML already
   shows. theme.js sets html.anim in <head> (no reduced motion, no
   Save-Data); this file adds html.motion once its setup worked. Any error,
   or reduced motion turned on mid-visit, runs halt(): every stop() puts
   its piece in the finished state and both classes go. Also: the
   third-party request counter in the footer. */
(function () {
  "use strict";

  var html = document.documentElement;
  var stops = [];

  /* Off-origin requests, minus the page's own fetches to OWN_HOSTS
     (CSP connect-src; check_site.py keeps both equal). */
  var OWN_HOSTS = ["api.github.com"];
  function counter() {
    var out = document.querySelector(".req-count"), ext = document.querySelector(".proof-ext");
    if (!out || !window.PerformanceObserver || !performance.getEntriesByType) return;
    var seen = {}, n = 0;
    var look = function (list) {
      list.forEach(function (e) {
        try {
          var u = new URL(e.name);
          var own = OWN_HOSTS.indexOf(u.hostname) > -1 && /^(fetch|xmlhttprequest)$/.test(e.initiatorType);
          if (/^https?:$/.test(u.protocol) && u.origin !== location.origin && !own && !seen[e.name]) seen[e.name] = ++n;
        } catch (x) {}
      });
      out.textContent = n;
      if (ext) ext.hidden = n === 0;
    };
    look(performance.getEntriesByType("resource"));
    try {
      new PerformanceObserver(function (l) { look(l.getEntries()); }).observe({ type: "resource", buffered: true });
    } catch (x) {}
  }

  function onScreen(el) {
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.bottom > 0 && r.top < innerHeight;
  }

  function once(target, threshold, fn) {
    var io = new IntersectionObserver(function (entries) {
      if (!entries.some(function (e) { return e.isIntersecting; })) return;
      io.disconnect();
      fn();
    }, { threshold: threshold });
    io.observe(target);
    return io;
  }

  function timers() {
    var list = [];
    var t = function (fn, ms, stop) {
      list.push(setTimeout(function () {
        try { fn(); } catch (x) { stop(); }
      }, ms));
    };
    t.clear = function () { list.forEach(clearTimeout); list = []; };
    return t;
  }

  /* The terminal types one scene (deck.js picks it) command by command;
     a line shows when its turn comes, and its output 200ms after the
     command. The untyped rest stays in place, hidden, so no glyph moves.
     The first scene is skipped when already on screen at load. */
  function terminal() {
    var term = document.querySelector(".term");
    if (!term) return;
    var all = term.querySelectorAll(".t-step"), text = [], later = timers();
    if (!all.length) return;
    var done = document.createElement("span"), rest = document.createElement("span");
    var cmd = function (el) { return el.querySelector(".t-cmd"); };
    var out = function (el) { return el.querySelector(".t-out") || done; };
    rest.className = "t-rest";
    for (var k = 0; k < all.length; k++) text[k] = cmd(all[k]).textContent;
    var stop = function () {
      later.clear();
      for (var j = 0; j < all.length; j++) {
        cmd(all[j]).textContent = text[j];
        all[j].classList.remove("t-wait");
        out(all[j]).classList.remove("t-hold");
      }
      term.classList.remove("typing");
    };
    stops.push(stop);
    var play = function (scene) {
      stop();
      var steps = scene.querySelectorAll(".t-step"), base = Array.prototype.indexOf.call(all, steps[0]);
      var type = function (s, i) {
        if (s >= steps.length) {
          term.classList.remove("typing");
          return later(function () { cmd(steps[s - 1]).textContent = text[base + s - 1]; }, 1400, stop);
        }
        var t = text[base + s];
        if (i === 0) {
          if (s) cmd(steps[s - 1]).textContent = text[base + s - 1];
          steps[s].classList.remove("t-wait");
          cmd(steps[s]).textContent = "";
          cmd(steps[s]).appendChild(done);
          cmd(steps[s]).appendChild(rest);
        }
        done.textContent = t.slice(0, i);
        rest.textContent = t.slice(i);
        if (i >= t.length) return later(function () {
          out(steps[s]).classList.remove("t-hold");
          later(function () { type(s + 1, 0); }, 420, stop);
        }, 200, stop);
        later(function () { type(s, i + 1); }, 18 + ((i * 37) % 17) + (t.charAt(i) === " " ? 30 : 0), stop);
      };
      term.classList.add("typing");
      for (var m = 0; m < steps.length; m++) {
        steps[m].classList.add("t-wait");
        out(steps[m]).classList.add("t-hold");
      }
      later(function () { type(0, 0); }, 300, stop);
    };
    var now = function () { return term.querySelector(".t-scene.is-on") || term.querySelector(".t-scene") || term; };
    if (!onScreen(term)) once(term, 0.45, function () { play(now()); });
    term.addEventListener("cr-deck", function () { try { play(now()); } catch (x) { stop(); } });
  }

  /* Already on screen at load: shown, not played. */
  function reveals() {
    var items = document.querySelectorAll("[data-reveal]");
    for (var i = 0; i < items.length; i++) {
      var el = items[i];
      if (onScreen(el)) el.classList.add("is-in", "no-anim");
      else once(el, 0.35, el.classList.add.bind(el.classList, "is-in"));
    }
  }

  /* A clip plays once in view, and again with its ↻ button: steps 3 and
     4 act out their screenshot (SVG over the still), and the drawn
     scenes do what they say. Inside an active deck (the four steps on a
     desk) a step plays when it is picked instead. */
  function clip(fig) {
    var box = fig.closest("[data-clip-box]"), button = box.querySelector(".clip-replay");
    var later = timers(), cl = box.classList, deck = fig.closest("[data-deck]");
    var ready = function (on) {
      if (on) button.removeAttribute("aria-disabled");
      else button.setAttribute("aria-disabled", "true");
    };
    var stop = function () { later.clear(); cl.remove("is-playing"); cl.add("is-played"); ready(true); };
    stops.push(stop);
    var play = function () {
      if (button.getAttribute("aria-disabled")) return;
      cl.remove("is-playing", "is-played");
      void fig.offsetWidth;
      cl.add("is-playing");
      ready(false);
      later(function () { cl.add("is-played"); ready(true); }, +fig.getAttribute("data-clip-ms") || 3600, stop);
    };
    var safe = function () { try { play(); } catch (x) { stop(); } };
    once(fig, 0.5, function () { if (!fig.closest(".deck-on")) safe(); });
    if (deck) deck.addEventListener("cr-deck", function () { if (cl.contains("is-on")) safe(); });
    button.addEventListener("click", safe);
  }

  /* shelf.js listens for "cr-halt" and finishes its pieces too. */
  function halt() {
    stops.forEach(function (s) { try { s(); } catch (x) {} });
    try { document.dispatchEvent(new Event("cr-halt")); } catch (x) {}
    html.classList.remove("anim", "motion");
  }

  counter();
  if (!html.classList.contains("anim") || !window.IntersectionObserver || !window.matchMedia) return html.classList.remove("anim");
  try {
    terminal();
    reveals();
    Array.prototype.forEach.call(document.querySelectorAll("[data-clip]"), clip);
    html.classList.add("motion");
  } catch (x) {
    halt();
  }

  /* Motion turned off mid-visit. */
  var still = matchMedia("(prefers-reduced-motion: reduce)");
  var off = function () { if (still.matches) halt(); };
  if (still.addEventListener) still.addEventListener("change", off);
  else if (still.addListener) still.addListener(off);
})();
