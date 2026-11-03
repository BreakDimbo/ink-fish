# ink-fish · 水墨游鱼

**中文** | [English](#english)

在网页背后的“纸”里游动的水墨鱼。一张 Canvas 2D、一个 `requestAnimationFrame` 循环，零依赖、无需构建，一个 `<script>` 标签即可使用。纯装饰：不接收鼠标事件，对读屏软件隐藏。

最初是 [zh-blog-mirrors](https://github.com/BreakDimbo/zh-blog-mirrors) 首页书架背后的动效，这里抽出来做成独立的小库。

| 浅色 | 深色 |
| --- | --- |
| ![ink-fish light preview](docs/preview-light.gif) | ![ink-fish dark preview](docs/preview-dark.gif) |

在线演示：打开 [`index.html`](index.html)（本地直接双击即可，或部署到 GitHub Pages）。

## 用法

```html
<link rel="stylesheet" href="src/ink-fish.css">
<script src="src/ink-fish.js"></script>
<script>
  // 整页背景（画布固定在视口）
  var fish = InkFish.mount(document.body, {
    fixed: true,                 // 水池不动，页面在它上面滚动（默认 false：带滚动视差）
    ripples: true,               // 鼠标下极淡的水波纹（默认 false）
    koi: true,                   // 几尾彩色锦鲤（默认 false）
    obstacles: ".card",          // 鱼会绕开这些元素，且元素下方不画墨
    text: "h1, .intro",          // 文字下方的墨色会变淡
    title: "h1"                  // 大鱼给标题让路
  });

  fish.set({ theme: "dark" });   // 运行时修改选项
  fish.destroy();                // 移除画布和所有监听
</script>
```

也可以挂在任意元素上（“局部水池”模式：画布随元素滚动，元素滚出视口时暂停）：

```js
InkFish.mount(document.querySelector("#pond"), { count: 14 });
```

或者不写 JS，用 data 属性自动初始化（属性值为可选的 JSON 选项）：

```html
<body data-ink-fish>
<div data-ink-fish='{"count": 20, "theme": "dark"}'></div>
```

页面需要同时引入 `src/ink-fish.css`（淡入、打印隐藏、`isolation` 层叠上下文）。

## 选项

| 选项 | 默认值 | 说明 |
| --- | --- | --- |
| `count` | `"auto"` | 鱼的数量。`"auto"` 按可游区域面积计算；数字为总数（约 62% 小鱼 / 30% 鲤鱼 / 8% 锦鲤）；或 `{ minnow, carp, koi }` |
| `density` | `1` | `"auto"` 时的面积系数 |
| `theme` | `"auto"` | `"auto"` / `"light"` / `"dark"`。auto：先看 `<html data-theme>`，否则跟随 `prefers-color-scheme` |
| `ink` | `{ light: "#1e1c19", dark: "#e8e2d8" }` | 页面正文颜色（单个 hex 或分主题）。宿主元素上的 CSS 变量 `--ink-fish-ink` 优先 |
| `opacity` | `1` | 墨色整体透明度系数 |
| `shadow` | `1` | 灯下投影的透明度系数，`0` 关闭投影 |
| `koi` | `false` | 彩色锦鲤：红白（kohaku）、丹顶（tancho）、山吹（yamabuki）、昭和（showa），用低饱和的朱砂与赭石“设色”。`true` 按宽度 3–6 尾（移动端 2 尾），或填数字；在 `count` 之外另加。注意与 `count.koi`（大的墨色鱼）不同；开启后墨色大鱼会相应减少 |
| `ripples` | `false` | 鼠标下的水波纹：每移动 ≥120px 且间隔 ≥340ms 才起一圈（不是每次 mousemove），点击起一圈略强的；触屏只在轻点时起。每圈三道波前，内坡一线暗、外坡一线亮，低对比、慢衰减，最多同时 5 圈；经过鱼时会让鱼身轮廓轻微折射、并把鱼轻推开。减少动态效果时关闭 |
| `fixed` | `false` | 整页模式：`true` 时水池固定在视口，页面在其上滚动（无视差，可游区域即视口）；`false` 保持 v1.0 的滚动视差 |
| `adaptive` | `true` | 若帧持续迟到（慢设备光栅化大画布），自动一次性降到 DPR 1 |
| `reducedMotion` | `"auto"` | `"auto"` 遵循 `prefers-reduced-motion`；`true` 始终“静水”模式；`false` 忽略 |
| `interactive` | `true` | 是否响应鼠标、点击、快速滚动 |
| `obstacles` | `""` | 选择器：绕行 + 擦除下方墨迹 |
| `bands` | `""` | 选择器：整行宽的水平“墙”（如工具栏），只绕行不擦除 |
| `text` | `""` | 选择器，或 `[{ selector, keep, feather }]`：文字下墨色变淡（`keep` 默认 0.24，`feather` 默认 30px） |
| `title` | `""` | 选择器：大锦鲤给它让出空间 |
| `hero` | `""` | 选择器：锦鲤只在它底部以上（桌面 +160px，移动端 +40px）活动 |
| `habitat` | `""` | 选择器（整页模式）：可游区域到此元素底部为止，默认 `<body>` |
| `ignore` | `"a,button,input,select,textarea,label,[data-ink-fish-ignore]"` | 在这些元素上点击不会惊鱼（`obstacles` / `bands` 自动加入） |
| `mobileQuery` | `"(max-width: 720px)"` | 匹配时使用移动端的数量与尺寸 |
| `maxDpr` | `1.5` | 设备像素比上限 |
| `fadeIn` | `true` | 首次出现时 2.4s 淡入 |

v1.1 新增的 `fixed`、`ripples`、`koi` 默认都关闭，v1.0 的用法与外观不变；唯一的结构变化是投影改为独立画布，宿主里会多一个 `canvas.ink-fish--shadow`（在主画布之前）。演示页三者都打开。

返回的实例：`{ canvas, stats, fish, running, layout(), set(opts), destroy() }`（`stats.dpr` 为当前画布 DPR）。`set({ koi })` 会让锦鲤淡入/淡出，不会打乱鱼群。`layout()` 用于页面结构变化但没有 resize 时重新测量。

## 渲染原理

- **一张画布、一个循环**：整页模式下画布 `position:fixed` 铺满视口，DPR 上限 1.5；固定步长 1/60 s 的模拟 + rAF 绘制。标签页隐藏、宿主滚出视口、或视口里没有空白水面时循环暂停，滚动/鼠标会唤醒。布局只在 resize / reflow 时读取，帧内不触碰 DOM。
- **三层景深**：远处小鱼、中层鲤鱼、近处大鱼，由远到近绘制。默认各自有滚动视差（`y − scrollY·(0.55+0.45·depth)`）；`fixed: true` 时水池静止、页面在其上滑过，滚动只移动“挖空”区域，不移动画布、不触发布局。
- **脊椎与身体波**：每条鱼 11 节脊椎，跟随头部轨迹，每个关节最多弯 ~11°，急转弯是弧线而不是折叠。一条从头到尾的正弦波叠加在脊椎法线方向，尾鳍摆频与速度、推力相关，小鱼更快。
- **冲刺—滑行节奏**：短暂发力后长时间滑行；转向有角速度上限并做缓动。
- **群游**：同种鱼之间做分离 / 对齐 / 聚合（boids），并用两条不可公度的慢正弦做漫游，轨迹不重复。
- **交互**：鼠标快速划过会惊散附近的鱼；静止的鼠标会吸引好奇的鱼过来“看一看”；点击空白处惊鱼；快速滚动像一股水流。
- **水墨质感**：身体是沿脊椎的二次贝塞尔轮廓，线性渐变让墨在头部和背脊积聚、向尾部化开；鳍和尾更淡；鲤鱼和锦鲤有一笔背脊线和眼睛，锦鲤尾鳍有细鳍条。
- **便宜的软阴影**：投影画在一张独立的 1/4 分辨率画布上，由合成器放大，插值得到柔边，不用 blur 滤镜，主画布也不用每帧做整幅放大拷贝。两张画布都提升为独立合成层（`will-change: transform; contain: strict`），重绘画布不会重绘页面；尺寸真正变化时才重新分配画布（移动端地址栏伸缩不会触发）。
- **水波纹**：每圈是三道向外扩散、逐渐减速的波前，内侧一道极淡的暗线、外侧一道极淡的亮线，像水面的斜坡；经过鱼时按径向把鱼的脊椎点推移 1–2px，形成折射感。
- **锦鲤**：与墨鱼同一套笔墨——先淡墨或赭石铺身，再把朱砂色块用柔边径向渐变“点”在身上（裁剪在身体轮廓内），白色锦鲤靠一圈细轮廓线立在纸上。
- **障碍与文字**：`obstacles` 区域用 `destination-out` 擦除；`text` 区域附近按距离平滑降低墨色。
- **主题**：浅色是暖调的墨，深色是略暖的浅墨；切换主题时 500ms 渐变过渡。
- **减少动态效果**：`prefers-reduced-motion` 下鱼几乎静止，约每秒绘制 10 次。

性能参考（在 zh-blog-mirrors 首页实测）：平均约 0.6 ms/帧；1440px 宽时 57 条鱼，390px 宽时 30 条。演示页（固定水池 + 锦鲤 + 波纹，headless Chromium）：1440px 约 0.9 ms/帧（58 条），390px 约 0.55 ms/帧（31 条）；锦鲤与波纹合计约 +0.06 ms/帧。滚动测试：4× CPU 降速、1440px 时平均帧间隔从 47.6 ms 降到 20.1 ms，长任务从 69 个降到 0。

## 浏览器支持

需要 Canvas 2D、`requestAnimationFrame`、`ResizeObserver`、`MutationObserver`、`matchMedia().addEventListener`（局部水池模式另需 `IntersectionObserver`）。即当前的 Chrome / Edge / Firefox，以及 Safari 14+ / iOS 14+。不支持 Canvas 的环境下 `mount()` 返回 `null`，页面不受影响。打印时隐藏。演示页已在无头 Chromium 中验证。

## 许可证

[MIT](LICENSE) © 2026 BreakDimbo

---

<a id="english"></a>

## English

Brush-ink fish swimming in the "paper" behind your web page. One Canvas 2D, one `requestAnimationFrame` loop, zero dependencies, no build step — a plain `<script>` tag. Purely decorative: it never takes pointer events and is hidden from screen readers.

It started life behind the bookshelves on the [zh-blog-mirrors](https://github.com/BreakDimbo/zh-blog-mirrors) homepage and is extracted here as a standalone library. Previews are above; the demo is [`index.html`](index.html) (works opened locally or on GitHub Pages).

### Usage

```html
<link rel="stylesheet" href="src/ink-fish.css">
<script src="src/ink-fish.js"></script>
<script>
  // whole-page background: the canvas is fixed to the viewport
  var fish = InkFish.mount(document.body, {
    fixed: true,                 // the pond stays put; the page scrolls over it (default false: parallax)
    ripples: true,               // faint water rings under the cursor (default false)
    koi: true,                   // a few painted koi (default false)
    obstacles: ".card",          // fish swim around these, and no ink is drawn under them
    text: "h1, .intro",          // ink thins under this text
    title: "h1"                  // the big fish give the headline room
  });

  fish.set({ theme: "dark" });   // change options at runtime
  fish.destroy();                // remove the canvas and every listener
</script>
```

Mount on any element for a local "pond" (the canvas scrolls with the element and pauses while it's off screen):

```js
InkFish.mount(document.querySelector("#pond"), { count: 14 });
```

Or auto-init with a data attribute (the value is optional JSON options):

```html
<body data-ink-fish>
<div data-ink-fish='{"count": 20, "theme": "dark"}'></div>
```

Include `src/ink-fish.css` as well (fade-in, hidden in print, `isolation` stacking context). `require("./src/ink-fish.js")` also works for bundlers (CommonJS); otherwise it sets `window.InkFish`.

### Options

| Option | Default | Description |
| --- | --- | --- |
| `count` | `"auto"` | Number of fish. `"auto"` scales with the open swimming area; a number is a total (≈62% minnows / 30% carp / 8% koi); or `{ minnow, carp, koi }` |
| `density` | `1` | Area multiplier for `"auto"` |
| `theme` | `"auto"` | `"auto"` / `"light"` / `"dark"`. Auto reads `<html data-theme>`, else `prefers-color-scheme` |
| `ink` | `{ light: "#1e1c19", dark: "#e8e2d8" }` | Your page's text colour (one hex or per theme). A `--ink-fish-ink` CSS variable on the host wins |
| `opacity` | `1` | Multiplies the ink alpha |
| `shadow` | `1` | Multiplies the lamp-shadow alpha; `0` turns shadows off |
| `koi` | `false` | Painted koi — kohaku, tancho, yamabuki, showa — in muted cinnabar and ochre washes. `true` = 3–6 by width (2 on mobile), or a number; added on top of `count`. Not the same as `count.koi` (the large ink fish); with painted koi on, there are fewer of those |
| `ripples` | `false` | Water rings under the cursor: one per ≥120px and ≥340ms of travel (never per mousemove), a slightly stronger one on click; on touch, on tap only. Three wavefronts per ring, a hairline of shade inside and of light outside, low contrast, slow decay, at most 5 at once; a passing ring bends the fish it crosses and nudges them aside. Off under reduced motion |
| `fixed` | `false` | Page mode: `true` keeps the pond still while the page scrolls over it (no parallax; the swimming area is the viewport); `false` keeps v1.0's scroll parallax |
| `adaptive` | `true` | If frames keep arriving late (a slow device rasterising a large canvas), drop once to DPR 1 |
| `reducedMotion` | `"auto"` | `"auto"` respects `prefers-reduced-motion`; `true` always calm; `false` ignores it |
| `interactive` | `true` | React to the cursor, taps and fast scrolling |
| `obstacles` | `""` | Selector: avoided, and the canvas is erased under them |
| `bands` | `""` | Selector: full-width horizontal walls (e.g. a toolbar), avoided but not erased |
| `text` | `""` | Selector, or `[{ selector, keep, feather }]`: ink thins under this text (`keep` 0.24, `feather` 30px by default) |
| `title` | `""` | Selector: the big koi give it room |
| `hero` | `""` | Selector: koi stay above its bottom (+160px desktop, +40px mobile) |
| `habitat` | `""` | Selector (page mode): the swimming area ends at this element's bottom; default `<body>` |
| `ignore` | `"a,button,input,select,textarea,label,[data-ink-fish-ignore]"` | Clicks here don't startle fish (`obstacles` / `bands` are added automatically) |
| `mobileQuery` | `"(max-width: 720px)"` | When it matches, mobile counts and sizes are used |
| `maxDpr` | `1.5` | Device-pixel-ratio cap |
| `fadeIn` | `true` | 2.4 s fade-in on first appearance |

The v1.1 options `fixed`, `ripples` and `koi` are all off by default, so v1.0 usage and look are unchanged; the one structural change is that shadows now live on their own canvas, so the host gets an extra `canvas.ink-fish--shadow` (just before the main canvas). The demo turns all three on.

The returned instance: `{ canvas, stats, fish, running, layout(), set(opts), destroy() }` (`stats.dpr` is the current canvas DPR). `set({ koi })` fades koi in or out without reshuffling the shoal. Call `layout()` after your page changes structure without a resize.

### How it renders

- **One canvas, one loop.** In page mode the canvas is `position:fixed` over the viewport, DPR capped at 1.5; a fixed 1/60 s simulation step plus rAF drawing. The loop pauses when the tab is hidden, the host is off screen, or no open water is visible; scrolling or the cursor wakes it. Layout is read only on resize/reflow, never inside a frame.
- **Three depth layers** — far minnows, mid carp, near large fish — painted far to near. By default each has scroll parallax (`y − scrollY·(0.55+0.45·depth)`); with `fixed: true` the pond stays still and the page slides over it — a scroll only moves the cut-outs, never the canvas, and never triggers layout.
- **Spine and body wave.** Each fish is an 11-segment spine that follows its head's path; joints bend at most ~11°, so a tight turn reads as a curve, never a fold. A sine wave travels head to tail along the spine normals; the tail-beat frequency follows speed and thrust and is faster for small fish.
- **Burst-and-glide** rhythm, with capped, eased angular velocity for turns.
- **Schooling** within each species (separation / alignment / cohesion), plus wandering from two slow incommensurate sines so paths never repeat.
- **Interaction.** A fast cursor scatters nearby fish, a still cursor draws the curious ones in to look, a click in open water startles them, and a fast scroll is felt as a current.
- **Ink look.** Bodies are quadratic-Bézier outlines along the spine with a linear gradient that pools ink at the head and washes out toward the tail; fins and tail are paler; carp and koi get a dorsal brush stroke and eyes, koi get fine tail rays.
- **Cheap soft shadows** are drawn on their own quarter-resolution canvas, which the compositor scales up — interpolation softens them with no blur filter, and the main canvas never pays for a full-size blit. Both canvases are promoted layers (`will-change: transform; contain: strict`), so redrawing them never repaints the page; the backing store is reallocated only when its size really changes (not when a mobile URL bar slides).
- **Ripples.** Each ring is a short train of three decelerating wavefronts: a hairline of shade on the inner slope, a hairline of light on the outer. Where a ring crosses a fish, the spine points shift radially by a pixel or two, which reads as refraction.
- **Koi.** The same brush language as the ink fish: a pale ink or ochre wash for the body, then cinnabar patches laid in with soft-edged radial washes clipped to the body outline; pale koi stand on the paper by a fine outline.
- **Obstacles and text.** Obstacle rects are erased with `destination-out`; ink fades smoothly near `text` rects.
- **Themes.** Warm sumi ink in light mode, slightly warmed pale ink in dark mode, cross-faded over 500 ms on a theme switch.
- **Reduced motion.** Under `prefers-reduced-motion` the fish barely drift and the canvas redraws about 10 times a second.

Performance, measured on the zh-blog-mirrors homepage: about 0.6 ms per frame on average; 57 fish at 1440px wide, 30 at 390px. On the demo page (fixed pond + koi + ripples, headless Chromium): ~0.9 ms/frame at 1440px (58 fish), ~0.55 ms/frame at 390px (31); koi and ripples together add ~0.06 ms/frame. In a scroll test at 1440px with a 4× CPU throttle, the mean frame interval went from 47.6 ms (v1.0 demo) to 20.1 ms and long tasks from 69 to 0.

### Browser support

Needs Canvas 2D, `requestAnimationFrame`, `ResizeObserver`, `MutationObserver` and `matchMedia().addEventListener` (plus `IntersectionObserver` for element mode): current Chrome, Edge and Firefox, and Safari 14+ / iOS 14+. Where Canvas is unavailable `mount()` returns `null` and the page is unaffected. Hidden in print. The demo is verified in headless Chromium.

### Reproducing the zh-blog-mirrors homepage

```js
InkFish.mount(document.body, {
  habitat: ".wrap", hero: "header.hero", title: "header.hero h1",
  obstacles: ".shelves .unit, .flat, #case", bands: ".bar",
  ignore: "a,button,input,label,.tape",
  text: [
    { selector: "header.hero .eyebrow", keep: 0.3, feather: 30 },
    { selector: "header.hero h1", keep: 0.16, feather: 44 },
    { selector: "header.hero .intro", keep: 0.24, feather: 34 },
    { selector: "header.hero .howto", keep: 0.26, feather: 28 },
    { selector: ".top > *", keep: 0.3, feather: 24 },
    { selector: "body > footer, .wrap > footer, main > .empty", keep: 0.24, feather: 30 }
  ]
});
```

### License

[MIT](LICENSE) © 2026 BreakDimbo
