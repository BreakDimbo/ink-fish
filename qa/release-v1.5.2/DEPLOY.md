# Deploy ink-fish v1.5.2

Approved by the owner ("上线", 2026-11-05 15:35 SGT). The release branch fast-forwards onto `origin/main`. Push fast-forward only, and never force.

- Base: `origin/main` = `6e725b9` (v1.5.1; tag `v1.5.1` already on origin). Checked with `git fetch origin` on 2026-11-05 at about 15:45 SGT.
- Release tip: the head of branch `v1.5.2-promoclick`. Its commit is the one that adds this file. The code was QA'd at `d512d3f`; later commits only add QA records, README, `?v=1.5.2` and this note.
- No bundle (the disk is nearly full). Push straight from the shared repo `/workspace/ink-fish` (`.git` common dir). The branch is checked out in the worktree `/workspace/ink-fish-r14`.

## 1. Check it is still a fast-forward

```sh
cd /workspace/ink-fish-r14        # or /workspace/ink-fish: same repo, same refs
git fetch origin
git rev-parse --short origin/main                                   # expected: 6e725b9
git merge-base --is-ancestor origin/main v1.5.2-promoclick && echo FF-OK
```

If this does not print FF-OK, or `origin/main` is no longer 6e725b9, someone pushed to main since. Stop, and do not force.

## 2. Push main (fast-forward only), then the tag

```sh
git push --dry-run origin v1.5.2-promoclick:refs/heads/main   # should show 6e725b9..<tip>  v1.5.2-promoclick -> main
git push origin v1.5.2-promoclick:refs/heads/main             # plain push: GitHub refuses it if it is not a fast-forward
git tag -a v1.5.2 v1.5.2-promoclick -m "ink-fish v1.5.2 — the first ripple is the one from the promo film"
git push origin refs/tags/v1.5.2
```

Push size: 18–19 commits, about 266 new blobs, about 208 MB raw. Most of it is QA mp4s; they are already compressed, so the pack is about the same size. The largest blob is 4.66 MB (`qa/demo-r14/drag-newbare-light.mp4`), far below GitHub's 50 MB warning and 100 MB limit. Allow a few minutes for the upload.

## 3. Verify the live demo

GitHub Pages serves the repo root of `main`; there is no build step. `index.html` loads `src/ink-fish.js?v=1.5.2` and `src/ink-fish.css?v=1.5.2`. Allow 1–10 minutes for the Pages build and the CDN (max-age 600).

URL: https://breakdimbo.github.io/ink-fish/

- `curl -s https://breakdimbo.github.io/ink-fish/src/ink-fish.js | head -1` prints `/*! ink-fish v1.5.2 …` (was v1.5.1).
- `curl -s https://breakdimbo.github.io/ink-fish/ | grep -c 'v=1.5.2'` prints 2.
- In a browser console, check that:
  - `InkFish.version === "1.5.2"`
  - `document.body.__inkFish.water === "real"` on a GPU machine
  - `document.body.__inkFish._peek === undefined` and `window.__inkFishGridGain === undefined`
  - there are no console errors
- By eye, in light and dark:
  - A click or tap opens one slow, soft ring (the promo film's), which refracts the floor and moves the caustics as it spreads, then fades over about 5 s. There is no big press packet and no swap after 0.25 s.
  - A press-and-hold has the same ring.
  - A drag opens with the wake alone. A slow start eases on with no big first splash, and a fast flick still draws a narrow V.
  - The wake fades about 2 s after you let go, and scrolling carries it with the page.

## Notes

- `qa/` is in `.gitignore`, but QA records are force-added. The push carries the demo-r14 and release-v1.5.2 QA media. Raw frame folders (`qa/demo-r14/frames`, `qa/demo-r14/stage`) are untracked and are not pushed.
- zh-blog-mirrors vendors its own copy. This push does not change it.
- QA: func 10/10, touch, behave and the light/dark × 1440/390 shots are all clean, with 0 page errors (`qa/release-v1.5.2/QA.md`). Shipped src has no QA hooks (`hooks-check.txt`).
- Perf vs live v1.5.1 (interleaved):
  - 1440 idle: −0.7 % lib ms, +1.8 % frame interval.
  - 1440 forced drag (rotated order, 6 reps): −2.6 % lib ms, +0.6 % frame interval, against an A/A floor of +0.8 % / +0.7 %.
  - 390 adaptive drag: +4.2 % (allowance 12 %).
  - Sources: `qa/demo-r14/perf3-*.md`, `perf4-*.md`.
