#!/usr/bin/env python3
"""Génère les pages HTML du site BRB Multiservices.

Toutes les informations (coordonnées, zone, prestations, textes) se modifient
dans les constantes ci-dessous, puis :
    python3 outils/generer.py
Les pages sont écrites à la racine du dépôt. Le site reste 100 % statique :
ce script n'est pas nécessaire à l'hébergement, seulement pour mettre à jour.
"""
import json
from html import escape
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Informations de l'entreprise
# ---------------------------------------------------------------------------
INFOS = {
    "nom": "BRB Multiservices",
    "gerant": "Mathis",                 # affiché sur le site
    "gerant_complet": "Mathis Bordes",  # mentions légales
    "tel": "07 81 78 73 60",
    "tel_intl": "+33781787360",
    "email": "contact.brbmultiservices@gmail.com",
    "horaires": "Du lundi au samedi, de 8 h à 19 h",
    "horaires_court": "Lun – sam, 8 h – 19 h",
    "ville": "Beaucaire",
    "cp": "30300",
    "siret": "981 177 272 00029",
    "adresse_siege": "59 rue de Ponthieu, bureau 326, 75008 Paris",
    "domaine": "https://brbmultiservices.fr",
    "maison": "Maison BRB",
    "maison_url": "https://maisonbrb.fr/",
    "hebergeur": "Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis",
    "hebergeur_site": "https://www.netlify.com",
    "mediateur": None,  # médiateur de la consommation : nom, adresse, site web
}

# La première commune est mise en avant.
ZONE = [
    "Beaucaire", "Tarascon", "Fourques", "Vallabrègues", "Jonquières-Saint-Vincent",
    "Comps", "Bellegarde", "Aramon", "Montfrin", "Meynes", "Redessan", "Manduel",
    "Boulbon", "Saint-Étienne-du-Grès", "Arles", "Nîmes",
]
ZONE_TEXTE = ("Basés à Beaucaire (30300), nous nous déplaçons dans le Gard et les Bouches-du-Rhône "
              "voisines, entre Nîmes, Arles et Tarascon, dans un rayon d'environ 30 km.")
GEO = {"latitude": 43.8083, "longitude": 4.6436}

# Icônes en trait (24 × 24)
I = {
    "meuble": '<rect x="4" y="3" width="16" height="15" rx="1"/><path d="M12 3v15M9.5 9.5v2M14.5 9.5v2M6 18v3M18 18v3"/>',
    "tv": '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4"/>',
    "outil": '<path d="M14 4l6 6"/><path d="M11 7l6 6-2 2-6-6z"/><path d="M10 10l-6.5 6.5a1.5 1.5 0 0 0 0 2.1l1.9 1.9a1.5 1.5 0 0 0 2.1 0L14 14"/>',
    "niveau": '<rect x="2" y="8" width="20" height="8" rx="4"/><circle cx="12" cy="12" r="2"/><path d="M7 8V5M17 8V5"/>',
    "etagere": '<path d="M4 3v18M20 3v18M4 9h16M4 15h16"/><rect x="7" y="5" width="3" height="4"/><rect x="13" y="11" width="4" height="4"/>',
    "carton": '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "tel": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "horloge": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "perso": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    "devis": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="M9 12l2 2 4-4"/>',
    "bouclier": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "balai": '<path d="M14 3l-4 9"/><path d="M7 12h8l2 9H5z"/><path d="M9 16v5M13 16v5"/>',
}


def svg(nom, cls="", sw="2"):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[nom]}</svg>')


