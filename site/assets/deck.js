/* Decks (six views, steps, terminal): [data-deck] holds buttons in
   [data-deck-ctl], [data-deck-panel]s (.is-on), a [data-deck-say] line
   and .vt tiles placed from data-deck-tiles. data-deck-mq limits it to a
   media query; data-deck-tabs makes there a WAI-ARIA tablist from each
   panel's <h3> (no roles outside it). With html.motion the chosen
   button's spine fills (--deck-ms) and steps on; hover/focus, off
   screen, hidden tab, reduced motion and cr-halt pause it. */
(function () {
  "use strict";
  var html = document.documentElement, each = function (l, f) { Array.prototype.forEach.call(l, f); };
  var set = function (el, k, v) { if (v == null) el.removeAttribute(k); else el.setAttribute(k, v); };
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)"), done = 0, all = [];
  each(document.querySelectorAll("[data-deck]"), function (box, n) {
    var ps = box.querySelectorAll("[data-deck-panel]"), tabs = box.hasAttribute("data-deck-tabs"), row, at = 0, seen = 0, bs;
    if (tabs) {
      row = document.createElement("li");
      row.className = "step-tabs";
      set(row, "role", "none");
      var list = row.appendChild(document.createElement("div")), sec = box.closest("[aria-labelledby]");
      set(list, "role", "tablist");
      set(list, "aria-orientation", "vertical");
      set(list, "aria-labelledby", sec && sec.getAttribute("aria-labelledby"));
      each(ps, function (p, i) {
        var h = p.querySelector("h3"), b = list.appendChild(document.createElement("button"));
        p.id = "dk" + n + i;
        h.id = p.id + "h";
        b.type = "button";
        b.className = "step-pick";
        set(b, "role", "tab");
        set(b, "aria-controls", p.id);
        each(h.childNodes, function (c) { b.appendChild(c.cloneNode(true)); });
      });
      box.insertBefore(row, box.firstChild);
      list.addEventListener("keydown", function (e) {
        var k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1, Home: -at, End: -1 - at }[e.key];
        if (k === undefined) return;
        e.preventDefault();
        go(at + k, 1);
        bs[at].focus();
      });
    }
    bs = box.querySelectorAll(tabs ? "[role=tablist] button" : "[data-deck-ctl] button");
    var ts = box.querySelectorAll(".vt"), say = box.querySelector("[data-deck-say]");
    var L = (box.getAttribute("data-deck-tiles") || "").split(";").filter(Boolean).map(function (v) { return v.split(","); });
    var mq = box.getAttribute("data-deck-mq"), wide = mq && window.matchMedia ? matchMedia(mq) : null;
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
      each(bs, function (b, i) {
        set(b, tabs ? "aria-selected" : "aria-pressed", i === at ? "true" : "false");
        if (tabs) b.tabIndex = i === at ? 0 : -1;
      });
      each(ps, function (p, i) { p.classList.toggle("is-on", i === at); });
      if (say) say.textContent = bs[at].getAttribute("data-say");
      if (fire) try { box.dispatchEvent(new CustomEvent("cr-deck", { detail: at })); } catch (x) {}
    };
    var on = function () { return !wide || wide.matches; };
    var hold = function () {
      var ok = on();
      box.classList.toggle("deck-on", ok);
      if (tabs) {
        row.hidden = !ok;
        set(box, "role", ok ? "none" : null);
        each(ps, function (p) {
          set(p, "role", ok ? "tabpanel" : null);
          set(p, "aria-labelledby", ok ? p.id + "h" : null);
        });
      } else each(bs, function (b) { b.hidden = false; b.disabled = !ok; });
      box.classList.toggle("play", ok && !done && seen && !document.hidden && !(still && still.matches) && html.classList.contains("motion"));
    };
    box.addEventListener("click", function (e) {
      var i = Array.prototype.indexOf.call(bs, e.target.closest("button"));
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
