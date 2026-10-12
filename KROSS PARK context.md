# KROSS PARK — Business Context

Last updated: July 28, 2026. Owner: Roberto Villalobos.

## What it is
Rooftop training club in Phrom Phong, Bangkok. Newest venture from the team behind KROSS, Thailand's largest padel chain (4 venues, 10 courts). Tagline concept: "Train above the city."

**Address:** 5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110 (marketed as Phrom Phong, not Watthana)
**Hours:** Daily 08:00–22:00

## Facilities
- 1 pickleball court with retractable roof (covers sun and light rain — never claim storm-proof)
- 1 ice bath (exactly one — never say "ice baths")
- Outdoor calisthenics strength park with HYROX equipment (monkey bars, sled track with numbered markings)
- Indoor gym/studio for personal training (1:1 or duo only, max 2 people; groups of 3+ on request only)

## Business model & pricing (THB)
Revenue: pickleball bookings, PT sessions, group class memberships/packs, private event hire.

**Pickleball:** court ฿800/hr flat (no peak pricing) · 1:1 coaching ฿1,500/hr · +฿200 per extra player in coached session · racket rental ฿100 · ice bath ฿500/session/person

**Personal training:** 1:1 session ฿2,200 (60 min, assessment included for new clients) · duo ฿3,000 total for 2 people
Packages (1:1): Starter ฿20,000/10 sessions (฿2,000 ea, 3mo) · Essential ฿36,000/20 (฿1,800 ea, +1 group class, 4mo) · Signature ฿50,000/30 (฿1,666 ea, +1 group class +1 pickleball session, 5mo)

**Group classes:** single class ฿700/person
Packs: Starter ฿4,500/10 (฿450 ea, 3mo) · Essential ฿8,000/20 (฿400 ea, 4mo) · Signature ฿10,500/30 (฿350 ea, 5mo)
Club membership (unlimited classes): ฿5,000/mo · ฿14,000/quarter · ฿48,000/year
Monthly member perks: 2 ice bath sessions, 1 pickleball session (full court, event or open match), 1 free event; plus 20% off merchandising and drinks (frequency of the 20% discount treated as always-on; unconfirmed whether capped)

## Classes (13 formats — names fixed, don't rename)
Start on Hyrox · Road to Hyrox · Power Lab · StrongHer 40+ · StrongHer Elevate · Booty & Core Burn · Athletic Performance · Latin Fire · Bodyweight & Suspension · Motion Lab · Animal Flow · Barbell Club · Reset & Restore
All run by professional coaches. **Rule: never name or describe individual coaches anywhere public** (staff may change; content must stay evergreen).

## Booking & contact hierarchy
1. **Bookings: KROSS App** (primary channel)
   - iOS: https://apps.apple.com/us/app/kross-padel/id6741785490
   - Android: https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo
2. **Talk to the team: LINE Official** @krosspark — https://line.me/R/ti/p/@531jlxud
3. **Updates: WhatsApp Community** — https://chat.whatsapp.com/Is66HkwpgYCAmzRa89bq48
4. Phone/WhatsApp direct: +66 92 572 6448 (wa.me/66925726448)
5. Email: krosspark2026@gmail.com
6. Instagram: @krossparkbangkok

## Brand system
- Colors: deep forest green #0B1D13 / #10281B, primary forest #1C4A33, court sage #9DBFAC, bone off-white #F4F2EB, white court-line accents
- Typography: Gotham Narrow exclusively (licensed, self-hosted woff2: Book 400, Medium 500, Bold 700, Black 800, Ultra 900). Display headlines: Ultra 900, all caps, condensed
- Signature motif: white double court-line strokes as section dividers/structure
- Logo: KROSS (bold) + PARK (light), green on light backgrounds, white version on dark
- Signage on-site reads "KROSSPARK — FITNESS & PICKLEBALL"
- Copy tone: confident, short, direct, no em dashes, honest claims only
- Photography: rooftop skyline, night court with branded surface, golden hour

## Website (live)
- Netlify: https://imaginative-puffpuff-311ad4.netlify.app (rename to krosspark.netlify.app planned; custom domain via Hostinger DNS pending: A @ → 75.2.60.5, CNAME www → netlify subdomain)
- Six static pages: Home, Pickleball, Classes, Personal Training, Events, Contact. English only.
- Stack: hand-coded HTML/CSS, generated via build.py (shared header/footer — edit build.py and rerun to change all pages). Netlify Forms enquiry form (name "enquiry"). Google Maps embed, no API key.
- Home hero: drone video (hero.mp4 5.2MB + hero.webm 3.7MB, 8s loop, poster frame). Classes page shows 6 of 13 classes + "Show all" expander. Tables use horizontal scroll wrappers on mobile.
- Class schedule intentionally placeholder: "check the app or WhatsApp Community"

## Pending / open items
- Membership perks: 20% discount cap unconfirmed
- Class timetable not yet published
- Netlify site rename + custom domain connection
- Google Business Profile setup + review collection (recommended, not done)
- Site improvements identified in audit, not yet implemented: OG tags/favicon/LocalBusiness schema, FAQ section (need answers: parking, showers/lockers, walk-in policy, rain policy for court bookings, cancellation policy), WhatsApp Community band on home page, analytics (GA4/Plausible), social proof/testimonials when available
- Verify KROSS App can actually sell KROSS PARK memberships/packs (membership CTAs currently point to app)
- Better court photo with players; longer hero video cut (15–20s orbit) when available

## Working preferences (Roberto)
- Token-efficient solutions, proactively flag better approaches
- No preamble or filler; direct answers
- Honest feedback, no flattery; challenge his approach when there's a better way
- Content must be low-maintenance (avoid anything requiring frequent site edits)
- Claude Code is his preferred build workflow for bigger projects
