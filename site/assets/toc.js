/* /features: the index beside the groups marks the one being read
   (aria-current="location"; CSS fills its Buckram spine). Without JS or
   IntersectionObserver it is a plain list of links. */
(function () {
  "use strict";
  var links = document.querySelectorAll(".toc a"), map = {};
  if (!links.length || !window.IntersectionObserver) return;
  Array.prototype.forEach.call(links, function (a) { map[a.getAttribute("href").slice(1)] = a; });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting || !map[e.target.id]) return;
      Array.prototype.forEach.call(links, function (a) { a.removeAttribute("aria-current"); });
      map[e.target.id].setAttribute("aria-current", "location");
    });
  }, { rootMargin: "-30% 0px -60% 0px" });
  Object.keys(map).forEach(function (id) {
    var s = document.getElementById(id);
    if (s) io.observe(s);
  });
})();
