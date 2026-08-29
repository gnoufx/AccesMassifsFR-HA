# 🌲🔥 [Intégration] Accès Massifs Forestiers France (15 départements, 179 massifs & Cartographie Leaflet)

Bonjour à tous,

C'est avec grand plaisir que je vous présente la nouvelle version majeure de mon intégration Home Assistant : **Accès Massifs Forestiers France** (anciennement *Accès Massifs 13*).

Initiellement développée pour les Bouches-du-Rhône (13), l'intégration couvre désormais l'ensemble des départements réglementés par les préfectures pour le risque d'incendie estival, soit **15 départements et 179 massifs forestiers**.

L'objectif : centraliser ces informations officielles dans Home Assistant pour planifier vos sorties en plein air et être alerté automatiquement dès qu'un massif est fermé au public.

---

## 🎯 L'Objectif de l'intégration

L'intégration récupère automatiquement les niveaux de vigilance et d'accès quotidiens depuis le site officiel de l'État : [risque-prevention-incendie.fr](https://www.risque-prevention-incendie.fr/).

Elle fournit les statuts de la **journée en cours** et bascule automatiquement sur les **prévisions du lendemain** dès que la préfecture les publie en fin de journée (généralement entre 17h30 et 18h30).

---

## 🗺️ 15 départements pris en charge (179 massifs)

| Dép. | Nom | Massifs surveillés | Précision géométrique |
|:---:|---|:---:|:---:|
| **04** | Alpes-de-Haute-Provence | 6 | Polygones vectoriels officiels |
| **06** | Alpes-Maritimes | 7 | Polygones vectoriels officiels |
| **07** | Ardèche | 9 | Polygones vectoriels officiels |
| **11** | Aude | 23 | Polygones vectoriels officiels |
| **13** | Bouches-du-Rhône | 26 | Polygones vectoriels officiels |
| **17** | Charente-Maritime | 4 | Polygones vectoriels officiels |
| **20** | Corse (*2A Corse-du-Sud & 2B Haute-Corse*) | 29 | Polygones vectoriels officiels |
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

* **🇫🇷 Sélection multi-départements** : Choisissez un ou plusieurs départements à surveiller lors de l'installation, modifiables à tout moment via les options.
* **🗺️ 100% Vrais polygones vectoriels (179 massifs)** : Rendu cartographique vectoriel interactif sous Leaflet traçant les frontières géographiques réelles de chaque massif avec coloration selon le niveau de risque et popups informatives au clic.
* **📊 Capteurs individuels et par département** :
  * Un capteur dédié par massif forestier (`sensor.acces_massif_<nom>`) avec coordonnées GPS, niveau de 0 à 4, couleur officielle, prévision pour le lendemain, etc.
  * Un capteur résumé par département configuré (`sensor.acces_massifs_fr_summary_<dept>`).
  * Un capteur résumé global (`sensor.acces_massifs_fr_summary`).
* **📥 Téléchargement automatique de l'historique** : L'intégration propose lors de la configuration (ou via le service `acces_massifs_fr.download_history`) de télécharger l'historique complet de la saison en cours pour alimenter immédiatement vos graphiques.
* **⏰ Configuration et planification dynamiques** : Entité native `time` (`time.acces_massifs_forestiers_france_heure_de_recuperation`) pour ajuster l'heure du scan quotidien directement depuis vos dashboards, sans redémarrage.
* **🗓️ Mode d'affichage temporel intelligent** : Les cartes adaptent leur état automatiquement : elles affichent les données d'aujourd'hui en journée, puis basculent sur les prévisions de demain dès publication préfectorale.
* **❄️ Gestion logique hors-saison (1er oct. – 31 mai)** : L'intégration bascule automatiquement tous les massifs à l'état "Autorisé" (vert) pour refléter l'accès libre hivernal et printanier, garantissant la cohérence de vos automatisations toute l'année. Polling allégé à 6h.
* **💾 Historique persistant multi-saisons** : Stockage JSON local autonome dans le dossier `.storage/` pour sauvegarder et afficher l'historique complet sur plusieurs années, indépendamment de la purge du recorder HA.
* **🛠️ Services dédiés** :
  * `acces_massifs_fr.force_update` : Force un rafraîchissement immédiat des données.
  * `acces_massifs_fr.download_history` : Télécharge / actualise l'historique d'une saison (`year`).

---