# Prestations : (identifiant, nom, icône, résumé, détails, exemples)
SERVICES = [
    ("montage-meubles", "Montage de meubles", "meuble",
     "Armoires, lits, meubles en kit, bureaux, dressings : montage soigné, réglé et fixé au mur si nécessaire.",
     "Vous avez reçu un meuble en kit et n'avez ni le temps ni l'outillage pour le monter ? Nous le montons "
     "proprement, en suivant la notice, puis nous réglons portes et tiroirs. Les meubles hauts sont fixés au mur "
     "pour plus de sécurité.",
     ["Armoires, commodes et meubles en kit", "Lits, bureaux et dressings", "Réglage des portes et tiroirs",
      "Fixation au mur des meubles hauts"]),
    ("fixations-murales", "Fixations murales", "tv",
     "Étagères, tringles à rideaux, supports TV, miroirs, cadres : perçage adapté à votre mur, niveau et solidité vérifiés.",
     "Placo, brique, béton : chaque mur demande ses propres chevilles. Nous choisissons la fixation adaptée au "
     "support et au poids, et vérifions le niveau pour un résultat droit et solide.",
     ["Étagères et tringles à rideaux", "Supports TV", "Miroirs, cadres et tableaux", "Choix des chevilles selon le mur"]),
    ("petites-reparations", "Petites réparations", "outil",
     "Porte qui frotte, poignée ou charnière cassée, joint silicone à reprendre : les petits ajustements du quotidien.",
     "Ces petits défauts qu'on finit par ne plus voir mais qui gênent tous les jours. Nous intervenons "
     "rapidement pour les remettre en état.",
     ["Porte qui frotte ou ferme mal", "Poignée ou charnière cassée", "Joint silicone à reprendre"]),
    ("bricolage-quotidien", "Bricolage du quotidien", "niveau",
     "Les petites interventions qui facilitent la vie : remplacement d'accessoires, réglages, petits travaux d'entretien.",
     "Pour toutes les petites tâches de la maison que vous repoussez depuis des semaines, un coup de main "
     "ponctuel, efficace et soigné.",
     ["Remplacement d'accessoires", "Réglages divers", "Petits travaux d'entretien"]),
    ("amenagement-rangement", "Aménagement et rangement", "etagere",
     "Installation de rangements, patères, crochets et accessoires pour optimiser vos espaces.",
     "Entrée, placard, garage ou buanderie : nous installons les rangements et accessoires qui vous font "
     "gagner de la place au quotidien.",
     ["Installation de rangements", "Patères et crochets", "Accessoires pour optimiser l'espace"]),
    ("aide-emmenagement", "Aide à l'emménagement", "carton",
     "Montage de meubles et fixations pour vous installer sereinement dans votre nouveau logement.",
     "Un déménagement laisse souvent une longue liste de choses à monter et à fixer. Nous nous en chargeons "
     "pour que vous profitiez vite de votre nouveau logement.",
     ["Montage des meubles", "Pose des étagères, tringles et supports TV", "Petits réglages d'installation"]),
]

ENGAGEMENTS = [
    ("devis", "Devis clair", "Vous décrivez le besoin, avec une photo si possible, et recevez un devis précis avant toute intervention."),
    ("horloge", "Ponctualité", "Un créneau convenu ensemble et respecté. Vous êtes prévenu en cas d'imprévu."),
    ("bouclier", "Travail soigné", "Le bon outillage et les bonnes fixations pour un résultat solide et durable."),
    ("balai", "Lieux propres", "Protection des sols, nettoyage en fin d'intervention et emballages emportés sur demande."),
]

FAQ = [
    ("Intervenez-vous pour les petits travaux à Beaucaire et aux alentours ?",
     "Oui. BRB Multiservices intervient à Beaucaire, Tarascon, Vallabrègues, Comps, Aramon, Montfrin, Nîmes, Arles et dans les communes voisines."),
    ("Quels types de travaux réalisez-vous ?",
     "Des petits travaux de bricolage : montage de meubles, fixations murales, petites réparations du quotidien, aménagements de rangement."),
    ("Faites-vous des travaux de rénovation, d'électricité ou de plomberie ?",
     "Non. BRB Multiservices se consacre aux petits travaux de bricolage. Pour la rénovation, la maçonnerie, l'électricité ou la plomberie, faites appel à un artisan qualifié du bâtiment."),
    ("Pouvez-vous fixer une télévision au mur ?",
     "Oui. Nous posons votre support TV en choisissant les chevilles adaptées à votre mur, avec un résultat de niveau et solide."),
    ("Le devis est-il gratuit ?",
     "Oui, le devis est gratuit et sans engagement. Une photo de ce qu'il y a à faire permet souvent de vous répondre plus vite."),
]

MANQUANT = "[à compléter]"
CURRENT = ' aria-current="page"'
MAIN = ' class="is-main"'
NL = "\n"
T = INFOS
TEL = f'tel:{T["tel_intl"]}'
MAIL = f'mailto:{T["email"]}'
# Retour à la ligne possible après « @ » pour les écrans étroits
EMAIL_HTML = escape(T["email"]).replace("@", "@<wbr>")
DOM = T["domaine"].rstrip("/")


def url(page):
    return DOM + "/" + ("" if page == "index.html" else page)


