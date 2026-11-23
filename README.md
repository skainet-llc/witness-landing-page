# WITNESS landing page

Static landing page for WITNESS by skAInet, deployed with GitHub Pages:
<https://witness.skainet.io/>

Plain HTML and CSS with a few lines of vanilla JS (mobile menu). No framework,
no build step for the page itself, no cookies, no trackers, no external
requests. All asset paths are relative, so the site works under the Pages
sub-path and on a custom domain root (add a `CNAME` file when the domain is
ready).

## Layout

| Path | Content |
|---|---|
| `index.html` | The page: hero, references, delivers, how it works, use cases, hardware, data ownership, insurers, downloads, contact |
| `assets/css/style.css` | skainet.io style: Biryani, `#262626` / `#E83B3B` / `#F2F2F2` / `#3C3B3B`, square shapes |
| `assets/js/main.js` | Mobile navigation toggle |
| `assets/fonts/biryani/` | Biryani, subset to Latin as WOFF2 (SIL Open Font License, `OFL.txt`) |
| `assets/logos/` | Reference logos as shown on edge-compute.skainet.io |
| `assets/img/` | Logo, favicons, OG image, edge compute and PowerProbe photos, Kelvion IR images |
| `assets/fig/` | Use-case figures (SVG), generated from the use-case one-pager repos |
| `tools/figures_svg.py` | Runs a use-case repo's `tools/figures.py` unchanged and writes SVG instead of PDF |
| `tools/build_downloads.py` | Fills the downloads section from the PDFs in `_site/downloads/` |
| `.github/workflows/pages.yml` | Build and deploy to GitHub Pages |

## Downloads

The one-pager PDFs come from the private repo `skainet-llc/witness-one-pagers`
and are not committed here. On every deploy the workflow

1. downloads the assets (`*.pdf`, `*.zip`) of the latest release of
   `skainet-llc/witness-one-pagers` into `_site/downloads/`, if the repository
   secret `ONEPAGERS_TOKEN` is set (a fine-grained token with read access to
   the contents of `witness-one-pagers`);
2. runs `tools/build_downloads.py _site`, which links every one-pager it finds
   and lists the others as available on request.

Without the secret, or without a release, the build still succeeds and the
section shows "Available on request: hello@skainet.io".

To refresh the page after a new one-pager release, re-run the workflow
(Actions, "Deploy to GitHub Pages", Run workflow) or send a repository
dispatch:

```sh
gh api repos/skainet-llc/witness-landing-page/dispatches -f event_type=onepagers-released
```

## Local preview

```sh
make serve     # http://localhost:8000, downloads show the fallback
make site      # assemble _site/ like CI (put PDFs in _site/downloads/ first)
```

## Figures

`make figures` regenerates `assets/fig/*.svg` from the sibling repos
`../witness-usecase-{railway-points,slide-gates,valves}` (Python 3 with
matplotlib). The curves are stylised, synthetic shapes, as in the one-pagers.
