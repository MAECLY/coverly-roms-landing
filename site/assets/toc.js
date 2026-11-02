/* /features: the index beside the groups marks the one being read
   (aria-current). From 1200px,
   each group's figure stays beside its list and its beats ([data-beat])
   share the pinned stretch evenly: the one read goes on the group,
   CSS draws it (cuts under reduced motion) and the six-views window
   switches view. Passive listener, no hijack. Without JS: plain
   links, finished scenes. */
(function () {
  "use strict";
  var each = function (l, f) { Array.prototype.forEach.call(l, f); };
  var links = document.querySelectorAll(".toc a"), map = {};
  if (!window.IntersectionObserver) return;
  each(links, function (a) { map[a.getAttribute("href").slice(1)] = a; });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || !map[e.target.id]) return;
      each(links, function (a) { a.removeAttribute("aria-current"); });
      map[e.target.id].setAttribute("aria-current", "location");
    });
  }, { rootMargin: "-30% 0px -60% 0px" });
  Object.keys(map).forEach(function (id) {
    var s = document.getElementById(id);
    if (s) io.observe(s);
  });
  var wide = window.matchMedia && matchMedia("(min-width: 1200px)"), gs = [], on = [], q = 0;
  each(document.querySelectorAll(".flist [data-beat='1']"), function (d) { gs.push(d.closest(".fgroup")); });
  if (!wide || !gs.length) return;
  var set = function (g, n) {
    if (g.getAttribute("data-beat") === n) return;
    g.setAttribute("data-beat", n);
    var b = g.querySelectorAll("[data-deck-ctl] button")[n - 1];
    if (b) b.click();
  };
  /* Beat = share of the pinned stretch (list - figure height, or to the
     page end) passed; the list is at least the figure + 120px a beat. */
  var go = function () {
    q = 0;
    if (wide.matches) on.forEach(function (g) {
      var l = g.querySelector(".flist"), f = l.previousElementSibling, n = l.querySelectorAll("[data-beat]").length,
        d = parseFloat(getComputedStyle(f).top) - l.getBoundingClientRect().top,
        p = d / Math.min(l.offsetHeight - f.offsetHeight, d + document.body.scrollHeight - innerHeight - scrollY);
      set(g, "" + Math.max(1, Math.min(n, Math.floor(p * n) + 1)) || n);
    });
  };
  var arm = function () {
    gs.forEach(function (g) {
      var l = g.querySelector(".flist");
      l.style.minHeight = wide.matches ? l.previousElementSibling.offsetHeight + 120 * l.querySelectorAll("[data-beat]").length + "px" : "";
      if (!wide.matches) g.removeAttribute("data-beat");
    });
    go();
  };
  var seen = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var k = on.indexOf(e.target);
      if (e.isIntersecting) k < 0 && on.push(e.target);
      else if (k > -1) on.splice(k, 1);
    });
    go();
  }, { rootMargin: "99px" });
  gs.forEach(function (g) { seen.observe(g); });
  addEventListener("scroll", function () { q = q || requestAnimationFrame(go); }, { passive: true });
  addEventListener("resize", arm);
  arm();
})();