def asset(chemin):
    return DOM + "/assets/" + chemin


def photo(nom, defaut):
    """Chemin de assets/img/photos/<nom>.jpg (ou .webp) s'il existe, sinon l'image provisoire."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        if (RACINE / "assets/img/photos" / f"{nom}.{ext}").exists():
            return f"assets/img/photos/{nom}.{ext}"
    return f"assets/img/photos/{defaut}"


def ld(obj):
    return ('  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2) + '\n  </script>\n')


def entreprise_ld():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": url("index.html") + "#entreprise",
        "name": T["nom"],
        "description": "Petits travaux de bricolage à Beaucaire : " + ", ".join(s[1].lower() for s in SERVICES) + ".",
        "url": url("index.html"),
        "logo": asset("img/logo/icone-512.png"),
        "image": asset("img/logo/logo-principal-fond-blanc.jpg"),
        "telephone": T["tel_intl"],
        "email": T["email"],
        "address": {"@type": "PostalAddress", "addressLocality": T["ville"], "postalCode": T["cp"],
                    "addressRegion": "Occitanie", "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", **GEO},
        "areaServed": [{"@type": "City", "name": v} for v in ZONE],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "08:00", "closes": "19:00",
        }],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Prestations " + T["nom"],
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
        },
        "parentOrganization": {"@type": "Organization", "name": T["maison"], "url": T["maison_url"]},
    }


def faq_ld():
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ],
    }


# ---------------------------------------------------------------------------
# Gabarit commun
# ---------------------------------------------------------------------------
NAV = [("index.html", "Accueil"), ("services.html", "Services"),
       ("realisations.html", "Réalisations"), ("contact.html", "Contact")]


def head(page, titre, desc, extra="", robots=None):
    rob = f'\n  <meta name="robots" content="{robots}">' if robots else ""
    t, d = escape(titre), escape(desc)
    return f'''<!doctype html>
<html lang="fr" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.className = 'js';</script>

  <title>{t}</title>
  <meta name="description" content="{d}">{rob}
  <link rel="canonical" href="{url(page)}">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="{T["nom"]}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url(page)}">
  <meta property="og:image" content="{asset("img/logo/logo-principal-fond-blanc.jpg")}">
  <meta property="og:image:width" content="1858">
  <meta property="og:image:height" content="545">
  <meta property="og:image:alt" content="Logo BRB Multiservices">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="assets/img/logo/favicon.ico" sizes="any">
  <link rel="icon" href="assets/img/logo/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/img/logo/apple-touch-icon-180.png">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#102A4D">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&display=swap">
  <link rel="stylesheet" href="assets/css/style.css">
  <script src="assets/js/main.js" defer></script>
{extra}</head>
<body>
'''


def header(page):
    items = "\n".join(
        f'          <li><a href="{p}"{CURRENT if p == page else ""}>{label}</a></li>'
        for p, label in NAV)
    return f'''  <a class="skip-link" href="#contenu">Aller au contenu</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html">
        <img src="assets/img/logo/logo-principal.png" srcset="assets/img/logo/logo-principal-400.png 400w, assets/img/logo/logo-principal.png 1858w" sizes="(min-width: 960px) 171px, 137px" width="1858" height="545" alt="BRB Multiservices — retour à l'accueil" fetchpriority="high">
      </a>
      <a class="btn btn--primary header-phone" href="{TEL}" aria-label="Appeler BRB Multiservices au {T["tel"]}">
        {svg("tel", sw="2.2")}
        <span class="label-long">{T["tel"]}</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
      <nav class="site-nav" id="site-nav" aria-label="Navigation principale">
        <ul>
{items}
        </ul>
      </nav>
    </div>
  </header>
'''


def footer():
    return f'''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <img class="footer-logo" src="assets/img/logo/logo-blanc-fond-fonce.png" srcset="assets/img/logo/logo-blanc-fond-fonce-400.png 400w, assets/img/logo/logo-blanc-fond-fonce.png 1858w" sizes="191px" width="1858" height="545" alt="BRB Multiservices" loading="lazy">
          <p>Petits travaux de bricolage à Beaucaire et dans un rayon d'environ 30 km : montage de meubles, fixations murales, petites réparations.</p>
          <p>Une activité de <a href="{T["maison_url"]}">{T["maison"]}</a>.</p>
        </div>
        <div>
          <h2 class="footer-title">Coordonnées</h2>
          <ul class="footer-list">
            <li><span class="k">Tél. :</span> <a href="{TEL}">{T["tel"]}</a></li>
            <li><span class="k">Email :</span> <a href="{MAIL}">{EMAIL_HTML}</a></li>
            <li><span class="k">Zone :</span> {T["ville"]} et alentours</li>
            <li><span class="k">Horaires :</span> {T["horaires_court"]}</li>
          </ul>
        </div>
        <nav aria-label="Liens du pied de page">
          <h2 class="footer-title">Navigation</h2>
          <ul class="footer-list">
            <li><a href="services.html">Services</a></li>
            <li><a href="realisations.html">Réalisations</a></li>
            <li><a href="contact.html">Contact et devis</a></li>
          </ul>
        </nav>
      </div>
      <div class="footer-bottom">
        <p>© <span data-year>2026</span> {T["nom"]} · {T["gerant_complet"]} EI · SIRET {T["siret"]}</p>
        <ul>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="mentions-legales.html#confidentialite">Politique de confidentialité</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <a class="btn btn--primary call-fab" href="{TEL}">
    {svg("tel", sw="2.2")}
    Appeler BRB Multiservices
  </a>
</body>
</html>
'''


def page_hero(h1, intro):
    return f'''    <section class="page-hero on-dark">
      <div class="container">
        <span class="level" aria-hidden="true"></span>
        <h1>{h1}</h1>
        <p>{intro}</p>
      </div>
    </section>
'''


def cta(titre, texte):
    return f'''    <section class="cta-band" aria-labelledby="cta-title">
      <div class="container cta-inner">
        <div>
          <span class="level level--on-orange" aria-hidden="true"></span>
          <h2 id="cta-title">{titre}</h2>
          <p>{texte}</p>
        </div>
        <div class="btn-row">
          <a class="btn btn--navy" href="{TEL}">Appeler</a>
          <a class="btn btn--outline" href="contact.html">Demander un devis</a>
        </div>
      </div>
    </section>
'''


def write(page, titre, desc, main, extra="", robots=None):
    html = head(page, titre, desc, extra, robots) + header(page) + '\n  <main id="contenu">\n' + main + '  </main>\n\n' + footer()
    (RACINE / page).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
def accueil():
    cartes = "".join(f'''          <li class="card">
            <span class="icon-box" aria-hidden="true">
              {svg(ic)}
            </span>
            <h3>{nom}</h3>
            <p>{resume}</p>
            <a class="card-link" href="services.html#{sid}">En savoir plus<span class="visually-hidden"> : {nom}</span><span aria-hidden="true"> →</span></a>
          </li>
''' for sid, nom, ic, resume, _, _ in SERVICES)

    engagements = "".join(f'''          <li class="feature">
            {svg(ic, "icon-line", "1.8")}
            <h3>{titre}</h3>
            <p>{texte}</p>
          </li>
''' for ic, titre, texte in ENGAGEMENTS)

    communes = "".join(f'            <li{MAIN if i == 0 else ""}>{v}</li>\n' for i, v in enumerate(ZONE))

    main = f'''
    <!-- HERO -->
    <section class="hero on-dark" aria-labelledby="hero-title">
      <div class="container hero-grid">
        <div>
          <img class="hero-logo" src="assets/img/logo/logo-blanc-fond-fonce.png" srcset="assets/img/logo/logo-blanc-fond-fonce-400.png 400w, assets/img/logo/logo-blanc-fond-fonce-800.png 800w, assets/img/logo/logo-blanc-fond-fonce.png 1858w" sizes="(min-width: 960px) 314px, 219px" width="1858" height="545" alt="BRB Multiservices">
          <h1 id="hero-title">Vos petits travaux de bricolage à Beaucaire, faits avec soin.</h1>
          <p class="hero-lead">Les petites tâches de la maison confiées à quelqu'un de soigneux, qui arrive à l'heure et laisse les lieux propres.</p>
          <p class="hero-zone">
            {svg("pin")}
            Beaucaire et alentours, dans un rayon d'environ 30 km
          </p>
          <div class="btn-row">
            <a class="btn btn--primary" href="{TEL}">
              {svg("tel", sw="2.2")}
              Appeler
            </a>
            <a class="btn btn--outline-light" href="contact.html">Demander un devis</a>
          </div>
        </div>

        <aside class="hero-card" aria-labelledby="hero-card-title">
          <h2 id="hero-card-title">Contact direct</h2>
          <ul class="info-list">
            <li>
              {svg("tel")}
              <div><span class="k">Téléphone</span><a class="v" href="{TEL}">{T["tel"]}</a></div>
            </li>
            <li>
              {svg("mail")}
              <div><span class="k">Email</span><a class="v" href="{MAIL}">{EMAIL_HTML}</a></div>
            </li>
            <li>
              {svg("horloge")}
              <div><span class="k">Horaires</span><span class="v">{T["horaires"]}</span></div>
            </li>
            <li>
              {svg("perso")}
              <div><span class="k">Votre interlocuteur</span><span class="v">{T["gerant"]}</span></div>
            </li>
          </ul>
        </aside>
      </div>
    </section>

    <!-- SERVICES -->
    <section class="section" aria-labelledby="services-title">
      <div class="container">
        <div class="section-head">
          <span class="level" aria-hidden="true"></span>
          <h2 id="services-title">Nos prestations</h2>
          <p>Ces petits travaux qu'on repousse depuis des semaines, réalisés proprement et rapidement.</p>
        </div>

        <ul class="cards cards--3">
{cartes}        </ul>
      </div>
    </section>

    <!-- POURQUOI NOUS CHOISIR -->
    <section class="section section--alt" aria-labelledby="why-title">
      <div class="container">
        <div class="section-head">
          <span class="level" aria-hidden="true"></span>
          <h2 id="why-title">Pourquoi nous choisir</h2>
          <p>Pour les petits travaux, la confiance compte autant que le geste. Voici nos engagements.</p>
        </div>

        <ul class="features features--4">
{engagements}        </ul>
      </div>
    </section>

    <!-- ZONE D'INTERVENTION -->
    <section class="section" aria-labelledby="zone-title">
      <div class="container zone-grid">
        <div>
          <span class="level" aria-hidden="true"></span>
          <h2 id="zone-title">Zone d'intervention</h2>
          <p class="lead">{ZONE_TEXTE}</p>
          <p>Votre commune n'apparaît pas dans la liste ? Appelez-nous, nous trouverons une solution.</p>
          <a class="btn btn--navy" href="{TEL}">Appeler le {T["tel"]}</a>
        </div>
        <div class="zone-box">
          <h3>Communes desservies</h3>
          <ul class="chips">
{communes}          </ul>
        </div>
      </div>
    </section>

''' + cta("Un meuble à monter, une étagère à poser ?",
          "Devis gratuit et sans engagement. Une photo de ce qu'il y a à faire permet souvent de vous répondre plus vite.")

    write("index.html",
          "BRB Multiservices — Petits travaux de bricolage et montage de meubles à Beaucaire",
          f"BRB Multiservices, petits travaux de bricolage à Beaucaire : montage de meubles, fixations murales, "
          f"petites réparations. Tarascon, Arles, Nîmes. Devis gratuit au {T['tel']}.",
          main, ld(entreprise_ld()))


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
def services():
    blocs = "".join(f'''        <article class="service-block" id="{sid}" aria-labelledby="{sid}-title">
          <div>
            <span class="icon-box" aria-hidden="true">
              {svg(ic)}
            </span>
            <h2 id="{sid}-title">{nom}</h2>
            <p class="lead">{resume}</p>
            <p>{details}</p>
            <ul class="check-list">
{"".join(f"              <li>{x}</li>" + NL for x in exemples)}            </ul>
            <a class="btn btn--primary" href="contact.html?besoin={sid}">Demander un devis<span class="visually-hidden"> : {nom}</span></a>
          </div>
          <figure class="photo service-media">
            <img src="{photo(sid, "placeholder.svg")}" width="1200" height="900" loading="lazy" decoding="async" alt="{nom} par BRB Multiservices à Beaucaire">
          </figure>
        </article>
''' for sid, nom, ic, resume, details, exemples in SERVICES)

    faq = "".join(f'''          <details class="faq-item">
            <summary>{q}</summary>
            <p>{r}</p>
          </details>
''' for q, r in FAQ)

    main = page_hero("Petits travaux de bricolage à Beaucaire et alentours",
                     "Montage de meubles, fixations murales, petites réparations : les petites tâches de la maison, réalisées proprement.") + f'''
    <section class="section" aria-label="Détail des prestations">
      <div class="container">
{blocs}      </div>
    </section>

    <section class="section section--alt" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <span class="level" aria-hidden="true"></span>
          <h2 id="faq-title">Questions fréquentes</h2>
        </div>
        <div class="faq">
{faq}        </div>
      </div>
    </section>

''' + cta("Besoin d'un coup de main ?",
          "Décrivez-nous ce qu'il y a à faire : devis gratuit et sans engagement.")

    write("services.html",
          "Montage de meubles, fixations murales, petites réparations à Beaucaire | BRB Multiservices",
          "Les prestations de BRB Multiservices à Beaucaire, Tarascon, Arles et Nîmes : montage de meubles, "
          "fixations murales et supports TV, petites réparations, rangements, aide à l'emménagement.",
          main, ld(faq_ld()))


# ---------------------------------------------------------------------------
# Réalisations
# ---------------------------------------------------------------------------
def realisations():
    projets = "".join(f'''          <li>
            <figure class="project">
              <div class="ba">
                <div class="ba-item">
                  <img src="{photo(f'chantier-{i}-avant', 'placeholder-avant.svg')}" width="1200" height="900" loading="lazy" decoding="async" alt="[Chantier {i} avant : description]">
                  <span class="ba-label ba-label--before">Avant</span>
                </div>
                <div class="ba-item">
                  <img src="{photo(f'chantier-{i}-apres', 'placeholder-apres.svg')}" width="1200" height="900" loading="lazy" decoding="async" alt="[Chantier {i} après : description]">
                  <span class="ba-label ba-label--after">Après</span>
                </div>
              </div>
              <figcaption>
                <h2>[Titre du chantier {i}]</h2>
                <p class="meta">[Prestation] — [Commune]</p>
                <p>[Une ou deux phrases sur le chantier : la demande du client, ce qui a été réalisé.]</p>
              </figcaption>
            </figure>
          </li>
''' for i in range(1, 7))

    main = page_hero("Nos réalisations à Beaucaire et alentours",
                     "Quelques interventions de BRB Multiservices, en avant / après.") + f'''
    <section class="section" aria-label="Galerie d'interventions avant et après">
      <div class="container">
        <ul class="gallery">
{projets}        </ul>
      </div>
    </section>

''' + cta("Votre projet est le prochain ?", "Parlez-nous de ce qu'il y a à faire : devis gratuit et sans engagement.")

    write("realisations.html",
          "Réalisations avant / après à Beaucaire — montage de meubles, fixations | BRB Multiservices",
          "Photos avant / après des interventions de BRB Multiservices à Beaucaire et alentours : montage de meubles, "
          "fixations murales, petites réparations, rangements.",
          main)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def contact():
    options = "".join(f'                  <option value="{sid}">{nom}</option>\n' for sid, nom, *_ in SERVICES)
    main = page_hero("Contact et devis gratuit à Beaucaire",
                     "Appelez-nous ou décrivez votre besoin dans le formulaire : réponse rapide, devis gratuit et sans engagement.") + f'''
    <section class="section" aria-label="Formulaire et coordonnées">
      <div class="container contact-grid">
        <div>
          <h2>Demander un devis</h2>
          <p class="form-note">Les champs marqués d'un <span class="req" aria-hidden="true">*</span> sont obligatoires.</p>

          <!--
            Formulaire compatible Netlify Forms : Netlify détecte automatiquement
            l'attribut data-netlify au déploiement et vous envoie les messages par email
            (Netlify > Site > Forms > Form notifications).

            FALLBACK MAILTO (hébergement hors Netlify : OVH, o2switch…) :
            remplacez la balise <form …> ci-dessous par :
              <form class="form" action="mailto:{T["email"]}" method="post" enctype="text/plain">
            et supprimez le champ caché "form-name" et le champ anti-spam "bot-field".
            Le mailto ouvre la messagerie du visiteur : moins fiable, à n'utiliser qu'en dépannage.
          -->
          <form class="form mt-2" name="contact" method="POST" action="merci.html" data-netlify="true" netlify-honeypot="bot-field">
            <input type="hidden" name="form-name" value="contact">
            <p class="hp-field">
              <label>Ne pas remplir ce champ : <input name="bot-field" tabindex="-1" autocomplete="off"></label>
            </p>

            <div class="form-row form-row--2">
              <div class="field">
                <label for="nom">Nom <span class="req" aria-hidden="true">*</span></label>
                <input id="nom" name="nom" type="text" autocomplete="name" required aria-required="true">
              </div>
              <div class="field">
                <label for="telephone">Téléphone <span class="req" aria-hidden="true">*</span></label>
                <input id="telephone" name="telephone" type="tel" autocomplete="tel" inputmode="tel" required aria-required="true">
              </div>
            </div>

            <div class="form-row form-row--2">
              <div class="field">
                <label for="email">Email <span class="hint-inline">(facultatif)</span></label>
                <input id="email" name="email" type="email" autocomplete="email">
              </div>
              <div class="field">
                <label for="besoin">Type de besoin <span class="req" aria-hidden="true">*</span></label>
                <select id="besoin" name="besoin" required aria-required="true">
                  <option value="">Choisissez…</option>
{options}                  <option value="autre">Autre demande</option>
                </select>
              </div>
            </div>

            <div class="field">
              <label for="message">Votre message <span class="req" aria-hidden="true">*</span>
                <span class="hint">Décrivez ce qu'il y a à faire, la commune et vos disponibilités. Vous pourrez nous envoyer une photo par SMS ou par email.</span>
              </label>
              <textarea id="message" name="message" rows="6" required aria-required="true"></textarea>
            </div>

            <p class="form-note">Vos informations servent uniquement à répondre à votre demande. Voir notre <a href="mentions-legales.html#confidentialite">politique de confidentialité</a>.</p>

            <div>
              <button class="btn btn--primary" type="submit">Envoyer ma demande</button>
            </div>
          </form>
        </div>

        <aside class="contact-aside on-dark" aria-labelledby="direct-title">
          <h2 id="direct-title">Contact direct</h2>
          <a class="btn btn--primary" href="{TEL}">{svg("tel", sw="2.2")} Appeler le {T["tel"]}</a>
          <ul class="info-list">
            <li>
              {svg("mail")}
              <div><span class="k">Email</span><a class="v" href="{MAIL}">{EMAIL_HTML}</a></div>
            </li>
            <li>
              {svg("pin")}
              <div><span class="k">Zone d'intervention</span><span class="v">{T["ville"]} et alentours (environ 30 km)</span><span class="k">{", ".join(ZONE[1:])}</span></div>
            </li>
            <li>
              {svg("horloge")}
              <div><span class="k">Horaires</span><span class="v">{T["horaires"]}</span></div>
            </li>
          </ul>
        </aside>
      </div>
    </section>

'''
    write("contact.html",
          "Contact et devis gratuit — petits travaux à Beaucaire | BRB Multiservices",
          f"Contactez BRB Multiservices à Beaucaire pour vos petits travaux de bricolage : appelez le {T['tel']} "
          f"ou demandez votre devis gratuit en ligne.",
          main)


def merci():
    main = page_hero("Merci, votre demande est envoyée",
                     "Nous revenons vers vous rapidement. Pour une demande urgente, appelez-nous directement.") + f'''
    <section class="section">
      <div class="container">
        <div class="btn-row">
          <a class="btn btn--primary" href="{TEL}">Appeler le {T["tel"]}</a>
          <a class="btn btn--outline" href="index.html">Retour à l'accueil</a>
        </div>
      </div>
    </section>

'''
    write("merci.html", "Demande envoyée | BRB Multiservices",
          "Votre demande a bien été envoyée à BRB Multiservices.", main, robots="noindex")


# ---------------------------------------------------------------------------
# Mentions légales
# ---------------------------------------------------------------------------
def mentions():
    med = T["mediateur"] or MANQUANT
    main = page_hero("Mentions légales et politique de confidentialité",
                     "Informations légales relatives au site de BRB Multiservices, petits travaux de bricolage à Beaucaire.") + f'''
    <section class="section">
      <div class="container prose">
        <nav class="toc" aria-label="Sommaire">
          <p>Sommaire</p>
          <ul>
            <li><a href="#editeur">Éditeur</a></li>
            <li><a href="#hebergeur">Hébergeur</a></li>
            <li><a href="#propriete">Propriété intellectuelle</a></li>
            <li><a href="#mediation">Médiation</a></li>
            <li><a href="#confidentialite">Confidentialité</a></li>
            <li><a href="#cookies">Cookies</a></li>
          </ul>
        </nav>

        <h2 id="editeur">Éditeur du site</h2>
        <p>Le présent site est édité par {T["gerant_complet"]}, entrepreneur individuel (EI), exerçant sous le nom commercial {T["maison"]} et sous l'enseigne {T["nom"]}.</p>
        <dl>
          <dt>Adresse</dt><dd>{T["adresse_siege"]}</dd>
          <dt>SIRET</dt><dd>{T["siret"]}</dd>
          <dt>Téléphone</dt><dd><a href="{TEL}">{T["tel"]}</a></dd>
          <dt>Email</dt><dd><a href="{MAIL}">{EMAIL_HTML}</a></dd>
          <dt>Directeur de la publication</dt><dd>{T["gerant_complet"]}</dd>
        </dl>

        <h2 id="hebergeur">Hébergeur</h2>
        <p>Le site est hébergé par {T["hebergeur"]} (<a href="{T["hebergeur_site"]}">{T["hebergeur_site"].replace("https://", "")}</a>).</p>

        <h2 id="propriete">Propriété intellectuelle</h2>
        <p>L'ensemble des contenus de ce site (textes, logo, photographies, mise en page) est la propriété exclusive de {T["maison"]}, sauf mention contraire. Toute reproduction, représentation ou adaptation, totale ou partielle, sans autorisation écrite préalable est interdite.</p>

        <h2>Responsabilité</h2>
        <p>Les informations présentées sur ce site sont fournies à titre indicatif et peuvent évoluer. Seul le devis remis avant chaque intervention fait foi quant au contenu et au prix des prestations.</p>

        <h2 id="mediation">Médiation de la consommation</h2>
        <p>Conformément aux articles L.611-1 et suivants du Code de la consommation, en cas de litige non résolu à l'amiable, le client consommateur peut recourir gratuitement au médiateur de la consommation suivant : {med}.</p>

        <h2 id="confidentialite">Politique de confidentialité</h2>

        <h3>Responsable du traitement</h3>
        <p>{T["gerant_complet"]} (EI), {T["adresse_siege"]}, <a href="{MAIL}">{EMAIL_HTML}</a>.</p>

        <h3>Données collectées</h3>
        <p>Le site ne collecte des données personnelles que lorsque vous remplissez le formulaire de contact : nom, téléphone, email (facultatif), type de besoin et contenu de votre message. Les informations transmises par téléphone ou par email sont traitées de la même façon.</p>

        <h3>Finalité et base légale</h3>
        <p>Ces données servent uniquement à répondre à votre demande, établir un devis et réaliser la prestation. Le traitement repose sur les mesures précontractuelles prises à votre demande (article 6.1.b du RGPD).</p>

        <h3>Destinataires</h3>
        <p>Vos données sont destinées exclusivement à {T["nom"]}. Elles ne sont ni vendues, ni cédées, ni louées. Les messages du formulaire transitent par l'hébergeur du site, Netlify, qui agit en qualité de sous-traitant. Netlify étant établi aux États-Unis, ce transfert est encadré par les clauses contractuelles types de la Commission européenne.</p>

        <h3>Durée de conservation</h3>
        <p>Les demandes sans suite sont conservées 3 ans au maximum à compter du dernier contact. Les données des clients sont conservées pendant la durée de la relation commerciale, puis archivées selon les obligations légales (comptables notamment).</p>

        <h3>Vos droits</h3>
        <p>Conformément au RGPD et à la loi « Informatique et libertés », vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données. Pour les exercer, écrivez à <a href="{MAIL}">{EMAIL_HTML}</a> ou appelez le <a href="{TEL}">{T["tel"]}</a>. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL (<a href="https://www.cnil.fr">www.cnil.fr</a>).</p>

        <h3 id="cookies">Cookies et services tiers</h3>
        <p>Ce site ne dépose aucun cookie publicitaire ni de mesure d'audience. Il ne dépose donc pas de cookie nécessitant votre consentement.</p>
        <p>Les polices de caractères sont chargées depuis le service Google Fonts, ce qui implique la transmission de votre adresse IP à Google lors de l'affichage des pages.</p>

        <p><em>Dernière mise à jour : 25 octobre 2026.</em></p>
      </div>
    </section>

'''
    write("mentions-legales.html",
          "Mentions légales et confidentialité | BRB Multiservices, Beaucaire",
          "Mentions légales, éditeur, hébergeur et politique de confidentialité du site de BRB Multiservices, "
          "petits travaux de bricolage à Beaucaire.",
          main)


if __name__ == "__main__":
    accueil()
    services()
    realisations()
    contact()
    merci()
    mentions()
    print("Pages générées.")
