# Third-party notices

ink-fish is MIT-licensed (see `LICENSE`). The real-water layer added in v1.3 (`water: "real"`) adapts
published *methods*; no third-party source code is copied into `src/`. The works it follows are credited here.

## Ultra Water — Humpalumps (MIT)

<https://github.com/Humpalumps/Ultra-Water>. Ultra Water's README and source showed the approach used here:
Cauchy–Poisson impact rings for point disturbances, the capillary–gravity dispersion ω² = gk + (σ/ρ)k³ with
σ/ρ = 7.4e-5 m³/s², area-ratio caustics sampled through cubic B-spline–smoothed slopes, Beer–Lambert
absorption of the water column and Fresnel-weighted reflection. ink-fish reimplements these ideas from scratch
for a top-down, page-background pond in WebGL2 and Canvas 2D.

> MIT License — Copyright (c) 2026 Humpalumps
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
> documentation files (the "Software"), to deal in the Software without restriction, including without limitation
> the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
> to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions
> of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
> THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
> CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
> DEALINGS IN THE SOFTWARE.

## Methods credited (no code)

- **Caustics:** Evan Wallace, "Rendering Realtime Caustics in WebGL" (2016): refract a grid onto the floor and
  let each triangle add old area / new area, so light is only redistributed (mean 1).
- **Ocean spectra and dispersion:** Jerry Tessendorf, "Simulating Ocean Water" (SIGGRAPH course notes, 1999–2004):
  dispersion relations and summing dispersive waves; the ambient swell is a small hand-picked set of them.
- **Bessel functions J0/J1:** polynomial approximations from Abramowitz & Stegun, *Handbook of Mathematical
  Functions*, §9.4.1–9.4.6 (a public U.S. government work).
- **Fresnel:** Schlick's approximation (1994).
