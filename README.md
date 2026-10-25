# BRB Multiservices — site vitrine

Site statique en HTML, CSS et JavaScript vanilla. Il n'y a ni framework ni étape de build : les fichiers s'hébergent tels quels (Netlify, OVH, o2switch…).

## Arborescence

```
/
├── index.html               Accueil
├── services.html            Services (une section par service)
├── realisations.html        Galerie avant / après
├── contact.html             Formulaire de devis + coordonnées
├── mentions-legales.html    Mentions légales + politique de confidentialité
├── merci.html               Page affichée après l'envoi du formulaire (non indexée)
├── sitemap.xml
├── robots.txt
├── site.webmanifest
├── netlify.toml             Configuration Netlify (aucun build)
├── outils/generer.py        Génère les pages HTML à partir des informations de l'entreprise
└── assets/
    ├── css/style.css        Feuille de style unique
    ├── js/main.js           Menu mobile, année du footer, pré-sélection du formulaire
    └── img/
        ├── logo/            Pack logo officiel (fichiers d'origine, non modifiés)
        └── photos/          Photos des services et des chantiers
```

## 1. Modifier les informations

Les pages HTML sont **générées** par `outils/generer.py`. Toutes les informations s'y trouvent, en haut du fichier :

- `INFOS` : nom, gérant, téléphone, email, horaires, ville, SIRET, adresse, domaine, hébergeur, médiateur ;
- `ZONE` et `ZONE_TEXTE` : communes desservies ;
- `SERVICES` : les 6 prestations (nom, icône, résumé, description, exemples) ;
- `ENGAGEMENTS` (« Pourquoi nous choisir ») et `FAQ`.

Après une modification :

```bash
python3 outils/generer.py
```

puis commitez et poussez : Netlify remet le site à jour. Ne modifiez pas les pages HTML à la main, elles seraient écrasées à la prochaine génération (le CSS et le JS, eux, se modifient directement).

