/* /features: the index beside the groups marks the one being read
   (aria-current="location"; CSS fills its Buckram spine). From 1200px,
   each group's figure stays beside its list and follows the reading: the
   first item of each beat ([data-beat]) puts its number on the group
   when it crosses the reading band, CSS draws that state (cuts under
   reduced motion) and the six-views window switches view. No scroll
   listener, no scroll hijack. Without JS: plain links, finished scenes. */
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
  var wide = window.matchMedia && matchMedia("(min-width: 1200px)"), beats = document.querySelectorAll(".flist [data-beat]");
  if (!wide || !beats.length) return;
  var set = function (g, n) {
    if (g.getAttribute("data-beat") === n) return;
    g.setAttribute("data-beat", n);
    var b = g.querySelectorAll("[data-deck-ctl] button")[n - 1];
    if (b) b.click();
  };
  var arm = function () {
    each(beats, function (d) {
      var g = d.closest(".fgroup");
      if (!wide.matches) g.removeAttribute("data-beat");
      else if (!g.hasAttribute("data-beat")) set(g, "1");
    });
  };
  var band = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting && wide.matches) set(e.target.closest(".fgroup"), e.target.getAttribute("data-beat"));
    });
  }, { rootMargin: "-35% 0px -45% 0px" });
  each(beats, function (d) { band.observe(d); });
  arm();
  if (wide.addEventListener) wide.addEventListener("change", arm);
})();
