# Deploy ink-fish v1.5.0

Approved by the owner ("可以，上线", 2026-11-04 20:34 SGT). The release branch fast-forwards onto `origin/main`. Push fast-forward only, and never force.

- Base: `origin/main` = `173a9c0` (v1.3.1; tag `v1.3.1` already on origin)
- Release tip: the head of branch `v1.5-gridwake` (see the bundle below; the code was QA'd at `0c4e9b4`, and later commits only add QA records and this note)
- Bundle: `/workspace/ink-fish-v1.5.bundle` (prerequisite `173a9c0`, ref `refs/heads/v1.5-gridwake`)

## 1. Get the release commits (if not deploying from /workspace/ink-fish)

```sh
git fetch origin
git bundle verify /workspace/ink-fish-v1.5.bundle
git fetch /workspace/ink-fish-v1.5.bundle v1.5-gridwake:v1.5-gridwake
```

## 2. Check it is still a fast-forward

```sh
git fetch origin
git merge-base --is-ancestor origin/main v1.5-gridwake && echo FF-OK
```

If this does not print FF-OK, someone pushed to main since 173a9c0. Stop and do not force.

## 3. Push main (fast-forward only), then the tag

```sh
git push origin v1.5-gridwake:refs/heads/main          # plain push: GitHub refuses it if it is not a fast-forward
git tag -a v1.5.0 v1.5-gridwake -m "ink-fish v1.5.0 — grid-sim drag wake"
git push origin refs/tags/v1.5.0
```

(Optional: `git push --dry-run origin v1.5-gridwake:refs/heads/main` first. It should show `173a9c0..<tip>  v1.5-gridwake -> main`.)

## 4. Verify the live demo

GitHub Pages serves the repo root of `main`; there is no build step and no dist. `index.html` loads `src/ink-fish.js?v=1.5.0` and `src/ink-fish.css?v=1.5.0`. Allow 1–10 minutes for the Pages build and the CDN (max-age 600).

URL: https://breakdimbo.github.io/ink-fish/

- `curl -s https://breakdimbo.github.io/ink-fish/src/ink-fish.js | head -1` prints `/*! ink-fish v1.5.0 …` (was v1.3.1)
- `curl -s https://breakdimbo.github.io/ink-fish/ | grep 'ink-fish.js?v=1.5.0'` matches
- In a browser console: `InkFish.version === "1.5.0"`, `document.body.__inkFish.water === "real"` on a GPU machine, `document.body.__inkFish._peek === undefined`, `window.__inkFishGridGain === undefined`; no console errors
- By eye, light and dark (theme switch on the page):
  - a slow drag only drags a small dimple;
  - a fast flick leaves a narrow V with fine crests on both arms and short ripples ahead;
  - the wake fades about 2 s after you let go;
  - scrolling carries the wake with the page.
- In dark: the press and lift rings and the V arms catch a faint sky sheen, and calm water stays dark.

## Notes

- `qa/` is in `.gitignore` but QA records are force-added. The push carries about 160 MB of QA media (mp4/png, the largest file 6.3 MB) from rounds r9–r12 plus release-v1.5. Raw frame folders (`qa/demo-r*/frames`, ~350 MB) are untracked and are not pushed.
- zh-blog-mirrors vendors its own copy (`assets/ink-fish/ink-fish.{js,css}`, v1.3.1, `?v=` hash token). This push does not change it, and updating it is a separate change in that repo.