Le contenu reprend celui de la page Multiservices du site de la maison mère, [Maison BRB](https://maisonbrb.fr/).

### Reste à compléter

| Élément | Où |
|---|---|
| Médiateur de la consommation (obligatoire avec une clientèle de particuliers) | `INFOS["mediateur"]` |
| Photos des prestations | voir ci-dessous |
| Chantiers avant / après : photos, titre, prestation, commune, description | fonction `realisations()` de `outils/generer.py` |

## 2. Ajouter les photos

1. Préparez des photos **au format paysage 4:3** (ex. 1200 × 900 px), en JPG ou WebP, de moins de 200 Ko chacune. Des outils gratuits comme [Squoosh](https://squoosh.app) permettent de les redimensionner et compresser.
2. Nommez-les exactement ainsi (en `.jpg` ou `.webp`) :
   - prestations : `montage-meubles`, `fixations-murales`, `petites-reparations`, `bricolage-quotidien`, `amenagement-rangement`, `aide-emmenagement` ;
   - réalisations : `chantier-1-avant`, `chantier-1-apres`, `chantier-2-avant`… jusqu'à `chantier-6-apres`.
3. Déposez-les dans `assets/img/photos/`.
4. Lancez `python3 outils/generer.py` : chaque photo présente remplace automatiquement l'image provisoire correspondante.
5. Pour les réalisations, renseignez aussi le titre, la prestation, la commune, la description et le texte `alt` des photos dans la fonction `realisations()` de `outils/generer.py`.

Si une photo n'est pas en 4:3, elle est recadrée automatiquement (`object-fit: cover`).

Une fois toutes les photos en place, les fichiers `placeholder*.svg` peuvent être supprimés.

## 3. Le logo

Les fichiers de `assets/img/logo/` sont ceux du pack officiel, copiés sans modification :

| Fichier | Usage |
|---|---|
| `logo-principal.png` | Header (fonds clairs) |
| `logo-blanc-fond-fonce.png` | Hero et footer (fonds bleu marine) |
| `logo-principal-fond-blanc.jpg` | Image de partage Open Graph |
| `icone-512.png` | JSON-LD (logo) et manifest |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon-180.png` | Favicons, déclarés dans le `<head>` de chaque page |

Les originaux font 1858 px de large et pèsent jusqu'à 760 Ko, alors qu'ils s'affichent sur moins de 320 px. Pour tenir l'objectif de performance (Lighthouse ≥ 90 sur mobile), des copies **simplement réduites** ont été ajoutées : `logo-principal-400.png`, `logo-blanc-fond-fonce-400.png` et `logo-blanc-fond-fonce-800.png`. Elles ont les mêmes proportions et les mêmes couleurs ; le navigateur choisit la bonne taille via `srcset`, et l'original reste dans `src`. Pour ne servir que les originaux, supprimez les attributs `srcset` et `sizes` des balises `<img>` du logo (le score de performance mobile descend alors vers 70).

La hauteur du logo est fixée en CSS (variable `--logo-h` dans `style.css`).

## 4. Le formulaire de contact

Sur Netlify, le formulaire fonctionne sans configuration : l'attribut `data-netlify="true"` est détecté au déploiement.

1. Dans Netlify : **Site configuration > Forms**, activez la détection des formulaires si elle est désactivée, puis redéployez.
2. **Forms > Form notifications > Add notification > Email notification** : indiquez l'adresse qui doit recevoir les demandes.
3. Les messages sont aussi consultables dans l'onglet **Forms**. Un champ piège (`bot-field`) filtre une partie des robots.

Après l'envoi, le visiteur arrive sur `merci.html`.

Hors Netlify (OVH, o2switch…), Netlify Forms ne fonctionne pas : un **fallback `mailto:`** est documenté en commentaire juste au-dessus du `<form>` dans `contact.html`. Il ouvre la messagerie du visiteur, ce qui est moins fiable ; chez ces hébergeurs, préférez un petit script PHP d'envoi ou un service comme Formspree.

Le lien « Demander un devis » de chaque service ouvre `contact.html?besoin=service-N`, ce qui pré-sélectionne le type de besoin.

## 5. Mettre le site en ligne sur Netlify

**Option A — glisser-déposer (le plus simple)**

1. Créez un compte gratuit sur [netlify.com](https://www.netlify.com).
2. Allez dans **Sites > Add new site > Deploy manually**.
3. Glissez-déposez le **dossier du site entier** (celui qui contient `index.html`).
4. Le site est en ligne en quelques secondes sur une adresse du type `nom-aleatoire.netlify.app`.
5. Pour une mise à jour, glissez-déposez de nouveau le dossier dans l'onglet **Deploys**.

**Option B — depuis GitHub (mises à jour automatiques)**

1. **Add new site > Import an existing project > GitHub**, puis choisissez ce dépôt.
2. Laissez la commande de build **vide** et le dossier de publication à `.` (c'est déjà ce que dit `netlify.toml`).
3. Chaque modification poussée sur la branche principale met le site à jour.

**Nom de domaine**

1. **Domain management > Add a domain** : saisissez `brbmultiservices.fr` et choisissez-le comme domaine principal (Netlify redirigera `www.brbmultiservices.fr` vers lui).
2. Suivez les instructions DNS de Netlify chez votre registrar (OVH, Gandi…). Le certificat HTTPS est automatique.
3. Remplacez le domaine provisoire dans les fichiers (voir plus haut), puis redéployez.

**Après la mise en ligne**

- Déclarez le site dans [Google Search Console](https://search.google.com/search-console) et soumettez `https://votre-domaine/sitemap.xml`.
- Créez ou mettez à jour votre fiche **Google Business Profile** avec le même nom, téléphone et adresse que sur le site : c'est le levier principal du référencement local.
- Vérifiez les données structurées avec le [test des résultats enrichis](https://search.google.com/test/rich-results).

## 6. Notes techniques

- **Couleurs** : marine `#102A4D`, orange `#E8711A`, orange texte `#C45508` (petit texte sur fond **blanc** uniquement : sur le blanc cassé `#F6F4F0`, son contraste passe sous le seuil AA), orange clair `#F28C38` (texte sur fond marine). Les boutons orange portent un texte marine (contraste 4,6:1) : du texte blanc sur cet orange ne passerait pas le seuil AA.
- **Police** : Archivo via Google Fonts. Pour éviter tout transfert vers Google (RGPD), vous pouvez héberger la police vous-même : téléchargez les fichiers `.woff2` (par exemple avec [google-webfonts-helper](https://gwfh.mranftl.com/fonts/archivo)), placez-les dans `assets/fonts/`, déclarez-les avec `@font-face` en haut de `style.css`, puis supprimez les trois balises Google Fonts du `<head>` de chaque page et le paragraphe correspondant dans la politique de confidentialité.
- **Header et footer** sont communs à toutes les pages et définis une seule fois dans `outils/generer.py` (fonctions `header()` et `footer()`).
- **Sans JavaScript**, le menu reste accessible (il s'affiche sous le logo) et le formulaire fonctionne.
- Scores Lighthouse mesurés en local (mobile, sans compression serveur) : performance 92 à 95, accessibilité 100, bonnes pratiques 100, SEO 100. Une fois les vraies photos ajoutées, vérifiez qu'elles restent légères.
