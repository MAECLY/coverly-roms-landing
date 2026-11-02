/* Decks (six views, four steps, terminal scenes): [data-deck] holds
   buttons in [data-deck-ctl] (or [data-deck-btn]), optional [data-deck-panel]s (.is-on), a
   [data-deck-say] line and, for the six views, .vt tiles placed from
   data-deck-tiles (gen_views.py). data-deck-mq limits it to a media query.
   Buttons switch at once, also under reduced motion. With html.motion the
   pressed button's spine fills (--deck-ms) and steps on; hover/focus
   (CSS), off screen, hidden tab, reduced motion and cr-halt pause it.
   "cr-deck" fires on each switch (motion.js listens). */
(function () {
  "use strict";
  var html = document.documentElement, each = function (l, f) { Array.prototype.forEach.call(l, f); };
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)"), done = 0, all = [];
  each(document.querySelectorAll("[data-deck]"), function (box) {
    var bs = box.querySelectorAll("[data-deck-ctl] button,[data-deck-btn]"), ps = box.querySelectorAll("[data-deck-panel]");
    var ts = box.querySelectorAll(".vt"), say = box.querySelector("[data-deck-say]");
    var L = (box.getAttribute("data-deck-tiles") || "").split(";").filter(Boolean).map(function (v) { return v.split(","); });
    var mq = box.getAttribute("data-deck-mq"), wide = mq && window.matchMedia ? matchMedia(mq) : null;
    var at = 0, seen = 0;
    if (!bs.length) return;
    var go = function (v, fire) {
      at = (v + bs.length) % bs.length;
      box.setAttribute("data-v", at);
      each(ts, function (t, i) {
        var p = L[at] && L[at][i] && L[at][i].split(" ");
        if (!p) return;
        t.style.transitionDelay = i * 30 + "ms";
        t.style.transform = "translate(" + p[0] + "px," + p[1] + "px) scale(" + p[2] + ")";
      });
      each(bs, function (b, i) { b.setAttribute("aria-pressed", i === at ? "true" : "false"); });
      each(ps, function (p, i) { p.classList.toggle("is-on", i === at); });
      if (say) say.textContent = bs[at].getAttribute("data-say");
      if (fire) try { box.dispatchEvent(new CustomEvent("cr-deck", { detail: at })); } catch (x) {}
    };
    var on = function () { return !wide || wide.matches; };
    var hold = function () {
      var ok = on();
      box.classList.toggle("deck-on", ok);
      each(bs, function (b) { b.hidden = false; b.disabled = !ok; });
      box.classList.toggle("play", ok && !done && seen && !document.hidden && !(still && still.matches) && html.classList.contains("motion"));
    };
    box.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      var i = Array.prototype.indexOf.call(bs, b);
      if (i >= 0 && on()) go(i, 1);
    });
    go(0);
    hold();
    all.push(hold);
    if (wide && wide.addEventListener) wide.addEventListener("change", hold);
    if (!html.classList.contains("motion") || !window.IntersectionObserver) return;
    box.addEventListener("animationend", function (e) {
      if (e.target === bs[at] && box.classList.contains("play")) go(at + 1, 1);
    });
    new IntersectionObserver(function (es) {
      seen = es[es.length - 1].isIntersecting;
      hold();
    }, { threshold: +box.getAttribute("data-deck-seen") || 0.4 }).observe(box);
  });
  var redo = function () { all.forEach(function (h) { h(); }); };
  document.addEventListener("visibilitychange", redo);
  document.addEventListener("cr-halt", function () { done = 1; redo(); });
  if (still && still.addEventListener) still.addEventListener("change", redo);
})();
