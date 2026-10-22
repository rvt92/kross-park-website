#!/usr/bin/env python3
"""Generates the KROSS PARK static pages with a shared shell.
Edit page content below, run `python build.py` (from any directory), done.
Output: the six site pages, privacy/thanks/404, and the Google Ads landing pages in go/."""

import hashlib, pathlib, re, urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
# Content hash of the stylesheet, appended as ?v= so nginx can cache assets for a year safely.
CSS_VER = hashlib.md5((HERE / "assets" / "styles.css").read_bytes()).hexdigest()[:8]

PAGES = {
    "index.html":      ("Home", "KROSS PARK | Rooftop Fitness &amp; Pickleball in Phrom Phong, Bangkok"),
    "pickleball.html": ("Pickleball", "Pickleball Court | KROSS PARK Bangkok"),
    "classes.html":    ("Classes", "Group Classes & Membership | KROSS PARK Bangkok"),
    "training.html":   ("Personal Training", "1:1 Personal Training | KROSS PARK Bangkok"),
    "events.html":     ("Events", "Rooftop Events & Venue Hire | KROSS PARK Bangkok"),
    "contact.html":    ("Contact", "Contact & Location | KROSS PARK Bangkok"),
    "privacy.html":    ("Privacy", "Privacy Policy | KROSS PARK Bangkok"),
    "thanks.html":     ("Thanks", "Message received | KROSS PARK Bangkok"),
    "404.html":        ("Not found", "Page not found | KROSS PARK Bangkok"),
}
NOINDEX = {"thanks.html", "404.html"}

NAV_ITEMS = [
    ("index.html", "Home"),
    ("pickleball.html", "Pickleball"),
    ("classes.html", "Classes"),
    ("training.html", "Personal Training"),
    ("events.html", "Events"),
    ("contact.html", "Contact"),
]


GA_ID = "G-YN3RY665Y2"
# Google Ads conversion tracking. Default: leave both empty and import the GA4 events
# (contact_click, app_download_click, generate_lead) as conversions inside Google Ads.
# Only set these if you create a conversion action directly in Google Ads instead:
# ADS_ID = "AW-123456789", ADS_LEAD_LABEL = "AbCdEfGhIj" (the label Google shows for the action).
ADS_ID = "AW-18523916986"
# The Ads account has an event-based conversion action named submit_lead_form (primary goal of the
# Performance Max campaign). Contact clicks and form submits send that event to the Ads tag.
ADS_LEAD_EVENT = "submit_lead_form"
ADS_LEAD_LABEL = ""   # only for a classic conversion action with an AW-xxx/LABEL snippet


def ga_head():
    ads = f"\ngtag('config', '{ADS_ID}');" if ADS_ID else ""
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_ID}');{ads}
</script>"""

ICONS = """<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">"""

def track_js():
    if ADS_ID and ADS_LEAD_LABEL:
        conv = f"gtag('event','conversion',{{send_to:'{ADS_ID}/{ADS_LEAD_LABEL}'}});"
    elif ADS_ID and ADS_LEAD_EVENT:
        conv = f"gtag('event','{ADS_LEAD_EVENT}',{{send_to:'{ADS_ID}'}});"
    else:
        conv = ""
    lead_conv = f"if(lead) {conv}" if conv else ""
    return f"""
document.addEventListener('click', function(e){{
  var a = e.target.closest('a'); if(!a || typeof gtag !== 'function') return;
  var h = a.href || '', lead = true;
  if(h.indexOf('apps.apple.com') > -1) gtag('event','app_download_click',{{platform:'ios'}});
  else if(h.indexOf('play.google.com') > -1) gtag('event','app_download_click',{{platform:'android'}});
  else if(h.indexOf('chat.whatsapp.com') > -1) {{ lead = false; gtag('event','community_join_click',{{}}); }}
  else if(h.indexOf('line.me') > -1) gtag('event','contact_click',{{channel:'line'}});
  else if(h.indexOf('wa.me') > -1) gtag('event','contact_click',{{channel:'whatsapp'}});
  else if(h.indexOf('mailto:') === 0) gtag('event','contact_click',{{channel:'email'}});
  else lead = false;
  {lead_conv}
}});
var enq = document.querySelector('form.enquiry');
if(enq) enq.addEventListener('submit', function(e){{
  if(typeof gtag === 'function') {{ gtag('event','generate_lead',{{form:'enquiry'}}); {conv} }}
  if(!window.fetch) return;  // old browser: normal submit, lands on /thanks
  e.preventDefault();
  var btn = enq.querySelector('button[type=submit]'), err = document.getElementById('formError');
  btn.disabled = true; btn.textContent = 'Sending...'; err.hidden = true;
  fetch(enq.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {{
    method: 'POST', body: new FormData(enq), headers: {{'Accept': 'application/json'}}
  }}).then(function(r){{ return r.json(); }}).then(function(d){{
    if(!d || String(d.success) !== 'true') throw new Error(d && d.message);
    enq.reset(); enq.hidden = true; document.getElementById('formOk').hidden = false;
  }}).catch(function(){{
    btn.disabled = false; btn.textContent = 'Send message'; err.hidden = false;
  }});
}});
"""

SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ExerciseGym",
  "name": "KROSS PARK Rooftop Fitness & Pickleball",
  "url": "https://krosspark.club/",
  "image": "https://krosspark.club/assets/img/og-image.jpg",
  "telephone": "+66925726448",
  "email": "krosspark2026@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana",
    "addressLocality": "Bangkok",
    "postalCode": "10110",
    "addressCountry": "TH"
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "08:00",
    "closes": "22:00"
  }],
  "sameAs": [
    "https://www.instagram.com/krossparkbangkok",
    "https://line.me/R/ti/p/@531jlxud"
  ],
  "parentOrganization": { "@type": "Organization", "name": "KROSS" }
}
</script>"""


def shell(page, title, body, desc):
    nav = "\n          ".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{label}</a></li>'
        for href, label in NAV_ITEMS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if page in NOINDEX else ''}
<link rel="canonical" href="{'https://krosspark.club/' + ('' if page == 'index.html' else page[:-5])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KROSS PARK">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{'https://krosspark.club/' + ('' if page == 'index.html' else page[:-5])}">
<meta property="og:image" content="https://krosspark.club/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{ICONS}
{ga_head()}
{SCHEMA if page == 'index.html' else ''}
<link rel="stylesheet" href="assets/styles.css?v={CSS_VER}">
</head>
<body>

<header class="site-header" id="siteHeader">
  <nav class="nav">
    <a class="logo" href="index.html"><img src="assets/img/logo-white.png" alt="KROSS PARK"></a>
    <a class="nav-line" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg><span>LINE OA</span></a>
    <button class="nav-toggle" aria-label="Open menu" onclick="document.getElementById('navLinks').classList.toggle('open')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <ul class="nav-links" id="navLinks">
          {nav}
          <li class="nav-line-item"><a class="nav-cta nav-cta-line" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">LINE OA</a></li>
          <li><a class="nav-cta" href="index.html#app">Get the App</a></li>
    </ul>
  </nav>
</header>

{body}

<a class="line-float" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener" aria-label="Chat with KROSS PARK on LINE"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg><span>Chat on LINE</span></a>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <a class="logo" href="index.html"><img src="assets/img/logo-white.png" alt="KROSS PARK"></a>
        <p style="margin-top:14px">Rooftop training club in Phrom Phong, Bangkok. Pickleball, strength, recovery and coaching, above the city.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="pickleball.html">Pickleball</a></li>
          <li><a href="classes.html">Classes</a></li>
          <li><a href="training.html">Personal Training</a></li>
          <li><a href="events.html">Events</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Visit</h4>
        <ul>
          <li>KROSS PARK Rooftop Fitness &amp; Pickleball</li>
          <li>5/9 Soi Phrom Si 1</li>
          <li>Khlong Tan Nuea, Watthana</li>
          <li>Bangkok 10110</li>
          <li>Daily 08:00 to 22:00</li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Talk to us</h4>
        <ul>
          <li><a href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">KROSS App for iOS</a></li>
          <li><a href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">KROSS App for Android</a></li>
          <li><a href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">LINE @krosspark</a></li>
          <li><a href="https://chat.whatsapp.com/Is66HkwpgYCAmzRa89bq48" target="_blank" rel="noopener">WhatsApp Community</a></li>
          <li><a href="https://wa.me/66925726448" target="_blank" rel="noopener">WhatsApp +66 92 572 6448</a></li>
          <li><a href="https://www.instagram.com/krossparkbangkok" target="_blank" rel="noopener">Instagram @krossparkbangkok</a></li>
          <li><a href="mailto:krosspark2026@gmail.com">krosspark2026@gmail.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 KROSS PARK. Part of the KROSS family.</span>
      <span>Rooftop training club, Bangkok · <a href="privacy.html">Privacy</a></span>
    </div>
  </div>
</footer>

<script>
const header = document.getElementById('siteHeader');
addEventListener('scroll', () => header.classList.toggle('scrolled', scrollY > 40), {{passive:true}});
if (location.pathname.split('/').pop() !== 'index.html' && location.pathname.split('/').pop() !== '') header.classList.add('scrolled');
const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add('in')), {{threshold:.12}});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
{track_js()}
</script>
</body>
</html>
"""

def esc_braces(s):  # body content is plain, only the shell uses f-string
    return s

BODIES = {}

BODIES["index.html"] = """
<!-- ============ HERO ============ -->
<section class="hero">
  <div class="hero-media">
    <video autoplay muted loop playsinline poster="assets/img/hero-poster.jpg">
      <source src="assets/video/hero.webm" type="video/webm">
      <source src="assets/video/hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="hero-overlay"></div>
  <div class="wrap hero-inner">
    <span class="eyebrow">Rooftop training club · Phrom Phong, Bangkok</span>
    <h1>Train above<br>the city</h1>
    <p class="lead">Sunset pickleball, sleds against the skyline, and an ice bath waiting when you have earned it. Eight floors above the noise, this is training the way Bangkok has never seen it.</p>
    <div class="hero-ctas">
      <a class="btn btn-solid" href="classes.html">Explore group classes</a>
      <a class="btn btn-solid" href="pickleball.html">Book the court</a>
    </div>
    <div class="hero-meta courtline light">
      <div>Pickleball</div>
      <div>Ice bath</div>
      <div>Outdoor strength park</div>
      <div>Training studio</div>
    </div>
  </div>
</section>

<!-- ============ INTRO ============ -->
<section class="section">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow" style="color:var(--forest-700)">The Park</span>
      <h2 style="margin-top:14px">One rooftop.<br>Everything you need.</h2>
    </div>
    <div>
      <p class="lead">KROSS PARK is the newest space from the team behind KROSS, Thailand's largest padel chain. We looked at a rooftop in Phrom Phong and saw what nobody else did: a training ground in the sky. Now the morning starts with pickleball before the heat, sleds run against the skyline, barbells move in the open air, and the day ends with a cold plunge and a view.</p>
      <p style="margin-top:16px; max-width:34em">Come for a game, a class, a session with your coach, or all three. The skyline comes free.</p>
    </div>
  </div>
</section>

<!-- ============ FACILITIES ============ -->
<section class="section section-dark on-dark">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Facilities</span>
      <h2>Built for people who train</h2>
    </div>
    <div class="grid grid-4 reveal">
      <a class="facility" href="pickleball.html">
        <span class="fnum">Court</span>
        <h3 class="courtline light">Pickleball</h3>
        <p>One dedicated court with a retractable roof for shade and light rain. Book it by the hour.</p>
      </a>
      <a class="facility" href="pickleball.html#recovery">
        <span class="fnum">Recovery</span>
        <h3 class="courtline light">Ice bath</h3>
        <p>A rooftop ice bath with a skyline view. Finish your session the hard way, feel it for days.</p>
      </a>
      <a class="facility" href="training.html#open-gym">
        <span class="fnum">Outdoor</span>
        <h3 class="courtline light">Strength park</h3>
        <p>Calisthenics rig and HYROX equipment in the open air, with the skyline as your gym wall. Open gym sessions from ฿300.</p>
      </a>
      <a class="facility" href="training.html">
        <span class="fnum">Indoor</span>
        <h3 class="courtline light">The studio</h3>
        <p>An indoor gym built for focused 1:1 personal training. Your coach, your plan, no crowds.</p>
      </a>
    </div>
  </div>
</section>

<!-- ============ CLASSES TEASER ============ -->
<section class="section section-sage">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Group classes</span>
      <h2>Coached sessions, real standards</h2>
      <p class="lead">Every class at KROSS PARK is run by a professional coach. Pick your discipline, pick your plan, show up.</p>
    </div>
    <div class="cards reveal">
      <div class="card">
        <span class="tag">Compete</span>
        <h3>HYROX</h3>
        <p>From your first sled push to race day. Structured HYROX prep with the real equipment.</p>
      </div>
      <div class="card">
        <span class="tag">Lift</span>
        <h3>Strength</h3>
        <p>Barbell Club, Power Lab and more. Compound lifts, progressive overload, real numbers.</p>
      </div>
      <div class="card">
        <span class="tag">StrongHer</span>
        <h3>Women's strength</h3>
        <p>StrongHer 40+ and StrongHer Elevate. Strength programs built for women, at every level.</p>
      </div>
      <div class="card">
        <span class="tag">Move</span>
        <h3>Move &amp; restore</h3>
        <p>Animal Flow, Motion Lab and Reset &amp; Restore. Mobility, control and recovery that transfers.</p>
      </div>
    </div>
    <p class="reveal" style="margin-top:22px; font-weight:700">13 class formats on the timetable. All run by professional coaches.</p>
    <div style="margin-top:36px" class="reveal">
      <a class="btn btn-green" href="classes.html">See classes &amp; membership</a>
    </div>
  </div>
</section>

<!-- ============ EVENTS TEASER ============ -->
<section class="section">
  <div class="wrap split reveal">
    <div class="split-media">
      <img src="assets/img/events.jpg" alt="KROSS PARK sign against the Bangkok skyline" loading="lazy">
    </div>
    <div>
      <span class="eyebrow" style="color:var(--forest-700)">The venue</span>
      <h2 style="margin-top:14px">A rooftop your event deserves</h2>
      <p class="lead" style="margin-top:16px">Brand launches, corporate wellness days, tournaments, shoots. The whole park is available for private hire, skyline included.</p>
      <div style="margin-top:26px">
        <a class="btn btn-green" href="events.html">Host an event</a>
      </div>
    </div>
  </div>
</section>

<!-- ============ APP BAND ============ -->
<section class="section section-green on-dark" id="app">
  <div class="wrap cta-band reveal">
    <span class="eyebrow">Bookings</span>
    <h2 style="margin-top:14px">Book everything on the KROSS App</h2>
    <p class="lead" style="margin-top:16px; color:rgba(255,255,255,.85)">Court time, classes and training sessions, all in one place.</p>
    <div style="margin-top:30px"><div class="store-btns">
      <a class="store-btn" href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        <span>App Store<small>Download for iOS</small></span>
      </a>
      <a class="store-btn" href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.6 1.8c-.4.2-.6.6-.6 1.1v18.2c0 .5.2.9.6 1.1l10.2-10.2L3.6 1.8zm11.5 8.9L6.9 2.5l10 5.7-1.8 2.5zm3.6 2.6c.7-.5.7-1.7 0-2.2l-2.1-1.2-2 2.3 2 2.3 2.1-1.2zM6.9 21.5l8.2-8.2 1.8 2.5-10 5.7z"/></svg>
        <span>Google Play<small>Download for Android</small></span>
      </a>
      <a class="store-btn" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg>
        <span>LINE<small>Book with the team, no app needed</small></span>
      </a>
    </div></div>
    <p style="margin-top:22px; font-size:.95rem; color:rgba(255,255,255,.8)">Questions first? <a href="contact.html" style="color:var(--white); font-weight:700">Talk to the team</a>.</p>
  </div>
</section>
"""

