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
  // 整页背景（画布固定在视口，带滚动视差）
  var fish = InkFish.mount(document.body, {
    obstacles: ".card",          // 鱼会绕开这些元素，且元素下方不画墨
    text: "h1, .intro",          // 文字下方的墨色会变淡
    title: "h1", hero: "header"  // 大锦鲤给标题让路，并留在 hero 区域附近
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

返回的实例：`{ canvas, stats, fish, running, layout(), set(opts), destroy() }`。`layout()` 用于页面结构变化但没有 resize 时重新测量。

## 渲染原理

- **一张画布、一个循环**：整页模式下画布 `position:fixed` 铺满视口，DPR 上限 1.5；固定步长 1/60 s 的模拟 + rAF 绘制。标签页隐藏、宿主滚出视口、或视口里没有空白水面时循环暂停，滚动/鼠标会唤醒。布局只在 resize / reflow 时读取，帧内不触碰 DOM。
- **三层景深**：远处小鱼、中层鲤鱼、近处锦鲤，各自有滚动视差（`y − scrollY·(0.55+0.45·depth)`），由远到近绘制。
- **脊椎与身体波**：每条鱼 11 节脊椎，跟随头部轨迹，每个关节最多弯 ~11°，急转弯是弧线而不是折叠。一条从头到尾的正弦波叠加在脊椎法线方向，尾鳍摆频与速度、推力相关，小鱼更快。
- **冲刺—滑行节奏**：短暂发力后长时间滑行；转向有角速度上限并做缓动。
- **群游**：同种鱼之间做分离 / 对齐 / 聚合（boids），并用两条不可公度的慢正弦做漫游，轨迹不重复。
- **交互**：鼠标快速划过会惊散附近的鱼；静止的鼠标会吸引好奇的鱼过来“看一看”；点击空白处惊鱼；快速滚动像一股水流。
- **水墨质感**：身体是沿脊椎的二次贝塞尔轮廓，线性渐变让墨在头部和背脊积聚、向尾部化开；鳍和尾更淡；鲤鱼和锦鲤有一笔背脊线和眼睛，锦鲤尾鳍有细鳍条。
- **便宜的软阴影**：投影画在 1/4 分辨率的离屏画布上再放大，借助插值得到柔边，不用 blur 滤镜。
- **障碍与文字**：`obstacles` 区域用 `destination-out` 擦除；`text` 区域附近按距离平滑降低墨色。
- **主题**：浅色是暖调的墨，深色是略暖的浅墨；切换主题时 500ms 渐变过渡。
- **减少动态效果**：`prefers-reduced-motion` 下鱼几乎静止，约每秒绘制 10 次。

性能参考（在 zh-blog-mirrors 首页实测）：平均约 0.6 ms/帧；1440px 宽时 57 条鱼，390px 宽时 30 条。

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
  // whole-page background: the canvas is fixed to the viewport, with scroll parallax
  var fish = InkFish.mount(document.body, {
    obstacles: ".card",          // fish swim around these, and no ink is drawn under them
    text: "h1, .intro",          // ink thins under this text
    title: "h1", hero: "header"  // the big koi give the headline room and stay near the hero
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

The returned instance: `{ canvas, stats, fish, running, layout(), set(opts), destroy() }`. Call `layout()` after your page changes structure without a resize.

### How it renders

- **One canvas, one loop.** In page mode the canvas is `position:fixed` over the viewport, DPR capped at 1.5; a fixed 1/60 s simulation step plus rAF drawing. The loop pauses when the tab is hidden, the host is off screen, or no open water is visible; scrolling or the cursor wakes it. Layout is read only on resize/reflow, never inside a frame.
- **Three depth layers** — far minnows, mid carp, near koi — each with scroll parallax (`y − scrollY·(0.55+0.45·depth)`), painted far to near.
- **Spine and body wave.** Each fish is an 11-segment spine that follows its head's path; joints bend at most ~11°, so a tight turn reads as a curve, never a fold. A sine wave travels head to tail along the spine normals; the tail-beat frequency follows speed and thrust and is faster for small fish.
- **Burst-and-glide** rhythm, with capped, eased angular velocity for turns.
- **Schooling** within each species (separation / alignment / cohesion), plus wandering from two slow incommensurate sines so paths never repeat.
- **Interaction.** A fast cursor scatters nearby fish, a still cursor draws the curious ones in to look, a click in open water startles them, and a fast scroll is felt as a current.
- **Ink look.** Bodies are quadratic-Bézier outlines along the spine with a linear gradient that pools ink at the head and washes out toward the tail; fins and tail are paler; carp and koi get a dorsal brush stroke and eyes, koi get fine tail rays.
- **Cheap soft shadows** are drawn on a quarter-resolution offscreen canvas and scaled up, so interpolation softens them with no blur filter.
- **Obstacles and text.** Obstacle rects are erased with `destination-out`; ink fades smoothly near `text` rects.
- **Themes.** Warm sumi ink in light mode, slightly warmed pale ink in dark mode, cross-faded over 500 ms on a theme switch.
- **Reduced motion.** Under `prefers-reduced-motion` the fish barely drift and the canvas redraws about 10 times a second.

Performance, measured on the zh-blog-mirrors homepage: about 0.6 ms per frame on average; 57 fish at 1440px wide, 30 at 390px.

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