## 🎨 Les Cartes Lovelace Custom Incluses

L'intégration inclut automatiquement deux cartes Lovelace avec éditeurs visuels natifs (UI Editors) :

### 1. Carte Accès & Cartographie (`acces-massifs-forecast-card`)
Affiche l'état d'accès de vos massifs forestiers sous forme de grille adaptative animée avec pulsation, couplée à une carte Leaflet interactive dessinant les polygones réels de vos massifs.
* **Support Multi-Massifs & Centrage Intelligent** : Vous pouvez cibler un sous-ensemble de massifs ou de départements. La carte s'adaptera automatiquement et ajustera son zoom pour se centrer exclusivement sur les zones sélectionnées.

```yaml
type: custom:acces-massifs-forecast-card
entity: sensor.acces_massifs_fr_summary
title: "Accès aux Massifs Forestiers"
show_map: true
map_height: 420
animate: true
mode: auto
```

### 2. Carte Historique (`acces-massifs-history-card`)
Affiche une matrice heatmap animée (jours en abscisse, massifs en ordonnée) retraçant l'ensemble des niveaux d'accès sur toute la saison (juin à septembre). Elle intègre des bulles d'aide au survol, un focus par clic sur une ligne et une sparkline SVG fluide affichant la tendance d'ouverture des massifs.

```yaml
type: custom:acces-massifs-history-card
entity: sensor.acces_massifs_fr_summary
title: "Historique de la saison"
animate: true
show_sparkline: true
```

---

## 🚀 Comment l'installer ?

### Option 1 : Via HACS (Recommandé)
1. Ouvrez **HACS** dans votre interface Home Assistant.
2. Cliquez sur **Intégrations** puis sur les **⋮** en haut à droite ➔ **Dépôts personnalisés**.
3. Ajoutez l'URL suivante : `https://github.com/gnoufx/AccesMassif13-HA`
4. Sélectionnez **Intégration** comme catégorie.
5. Cliquez sur **Ajouter**, recherchez **Accès Massifs Forestiers France** et cliquez sur **Télécharger**.
6. **Redémarrez Home Assistant**.

### Option 2 : Installation manuelle
1. Téléchargez le code depuis le dépôt GitHub : [GitHub - gnoufx/AccesMassif13-HA](https://github.com/gnoufx/AccesMassif13-HA).
2. Copiez le dossier `custom_components/acces_massifs_fr/` dans le répertoire `config/custom_components/` de votre Home Assistant.
3. **Redémarrez Home Assistant**.

---

## ⚙️ Configuration

L'intégration se configure très simplement via l'interface utilisateur :

1. Allez dans **Paramètres ➔ Appareils & Services ➔ Ajouter une intégration**.
2. Recherchez **Accès Massifs Forestiers France**.
3. Cochez les **départements** souhaités.
4. Définissez l'heure et la minute souhaitées pour la récupération quotidienne des données (ex. `18:30`).
5. Choisissez si vous souhaitez télécharger immédiatement l'historique de la saison en cours.

> **Astuce** : Vous pouvez modifier l'heure de synchronisation à tout moment en modifiant directement la valeur de l'entité `time.acces_massifs_forestiers_france_heure_de_recuperation` depuis vos dashboards.

---

## 🔔 Exemple d'automatisation (Notification Smartphone)

Pour être notifié le soir sur votre smartphone si votre massif préféré est interdit pour le lendemain :

```yaml
alias: "Alerte Calanques Interdites pour demain"
description: "Envoie une notification si les Calanques sont interdites d'accès pour demain"
trigger:
  - platform: state
    entity_id: sensor.acces_massifs_fr_summary
condition: []
action:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ state_attr('sensor.acces_massif_calanques', 'tomorrow_color') in ['red', 'black'] }}"
        sequence:
          - action: notify.mobile_app_votre_smartphone
            data:
              title: "🔴 Calanques interdites demain"
              message: "Attention, l'accès au massif des Calanques sera interdit demain pour risque incendie !"
mode: single
```

---

## 💬 Retours & Contributions

N'hésitez pas à me faire vos retours, suggestions d'amélioration ou à remonter d'éventuels bugs. Les contributions et les pull requests sur GitHub sont les bienvenues !

🔗 **Lien du dépôt GitHub** : [gnoufx/AccesMassif13-HA](https://github.com/gnoufx/AccesMassif13-HA)