BODIES["pickleball.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Court · Retractable roof</span>
    <h1>Pickleball<br>with a view</h1>
    <p class="lead">One dedicated pickleball court on a rooftop in Phrom Phong, Bangkok, with a retractable roof for shade and light rain. Book by the hour on the KROSS App.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split reveal">
    <div class="split-media">
      <img src="assets/img/court.jpg" alt="KROSS PARK rooftop pickleball court at night under the retractable roof" loading="lazy">
    </div>
    <div>
      <span class="eyebrow" style="color:var(--forest-700)">The court</span>
      <h2 style="margin-top:14px">Covered when it counts</h2>
      <p class="lead" style="margin-top:16px">The retractable roof keeps the Bangkok sun off your match and covers you through light rain, so most bookings run exactly as planned.</p>
      <p style="margin-top:16px; max-width:34em">Rental rackets available at the park. Beginners welcome, and our coaches run sessions on court if you want to learn the game properly from day one.</p>
    </div>
  </div>
</section>

<section class="section section-sage">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Rates</span>
      <h2>Court rates</h2>
    </div>
    <div class="reveal">
      <div class="table-scroll"><table class="rates">
        <tr><th>Booking</th><th>Rate</th></tr>
        <tr><td><strong>Court hire, 1 hour</strong></td><td>฿800</td></tr>
        <tr><td><strong>1:1 coaching, 1 hour</strong></td><td>฿1,500</td></tr>
        <tr><td><strong>Extra player in a coached session</strong></td><td>฿200 per player</td></tr>
        <tr><td><strong>Racket rental</strong></td><td>฿100</td></tr>
        <tr><td><strong>Ice bath session</strong></td><td>฿500 per person</td></tr>
      </table></div>
      <p style="margin-top:18px; font-size:.95rem">Book your slot on the KROSS App. It takes a minute.</p>
      <div style="margin-top:22px"><div class="store-btns">
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        <span>App Store<small>Download for iOS</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.6 1.8c-.4.2-.6.6-.6 1.1v18.2c0 .5.2.9.6 1.1l10.2-10.2L3.6 1.8zm11.5 8.9L6.9 2.5l10 5.7-1.8 2.5zm3.6 2.6c.7-.5.7-1.7 0-2.2l-2.1-1.2-2 2.3 2 2.3 2.1-1.2zM6.9 21.5l8.2-8.2 1.8 2.5-10 5.7z"/></svg>
        <span>Google Play<small>Download for Android</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg>
        <span>LINE<small>Book with the team, no app needed</small></span>
      </a>
    </div></div>
    </div>
  </div>
</section>

<section class="section section-dark on-dark" id="recovery">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow" style="color:var(--sage)">Recovery</span>
      <h2 style="margin-top:14px">The ice bath.<br>Zero excuses.</h2>
      <p class="lead" style="margin-top:16px">Finish your match or your session with a plunge. Cold water recovery on a rooftop is a different experience, and yes, it counts double during hot season. ฿500 per session.</p>
    </div>
    <div class="split-media">
      <img src="assets/img/icebath.jpg" alt="Ice bath on the KROSS PARK rooftop with the Bangkok skyline behind" loading="lazy">
    </div>
  </div>
</section>
"""

BODIES["classes.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Group classes · Membership</span>
    <h1>Coached, not<br>just supervised</h1>
    <p class="lead">13 class formats, all run by professional coaches. Join the Club for unlimited classes, or buy a pack and use it your way.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow" style="color:var(--forest-700)">The classes</span>
      <h2>Find your discipline</h2>
    </div>
    <div class="cards reveal">
      <div class="card">
        <span class="tag">HYROX</span>
        <h3>Start on Hyrox</h3>
        <p>The fundamentals of HYROX: the core movements, pacing and workout structure. The right first step.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">HYROX</span>
        <h3>Road to Hyrox</h3>
        <p>Progressive conditioning that builds the strength, endurance and race specific skills to get you to the start line.</p>
      </div>
      <div class="card">
        <span class="tag">Strength</span>
        <h3>Power Lab</h3>
        <p>Compound lifts and explosive movements to build serious strength and athletic power.</p>
      </div>
      <div class="card">
        <span class="tag">StrongHer</span>
        <h3>StrongHer 40+</h3>
        <p>Strength for women over 40. Muscle maintenance, bone health, mobility and functional fitness.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">StrongHer</span>
        <h3>StrongHer Elevate</h3>
        <p>Intermediate to advanced women's strength. Lean muscle, confidence and lifting technique.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">Strength</span>
        <h3>Booty &amp; Core Burn</h3>
        <p>Glutes, hips and core through focused strength and endurance work.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">Performance</span>
        <h3>Athletic Performance</h3>
        <p>Speed, agility, power and coordination. Train like an athlete, move like one everywhere else.</p>
      </div>
      <div class="card">
        <span class="tag">Cardio</span>
        <h3>Latin Fire</h3>
        <p>High energy cardio dance with Latin music and choreography. Sweat, smile, repeat.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">Functional</span>
        <h3>Bodyweight &amp; Suspension</h3>
        <p>Bodyweight and suspension training for strength, stability and mobility that holds up in real life.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">Move</span>
        <h3>Motion Lab</h3>
        <p>Mobility, flexibility, balance and coordination. The class that makes every other class better.</p>
      </div>
      <div class="card">
        <span class="tag">Move</span>
        <h3>Animal Flow</h3>
        <p>Ground based movement inspired by animal locomotion. Mobility, core strength and total body control.</p>
      </div>
      <div class="card hidden-class">
        <span class="tag">Strength</span>
        <h3>Barbell Club</h3>
        <p>Squats, deadlifts, presses and Olympic lift variations. Technique first, progressive overload always.</p>
      </div>
      <div class="card">
        <span class="tag">Recover</span>
        <h3>Reset &amp; Restore</h3>
        <p>Stretching, mobility, breathwork and gentle movement to reduce soreness and recover properly.</p>
      </div>
    </div>
    <div class="reveal" style="margin-top:28px">
      <button class="btn btn-green" id="showAllClasses" onclick="document.querySelector('.cards').classList.add('expanded'); this.style.display='none'">Show all 13 classes</button>
    </div>
    <div class="placeholder-note reveal" style="margin-top:28px">
      Weekly schedule coming soon. Check the KROSS App or join the WhatsApp Community for this week's timetable.
      <!-- SCHEDULE PLACEHOLDER: replace this block with the timetable when ready -->
    </div>
  </div>
</section>

<section class="section section-sage">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Club membership</span>
      <h2>Unlimited classes</h2>
      <p class="lead">One membership, every class on the timetable, plus member perks across the park. Longer commitment, better rate.</p>
    </div>
    <div class="plans reveal">
      <div class="plan">
        <span class="tag" style="font-size:.74rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:var(--forest-600)">Monthly</span>
        <h3>Club monthly</h3>
        <div class="price">฿5,000<small>/month</small></div>
        <ul>
          <li>Unlimited group classes</li>
          <li>Monthly member perks included</li>
          <li>No lock in</li>
        </ul>
        <a class="btn btn-green" href="index.html#app">Join on the app</a>
      </div>
      <div class="plan">
        <span class="tag" style="font-size:.74rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:var(--forest-600)">Quarterly</span>
        <h3>Club quarterly</h3>
        <div class="price">฿14,000<small>/3 months</small></div>
        <ul>
          <li>Unlimited group classes</li>
          <li>Monthly member perks included</li>
          <li>Works out at ฿4,667 per month</li>
        </ul>
        <a class="btn btn-green" href="index.html#app">Join on the app</a>
      </div>
      <div class="plan featured">
        <span class="tag" style="font-size:.74rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:var(--sage)">Annual · Best value</span>
        <h3>Club annual</h3>
        <div class="price">฿48,000<small>/year</small></div>
        <ul>
          <li>Unlimited group classes</li>
          <li>Monthly member perks included</li>
          <li>Works out at ฿4,000 per month</li>
        </ul>
        <a class="btn btn-solid" href="index.html#app">Join on the app</a>
      </div>
    </div>
    <p class="reveal" style="margin-top:18px; font-size:.95rem">Not on the app yet? <a href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener" style="font-weight:700">Message us on LINE</a> and we set you up.</p>
    <div class="card reveal" style="margin-top:22px">
      <span class="tag">Member perks</span>
      <p>Every month: 2 ice bath sessions, 1 pickleball session (full court, event or open match) and 1 free event. Plus 20% off merchandising and drinks, always.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow" style="color:var(--forest-700)">Class packs</span>
      <h2>Prefer to pay as you train?</h2>
      <p class="lead">Buy a pack of sessions and book the classes you want, when you want them.</p>
    </div>
    <div class="reveal">
      <div class="table-scroll"><table class="rates">
        <tr><th>Pack</th><th>Sessions</th><th>Price</th><th>Per session</th><th>Valid for</th></tr>
        <tr><td><strong>Single class</strong></td><td>1</td><td>฿700</td><td>฿700</td><td>—</td></tr>
        <tr><td><strong>Starter</strong></td><td>10</td><td>฿4,500</td><td>฿450</td><td>3 months</td></tr>
        <tr><td><strong>Essential</strong></td><td>20</td><td>฿8,000</td><td>฿400</td><td>4 months</td></tr>
        <tr><td><strong>Signature</strong></td><td>30</td><td>฿10,500</td><td>฿350</td><td>5 months</td></tr>
      </table></div>
    </div>
  </div>
</section>
"""

BODIES["training.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Personal training · The studio</span>
    <h1>Your coach.<br>Your plan.</h1>
    <p class="lead">Personal training in a dedicated indoor studio in Phrom Phong, Bangkok. Work with a personal trainer 1:1 or bring a partner, and train to a plan built around you.</p>
  </div>
</section>

<section class="section">
  <div class="wrap split reveal">
    <div>
      <span class="eyebrow" style="color:var(--forest-700)">How it works</span>
      <h2 style="margin-top:14px">Built around you</h2>
      <p class="lead" style="margin-top:16px">Every PT journey at KROSS PARK starts with an assessment. Your coach maps where you are, where you want to be, and builds the program that gets you there.</p>
      <p style="margin-top:16px; max-width:34em">Sessions run 1:1 or as a duo in our indoor studio, built for focused work, with the rooftop strength park and ice bath available when your program calls for them. Strength, fat loss, HYROX prep, return from injury, sport specific work. Whatever the goal, it gets a plan.</p>
      <div style="margin-top:26px">
        <a class="btn btn-green" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">Book your assessment on LINE</a>
      </div>
    </div>
    <div class="split-media">
      <img src="assets/img/studio.jpg" alt="Personal training session in the KROSS PARK indoor studio" loading="lazy">
    </div>
  </div>
</section>

<section class="section section-sage">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Rates</span>
      <h2>Sessions &amp; packages</h2>
    </div>
    <div class="reveal">
      <div class="table-scroll"><table class="rates">
        <tr><th>Session</th><th>Price</th><th>Notes</th></tr>
        <tr><td><strong>1:1 session</strong></td><td>฿2,200</td><td>60 minutes, includes assessment for new clients</td></tr>
        <tr><td><strong>Duo session</strong></td><td>฿3,000</td><td>2 people, total price</td></tr>
      </table></div>
      <div style="height:22px"></div>
      <div class="table-scroll"><table class="rates">
        <tr><th>1:1 package</th><th>Sessions</th><th>Price</th><th>Per session</th><th>Extras</th><th>Valid for</th></tr>
        <tr><td><strong>Starter</strong></td><td>10</td><td>฿20,000</td><td>฿2,000</td><td>—</td><td>3 months</td></tr>
        <tr><td><strong>Essential</strong></td><td>20</td><td>฿36,000</td><td>฿1,800</td><td>1 group class</td><td>4 months</td></tr>
        <tr><td><strong>Signature</strong></td><td>30</td><td>฿50,000</td><td>฿1,666</td><td>1 group class + 1 pickleball session</td><td>5 months</td></tr>
      </table></div>
      <p style="margin-top:18px; font-size:.95rem">Groups of 3 or more? <a href="contact.html" style="font-weight:700">Get in touch</a> and we build it on request.</p>
    </div>
  </div>
</section>

<section class="section" id="open-gym">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow" style="color:var(--forest-700)">Open gym</span>
      <h2>Train on your own terms</h2>
      <p class="lead">Prefer to run your own program? Book an open gym session and train in the outdoor strength park, with the calisthenics rig and HYROX equipment against the skyline.</p>
    </div>
    <div class="reveal">
      <div class="table-scroll"><table class="rates">
        <tr><th>Session</th><th>Price</th><th>Notes</th></tr>
        <tr><td><strong>Open gym session</strong></td><td>฿300</td><td>Single session</td></tr>
      </table></div>
      <p style="margin-top:18px; font-size:.95rem">Book your session on the KROSS App.</p>
      <div style="margin-top:22px"><div class="store-btns">
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        <span>App Store<small>Download for iOS</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.6 1.8c-.4.2-.6.6-.6 1.1v18.2c0 .5.2.9.6 1.1l10.2-10.2L3.6 1.8zm11.5 8.9L6.9 2.5l10 5.7-1.8 2.5zm3.6 2.6c.7-.5.7-1.7 0-2.2l-2.1-1.2-2 2.3 2 2.3 2.1-1.2zM6.9 21.5l8.2-8.2 1.8 2.5-10 5.7z"/></svg>
        <span>Google Play<small>Download for Android</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg>
        <span>LINE<small>Book with the team, no app needed</small></span>
      </a>
    </div></div>
    </div>
  </div>
</section>
"""

BODIES["events.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Venue hire · Private events</span>
    <h1>Rent the<br>rooftop</h1>
    <p class="lead">A skyline venue with a court, a strength park and a story. The whole space is available for private hire.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow" style="color:var(--forest-700)">What runs well here</span>
      <h2>Made for events that move</h2>
    </div>
    <div class="cards reveal">
      <div class="card">
        <span class="tag">Brands</span>
        <h3>Launches &amp; activations</h3>
        <p>A rooftop with a pickleball court photographs like nothing else in Bangkok. Bring your brand up here.</p>
      </div>
      <div class="card">
        <span class="tag">Companies</span>
        <h3>Corporate wellness</h3>
        <p>Team training days, tournaments and offsites run by our coaches. Your team leaves tired and talking about it.</p>
      </div>
      <div class="card">
        <span class="tag">Sport</span>
        <h3>Tournaments &amp; socials</h3>
        <p>Pickleball round robins, HYROX throwdowns, community events. We handle format, gear and coaching.</p>
      </div>
      <div class="card">
        <span class="tag">Production</span>
        <h3>Shoots &amp; content</h3>
        <p>Skyline backdrops, court graphics and golden hour light. Available for photo and video production.</p>
      </div>
    </div>
    <div class="hero-ctas reveal" style="margin-top:36px">
      <a class="btn btn-green" href="contact.html">Enquire about your event</a>
      <a class="btn btn-outline dark-context" href="https://wa.me/66918027263" target="_blank" rel="noopener">WhatsApp us</a>
    </div>
  </div>
</section>

<section class="section section-dark on-dark">
  <div class="wrap split reveal">
    <div class="split-media">
      <img src="assets/img/events-2.jpg" alt="Outdoor strength park at KROSS PARK with monkey bars and sled track at sunset" loading="lazy">
    </div>
    <div>
      <span class="eyebrow" style="color:var(--sage)">The details</span>
      <h2 style="margin-top:14px">Tell us the plan</h2>
      <p class="lead" style="margin-top:16px">Capacity, catering options and rates depend on your format. Send us the date, the headcount and the idea, and we come back with a proposal within 48 hours.</p>
    </div>
  </div>
</section>
"""

BODIES["contact.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Contact · Location</span>
    <h1>Come up<br>and see us</h1>
    <p class="lead">Bookings live on the KROSS App. For everything else, LINE Official is the fastest way to reach the team, and the WhatsApp Community keeps you up to date.</p>
  </div>
</section>

<section class="section">
  <div class="wrap contact-grid">
    <div class="reveal">
      <span class="eyebrow" style="color:var(--forest-700)">Enquiry form</span>
      <h2 style="margin:14px 0 26px">Send us a message</h2>
      <!-- FormSubmit (formsubmit.co) posts the form straight to the inbox, no backend needed.
           The first submission sends a one-time activation email to krosspark2026@gmail.com; confirm it once. -->
      <form class="enquiry" name="enquiry" method="POST" action="https://formsubmit.co/krosspark2026@gmail.com">
        <input type="hidden" name="_subject" value="KROSS PARK website enquiry">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" value="https://krosspark.club/thanks">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="field">
          <label for="f-name">Name</label>
          <input id="f-name" name="name" type="text" required>
        </div>
        <div class="field">
          <label for="f-email">Email</label>
          <input id="f-email" name="email" type="email" required>
        </div>
        <div class="field">
          <label for="f-phone">Phone (optional)</label>
          <input id="f-phone" name="phone" type="tel">
        </div>
        <div class="field">
          <label for="f-interest">I'm interested in</label>
          <select id="f-interest" name="interest" required>
            <option value="">Choose one</option>
            <option>Pickleball booking</option>
            <option>Group classes and membership</option>
            <option>Personal training</option>
            <option>Hosting an event</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field">
          <label for="f-message">Message</label>
          <textarea id="f-message" name="message" rows="5" required></textarea>
        </div>
        <button class="btn btn-green" type="submit">Send message</button>
        <p class="form-note" id="formError" hidden>Something went wrong. Please try again, or message us on LINE.</p>
      </form>
      <div class="form-ok" id="formOk" hidden>
        <span class="eyebrow" style="color:var(--forest-700)">Message received</span>
        <h3 style="margin-top:12px">Got it. Talk soon.</h3>
        <p style="margin-top:10px">We reply by email, usually within a day. Need an answer faster? <a href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener" style="font-weight:700">LINE @krosspark</a> is the quickest way to reach the team.</p>
      </div>
    </div>
    <div class="contact-channels reveal">
      <div class="channel">
        <span class="tag">Bookings · KROSS App</span>
        <div style="margin-top:10px"><div class="store-btns">
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        <span>App Store<small>Download for iOS</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.6 1.8c-.4.2-.6.6-.6 1.1v18.2c0 .5.2.9.6 1.1l10.2-10.2L3.6 1.8zm11.5 8.9L6.9 2.5l10 5.7-1.8 2.5zm3.6 2.6c.7-.5.7-1.7 0-2.2l-2.1-1.2-2 2.3 2 2.3 2.1-1.2zM6.9 21.5l8.2-8.2 1.8 2.5-10 5.7z"/></svg>
        <span>Google Play<small>Download for Android</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg>
        <span>LINE<small>Book with the team, no app needed</small></span>
      </a>
    </div></div>
      </div>
      <div class="channel">
        <span class="tag">Talk to the team · LINE Official</span>
        <a href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">LINE @krosspark</a>
      </div>
      <div class="channel">
        <span class="tag">Stay updated · WhatsApp Community</span>
        <a href="https://chat.whatsapp.com/Is66HkwpgYCAmzRa89bq48" target="_blank" rel="noopener">Join the community</a>
        <p style="margin-top:6px; font-size:.9rem">Events, class schedules, pickleball and training updates, first.</p>
      </div>
      <div class="channel">
        <span class="tag">Phone · WhatsApp</span>
        <a href="https://wa.me/66925726448" target="_blank" rel="noopener">+66 92 572 6448</a>
      </div>
      <div class="channel">
        <span class="tag">Email</span>
        <a href="mailto:krosspark2026@gmail.com">krosspark2026@gmail.com</a>
      </div>
      <div class="channel">
        <span class="tag">Instagram</span>
        <a href="https://www.instagram.com/krossparkbangkok" target="_blank" rel="noopener">@krossparkbangkok</a>
      </div>
      <div class="channel">
        <span class="tag">Address</span>
        <p style="font-weight:800; font-size:1.05rem">5/9 Soi Phrom Si 1, Khlong Tan Nuea,<br>Watthana, Bangkok 10110</p>
      </div>
      <div class="channel">
        <span class="tag">Hours</span>
        <p style="font-weight:800; font-size:1.05rem">Daily 08:00 to 22:00</p>
      </div>
      <iframe class="map-embed" loading="lazy" title="KROSS PARK location map"
        src="https://www.google.com/maps?q=5/9+Soi+Phrom+Si+1,+Khlong+Tan+Nuea,+Watthana,+Bangkok+10110&output=embed"></iframe>
    </div>
  </div>
</section>
"""

BODIES["privacy.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Privacy</span>
    <h1>Privacy<br>policy</h1>
    <p class="lead">What we collect on krosspark.club, why, and how to reach us about it. Last updated 22 October 2026.</p>
  </div>
</section>

<section class="section">
  <div class="wrap" style="max-width:820px">
    <h3>Who we are</h3>
    <p style="margin:10px 0 28px">KROSS PARK, 5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110, Thailand. Email <a href="mailto:krosspark2026@gmail.com">krosspark2026@gmail.com</a>.</p>

    <h3>Enquiry form</h3>
    <p style="margin:10px 0 28px">When you send the form on our contact page we receive your name, email, phone number if you give it, what you are interested in and your message. The form is delivered by FormSubmit (formsubmit.co), which passes it to our inbox. We use it only to answer you. We do not sell or share it.</p>

    <h3>Analytics and advertising</h3>
    <p style="margin:10px 0 28px">We use Google Analytics 4 to understand how the site is used, and Google Ads to measure whether our ads lead to a visit, a message or an app download. Both set cookies and record your approximate location, device and pages viewed. Google's own privacy policy applies to that data. You can block these cookies in your browser or with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out add-on</a>.</p>

    <h3>Third parties on the page</h3>
    <p style="margin:10px 0 28px">The map on the contact page is embedded from Google Maps. Links to the KROSS App, LINE, WhatsApp and Instagram take you to those services, each with its own privacy policy. Bookings and payments happen in the KROSS App, not on this site.</p>

    <h3>Your rights</h3>
    <p style="margin:10px 0 28px">Under Thailand's Personal Data Protection Act you can ask what we hold about you, ask us to correct it, or ask us to delete it. Email <a href="mailto:krosspark2026@gmail.com">krosspark2026@gmail.com</a> and we handle it.</p>
  </div>
</section>
"""

BODIES["thanks.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Message received</span>
    <h1>Got it.<br>Talk soon.</h1>
    <p class="lead">Your message is in our inbox. We reply by email, usually within a day. Need an answer faster? LINE is the quickest way to reach the team.</p>
    <div class="hero-ctas">
      <a class="btn btn-solid" href="https://line.me/R/ti/p/@531jlxud" target="_blank" rel="noopener">LINE @krosspark</a>
      <a class="btn btn-outline" href="index.html">Back to the site</a>
    </div>
  </div>
</section>
"""

BODIES["404.html"] = """
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">404</span>
    <h1>Nothing<br>up here</h1>
    <p class="lead">That page does not exist or has moved. The rooftop is still where it always was.</p>
    <div class="hero-ctas">
      <a class="btn btn-solid" href="index.html">Home</a>
      <a class="btn btn-outline" href="pickleball.html">Pickleball</a>
      <a class="btn btn-outline" href="classes.html">Classes</a>
      <a class="btn btn-outline" href="training.html">Personal training</a>
    </div>
  </div>
</section>
"""


# ============================================================
# Google Ads landing pages: krosspark.club/go/<slug>
# One per ad group. No navigation, one offer, LINE as the primary action, WhatsApp second.
# noindex so they never compete with the organic pages. Edit copy here only.
# ============================================================

WA_NUMBER = "66925726448"
LINE_URL = "https://line.me/R/ti/p/@531jlxud"
MAPS_URL = "https://www.google.com/maps?q=5/9+Soi+Phrom+Si+1,+Khlong+Tan+Nuea,+Watthana,+Bangkok+10110"
LINE_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 5.64 2 10.13c0 4.03 3.57 7.4 8.4 8.03.33.07.77.22.88.5.1.26.07.66.03.92l-.14.86c-.04.26-.2 1 .88.55 1.08-.46 5.82-3.43 7.94-5.87C21.53 13.53 22 11.9 22 10.13 22 5.64 17.52 2 12 2zM8.6 12.9H6.5a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 1 0v3.3h1.6a.5.5 0 0 1 0 1zm1.9-.5a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 1 0v3.8zm4.5 0a.5.5 0 0 1-.9.3l-1.9-2.6v2.3a.5.5 0 0 1-1 0V8.6a.5.5 0 0 1 .9-.3l1.9 2.6V8.6a.5.5 0 0 1 1 0v3.8zm3.3-2.4a.5.5 0 0 1 0 1h-1.6v.9h1.6a.5.5 0 0 1 0 1h-2.1a.5.5 0 0 1-.5-.5V8.6a.5.5 0 0 1 .5-.5h2.1a.5.5 0 0 1 0 1h-1.6v.9h1.6z"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.2 22l5.2-1.4A9.8 9.8 0 1 0 12 2.2zm0 1.7a8.1 8.1 0 1 1-4.1 15.1l-.3-.2-3.1.8.8-3-.2-.3A8.1 8.1 0 0 1 12 3.9zM8.9 7.3c-.2 0-.5.1-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.2 5 4.4 2.5 1 3 .8 3.5.7.5 0 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.2-.2-.5-.3l-1.9-.9c-.3-.1-.5-.1-.6.1l-.9 1.1c-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.4.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2c-.2-.5-.4-.5-.6-.5h-.5z"/></svg>'

STORE_BTNS = """<div class="store-btns">
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://apps.apple.com/us/app/kross-padel/id6741785490" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
        <span>App Store<small>Download for iOS</small></span>
      </a>
      <a class="store-btn" style="background:var(--forest-700); color:var(--white)" href="https://play.google.com/store/apps/details?id=com.krosspadel.bookandgo" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.6 1.8c-.4.2-.6.6-.6 1.1v18.2c0 .5.2.9.6 1.1l10.2-10.2L3.6 1.8zm11.5 8.9L6.9 2.5l10 5.7-1.8 2.5zm3.6 2.6c.7-.5.7-1.7 0-2.2l-2.1-1.2-2 2.3 2 2.3 2.1-1.2zM6.9 21.5l8.2-8.2 1.8 2.5-10 5.7z"/></svg>
        <span>Google Play<small>Download for Android</small></span>
      </a>
    </div>"""

LANDINGS = {
    "pickleball": dict(
        title="Rooftop Pickleball Court in Phrom Phong | KROSS PARK Bangkok",
        desc="Book a rooftop pickleball court in Phrom Phong, Bangkok. ฿800 per hour flat, retractable roof, rackets to rent, coaching available. Open daily 08:00 to 22:00.",
        eyebrow="Pickleball · Phrom Phong, Bangkok",
        h1="Rooftop pickleball in Phrom Phong",
        lead="A dedicated rooftop court with a retractable roof for sun and light rain. ฿800 an hour, flat, any time of day. Rackets at the park, coaching if you want it.",
        image="court.jpg",
        alt="KROSS PARK rooftop pickleball court at night under the retractable roof",
        meta=["Retractable roof", "Rackets to rent", "Ice bath", "Daily 08:00 to 22:00"],
        proof=[
            ("฿800 / hour", "Flat rate. No peak pricing."),
            ("Retractable roof", "Shade from the sun, cover from light rain."),
            ("08:00 to 22:00", "Open every day. Book by the hour."),
        ],
        rates_title="Court rates",
        rates=[
            ("Court hire, 1 hour", "฿800"),
            ("1:1 coaching, 1 hour", "฿1,500"),
            ("Extra player in a coached session", "฿200 per player"),
            ("Racket rental", "฿100"),
            ("Ice bath session", "฿500 per person"),
        ],
        book_note="Book your hour on the KROSS App, or message us on LINE or WhatsApp and we do it for you.",
        secondary=("#book", "Book on the app"),
        faq=[
            ("How do I book?", "Download the KROSS App, pick KROSS PARK, choose your hour and confirm. Or message us on LINE or WhatsApp and we book it for you."),
            ("I have never played. Can I still come?", "Yes. Pickleball is quick to pick up. Rent rackets at the park for ฿100, or book a 1:1 coaching hour for ฿1,500 and add friends at ฿200 each."),
            ("What about the heat and the rain?", "The roof closes over the court for sun and light rain, so most bookings run exactly as planned."),
            ("Where are you?", "5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110, in Phrom Phong. Open daily 08:00 to 22:00."),
        ],
        wa_text="Hi KROSS PARK, I saw your ad and would like to book the pickleball court.",
    ),
    "classes": dict(
        title="Coached Group Classes in Phrom Phong | KROSS PARK Bangkok",
        desc="Group fitness classes on a rooftop in Phrom Phong, Bangkok. HYROX, strength, StrongHer, mobility and recovery, 13 formats run by professional coaches. Single class ฿700, unlimited from ฿4,000 a month.",
        eyebrow="Group classes · Phrom Phong, Bangkok",
        h1="Coached classes on a Bangkok rooftop",
        lead="13 formats, from HYROX prep and barbell strength to mobility and recovery, every one run by a professional coach. Drop in for a single class or join the Club for unlimited training.",
        image="hero-poster.jpg",
        alt="KROSS PARK rooftop training ground above Phrom Phong, Bangkok",
        meta=["HYROX", "Strength", "StrongHer", "Mobility & recovery"],
        proof=[
            ("13 formats", "HYROX, strength, StrongHer, movement, recovery."),
            ("Pro coaches", "Every class is coached, not just supervised."),
            ("From ฿350 / class", "Packs of 10, 20 or 30, or unlimited from ฿4,000 a month."),
        ],
        rates_title="Classes & membership",
        rates=[
            ("Single class", "฿700"),
            ("Starter pack, 10 classes", "฿4,500"),
            ("Essential pack, 20 classes", "฿8,000"),
            ("Signature pack, 30 classes", "฿10,500"),
            ("Club membership, unlimited classes", "฿5,000 / month"),
            ("Club membership, quarterly", "฿14,000"),
            ("Club membership, annual", "฿48,000"),
        ],
        book_note="Message us on LINE or WhatsApp with your goal and we book your first class. Classes also live on the KROSS App.",
        secondary=("wa", "WhatsApp"),
        faq=[
            ("Which class should I start with?", "Tell us your goal on LINE or WhatsApp and we point you to the right format. Start on Hyrox is the entry point to HYROX training, Barbell Club and Power Lab cover strength, and StrongHer 40+ and StrongHer Elevate are strength programs built for women."),
            ("What does membership include?", "Unlimited classes, plus every month two ice bath sessions, one pickleball session, one free event, and 20% off merchandise and drinks."),
            ("When are the classes?", "The timetable lives in the KROSS App and our WhatsApp Community. Message us and we send you this week's schedule."),
            ("Where are you?", "5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110, in Phrom Phong. Open daily 08:00 to 22:00."),
        ],
        wa_text="Hi KROSS PARK, I saw your ad and would like to book my first class.",
    ),
    "training": dict(
        title="Personal Trainer in Phrom Phong | KROSS PARK Bangkok",
        desc="Personal training in Phrom Phong, Bangkok. 1:1 or duo sessions in a private indoor studio, with a rooftop strength park and ice bath. ฿2,200 per session, assessment included. Packages from ฿1,666 per session.",
        eyebrow="Personal training · Phrom Phong, Bangkok",
        h1="Your coach. Your plan. Your rooftop.",
        lead="1:1 personal training in a private indoor studio in Phrom Phong, with an outdoor strength park and an ice bath upstairs when your program calls for them. Every journey starts with an assessment.",
        image="studio.jpg",
        alt="Personal training session in the KROSS PARK indoor studio",
        meta=["Indoor studio", "1:1 or duo", "Strength park", "Ice bath"],
        proof=[
            ("Assessment first", "Your coach maps where you are before writing the plan."),
            ("1:1 or duo", "Two people maximum. Focused sessions, no crowds."),
            ("From ฿1,666 / session", "Packages of 10, 20 or 30 sessions."),
        ],
        rates_title="Sessions & packages",
        rates=[
            ("1:1 session, 60 minutes", "฿2,200"),
            ("Duo session, 2 people", "฿3,000 total"),
            ("Starter, 10 sessions", "฿20,000"),
            ("Essential, 20 sessions", "฿36,000"),
            ("Signature, 30 sessions", "฿50,000"),
        ],
        book_note="Message us on LINE or WhatsApp and we book your assessment with a coach.",
        secondary=("wa", "WhatsApp"),
        faq=[
            ("What happens in the first session?", "An assessment. Your coach looks at how you move, where your strength is and what you want, then builds the program. It is included in your first 1:1 session."),
            ("What can I train for?", "Strength, fat loss, HYROX prep, return from injury, sport specific work. Whatever the goal, it gets a plan."),
            ("Can I train with a friend?", "Yes. Duo sessions are ฿3,000 for two people. Groups of three or more on request."),
            ("Where are you?", "5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110, in Phrom Phong. Open daily 08:00 to 22:00."),
        ],
        wa_text="Hi KROSS PARK, I saw your ad and would like to book a personal training assessment.",
    ),
}


def landing(slug, c):
    url = f"https://krosspark.club/go/{slug}"
    wa = f"https://wa.me/{WA_NUMBER}?text=" + urllib.parse.quote(c["wa_text"])
    sec_href, sec_label = c["secondary"]
    meta = "".join(f"<div>{m}</div>" for m in c["meta"])
    proof = "".join(f"<div><strong>{a}</strong><span>{b}</span></div>" for a, b in c["proof"])
    rates = "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>" for a, b in c["rates"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faq"])
    line_btn = f'<a class="btn btn-solid wa-btn" href="{LINE_URL}" target="_blank" rel="noopener">{LINE_ICON}Chat on LINE</a>'
    wa_outline = f'<a class="btn btn-outline wa-btn" href="{wa}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>'
    sec_btn = wa_outline if sec_href == "wa" else f'<a class="btn btn-outline" href="{sec_href}">{sec_label}</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{c["title"]}</title>
<meta name="description" content="{c["desc"]}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KROSS PARK">
<meta property="og:title" content="{c["title"]}">
<meta property="og:description" content="{c["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://krosspark.club/assets/img/og-image.jpg">
{ICONS.replace('href="assets/', 'href="/assets/')}
{ga_head()}
<link rel="stylesheet" href="/assets/styles.css?v={CSS_VER}">
</head>
<body class="landing">

<header class="lp-header">
  <nav class="nav">
    <a class="logo" href="/"><img src="/assets/img/logo-white.png" alt="KROSS PARK"></a>
    <a class="nav-cta" href="{LINE_URL}" target="_blank" rel="noopener">{LINE_ICON}LINE</a>
  </nav>
</header>

<section class="hero lp-hero">
  <div class="hero-media"><img src="/assets/img/{c["image"]}" alt="{c["alt"]}"></div>
  <div class="hero-overlay"></div>
  <div class="wrap hero-inner">
    <span class="eyebrow">{c["eyebrow"]}</span>
    <h1>{c["h1"]}</h1>
    <p class="lead">{c["lead"]}</p>
    <div class="hero-ctas">
      {line_btn}
      {sec_btn}
    </div>
    <div class="hero-meta courtline light">{meta}</div>
  </div>
</section>

<section class="section section-sage">
  <div class="wrap">
    <div class="proof reveal">{proof}</div>
  </div>
</section>

<section class="section" id="book">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Rates</span>
      <h2>{c["rates_title"]}</h2>
    </div>
    <div class="reveal">
      <div class="table-scroll"><table class="rates">
        <tr><th>Item</th><th>Price</th></tr>
        {rates}
      </table></div>
      <p style="margin-top:18px; font-size:.95rem">{c["book_note"]}</p>
      <div class="hero-ctas" style="margin-top:22px">
        <a class="btn btn-green wa-btn" href="{LINE_URL}" target="_blank" rel="noopener">{LINE_ICON}Chat on LINE</a>
        <a class="btn btn-outline dark-context wa-btn" href="{wa}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>
      </div>
      <div style="margin-top:22px">{STORE_BTNS}</div>
    </div>
  </div>
</section>

<section class="section section-sage">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Good to know</span>
      <h2>Questions</h2>
    </div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>

<section class="section section-green on-dark">
  <div class="wrap cta-band reveal">
    <span class="eyebrow">Find us</span>
    <h2 style="margin-top:14px">Rooftop, Phrom Phong</h2>
    <p class="lead" style="margin-top:16px; color:rgba(255,255,255,.85)">5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110. Open daily 08:00 to 22:00.</p>
    <div class="hero-ctas">
      {line_btn}
      <a class="btn btn-outline" href="{MAPS_URL}" target="_blank" rel="noopener">Open in Google Maps</a>
    </div>
  </div>
</section>

<footer class="lp-footer">
  <div class="wrap">
    <span>© 2026 KROSS PARK. Part of the KROSS family.</span>
    <span><a href="/">Full site</a> · <a href="/privacy">Privacy</a> · <a href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener">WhatsApp +66 92 572 6448</a></span>
  </div>
</footer>

<div class="lp-sticky">
  {line_btn}
  {wa_outline}
</div>

<script>
if (typeof gtag === 'function') gtag('event', 'landing_view', {{campaign: '{slug}'}});
const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add('in')), {{threshold:.12}});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
{track_js()}
</script>
</body>
</html>
"""


def clean_links(html):
    """Internal links are written as page.html; the server serves clean URLs, so emit those."""
    html = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', html)
    return re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', html)


for page, (label, title) in PAGES.items():
    desc = {
        "index.html": "Rooftop fitness and pickleball in Phrom Phong, Bangkok. Pickleball court, open gym, group classes, 1:1 personal training and an ice bath.",
        "pickleball.html": "Book Bangkok's rooftop pickleball court at KROSS PARK on the KROSS App. Retractable roof, coaching available, ice bath recovery.",
        "classes.html": "Group classes at KROSS PARK Bangkok: HYROX, strength, StrongHer, movement and recovery. Club membership from ฿4,000 per month or class packs.",
        "training.html": "Personal training in Phrom Phong, Bangkok. 1:1 or duo sessions in a dedicated indoor studio, assessment based coaching, plus open gym sessions.",
        "events.html": "Hire a rooftop venue in the heart of Bangkok. KROSS PARK is available for brand activations, corporate wellness, tournaments and shoots.",
        "contact.html": "Contact KROSS PARK Bangkok via LINE, WhatsApp or enquiry form. 5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110.",
        "privacy.html": "How KROSS PARK handles the data you share on krosspark.club: enquiry form, analytics and advertising cookies, and your rights.",
        "thanks.html": "Your message to KROSS PARK has been received.",
        "404.html": "That page does not exist on krosspark.club.",
    }[page]
    html = clean_links(shell(page, title, BODIES[page], desc))
    (HERE / page).write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {page} ({len(html)} bytes)")

(HERE / "go").mkdir(exist_ok=True)
for slug, cfg in LANDINGS.items():
    html = clean_links(landing(slug, cfg))
    (HERE / "go" / f"{slug}.html").write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote go/{slug}.html ({len(html)} bytes)")
