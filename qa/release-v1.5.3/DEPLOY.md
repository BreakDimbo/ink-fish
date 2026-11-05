# Deploy ink-fish v1.5.3

Approved by the owner ("上线", 2026-11-05 ~16:48 SGT). The release branch fast-forwards onto `origin/main`. Push fast-forward only, and never force.

- Base: `origin/main` = `aa6c705` (v1.5.2; tag `v1.5.2` already on origin, object `c7664fc`; no `v1.5.3` tag on origin yet). Checked with `git fetch origin` and `git ls-remote` on 2026-11-05 at about 16:50 SGT.
- Release tip: the head of branch `v1.5.3-slowclick`. Its commit is the one that adds this file. The code was QA'd at `09a29ad` (r15) and re-QA'd as released at `c7e3daf`, which has the `?v=1.5.3` bump and the version banner (`qa/release-v1.5.3/QA.md`). Later commits only add QA records and this note.
- No bundle. Push straight from the shared repo `/workspace/ink-fish` (`.git` common dir). The branch is checked out in the worktree `/workspace/ink-fish-r15`.

## 1. Check it is still a fast-forward

```sh
cd /workspace/ink-fish-r15        # or /workspace/ink-fish: same repo, same refs
git fetch origin
git rev-parse --short origin/main                                   # expected: aa6c705
git merge-base --is-ancestor origin/main v1.5.3-slowclick && echo FF-OK
git rev-list --count origin/main..v1.5.3-slowclick                  # expected: 9
```

If this does not print FF-OK, or `origin/main` is no longer aa6c705, someone pushed to main since. Stop, and do not force.

## 2. Push main (fast-forward only), then the tag

```sh
git push --dry-run origin v1.5.3-slowclick:refs/heads/main   # should show aa6c705..<tip>  v1.5.3-slowclick -> main
git push origin v1.5.3-slowclick:refs/heads/main             # plain push: GitHub refuses it if it is not a fast-forward
git tag -a v1.5.3 v1.5.3-slowclick -m "ink-fish v1.5.3 — water at a real pond's speed"
git push origin refs/tags/v1.5.3
```

Push size: 9 commits (aa6c705..tip), about 65 new blobs, about 9.7 MB raw. Most of it is the r15 side-by-side mp4s and the release shots. The largest blob is 2.29 MB (`qa/demo-r15/click-sbs-guides-light.mp4`), far below GitHub's 50 MB warning and 100 MB limit.

## 3. Verify the live demo

GitHub Pages serves the repo root of `main`; there is no build step. `index.html` loads `src/ink-fish.js?v=1.5.3` and `src/ink-fish.css?v=1.5.3`. Allow 1–10 minutes for the Pages build (Actions → "pages build and deployment" green) and the CDN (max-age 600).

URL: https://breakdimbo.github.io/ink-fish/

- `curl -s https://breakdimbo.github.io/ink-fish/src/ink-fish.js | head -1` prints `/*! ink-fish v1.5.3 …` (was v1.5.2).
- `curl -s https://breakdimbo.github.io/ink-fish/src/ink-fish.js | grep -c 'version: "1.5.3"'` prints 1.
- `curl -s https://breakdimbo.github.io/ink-fish/ | grep -c 'v=1.5.3'` prints 2 (and `grep -c 'v=1.5.2'` prints 0).
- In a browser console, check that:
  - `InkFish.version === "1.5.3"`
  - `document.body.__inkFish.water === "real"` on a GPU machine
  - `document.body.__inkFish._peek === undefined` and `window.__inkFishGridGain === undefined`
  - there are no console errors
- By eye, in light and dark:
  - A click or tap opens one soft ring that spreads at about a real pond's pace (about 86 px/s, the promo film's ring), not the fast screen-filling rings of v1.5.2. It refracts the floor and fades over about 5 s.
  - A press-and-hold has the same ring.
  - A slow drag leaves a faint V (new, and physically right). A fast flick draws a narrow V like in v1.5.2, which lingers a little longer (about 1.6 s).
  - The wake fades after you let go, and scrolling carries it with the page.

## Notes

- `qa/` is in `.gitignore`, but QA records are force-added. The push carries the demo-r15 and release-v1.5.3 QA media. Local scratch (`qa/release-v1.5.3/behave/`, `__pycache__`, the `qahooks152.py` copy) is untracked and is not pushed.
- Outside `qa/`, only `README.md` (v1.5.3 changelog, EN + ZH), `index.html` (`?v=1.5.3` ×2) and `src/ink-fish.js` (physics + banner/version) change vs aa6c705. No new options, globals or API.
- zh-blog-mirrors and hub-fish vendor their own copies. This push does not change them.
- QA: func 10/10, touch, behave and the light/dark × 1440/390 shots are all clean, with 0 page errors (`qa/release-v1.5.3/QA.md`). The shipped src has no QA hooks (`hooks-check.txt`).
- Perf vs live v1.5.2 (r15, interleaved; `qa/demo-r15/perf-vs-152.md`, `perf-aa.md`):
  - 1440 drag: 6.443 → 6.698 ms lib (+4.0 %, allowance 1.640 ms).
  - 1440 idle: 6.209 → 6.654 ms (+7.2 %, allowance 0.543 ms).
  - The A/A floor is drag +6.0 % and idle +0.9 %. A partial idle re-run (`perf2-idle-*.md`, 17/21 runs) gave +8.7 % against an A/A of +14 %, so the box noise exceeds 5 %. Pooled: idle +5.5 %, drag +0.9 %. 0 errors.
- Trade-offs (from `qa/demo-r15/README.md`): one CSS-px scale everywhere, so the water runs about 28 % fast relative to the fish on a 390 px phone. Slow drags now leave a faint V. Flick wakes linger about 1.6 s. The click ring's tail is a little longer than in the film. The arrival hover ring is folded into the click.
