# Brainrot Colour Chaos — marketing site

Static single-page website for the hardcover colouring book **Brainrot Colour Chaos: Nothing Special Edition**. Every product link points to the Amazon Australia listing: <https://www.amazon.com.au/dp/B0HKVGHHHG>.

It's plain HTML, CSS and vanilla JavaScript modules. There's no framework, build step, analytics, cookies or backend.

## Structure

```
site/                  Deployed directory (GitHub Pages publishes this folder)
  index.html
  css/styles.css
  js/main.js           Entry module
  js/lightbox.js       Accessible <dialog> image lightbox
  assets/img/          Web-optimised WebP derivatives + QR code
  assets/og-image.jpg  Social sharing image (real front cover)
tools/optimise_images.py   One-off image optimiser (Pillow)
.github/workflows/deploy.yml   Pages deployment on push to main
```

The original high-resolution artwork is **not** stored in this repository. It stays untouched in the supplied asset bundle (`Brainrot_Colour_Chaos_Website_Claude_Code_Bundle/website_package/assets`).

## Local preview

```bash
python -m http.server 8000 --directory site
```

Then open <http://localhost:8000>. Serve the folder over HTTP rather than opening the file directly, because ES modules need it.

## Regenerating images

```bash
pip install pillow
python tools/optimise_images.py "path/to/website_package/assets"
```

## Deployment

Every push to `main` runs `.github/workflows/deploy.yml`, which uploads `site/` and deploys it to GitHub Pages. In **Settings → Pages**, the source must be set to **GitHub Actions**.

Live URL: <https://reevegibsone-cmyk.github.io/brainrot-colour-chaos-site/>

If the site moves to a custom domain, update the `canonical` and `og:` URLs in `site/index.html`.

## Content guardrails

- Every product CTA uses the exact Amazon Australia URL above, with `target="_blank" rel="noopener noreferrer"`.
- The page shows no prices, reviews, ratings, stock or delivery claims, no Amazon logo, and no "Buy now" wording.
- The full-colour Ruotino image is always labelled *Colour inspiration artwork — not a photographed book page.*
- Books 2 and 3 appear only as *Coming later*.
- Web fonts (Baloo 2, Nunito Sans) load from Google Fonts. Google Fonts sets no cookies. To remove that third-party request, self-host the two families' `.woff2` files and replace the `<link>` in `index.html`.
