# KROSS PARK website

Source for https://krosspark.club, the KROSS PARK rooftop fitness and pickleball site in Phrom Phong, Bangkok.

## Layout
- `site/` is the Netlify publish directory. Everything in it goes live as is.
- `site/build.py` generates the six HTML pages from one shared shell. Edit copy there, never in the generated HTML.
- `site/_redirects` holds Netlify redirects. `netlify.toml` at the repo root points Netlify at `site/`.
- `KROSS PARK context.md` is business context for the site.

## Editing
```
python site/build.py
```
Then commit the regenerated HTML together with `build.py`. Netlify deploys on push once the repo is linked.

## Fonts
Gotham Narrow is licensed. Keep this repo private and the fonts on krosspark.club only.
