# Deploy ink-fish v1.5.1

Approved by the owner ("可以，上线并更新github", 2026-11-05 09:39 SGT). The release branch fast-forwards onto `origin/main`. Push fast-forward only, and never force.

- Base: `origin/main` = `f4a3191` (v1.5.0; tag `v1.5.0` already on origin)
- Release tip: `657cb4d5e4b8fd9f0e69a9dd887368fefe3aff31` on branch `v1.5.1-click` (code QA'd from `2c6a14c` / `2370e13`; later commits are README/`?v=`, release QA harness and records, and this note)
- Bundle: `/workspace/ink-fish-v1.5.1.bundle` (prerequisite `f4a3191`, ref `refs/heads/v1.5.1-click`)

## 1. Get the release commits (if not deploying from /workspace/ink-fish)

```sh
git fetch origin
git bundle verify /workspace/ink-fish-v1.5.1.bundle
git fetch /workspace/ink-fish-v1.5.1.bundle v1.5.1-click:v1.5.1-click
```

## 2. Check it is still a fast-forward

```sh
git fetch origin
git merge-base --is-ancestor origin/main v1.5.1-click && echo FF-OK
# expected: origin/main is still f4a3191
```

If this does not print FF-OK, someone pushed to main since f4a3191. Stop and do not force.

## 3. Push main (fast-forward only), then the tag

```sh
git push origin v1.5.1-click:refs/heads/main          # plain push: GitHub refuses it if it is not a fast-forward
git tag -a v1.5.1 v1.5.1-click -m "ink-fish v1.5.1 — click restored to v1.2.1 hairline rings"
git push origin refs/tags/v1.5.1
```

(Optional: `git push --dry-run origin v1.5.1-click:refs/heads/main` first. It should show `f4a3191..<tip>  v1.5.1-click -> main`.)

## 4. Verify the live demo

GitHub Pages serves the repo root of `main`; there is no build step and no dist. `index.html` loads `src/ink-fish.js?v=1.5.1` and `src/ink-fish.css?v=1.5.1`. Allow 1–10 minutes for the Pages build and the CDN (max-age 600).

URL: https://breakdimbo.github.io/ink-fish/

- `curl -s https://breakdimbo.github.io/ink-fish/src/ink-fish.js | head -1` prints `/*! ink-fish v1.5.1 …` (was v1.5.0)
- `curl -s https://breakdimbo.github.io/ink-fish/ | grep 'ink-fish.js?v=1.5.1'` matches
- In a browser console: `InkFish.version === "1.5.1"`, `document.body.__inkFish.water === "real"` on a GPU machine, `document.body.__inkFish._peek === undefined`, `window.__inkFishGridGain === undefined`; no console errors
- By eye, light and dark (theme switch on the page):
  - a click or tap draws a few thin hairline rings that grow and fade (no press/lift packet, no dimple, no grid stamp);
  - a slow drag still carries only its dent; a fast flick still leaves a narrow V;
  - the wake fades about 2 s after you let go;
  - scrolling carries the wake with the page.

## Notes

- `qa/` is in `.gitignore` but QA records are force-added. The push carries the r13 and release-v1.5.1 QA media. Raw frame folders (`qa/demo-r*/frames`) are untracked and are not pushed.
- zh-blog-mirrors vendors its own copy (`assets/ink-fish/ink-fish.{js,css}`). This push does not change it.
- Perf note for the Deployer: primary 1440 forced idle/drag PASSed in every interleaved run against live v1.5.0 (drag +1.2 % to +2.0 %). A 390@4× adaptive drag row was flaky across three runs on SwiftShader; see `qa/release-v1.5.1/perf.md`. Func 10/10, touch, behave (incl. click: tap/hold leave no grid; flick wakes it) and demo shots all clean, 0 page errors. Shipped src has no QA hooks.
