/* The six library views (#ordenar, #tidy). The HTML is the Covers frame;
   this shows the buttons, which switch views at once (also under reduced
   motion) and move the same eight tiles into each layout (CSS eases
   them). With html.motion the pressed button's spine fills for 3 s and
   its animationend steps on; hover or focus pauses it (CSS), and so do
   off screen, a hidden tab, reduced motion and cr-halt. */
(function () {
  "use strict";
  var box = document.querySelector(".vw"), ctl = box && box.querySelector(".vw-ctl");
  if (!ctl) return;
  var html = document.documentElement, bs = ctl.querySelectorAll("button"), ts = box.querySelectorAll(".vt");
  var say = box.querySelector(".vw-say"), at = 0, seen = 0, done = 0;
  /* x y scale of each tile, per view: Covers, Details, Columns, Gallery,
     Art slots, Shelves. The first matches the markup's transforms. */
  var L = "160 50 1.9,258 50 1.9,356 50 1.9,454 50 1.9,160 186 1.9,258 186 1.9,356 186 1.9,454 186 1.9;156 66 .7,156 100 .7,156 134 .7,156 168 .7,156 202 .7,156 236 .7,156 270 .7,156 304 .7;312 50 .5,312 76 .5,452 56 2.8,312 128 .5,312 154 .5,312 180 .5,312 206 .5,312 232 .5;210 282 .9,246 282 .9,279 48 5,318 282 .9,354 282 .9,390 282 .9,426 282 .9,462 282 .9;156 48 .75,156 85 .75,156 122 .75,156 159 .75,156 196 .75,156 233 .75,156 270 .75,156 307 .75;160 66 1.9,236 66 1.9,312 66 1.9,388 66 1.9,160 196 1.9,236 196 1.9,312 196 1.9,388 196 1.9"
    .split(";").map(function (v) { return v.split(","); });
  var go = function (v) {
    at = v % bs.length;
    box.setAttribute("data-v", at);
    Array.prototype.forEach.call(ts, function (t, i) {
      var p = L[at][i].split(" ");
      t.style.transitionDelay = i * 30 + "ms";
      t.style.transform = "translate(" + p[0] + "px," + p[1] + "px) scale(" + p[2] + ")";
    });
    Array.prototype.forEach.call(bs, function (b, i) {
      b.hidden = false;
      b.setAttribute("aria-pressed", i === at ? "true" : "false");
    });
    say.textContent = bs[at].getAttribute("data-say");
  };
  ctl.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (b) go(Array.prototype.indexOf.call(bs, b));
  });
  go(0);
  if (!html.classList.contains("motion") || !window.IntersectionObserver) return;
  var still = matchMedia("(prefers-reduced-motion: reduce)");
  var hold = function () {
    box.classList.toggle("play", !done && seen && !document.hidden && !still.matches && html.classList.contains("motion"));
  };
  ctl.addEventListener("animationend", function (e) {
    if (e.target === bs[at] && box.classList.contains("play")) go(at + 1);
  });
  new IntersectionObserver(function (es) {
    seen = es[es.length - 1].isIntersecting;
    hold();
  }, { threshold: 0.4 }).observe(box);
  document.addEventListener("visibilitychange", hold);
  document.addEventListener("cr-halt", function () { done = 1; hold(); });
  if (still.addEventListener) still.addEventListener("change", hold);
})();
