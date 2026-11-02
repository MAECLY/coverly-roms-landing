/* #formatos, every system (scripts/site/systems.py writes the list):
   the icon sprite is swapped into the <i data-i> placeholders when the
   section comes near; two shelves made from the list loop under
   html.motion (hover, off screen, hidden tab, the pause button, reduced
   motion and cr-halt stop them); the list gets its search and filters. */
(function () {
  "use strict";
  var box = document.querySelector(".sys");
  if (!box || !window.IntersectionObserver) return;
  var html = document.documentElement, each = function (l, f) { Array.prototype.forEach.call(l, f); };
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)"), NS = "http://www.w3.org/2000/svg";
  var lis = box.querySelectorAll(".sys-all li"), shelf = box.querySelector(".sys-shelf"), rows = [[], []], lit = 0;
  var norm = function (s) { return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase(); };
  each(lis, function (li) {
    var h = li.parentNode.parentNode.querySelector("h5"), mk = h ? h.firstChild.nodeValue.trim() : "", name = li.textContent;
    var f = li.closest(".sys-g").getAttribute("data-f"), p = document.createElement("span");
    li.k = norm(name + " " + (li.getAttribute("data-k") || "") + " " + mk);
    p.className = "sys-p";
    p.appendChild(li.firstChild.cloneNode(true));
    p.appendChild(document.createTextNode(li.getAttribute("data-s") || name));
    rows[f === "console" || f === "handheld" ? 0 : 1].push(p);
  });
  var moving = html.classList.contains("motion") && !(still && still.matches), sets = [];
  rows.forEach(function (ps) {
    var row = shelf.appendChild(document.createElement("div")), t = row.appendChild(document.createElement("div"));
    var set = t.appendChild(document.createElement("div"));
    row.className = "sys-row";
    t.className = "sys-track";
    set.className = "sys-set";
    ps.forEach(function (p) { set.appendChild(p); });
    if (moving) {
      var c = t.appendChild(set.cloneNode(true));
      c.setAttribute("inert", "");
      sets.push(c);
    }
  });
  var light = function () {
    if (lit++) return;
    each(box.querySelectorAll("i[data-i]"), function (i) {
      var s = i.appendChild(document.createElementNS(NS, "svg")), u = s.appendChild(document.createElementNS(NS, "use"));
      s.setAttribute("aria-hidden", "true");
      s.setAttribute("focusable", "false");
      u.setAttribute("href", box.getAttribute("data-sprite") + "#" + i.getAttribute("data-i"));
      i.className = "on";
    });
  };
  new IntersectionObserver(function (es) { if (es[0].isIntersecting) light(); }, { rootMargin: "800px 0px" }).observe(box);
  var det = box.querySelector("details");
  det.addEventListener("toggle", light);
  var pause = box.querySelector(".sys-pause"), cl = box.classList, say = [pause.textContent, pause.getAttribute("data-alt")];
  var hold = function (on) {
    cl.toggle("is-paused", on);
    pause.textContent = say[on ? 1 : 0];
    try { sessionStorage.setItem("sys-paused", on ? "1" : ""); } catch (x) {}
  };
  var stop = function () {
    cl.add("is-still");
    pause.hidden = true;
    sets.forEach(function (c) { c.remove(); });
  };
  if (moving) {
    pause.hidden = false;
    try { if (sessionStorage.getItem("sys-paused")) hold(true); } catch (x) {}
    pause.addEventListener("click", function () { hold(!cl.contains("is-paused")); });
    new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) shelf.removeAttribute("data-off");
      else shelf.setAttribute("data-off", "");
    }).observe(shelf);
    document.addEventListener("visibilitychange", function () { cl.toggle("is-hidden", document.hidden); });
    document.addEventListener("cr-halt", stop);
    if (still && still.addEventListener) still.addEventListener("change", function () { if (still.matches) stop(); });
  }
  var q = box.querySelector("#sys-q"), out = box.querySelector(".sys-n"), none = box.querySelector(".sys-none"), fam = "";
  var fb = box.querySelectorAll(".sys-fams button");
  var run = function () {
    var v = norm(q.value.trim()), n = 0;
    each(lis, function (li) {
      var ok = (!fam || li.closest(".sys-g").getAttribute("data-f") === fam) && li.k.indexOf(v) >= 0;
      li.hidden = !ok;
      n += ok;
    });
    each(box.querySelectorAll(".sys-m,.sys-g"), function (g) { g.hidden = !g.querySelector("li:not([hidden])"); });
    none.hidden = n > 0;
    out.textContent = n + " " + out.getAttribute(n === 1 ? "data-one" : "data-many");
  };
  box.querySelector(".sys-tools").hidden = false;
  q.addEventListener("input", run);
  q.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && q.value) {
      q.value = "";
      run();
    }
  });
  box.querySelector(".sys-fams").addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    fam = b.getAttribute("data-f");
    each(fb, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    run();
  });
})();
