/*! ink-fish v1.0.0 — brush-ink fish swimming behind your page. MIT © 2026 BreakDimbo
    https://github.com/BreakDimbo/ink-fish

   One Canvas 2D (DPR <= 1.5) and one rAF loop per instance, paused when the tab is hidden, the host is
   off screen, or no open water is visible. Three depth layers (far minnows, mid carp, near koi), each
   with scroll parallax. Every fish has a spine of segments that follows its head's path. A body wave
   runs from head to tail, its tail beat tied to speed and thrust, and it swims in burst-and-glide
   rhythm. Fish school with their own layer (separation / alignment / cohesion), keep clear of
   obstacles and the headline, ease away from a fast cursor and drift curiously towards a still one.
   Soft shadows are drawn on a quarter-res layer and scaled up, so they cost no blur filter. Obstacles
   are erased from the canvas; ink under text is thinned. Layout is read only on resize/reflow, never
   inside the frame.

   Usage:   var fish = InkFish.mount(document.body, { obstacles: ".card" });  …  fish.destroy();
   or:      <body data-ink-fish>   (options as JSON in the attribute value)                          */
(function (root, factory) {
  "use strict";
  var api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.InkFish = api;
})(typeof window !== "undefined" ? window : this, function (Wn) {
  "use strict";
  var M = Math, PI = M.PI, TAU = PI * 2;

  var DEFAULTS = {
    count: "auto",            // "auto" (from the open area), a total number, or { minnow, carp, koi }
    density: 1,               // multiplies the open area used by "auto"
    theme: "auto",            // "auto" | "light" | "dark"; auto = <html data-theme>, else prefers-color-scheme
    ink: { light: "#1e1c19", dark: "#e8e2d8" }, // your page's text colour (one hex, or per theme); CSS var --ink-fish-ink on the host wins
    opacity: 1,               // multiplies the ink alpha
    shadow: 1,                // multiplies the lamp-shadow alpha; 0 turns shadows off
    reducedMotion: "auto",    // "auto" (respect prefers-reduced-motion) | true (always calm) | false (ignore)
    interactive: true,        // fish react to the cursor, taps and fast scrolling
    obstacles: "",            // selector: fish swim around these, and the canvas is erased under them
    bands: "",                // selector: full-width horizontal walls (e.g. a toolbar); avoided, not erased
    text: "",                 // selector, or [{ selector, keep, feather }]: ink thins under this text
    title: "",                // selector: the big koi give this element room
    hero: "",                 // selector: koi stay above its bottom (+160px, +40px on mobile)
    habitat: "",              // selector (page mode): the habitat ends at this element's bottom; default <body>
    ignore: "a,button,input,select,textarea,label,[data-ink-fish-ignore]", // taps here don't startle fish
    mobileQuery: "(max-width: 720px)",
    maxDpr: 1.5,
    fadeIn: true
  };

  var hex = function (v) {
    var m = (v || "").trim().match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
    if (!m) return null;
    var h = m[1].length === 3 ? m[1].replace(/./g, "$&$&") : m[1], n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  };
  var assign = function (a) {
    for (var i = 1; i < arguments.length; i++) { var b = arguments[i]; if (b) for (var k in b) if (Object.prototype.hasOwnProperty.call(b, k)) a[k] = b[k]; }
    return a;
  };
  var instances = [];

  function mount(host, options) {
    var D = Wn.document;
    if (typeof host === "string") host = D.querySelector(host);
    if (!host || host === D.documentElement) host = D.body;
    if (!Wn.CanvasRenderingContext2D || !Wn.requestAnimationFrame || !host) return null;
    if (host.__inkFish) host.__inkFish.destroy();
    var O = assign({}, DEFAULTS, options);
    var page = host === D.body; // page mode: fixed viewport canvas with scroll parallax; else local to the host
    var q = function (sel) { if (!sel) return null; return typeof sel === "string" ? D.querySelector(sel) : sel; };
    var qa = function (sel) { if (!sel) return []; return typeof sel === "string" ? Array.prototype.slice.call(D.querySelectorAll(sel)) : [].concat(sel); };

    var MQ = function (s) { return Wn.matchMedia ? Wn.matchMedia(s) : { matches: false, addEventListener: function () {}, removeEventListener: function () {} }; };
    var RMQ = MQ("(prefers-reduced-motion: reduce)"), MOB = MQ(O.mobileQuery), DARKQ = MQ("(prefers-color-scheme: dark)");
    var RM = { get matches() { return O.reducedMotion === "auto" ? RMQ.matches : !!O.reducedMotion; } };
    var cv = D.createElement("canvas");
    cv.className = "ink-fish" + (page ? "" : " ink-fish--local");
    cv.setAttribute("aria-hidden", "true");
    cv.style.pointerEvents = "none";
    var hostPos = null;
    if (!page && getComputedStyle(host).position === "static") { hostPos = host.style.position; host.style.position = "relative"; }
    host.classList.add("ink-fish-host");
    host.insertBefore(cv, host.firstChild);
    var g = cv.getContext("2d");
    var shc = D.createElement("canvas"), sg = shc.getContext("2d");
    var SH = 0.25; // shadow layer scale

    var vw = 0, vh = 0, dpr = 1, PW = 0, PH = 0, sy = page ? (Wn.scrollY || 0) : 0, heroB = 0, mobile = MOB.matches;
    var obs = [], walls = [], texts = [], title = null, fish = [], T = 0, dead = false, onScreen = true;
    var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
    var rnd = function (a, b) { return a + M.random() * (b - a); };
    var wrapA = function (a) { while (a > PI) a -= TAU; while (a < -PI) a += TAU; return a; };
    var sstep = function (a, b, x) { x = clamp((x - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
    // origin of the canvas in client coordinates (page mode: the viewport, so 0,0)
    var origin = function () { if (page) return [0, 0]; var r = host.getBoundingClientRect(); return [r.left + host.clientLeft, r.top + host.clientTop]; };

    // ── palette: ink on paper in light mode, pale ink on dark paper ────────────
    var pal = null, palFrom = null, palTo = null, palAt = -1;
    var isDark = function () {
      if (O.theme === "dark") return true;
      if (O.theme === "light") return false;
      var t = D.documentElement.getAttribute("data-theme");
      if (t === "dark") return true;
      if (t === "light") return false;
      return DARKQ.matches;
    };
    var readPal = function () {
      var dark = isDark(), src = O.ink;
      var css = hex(getComputedStyle(host).getPropertyValue("--ink-fish-ink"));
      var ink = css || hex(typeof src === "string" ? src : (src && (dark ? src.dark : src.light))) || (dark ? [232, 226, 216] : [30, 28, 25]);
      var op = +O.opacity, sh = +O.shadow;
      if (!(op >= 0)) op = 1;
      if (!(sh >= 0)) sh = 1;
      // ink: a warm sumi in light mode; in dark mode the page's pale ink, a touch warmer.
      return dark
        ? { ink: [ink[0] * 0.94 + 10, ink[1] * 0.92 + 6, ink[2] * 0.86], a: 1.12 * op, sh: [0, 0, 0], sa: 0.26 * sh }
        : { ink: [ink[0] + 8, ink[1] + 4, ink[2]], a: 1 * op, sh: [52, 38, 22], sa: 0.13 * sh };
    };
    var mixPal = function (a, b, k) {
      var l = function (x, y) { return x + (y - x) * k; };
      return { ink: [l(a.ink[0], b.ink[0]), l(a.ink[1], b.ink[1]), l(a.ink[2], b.ink[2])], a: l(a.a, b.a), sh: [l(a.sh[0], b.sh[0]), l(a.sh[1], b.sh[1]), l(a.sh[2], b.sh[2])], sa: l(a.sa, b.sa) };
    };
    var syncPal = function () {
      if (dead) return;
      var p = readPal();
      if (pal && JSON.stringify(p) === JSON.stringify(palTo)) return;
      if (!pal) { pal = palTo = p; return; }
      palFrom = pal; palTo = p; palAt = performance.now();
      wake();
    };
    var inkRGB = "";
    var tickPal = function (now) {
      if (palAt >= 0) {
        var k = clamp((now - palAt) / 500, 0, 1);
        pal = mixPal(palFrom, palTo, k * k * (3 - 2 * k));
        if (k >= 1) palAt = -1;
      }
      inkRGB = M.round(pal.ink[0]) + "," + M.round(pal.ink[1]) + "," + M.round(pal.ink[2]);
    };

    // ── layout (read only on resize / reflow) ──────────────────────────────────
    var ox = 0, oy0 = 0;
    var rectOf = function (el, grow) {
      if (!el) return null;
      var r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return null;
      grow = grow || 0;
      return { l: r.left - ox - grow, t: r.top - oy0 + sy - grow, r: r.right - ox + grow, b: r.bottom - oy0 + sy + grow };
    };
    var textSpecs = function () {
      var t = O.text;
      if (!t) return [];
      if (typeof t === "string") return [{ selector: t }];
      return [].concat(t);
    };
    var measure = function () {
      var o = origin(); ox = o[0]; oy0 = o[1];
      sy = page ? (Wn.scrollY || 0) : 0;
      vw = page ? D.documentElement.clientWidth : host.clientWidth;
      vh = page ? Wn.innerHeight : host.clientHeight;
      dpr = M.min(Wn.devicePixelRatio || 1, +O.maxDpr || 1.5);
      mobile = MOB.matches;
      var hr = rectOf(q(O.hero));
      heroB = hr ? hr.b : vh;
      if (page) {
        var hab = q(O.habitat) || D.body;
        PH = M.max(M.ceil(hab.getBoundingClientRect().bottom + sy), heroB);
      } else PH = M.max(vh, heroB);
      PW = vw;
      obs = [];
      qa(O.obstacles).forEach(function (el) { var r = rectOf(el); if (r) obs.push(r); });
      walls = obs.slice();
      qa(O.bands).forEach(function (el) { var b = rectOf(el); if (b) walls.push({ l: 0, t: b.t, r: vw, b: b.b }); }); // full-width walls
      texts = [];
      textSpecs().forEach(function (s) {
        if (typeof s === "string" || (s && s.nodeType)) s = { selector: s };
        var keep = s.keep != null ? +s.keep : 0.24, f = s.feather != null ? +s.feather : 30;
        qa(s.selector).forEach(function (el) { var r = rectOf(el); if (r) texts.push({ r: r, keep: keep, f: f }); });
      });
      title = rectOf(q(O.title), mobile ? 10 : 22);
      cv.width = M.round(vw * dpr); cv.height = M.round(vh * dpr);
      cv.style.width = vw + "px"; cv.style.height = vh + "px";
      shc.width = M.ceil(vw * SH); shc.height = M.ceil(vh * SH);
    };

    // ── species and population ────────────────────────────────────────────────
    // d: depth (0 far … 1 near). pz: scroll parallax (screen y = y − scrollY·pz).
    var KIND = [
      { name: "minnow", d: [0.2, 0.38], L: [15, 23], wr: 0.072, tl: 0.2, vmax: [34, 46], cruise: 0.42, school: 1, avoid: 0, fins: 0, tone: [0.1, 0.13] },
      { name: "carp", d: [0.5, 0.66], L: [32, 44], wr: 0.095, tl: 0.23, vmax: [38, 52], cruise: 0.2, school: 0.55, avoid: 1, fins: 1, tone: [0.17, 0.21] },
      { name: "koi", d: [0.86, 1], L: [62, 88], wr: 0.122, tl: 0.38, vmax: [30, 40], cruise: 0.08, school: 0.12, avoid: 1, fins: 2, tone: [0.27, 0.32] }
    ];
    var free = function (x, y, pad) {
      for (var i = 0; i < walls.length; i++) { var o = walls[i]; if (x > o.l - pad && x < o.r + pad && y > o.t - pad && y < o.b + pad) return false; }
      return true;
    };
    var heroEl = function () { return !!q(O.hero); };
    var koiB = PH;
    var habitatB = function (k) { return k === 2 ? koiB : PH; };
    var spawn = function (k, near) {
      var K = KIND[k], f = { k: k, K: K }, s = mobile ? 0.78 : 1, tries = 0;
      f.d = rnd(K.d[0], K.d[1]); f.pz = 0.55 + 0.45 * f.d;
      f.L = rnd(K.L[0], K.L[1]) * s; f.vmax = rnd(K.vmax[0], K.vmax[1]) * (mobile ? 0.85 : 1);
      f.tone = rnd(K.tone[0], K.tone[1]);
      var hb = habitatB(k);
      do {
        f.x = near ? near.x + rnd(-60, 60) : rnd(20, vw - 20);
        f.y = near ? near.y + rnd(-40, 40) : rnd(20, hb - 20);
        tries++;
      } while (tries < 40 && (K.avoid && !free(f.x, f.y + sy * (1 - f.pz), f.L)));
      f.a = near ? near.a + rnd(-0.4, 0.4) : rnd(-PI, PI);
      f.v = f.vmax * 0.3; f.w = 0; f.th = K.cruise; f.thT = K.cruise; f.mode = 0; f.tm = rnd(0, 2);
      f.ph = rnd(0, TAU); f.amp = f.L * 0.05; f.vm = 1; f.cur = M.random(); f.fade = 0;
      f.w1 = rnd(0.07, 0.16); f.w2 = rnd(0.21, 0.37); f.p1 = rnd(0, TAU); f.p2 = rnd(0, TAU);
      f.n = 11; f.seg = f.L / (f.n - 1); f.px = new Float32Array(f.n); f.py = new Float32Array(f.n);
      for (var i = 0; i < f.n; i++) { f.px[i] = f.x - M.cos(f.a) * f.seg * i; f.py[i] = f.y - M.sin(f.a) * f.seg * i; }
      return f;
    };
    var counts = function () {
      var C = O.count;
      if (C && typeof C === "object") return [M.max(0, C.minnow | 0), M.max(0, C.carp | 0), M.max(0, C.koi | 0)];
      if (typeof C === "number" || (typeof C === "string" && C !== "auto" && !isNaN(+C))) {
        var n = M.max(0, M.round(+C)), kq = n >= 6 ? M.max(1, M.round(n * 0.08)) : 0, cq = M.round(n * 0.3);
        return [M.max(0, n - kq - cq), cq, kq];
      }
      // "auto": open water on the canvas (24 px grid), excluding the obstacles
      var area = 0, heroArea = vw * heroB, dn = +O.density > 0 ? +O.density : 1;
      for (var y = 12; y < PH; y += 24) for (var x = 12; x < vw; x += 24) if (free(x, y, 16)) area += 576;
      area *= dn;
      return [
        M.round(clamp(area / (mobile ? 10000 : 38000), mobile ? 10 : 16, mobile ? 20 : 36)),
        M.round(clamp(area / (mobile ? 26000 : 70000), mobile ? 4 : 8, mobile ? 8 : 18)),
        mobile ? 2 : M.round(clamp(heroArea * dn / 160000, 3, 5))
      ];
    };
    var populate = function () {
      koiB = heroEl() ? heroB + (mobile ? 40 : 160) : PH;
      var c = counts(), minnows = c[0], carp = c[1], koi = c[2];
      fish = [];
      // minnows arrive in small schools
      while (fish.length < minnows) { var lead = spawn(0), n = 3 + (M.random() * 5) | 0; fish.push(lead); for (var j = 1; j < n && fish.length < minnows; j++) fish.push(spawn(0, lead)); }
      for (var k = 0; k < carp; k++) fish.push(k % 3 && fish.length ? spawn(1, fish[fish.length - 1].k === 1 ? fish[fish.length - 1] : null) : spawn(1));
      for (var qk = 0; qk < koi; qk++) fish.push(spawn(2));
      fish.sort(function (a, b) { return a.d - b.d; }); // paint far → near
    };

    // ── input ─────────────────────────────────────────────────────────────────
    var ptr = { x: 0, y: 0, on: false, sp: 0, t: 0, idle: 9 }, svel = 0, lastSy = sy;
    var L_ = []; // listeners to remove on destroy
    var on = function (t, ev, fn, o) { t.addEventListener(ev, fn, o); L_.push([t, ev, fn, o]); };
    var kick = function (f, k) { f.mode = 1; f.tm = rnd(0.35, 0.6); f.thT = M.max(f.thT, k); };
    var inside = function (x, y) { return page || (x >= 0 && y >= 0 && x <= vw && y <= vh); };
    on(Wn, "pointermove", function (e) {
      if (!O.interactive) return;
      if (e.pointerType === "touch") { ptr.on = false; return; }
      var o = origin(), cx = e.clientX - o[0], cy = e.clientY - o[1];
      var now = performance.now(), dt = M.max(8, now - ptr.t);
      var sp = M.hypot(cx - ptr.x, cy - ptr.y) / dt * 1000;
      ptr.sp = ptr.sp * 0.7 + sp * 0.3; ptr.x = cx; ptr.y = cy; ptr.t = now; ptr.idle = 0;
      ptr.on = inside(cx, cy) && free(cx, cy + sy, 6);
      wake();
    }, { passive: true });
    var off = function () { ptr.on = false; };
    on(D.documentElement, "pointerleave", off);
    on(Wn, "blur", off);
    var ignoreSel = function () { return [O.ignore, typeof O.obstacles === "string" ? O.obstacles : "", typeof O.bands === "string" ? O.bands : ""].filter(Boolean).join(","); };
    on(Wn, "pointerdown", function (e) {
      // a tap or click in open water startles the fish nearby (no ripple, no splash)
      if (!O.interactive) return;
      var t = e.target, sel = ignoreSel();
      if (RM.matches || (sel && t && t.closest && t.closest(sel))) return;
      var o = origin(), x = e.clientX - o[0], y = e.clientY - o[1];
      if (!inside(x, y) || !free(x, y + sy, 4)) return;
      for (var i = 0; i < fish.length; i++) {
        var f = fish[i], dx = f.x - x, dy = f.y - sy * f.pz - y, d = M.hypot(dx, dy);
        if (d < 240 * (0.6 + f.d)) { f.a = wrapA(f.a + clamp(wrapA(M.atan2(dy, dx) - f.a), -1.4, 1.4) * 0.5); kick(f, 1); }
      }
    }, { passive: true });
    if (page) on(Wn, "scroll", function () { sy = Wn.scrollY || 0; wake(); }, { passive: true });

    // ── simulation ────────────────────────────────────────────────────────────
    var step = function (dt) {
      T += dt;
      var rm = RM.matches;
      ptr.idle += dt;
      for (var i = 0; i < fish.length; i++) {
        var f = fish[i], K = f.K, L = f.L, oy = sy * (1 - f.pz); // page y = layer y + oy
        var ca = M.cos(f.a), sa = M.sin(f.a);
        var fx = ca * 1.6, fy = sa * 1.6;
        // wander: two slow incommensurate sines, so courses curve without repeating
        var wa = f.a + (M.sin(T * f.w1 + f.p1) * 0.65 + M.sin(T * f.w2 + f.p2) * 0.35) * 1.1;
        fx += M.cos(wa) * 0.8; fy += M.sin(wa) * 0.8;
        // school with fish of the same kind
        if (K.school > 0) {
          var R = M.min(L * 5.5, f.k === 2 ? 170 : 200), R2 = R * R, sep = L * 1.25, n = 0, ax = 0, ay = 0, cx = 0, cy = 0, sx = 0, sy2 = 0;
          for (var j = 0; j < fish.length; j++) {
            var o = fish[j];
            if (o === f || o.k !== f.k) continue;
            var dx = o.x - f.x, dy = o.y - f.y, d2 = dx * dx + dy * dy;
            if (d2 > R2) continue;
            var d = M.sqrt(d2) || 1;
            n++; ax += M.cos(o.a); ay += M.sin(o.a); cx += dx; cy += dy;
            if (d < sep) { var k = (1 - d / sep); sx -= dx / d * k; sy2 -= dy / d * k; }
          }
          if (n) {
            fx += (ax / n) * 1.1 * K.school + (cx / n) / R * 1.4 * K.school + sx * 2.6;
            fy += (ay / n) * 1.1 * K.school + (cy / n) / R * 1.4 * K.school + sy2 * 2.6;
          }
        }
        // pond edges: fish may slip a little past the sides, never far
        var mx = L * 0.6 + 30, hb = habitatB(f.k) - oy, top = 24;
        if (f.x < -L * 0.4 + mx) fx += (1 - (f.x + L * 0.4) / mx) * 3;
        if (f.x > vw + L * 0.4 - mx) fx -= (1 - (vw + L * 0.4 - f.x) / mx) * 3;
        if (f.y < top + mx) fy += (1 - (f.y - top) / mx) * 3;
        if (f.y > hb - mx) fy -= (1 - (hb - f.y) / mx) * 3;
        // keep clear of obstacles and bands (probe the head and a point ahead)
        if (K.avoid) {
          var Mg = 22 + L * 0.55;
          for (var p = 0; p < 2; p++) {
            var qx = f.x + ca * L * 1.3 * p, qy = f.y + oy + sa * L * 1.3 * p;
            for (var w = 0; w < walls.length; w++) {
              var r = walls[w];
              if (qx < r.l - Mg || qx > r.r + Mg || qy < r.t - Mg || qy > r.b + Mg) continue;
              var dl = qx - (r.l - Mg), dr = r.r + Mg - qx, dt2 = qy - (r.t - Mg), db = r.b + Mg - qy, mn = M.min(dl, dr, dt2, db), s = 3.2 * (1 - mn / (Mg + 40)) + 0.6;
              if (mn === dl) fx -= s; else if (mn === dr) fx += s; else if (mn === dt2) fy -= s; else fy += s;
            }
          }
          // the large fish give the headline room
          if (f.k === 2 && title) {
            var tx = clamp(f.x, title.l, title.r), ty = clamp(f.y + oy, title.t, title.b), ex = f.x - tx, ey = f.y + oy - ty, de = M.hypot(ex, ey);
            if (de < 50) { fx += (de ? ex / de : 0) * 1.4 * (1 - de / 50); fy += (de ? ey / de : -1) * 1.4 * (1 - de / 50); }
          }
        }
        // cursor: a quick movement scatters them; a still cursor in open water draws the curious ones in
        if (ptr.on && !rm) {
          var px = ptr.x, py = ptr.y + sy * f.pz, ex2 = f.x - px, ey2 = f.y - py, dp = M.hypot(ex2, ey2) || 1;
          var reach = (130 + L) * (0.5 + f.d * 0.7);
          if (ptr.sp > 900 && ptr.idle < 0.15 && dp < reach) {
            fx += ex2 / dp * 4.5; fy += ey2 / dp * 4.5; if (f.mode === 0 || f.thT < 0.8) kick(f, 0.9 + 0.1 * f.d);
          } else if (f.k > 0 && f.cur > 0.45 && ptr.idle > 0.5 && dp < 320) {
            var ring = 46 + L * 0.9, kk = clamp((dp - ring) / ring, -1, 1);
            fx -= ex2 / dp * kk * 1.5; fy -= ey2 / dp * kk * 1.5;
            if (dp < ring * 1.6) { f.vm = M.min(f.vm, 0.45); if (f.mode === 1 && f.thT > 0.5) f.thT = 0.3; } // hover and look, don't circle
          } else if (dp < reach * 0.7) {
            var kq = 1 - dp / (reach * 0.7); fx += ex2 / dp * kq * 1.6; fy += ey2 / dp * kq * 1.6;
          }
        }
        // a fast scroll is felt as a current: a few fish dart, the rest lean with it
        if (!rm && O.interactive && M.abs(svel) > 1400 && M.random() < dt * 0.9 * (1 - f.d * 0.5)) kick(f, 0.8);
        fy += clamp(svel / 2400, -1, 1) * 0.5 * (1.2 - f.d);

        // ── turning: limited curvature, eased angular velocity ──
        var da = wrapA(M.atan2(fy, fx) - f.a);
        var wmax = (0.45 + 2.1 * f.v / f.vmax) * (f.k === 2 ? 0.7 : 1);
        var wt = clamp(da * 2.2, -wmax, wmax);
        f.w += (wt - f.w) * M.min(1, dt * 3);
        f.a = wrapA(f.a + f.w * dt);

        // ── rhythm: burst, then a long glide ──
        f.tm -= dt;
        if (f.tm <= 0) {
          if (f.mode === 1 || rm) { f.mode = 0; f.tm = rnd(1.1, 3.4) * (f.k === 2 ? 1.6 : 1) * (rm ? 3 : 1); f.thT = K.cruise * rnd(0.6, 1.3); }
          else { f.mode = 1; f.tm = rnd(0.35, 0.8) * (0.7 + L / 120); f.thT = rnd(0.55, 0.9); }
        }
        f.th += (f.thT - f.th) * M.min(1, dt * (f.thT > f.th ? 5 : 1.4));
        f.vm += (1 - f.vm) * M.min(1, dt * 0.6);
        var vt = f.vmax * (0.14 + 0.86 * f.th) * f.vm * (rm ? 0.35 : 1);
        f.v += (vt - f.v) * M.min(1, dt * (vt > f.v ? 2.4 : 0.5));
        f.x += M.cos(f.a) * f.v * dt; f.y += M.sin(f.a) * f.v * dt;
        // tail beat: faster with speed and thrust, faster for small fish; wider when thrusting or turning
        var fq = (0.3 + 2.3 * f.th + 0.8 * f.v / f.vmax) * M.pow(40 / L, 0.3);
        f.ph += TAU * fq * dt;
        var at = L * (0.03 + 0.1 * f.th + 0.06 * M.min(1, M.abs(f.w)));
        f.amp += (at - f.amp) * M.min(1, dt * 4);
        // spine follows the head's path
        f.px[0] = f.x; f.py[0] = f.y;
        for (var s2 = 1; s2 < f.n; s2++) {
          var vx = f.px[s2 - 1] - f.px[s2], vy = f.py[s2 - 1] - f.py[s2];
          // joints bend at most ~11°, so a tight turn reads as a curve, never a fold
          var ja = M.atan2(vy, vx), pa = s2 === 1 ? f.a : M.atan2(f.py[s2 - 2] - f.py[s2 - 1], f.px[s2 - 2] - f.px[s2 - 1]);
          ja = pa + clamp(wrapA(ja - pa), -0.2, 0.2);
          f.px[s2] = f.px[s2 - 1] - M.cos(ja) * f.seg; f.py[s2] = f.py[s2 - 1] - M.sin(ja) * f.seg;
        }
        f.fade = M.min(1, f.fade + dt * 0.5);
      }
    };

    // ── drawing ───────────────────────────────────────────────────────────────
    var N = 11, CX = new Float32Array(N), CY = new Float32Array(N), NX = new Float32Array(N), NY = new Float32Array(N), WD = new Float32Array(N);
    var LX = new Float32Array(N), LY = new Float32Array(N), RX = new Float32Array(N), RY = new Float32Array(N);
    var shape = function (s) {
      // top-down fish: rounded head, widest at a third, slender peduncle
      return s < 0.3 ? 0.5 + 0.5 * M.sin(s / 0.3 * PI / 2) : 0.13 + 0.87 * M.pow(M.cos((s - 0.3) / 0.7 * PI / 2), 1.25);
    };
    var spine = function (f, oy) {
      var n = f.n;
      for (var i = 0; i < n; i++) {
        var s = i / (n - 1), a = f.px[i], b = f.py[i] - oy;
        var i0 = i > 0 ? i - 1 : 0, i1 = i < n - 1 ? i + 1 : n - 1;
        var tx = f.px[i0] - f.px[i1], ty = f.py[i0] - f.py[i1], tl = M.hypot(tx, ty) || 1;
        var nx = -ty / tl, ny = tx / tl;
        var o = f.amp * (0.14 + 0.86 * s * s) * M.sin(f.ph - s * 5.4);
        CX[i] = a + nx * o; CY[i] = b + ny * o;
      }
      var bank = clamp(f.w * 0.22, -0.3, 0.3);
      for (var k = 0; k < n; k++) {
        var j0 = k > 0 ? k - 1 : 0, j1 = k < n - 1 ? k + 1 : n - 1;
        var ux = CX[j0] - CX[j1], uy = CY[j0] - CY[j1], ul = M.hypot(ux, uy) || 1;
        NX[k] = -uy / ul; NY[k] = ux / ul;
        var w = f.L * f.K.wr * shape(k / (n - 1)) * (1 - M.abs(bank) * 0.25);
        WD[k] = w;
        LX[k] = CX[k] + NX[k] * w * (1 + bank); LY[k] = CY[k] + NY[k] * w * (1 + bank);
        RX[k] = CX[k] - NX[k] * w * (1 - bank); RY[k] = CY[k] - NY[k] * w * (1 - bank);
      }
    };
    var bodyPath = function (c, f, sc, dx, dy) {
      var n = f.n, hx = CX[0] - CX[1], hy = CY[0] - CY[1], hl = M.hypot(hx, hy) || 1;
      var tipX = CX[0] + hx / hl * f.L * 0.05, tipY = CY[0] + hy / hl * f.L * 0.05;
      c.moveTo((tipX + dx) * sc, (tipY + dy) * sc);
      c.quadraticCurveTo((LX[0] + dx) * sc, (LY[0] + dy) * sc, ((LX[0] + LX[1]) / 2 + dx) * sc, ((LY[0] + LY[1]) / 2 + dy) * sc);
      for (var i = 1; i < n - 1; i++) c.quadraticCurveTo((LX[i] + dx) * sc, (LY[i] + dy) * sc, ((LX[i] + LX[i + 1]) / 2 + dx) * sc, ((LY[i] + LY[i + 1]) / 2 + dy) * sc);
      c.lineTo((LX[n - 1] + dx) * sc, (LY[n - 1] + dy) * sc);
      c.lineTo((RX[n - 1] + dx) * sc, (RY[n - 1] + dy) * sc);
      for (var k = n - 2; k > 0; k--) c.quadraticCurveTo((RX[k] + dx) * sc, (RY[k] + dy) * sc, ((RX[k] + RX[k - 1]) / 2 + dx) * sc, ((RY[k] + RY[k - 1]) / 2 + dy) * sc);
      c.quadraticCurveTo((RX[0] + dx) * sc, (RY[0] + dy) * sc, (tipX + dx) * sc, (tipY + dy) * sc);
    };
    var tailPath = function (c, f, sc, dx, dy) {
      var n = f.n, e = n - 1, bx = CX[e], by = CY[e];
      var ta = M.atan2(CY[e] - CY[e - 2], CX[e] - CX[e - 2]);
      var lag = M.sin(f.ph - 5.4 - 1.1); // the fin trails the peduncle
      ta += lag * clamp(f.amp / f.L * 3.2, 0, 0.55);
      var lt = f.L * f.K.tl, spr = 0.36 + 0.16 * (1 - f.th), bend = lag * (f.k === 2 ? 0.4 : 0.22);
      var t1 = ta + spr, t2 = ta - spr, w = WD[e] * 1.1;
      var nx = -M.sin(ta), ny = M.cos(ta), ux = M.cos(ta), uy = M.sin(ta);
      var p = function (x, y) { return [(x + dx) * sc, (y + dy) * sc]; };
      var A = p(bx + nx * w, by + ny * w), B = p(bx - nx * w, by - ny * w);
      var X1 = p(bx + M.cos(t1) * lt, by + M.sin(t1) * lt), X2 = p(bx + M.cos(t2) * lt, by + M.sin(t2) * lt);
      var C1 = p(bx + M.cos(t1 - bend) * lt * 0.55, by + M.sin(t1 - bend) * lt * 0.55), C2 = p(bx + M.cos(t2 - bend) * lt * 0.55, by + M.sin(t2 - bend) * lt * 0.55);
      var Nn = p(bx + ux * lt * 0.48, by + uy * lt * 0.48), NC1 = p(bx + M.cos(ta + spr * 0.5) * lt * 0.78, by + M.sin(ta + spr * 0.5) * lt * 0.78), NC2 = p(bx + M.cos(ta - spr * 0.5) * lt * 0.78, by + M.sin(ta - spr * 0.5) * lt * 0.78);
      c.moveTo(A[0], A[1]);
      c.quadraticCurveTo(C1[0], C1[1], X1[0], X1[1]);
      c.quadraticCurveTo(NC1[0], NC1[1], Nn[0], Nn[1]);
      c.quadraticCurveTo(NC2[0], NC2[1], X2[0], X2[1]);
      c.quadraticCurveTo(C2[0], C2[1], B[0], B[1]);
      c.closePath();
      return [bx, by, ta, lt, spr];
    };
    var finPath = function (c, f, i, side, len, splay) {
      // a teardrop fin from the body edge, swept back, its tip trailing the stroke
      var bx = CX[i] + NX[i] * WD[i] * 0.8 * side, by = CY[i] + NY[i] * WD[i] * 0.8 * side;
      var tx = CX[i] - CX[i + 1], ty = CY[i] - CY[i + 1], tl = M.hypot(tx, ty) || 1; tx /= tl; ty /= tl; // forward
      var bk = M.PI - splay, cs = M.cos(bk), sn = M.sin(bk) * side;
      var dx = tx * cs - ty * sn, dy = tx * sn + ty * cs; // rotate forward by (π − splay) towards the side
      var ex = bx + dx * len, ey = by + dy * len;
      var px = -dy, py = dx;
      c.moveTo(bx + tx * len * 0.16, by + ty * len * 0.16);
      c.quadraticCurveTo(bx + dx * len * 0.55 + px * len * 0.28 * side + tx * len * 0.1, by + dy * len * 0.55 + py * len * 0.28 * side + ty * len * 0.1, ex, ey);
      c.quadraticCurveTo(bx + dx * len * 0.4 - tx * len * 0.12, by + dy * len * 0.4 - ty * len * 0.12, bx - tx * len * 0.14, by - ty * len * 0.14);
      c.closePath();
    };
    var fadeAt = function (x, y) {
      // ink thins under text (screen coordinates)
      var k = 1;
      for (var i = 0; i < texts.length; i++) {
        var t = texts[i], r = t.r, top = r.t - sy, bot = r.b - sy;
        var ddx = x < r.l ? r.l - x : x > r.r ? x - r.r : 0, ddy = y < top ? top - y : y > bot ? y - bot : 0;
        if (ddx > t.f || ddy > t.f) continue;
        var d = M.sqrt(ddx * ddx + ddy * ddy);
        k = M.min(k, t.keep + (1 - t.keep) * sstep(0, t.f, d));
      }
      return k;
    };

    var stats = { n: 0, ms: 0, max: 0, drawn: 0, ring: new Float32Array(600) };
    var render = function () {
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.clearRect(0, 0, cv.width, cv.height);
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      var drawn = 0, alphaAll = pal.a;
      if (pal.sa > 0) {
        sg.setTransform(1, 0, 0, 1, 0, 0);
        sg.clearRect(0, 0, shc.width, shc.height);
        sg.fillStyle = "#000";
        // shadows: mid and near fish cast a soft shadow on the paper, offset by their height under the lamp
        sg.beginPath();
        for (var i = 0; i < fish.length; i++) {
          var f = fish[i];
          if (f.k === 0) continue;
          var oy = sy * f.pz, sx0 = f.x, sy0 = f.y - oy;
          if (sx0 < -f.L * 2 || sx0 > vw + f.L * 2 || sy0 < -f.L * 2 || sy0 > vh + f.L * 2) { f.vis = 0; continue; }
          spine(f, oy);
          var h = 3 + f.d * 9;
          bodyPath(sg, f, SH, h * 0.55, h);
        }
        sg.fill();
        g.globalAlpha = pal.sa;
        g.imageSmoothingEnabled = true;
        g.drawImage(shc, 0, 0, shc.width, shc.height, 0, 0, shc.width / SH, shc.height / SH);
        g.globalAlpha = 1;
      }

      for (var qq = 0; qq < fish.length; qq++) {
        var F = fish[qq], oy2 = sy * F.pz, hx = F.x, hy = F.y - oy2;
        if (hx < -F.L * 2 || hx > vw + F.L * 2 || hy < -F.L * 2 || hy > vh + F.L * 2) continue;
        drawn++;
        spine(F, oy2);
        var al = F.tone * alphaAll * F.fade * fadeAt(CX[3], CY[3]);
        if (al < 0.004) continue;
        var e = F.n - 1;
        // fins first, paler than the body (ink thinned with water)
        g.fillStyle = "rgba(" + inkRGB + "," + (al * 0.5).toFixed(3) + ")";
        g.beginPath();
        var tail = tailPath(g, F, 1, 0, 0);
        if (F.K.fins) {
          var spl = 0.5 + 0.75 * (1 - F.th) + 0.12 * M.sin(F.ph * 0.5);
          var spr = 0.5 + 0.75 * (1 - F.th) + 0.12 * M.sin(F.ph * 0.5 + 1.7);
          var fl = F.L * (F.k === 2 ? 0.23 : 0.16);
          finPath(g, F, 2, 1, fl, spl + clamp(F.w * 0.4, -0.3, 0.3));
          finPath(g, F, 2, -1, fl, spr - clamp(F.w * 0.4, -0.3, 0.3));
          if (F.k === 2) { finPath(g, F, 6, 1, fl * 0.6, spl * 0.8); finPath(g, F, 6, -1, fl * 0.6, spr * 0.8); }
        }
        g.fill();
        // body: ink pooled at the head and along the back, washing out toward the tail
        var gr = g.createLinearGradient(CX[0], CY[0], CX[e], CY[e]);
        gr.addColorStop(0, "rgba(" + inkRGB + "," + (al * 1.05).toFixed(3) + ")");
        gr.addColorStop(0.45, "rgba(" + inkRGB + "," + (al * 0.82).toFixed(3) + ")");
        gr.addColorStop(1, "rgba(" + inkRGB + "," + (al * 0.5).toFixed(3) + ")");
        g.fillStyle = gr;
        g.beginPath();
        bodyPath(g, F, 1, 0, 0);
        g.fill();
        if (F.k > 0) {
          // the dorsal ridge: one darker brush stroke down the back
          g.strokeStyle = "rgba(" + inkRGB + "," + (al * 0.55).toFixed(3) + ")";
          g.lineWidth = F.L * (F.k === 2 ? 0.03 : 0.026);
          g.lineCap = "round";
          g.beginPath();
          g.moveTo(CX[1], CY[1]);
          for (var s = 2; s < 7; s++) g.quadraticCurveTo(CX[s], CY[s], (CX[s] + CX[s + 1]) / 2, (CY[s] + CY[s + 1]) / 2);
          g.stroke();
          if (F.k === 2) {
            // fine rays in the tail
            g.lineWidth = 0.6;
            g.strokeStyle = "rgba(" + inkRGB + "," + (al * 0.38).toFixed(3) + ")";
            g.beginPath();
            for (var r2 = -1; r2 <= 1; r2 += 0.5) {
              var ra = tail[2] + r2 * tail[4] * 0.85, rl = tail[3] * (0.62 + 0.3 * M.abs(r2));
              g.moveTo(tail[0], tail[1]); g.lineTo(tail[0] + M.cos(ra) * rl, tail[1] + M.sin(ra) * rl);
            }
            g.stroke();
          }
          // eyes
          g.fillStyle = "rgba(" + inkRGB + "," + M.min(1, al * 1.9).toFixed(3) + ")";
          g.beginPath();
          var er = M.max(0.7, F.L * 0.014);
          var ex = (CX[0] * 0.7 + CX[1] * 0.3), ey = (CY[0] * 0.7 + CY[1] * 0.3), ew = WD[1] * 0.62;
          g.moveTo(ex + NX[0] * ew + er, ey + NY[0] * ew); g.arc(ex + NX[0] * ew, ey + NY[0] * ew, er, 0, TAU);
          g.moveTo(ex - NX[0] * ew + er, ey - NY[0] * ew); g.arc(ex - NX[0] * ew, ey - NY[0] * ew, er, 0, TAU);
          g.fill();
        }
      }
      // obstacles stay clean
      g.globalCompositeOperation = "destination-out";
      g.fillStyle = "#000";
      for (var o = 0; o < obs.length; o++) {
        var R = obs[o];
        if (R.b - sy < 0 || R.t - sy > vh) continue;
        g.fillRect(R.l - 2, R.t - sy - 2, R.r - R.l + 4, R.b - R.t + 4);
      }
      g.globalCompositeOperation = "source-over";
      stats.drawn = drawn;
    };

    // ── loop ──────────────────────────────────────────────────────────────────
    var STEP = 1 / 60, raf = 0, last = 0, acc = 0, running = false, shown = false, rmLast = 0;
    var waterOnScreen = function () {
      if (!onScreen) return false;
      if (!page || sy < heroB) return true;
      // below the hero: only the margins beside the obstacles show water
      var m = 0;
      for (var i = 0; i < obs.length; i++) { var r = obs[i]; if (r.b > sy && r.t < sy + vh) m = M.max(m, M.min(r.l, vw - r.r)); }
      return m > 36 || !obs.length;
    };
    var frame = function (now) {
      raf = 0;
      if (dead || !shown || D.hidden || !onScreen) { running = false; return; }
      var t0 = performance.now();
      var dt = M.min(0.1, (now - last) / 1000);
      last = now;
      svel = page ? svel * 0.85 + ((sy - lastSy) / M.max(dt, 1 / 240)) * 0.15 : 0; lastSy = sy;
      if (RM.matches) {
        // nearly still: a slow drift, drawn ~10 times a second
        if (now - rmLast < 100) { raf = requestAnimationFrame(frame); return; }
        step(M.min(0.1, (now - rmLast) / 1000) * 0.25); rmLast = now;
      } else {
        acc += dt;
        var n = 0;
        while (acc >= STEP && n < 4) { step(STEP); acc -= STEP; n++; }
        if (n === 4) acc = 0;
      }
      tickPal(now);
      render();
      var ms = performance.now() - t0;
      stats.ring[stats.n % 600] = ms; stats.n++; stats.ms += ms; if (ms > stats.max) stats.max = ms;
      if (!waterOnScreen() && palAt < 0) { running = false; return; } // nothing to see; scroll wakes it
      raf = requestAnimationFrame(frame);
    };
    function wake() {
      if (dead || running || !shown || D.hidden || !onScreen || !fish.length) return;
      running = true; last = performance.now(); rmLast = 0; lastSy = sy;
      raf = requestAnimationFrame(frame);
    }
    on(D, "visibilitychange", function () { if (!D.hidden) wake(); });

    // ── relayout ──────────────────────────────────────────────────────────────
    var lastDims = "", lt = 0, lraf = 0, booted = false;
    var layout = function () {
      if (dead || !booted) return;
      var old = lastDims;
      measure();
      var dims = vw + "x" + PH + "@" + mobile;
      lastDims = dims;
      if (!fish.length || dims.split("x")[0] !== old.split("x")[0] || mobile !== (old.indexOf("true") > 0)) populate();
      if (shown) { tickPal(performance.now()); render(); wake(); }
    };
    var relayout = function () { cancelAnimationFrame(lraf); lraf = requestAnimationFrame(layout); };
    var RO = Wn.ResizeObserver ? new ResizeObserver(function () { clearTimeout(lt); lt = setTimeout(relayout, 120); }) : null;
    if (RO) RO.observe(page ? (q(O.habitat) || D.body) : host);
    on(Wn, "resize", relayout);
    var MO = new MutationObserver(syncPal);
    MO.observe(D.documentElement, { attributes: true, attributeFilter: ["data-theme", "class", "style"] });
    if (!page) MO.observe(host, { attributes: true, attributeFilter: ["class", "style"] });
    on(DARKQ, "change", syncPal);
    on(Wn, "pageshow", syncPal);
    on(RMQ, "change", wake);
    // element mode: pause while the host is scrolled out of view
    var IO = !page && Wn.IntersectionObserver ? new IntersectionObserver(function (es) {
      onScreen = es[es.length - 1].isIntersecting;
      if (onScreen) wake();
    }) : null;
    if (IO) IO.observe(host);

    // ── start after the page's first paint; settle the schools off-screen, then fade in ─
    var boot = function () {
      if (dead) return;
      booted = true;
      syncPal(); tickPal(0);
      measure(); lastDims = vw + "x" + PH + "@" + mobile;
      populate();
      var warm = 0;
      var settle = function () {
        if (dead) return;
        for (var i = 0; i < 20; i++) step(STEP);
        if (++warm < 8) return requestAnimationFrame(settle);
        for (var k = 0; k < fish.length; k++) fish[k].fade = 1;
        shown = true;
        render();
        if (O.fadeIn) cv.classList.add("on"); else { cv.style.transition = "none"; cv.classList.add("on"); }
        wake();
      };
      requestAnimationFrame(settle);
    };
    var start = function () { requestAnimationFrame(function () { setTimeout(boot, 0); }); };
    if (D.readyState === "loading") on(D, "DOMContentLoaded", start, { once: true }); else start();

    var api = {
      canvas: cv,
      stats: stats,
      get fish() { return fish; },
      get running() { return running; },
      /** Re-read layout (obstacles, text, sizes) after your page changes without a resize. */
      layout: layout,
      /** Change options at runtime, e.g. set({ theme: "dark" }) or set({ count: 20 }). */
      set: function (o) {
        var repop = o && ("count" in o || "density" in o);
        assign(O, o);
        syncPal();
        if (booted) { measure(); if (repop) { populate(); for (var k = 0; k < fish.length; k++) fish[k].fade = 1; } if (shown) { tickPal(performance.now()); render(); wake(); } }
        return api;
      },
      destroy: function () {
        if (dead) return;
        dead = true; running = false;
        cancelAnimationFrame(raf); cancelAnimationFrame(lraf); clearTimeout(lt);
        L_.forEach(function (l) { l[0].removeEventListener(l[1], l[2], l[3]); });
        if (RO) RO.disconnect(); MO.disconnect(); if (IO) IO.disconnect();
        if (cv.parentNode) cv.parentNode.removeChild(cv);
        host.classList.remove("ink-fish-host");
        if (hostPos !== null) host.style.position = hostPos;
        if (host.__inkFish === api) delete host.__inkFish;
        var i = instances.indexOf(api); if (i >= 0) instances.splice(i, 1);
      }
    };
    host.__inkFish = api;
    instances.push(api);
    return api;
  }

  // ── auto-init: <body data-ink-fish> or <div data-ink-fish='{"count":30}'> ──
  var autoInit = function () {
    var D = Wn.document;
    Array.prototype.forEach.call(D.querySelectorAll("[data-ink-fish]"), function (el) {
      if (el.__inkFish) return;
      var raw = el.getAttribute("data-ink-fish"), opts = {};
      if (raw && raw.trim()) { try { opts = JSON.parse(raw); } catch (e) { if (Wn.console) console.warn("ink-fish: data-ink-fish is not valid JSON", e); } }
      mount(el, opts);
    });
  };
  if (Wn && Wn.document) {
    if (Wn.document.readyState === "loading") Wn.document.addEventListener("DOMContentLoaded", autoInit, { once: true });
    else autoInit();
  }

  return { mount: mount, init: autoInit, defaults: DEFAULTS, instances: instances, version: "1.0.0" };
});
