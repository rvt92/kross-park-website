#!/usr/bin/env python3
"""Generates the KROSS PARK static pages with a shared shell.
Edit page content below, run `python3 build.py`, done."""

PAGES = {
    "index.html":      ("Home", "KROSS PARK | Rooftop Fitness &amp; Pickleball in Phrom Phong, Bangkok"),
    "pickleball.html": ("Pickleball", "Pickleball Court | KROSS PARK Bangkok"),
    "classes.html":    ("Classes", "Group Classes & Membership | KROSS PARK Bangkok"),
    "training.html":   ("Personal Training", "1:1 Personal Training | KROSS PARK Bangkok"),
    "events.html":     ("Events", "Rooftop Events & Venue Hire | KROSS PARK Bangkok"),
    "contact.html":    ("Contact", "Contact & Location | KROSS PARK Bangkok"),
}

NAV_ITEMS = [
    ("index.html", "Home"),
    ("pickleball.html", "Pickleball"),
    ("classes.html", "Classes"),
    ("training.html", "Personal Training"),
    ("events.html", "Events"),
    ("contact.html", "Contact"),
]


GA_HEAD = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-YN3RY665Y2"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-YN3RY665Y2');
</script>"""

ICONS = """<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">"""

TRACK_JS = """
document.addEventListener('click', function(e){
  var a = e.target.closest('a'); if(!a || typeof gtag !== 'function') return;
  var h = a.href || '';
  if(h.indexOf('apps.apple.com') > -1) gtag('event','app_download_click',{platform:'ios'});
  else if(h.indexOf('play.google.com') > -1) gtag('event','app_download_click',{platform:'android'});
  else if(h.indexOf('chat.whatsapp.com') > -1) gtag('event','community_join_click',{});
  else if(h.indexOf('line.me') > -1) gtag('event','contact_click',{channel:'line'});
  else if(h.indexOf('wa.me') > -1) gtag('event','contact_click',{channel:'whatsapp'});
  else if(h.indexOf('mailto:') === 0) gtag('event','contact_click',{channel:'email'});
});
var enq = document.querySelector('form.enquiry');
if(enq) enq.addEventListener('submit', function(){ if(typeof gtag === 'function') gtag('event','generate_lead',{form:'enquiry'}); });
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
<link rel="canonical" href="{'https://krosspark.club/' + ('' if page == 'index.html' else page[:-5])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KROSS PARK">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{'https://krosspark.club/' + ('' if page == 'index.html' else page[:-5])}">
<meta property="og:image" content="https://krosspark.club/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{ICONS}
{GA_HEAD}
{SCHEMA if page == 'index.html' else ''}
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<header class="site-header" id="siteHeader">
  <nav class="nav">
    <a class="logo" href="index.html"><img src="assets/img/logo-white.png" alt="KROSS PARK"></a>
    <button class="nav-toggle" aria-label="Open menu" onclick="document.getElementById('navLinks').classList.toggle('open')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <ul class="nav-links" id="navLinks">
          {nav}
          <li><a class="nav-cta" href="index.html#app">Get the App</a></li>
    </ul>
  </nav>
</header>

{body}

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
      <span>Rooftop training club, Bangkok</span>
    </div>
  </div>
</footer>

<script>
const header = document.getElementById('siteHeader');
addEventListener('scroll', () => header.classList.toggle('scrolled', scrollY > 40), {{passive:true}});
if (location.pathname.split('/').pop() !== 'index.html' && location.pathname.split('/').pop() !== '') header.classList.add('scrolled');
const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add('in')), {{threshold:.12}});
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
{TRACK_JS}
</script>
</body>
</html>
"""

import pathlib, re

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
      <a class="btn btn-solid" href="pickleball.html">Book the court</a>
      <a class="btn btn-outline" href="classes.html">Explore classes</a>
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
        <a class="btn btn-green" href="contact.html">Book your assessment</a>
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
      <!-- Netlify Forms: works automatically once deployed on Netlify. Submissions land in your Netlify dashboard and can be forwarded to email under Site settings, Forms, Notifications. -->
      <form class="enquiry" name="enquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="enquiry">
        <p style="display:none"><label>Leave this empty: <input name="bot-field"></label></p>
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
      </form>
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

for page, (label, title) in PAGES.items():
    desc = {
        "index.html": "Rooftop fitness and pickleball in Phrom Phong, Bangkok. Pickleball court, open gym, group classes, 1:1 personal training and an ice bath.",
        "pickleball.html": "Book Bangkok's rooftop pickleball court at KROSS PARK on the KROSS App. Retractable roof, coaching available, ice bath recovery.",
        "classes.html": "Group classes at KROSS PARK Bangkok: HYROX, strength, StrongHer, movement and recovery. Club membership from ฿4,000 per month or class packs.",
        "training.html": "Personal training in Phrom Phong, Bangkok. 1:1 or duo sessions in a dedicated indoor studio, assessment based coaching, plus open gym sessions.",
        "events.html": "Hire a rooftop venue in the heart of Bangkok. KROSS PARK is available for brand activations, corporate wellness, tournaments and shoots.",
        "contact.html": "Contact KROSS PARK Bangkok via LINE, WhatsApp or enquiry form. 5/9 Soi Phrom Si 1, Khlong Tan Nuea, Watthana, Bangkok 10110.",
    }[page]
    html = shell(page, title, BODIES[page], desc)
    pathlib.Path(page).write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {page} ({len(html)} bytes)")
