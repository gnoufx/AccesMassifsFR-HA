# 🌲🔥 Accès Massifs Forestiers France

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.5.0+-blue.svg)](https://www.home-assistant.io)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](https://github.com/acces-massifs-fr-ha)

Intégration Home Assistant personnalisée et haut de gamme pour surveiller automatiquement les **niveaux d'accès aux 179 massifs forestiers de 15 départements en France** depuis les sites officiels des Préfectures : [risque-prevention-incendie.fr](https://www.risque-prevention-incendie.fr/).

---

## 🗺️ Départements pris en charge (15 départements, 179 massifs)

| Département | Nom | Massifs surveillés | Précision géométrique |
|:---:|---|:---:|:---:|
| **04** | Alpes-de-Haute-Provence | 6 | Polygones vectoriels officiels |
| **06** | Alpes-Maritimes | 7 | Polygones vectoriels officiels |
| **07** | Ardèche | 9 | Polygones vectoriels officiels |
| **11** | Aude | 23 | Polygones vectoriels officiels |
| **13** | Bouches-du-Rhône | 26 | Polygones vectoriels officiels |
| **17** | Charente-Maritime | 4 | Polygones vectoriels officiels |
| **20** | Corse (Corse-du-Sud 2A & Haute-Corse 2B) | 29 | Polygones vectoriels officiels |
| **26** | Drôme | 10 | Polygones vectoriels officiels |
| **30** | Gard | 8 | Polygones vectoriels officiels |
| **34** | Hérault | 9 | Polygones vectoriels officiels |
| **42** | Loire | 9 | Polygones vectoriels officiels |
| **66** | Pyrénées-Orientales | 9 | Polygones vectoriels officiels |
| **81** | Tarn | 6 | Polygones vectoriels officiels |
| **83** | Var | 9 | Polygones vectoriels officiels |
| **84** | Vaucluse | 15 | Polygones vectoriels officiels |

---

## ✨ Fonctionnalités majeures

*   🇫🇷 **Couverture multi-départements** — Choisissez un ou plusieurs départements à surveiller lors de la configuration ou modifiez-les à tout moment dans les options.
*   🗺️ **100% Vrais polygones vectoriels (179 massifs)** — Rendu Leaflet interactif traçant les frontières géographiques réelles de chaque massif avec coloration selon le niveau de risque et popups détaillées au clic.
*   📊 **Capteurs individuels et par département** :
    *   Un capteur dédié par massif forestier (`sensor.acces_massif_<nom>`).
    *   Un capteur résumé par département sélectionné (`sensor.acces_massifs_fr_summary_<dept>`).
    *   Un capteur résumé global (`sensor.acces_massifs_fr_summary`).
*   📥 **Téléchargement automatique de l'historique** — L'intégration propose lors de la configuration (ou via le service `acces_massifs_fr.download_history`) de télécharger l'historique complet de la saison pour alimenter immédiatement vos graphiques.
*   ⏰ **Configuration horaire dynamique** — Entité native `time` (**Heure de récupération**) pour ajuster à chaud l'heure du scan quotidien (défaut : 18h00).
*   🗓️ **Mode d'affichage temporel intelligent** — Affichage des données d'**aujourd'hui** en journée, puis bascule automatique sur les prévisions de **demain** dès publication préfectorale.
*   ❄️ **Gestion automatique hors-saison (1er oct. – 31 mai)** :
    *   Bascule automatique à l'état **"Autorisé" (vert, niveau 1)** pour l'accès libre hivernal.
    *   Polling ralenti à **6 heures** pour préserver les ressources.
*   🎨 **Deux cartes Lovelace premium** :
    *   `acces-massifs-forecast-card` : Carte cartographique vectorielle interactive avec zoom automatique et fiche résumé.
    *   `acces-massifs-history-card` : Grille heatmap d'historique sur toute la saison.
*   ⚙️ **Éditeurs Visuels Natifs (UI Editors)** — Les cartes se configurent graphiquement sans code YAML.

---

## 🚀 Installation

### Via HACS (Recommandé)

1. Ouvrez **HACS** dans votre Home Assistant ➔ **Intégrations**.
2. Cliquez sur les **⋮** en haut à droite ➔ **Dépôts personnalisés**.
3. Ajoutez l'URL de ce dépôt Git et sélectionnez **Intégration** comme catégorie.
4. Recherchez **Accès Massifs Forestiers France** et cliquez sur **Télécharger**.
5. **Redémarrez Home Assistant**.

### Installation manuelle

1. Copiez le dossier `custom_components/acces_massifs_fr/` dans le répertoire `config/custom_components/` de votre Home Assistant.
2. **Redémarrez Home Assistant**.

---

## ⚙️ Configuration

1. Allez dans **Paramètres ➔ Appareils & Services ➔ Ajouter une intégration**.
2. Recherchez **Accès Massifs Forestiers France**.
3. Cochez les **départements** à surveiller.
4. Définissez l'heure de synchronisation (défaut : `18:30`).
5. Indiquez si vous souhaitez télécharger l'historique de la saison en cours.

---

## 🛠️ Services disponibles

*   `acces_massifs_fr.force_update` : Force un rafraîchissement immédiat des données du jour et du lendemain.
*   `acces_massifs_fr.download_history` : Télécharge ou actualise l'historique d'une saison (paramètre optionnel `year`).

---

## 🎨 Cartes Lovelace Custom

### 1. Carte Prévisions & Cartographie (`acces-massifs-forecast-card`)

```yaml
type: custom:acces-massifs-forecast-card
entity: sensor.acces_massifs_fr_summary
title: "Accès aux Massifs Forestiers"
show_map: true
map_height: 400
mode: auto
```

### 2. Carte Historique (`acces-massifs-history-card`)

```yaml
type: custom:acces-massifs-history-card
entity: sensor.acces_massifs_fr_summary
title: "Historique de la saison"
```
