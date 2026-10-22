# KROSS PARK website

Source for https://krosspark.club, the KROSS PARK rooftop fitness and pickleball site in Phrom Phong, Bangkok.

## Hosting
Self-hosted on the OVH VPS through Coolify. The `Dockerfile` packs `site/` into an nginx image;
`nginx.conf` gives clean URLs (`/pickleball` serves `pickleball.html`), 301s from the old `.html`
and `/personal-training` URLs, the 404 page, gzip and cache headers. Coolify builds the image from
this repo on every push to `main` and puts its Traefik proxy (HTTPS) in front.

## Layout
- `site/build.py` generates every page from one shared shell. Edit copy there, never in the HTML.
- `site/go/*.html` are the Google Ads landing pages (`/go/pickleball`, `/go/classes`, `/go/training`),
  generated from the `LANDINGS` dict in `build.py`. They are `noindex`, have no navigation, and use
  WhatsApp as the primary action with a prefilled message per campaign.
- `site/privacy.html`, `site/thanks.html`, `site/404.html` are generated too.
- The enquiry form posts to FormSubmit (formsubmit.co) and lands in krosspark2026@gmail.com.
- `KROSS PARK context.md` is business context for the site.

## Editing
```
python site/build.py
git add -A && git commit -m "..." && git push
```
Coolify redeploys automatically. `styles.css` is cache-busted with a content hash, so CSS edits
show up immediately after a deploy.

## Tracking
GA4 (`G-YN3RY665Y2`) is on every page. Clicks on WhatsApp, LINE, email and the app stores fire
`contact_click` / `app_download_click`; the form fires `generate_lead`; landing pages fire
`landing_view`. Import those GA4 events as conversions in Google Ads. If you prefer a conversion
action created inside Google Ads, set `ADS_ID` and `ADS_LEAD_LABEL` at the top of `build.py`.

## Fonts
Gotham Narrow is licensed. Keep this repo private and the fonts on krosspark.club only.
