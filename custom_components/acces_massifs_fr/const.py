"""Constants for the Accès Massifs Forestiers France integration."""

from __future__ import annotations

DOMAIN = "acces_massifs_fr"

# ── Season window ──────────────────────────────────────────────────────────────
SEASON_START_MONTH = 5
SEASON_START_DAY = 31
SEASON_END_MONTH = 9
SEASON_END_DAY = 30

# ── Default scan schedule ──────────────────────────────────────────────────────
DEFAULT_SCAN_HOUR = 18
DEFAULT_SCAN_MINUTE = 30

# ── Data source ────────────────────────────────────────────────────────────────
# {dept} is replaced by department number, {date} by YYYYMMDD
DATA_URL_TEMPLATE = (
    "https://www.risque-prevention-incendie.fr/static/{dept}/import_data/{date}.json"
)

# ── Config‑flow keys ──────────────────────────────────────────────────────────
CONF_SCAN_HOUR = "scan_hour"
CONF_SCAN_MINUTE = "scan_minute"
CONF_DEPARTMENTS = "departments"
CONF_DOWNLOAD_HISTORY = "download_history"
DEFAULT_DOWNLOAD_HISTORY = True


# ── Departments registry ────────────────────────────────────────────────────────
DEPARTMENTS: dict[str, str] = {
    "04": "Alpes-de-Haute-Provence",
    "06": "Alpes-Maritimes",
    "07": "Ardèche",
    "11": "Aude",
    "13": "Bouches-du-Rhône",
    "17": "Charente-Maritime",
    "20": "Corse",
    "26": "Drôme",
    "30": "Gard",
    "34": "Hérault",
    "42": "Loire",
    "66": "Pyrénées-Orientales",
    "81": "Tarn",
    "83": "Var",
    "84": "Vaucluse",
}

# ── Level → label / color mappings ─────────────────────────────────────────────
LEVEL_LABELS: dict[int, str] = {
    0: "Non disponible",
    1: "Autorisé",
    2: "Autorisé",
    3: "Interdit",
    4: "Interdit",
    5: "Interdit",
    6: "Interdit",
}

LEVEL_COLORS: dict[int, str] = {
    0: "unknown",
    1: "green",
    2: "green",
    3: "red",
    4: "red",
    5: "red",
    6: "red",
}

# ── Massif registry ───────────────────────────────────────────────────────────
# Synchronized with official FlatGeobuf vector polygons (179 massifs in total)
MASSIFS: dict[str, dict[str, str | float]] = {
    # ── 04 ─────────────────────────────────────────────────────────────
    "41": {"name": "ROUGON", "dept": "04", "latitude": 43.7691, "longitude": 6.3999},
    "42": {"name": "ESPARRON-DE-VERDON", "dept": "04", "latitude": 43.7287, "longitude": 5.9544},
    "43": {"name": "MONTAGNAC-MONTPEZAT", "dept": "04", "latitude": 43.7399, "longitude": 6.0973},
    "44": {"name": "CASTELLANE", "dept": "04", "latitude": 43.8147, "longitude": 6.5036},
    "45": {"name": "GREOUX-LES-BAINS", "dept": "04", "latitude": 43.7355, "longitude": 5.8714},
    "46": {"name": "QUINSON", "dept": "04", "latitude": 43.6946, "longitude": 6.0165},
    # ── 06 ─────────────────────────────────────────────────────────────
    "61": {"name": "LITTORAL EST", "dept": "06", "latitude": 43.7633, "longitude": 7.3152},
    "62": {"name": "MOYEN PAYS OUEST", "dept": "06", "latitude": 43.9131, "longitude": 7.3416},
    "63": {"name": "HAUT PAYS", "dept": "06", "latitude": 44.0982, "longitude": 7.157},
    "64": {"name": "MOYEN PAYS OUEST", "dept": "06", "latitude": 43.8571, "longitude": 6.9328},
    "65": {"name": "LITTORAL OUEST", "dept": "06", "latitude": 43.6461, "longitude": 7.0002},
    "66": {"name": "TANNERON", "dept": "06", "latitude": 43.5734, "longitude": 6.9045},
    "67": {"name": "HAUT ESTERON", "dept": "06", "latitude": 43.8348, "longitude": 6.7584},
    # ── 07 ─────────────────────────────────────────────────────────────
    "71": {"name": "Haut Vivarais", "dept": "07", "latitude": 45.0954, "longitude": 4.6655},
    "72": {"name": "Boutières", "dept": "07", "latitude": 44.8572, "longitude": 4.5255},
    "73": {"name": "Haut Plateau Nord", "dept": "07", "latitude": 45.0375, "longitude": 4.4118},
    "74": {"name": "Cévennes", "dept": "07", "latitude": 44.5993, "longitude": 4.1846},
    "75": {"name": "Bas Vivarais", "dept": "07", "latitude": 44.5069, "longitude": 4.3633},
    "76": {"name": "Vallée du Rhône Sud", "dept": "07", "latitude": 44.5718, "longitude": 4.6029},
    "77": {"name": "Haut plateau Sud", "dept": "07", "latitude": 44.7922, "longitude": 4.1082},
    "78": {"name": "Vallée du Rhône Nord", "dept": "07", "latitude": 45.0831, "longitude": 4.7798},
    "79": {"name": "Coiron", "dept": "07", "latitude": 44.6535, "longitude": 4.5474},
    # ── 11 ─────────────────────────────────────────────────────────────
    "111": {"name": "Clape", "dept": "11", "latitude": 43.193, "longitude": 3.127},
    "112": {"name": "FONTFROIDE", "dept": "11", "latitude": 43.0836, "longitude": 2.8672},
    "113": {"name": "PINEDES CREMADES", "dept": "11", "latitude": 43.1012, "longitude": 2.6753},
    "114": {"name": "CORBIERES MARITIMES", "dept": "11", "latitude": 42.9539, "longitude": 2.8982},
    "115": {"name": "CAVAYERE DROITE", "dept": "11", "latitude": 43.1823, "longitude": 2.4246},
    "116": {"name": "MINERVOIS", "dept": "11", "latitude": 43.3243, "longitude": 2.4643},
    "117": {"name": "PLAINE DU MINERVOIS", "dept": "11", "latitude": 43.2576, "longitude": 2.6276},
    "118": {"name": "LEZIGNANAIS", "dept": "11", "latitude": 43.2048, "longitude": 2.7242},
    "119": {"name": "CORBIERES OCCIDENTALES", "dept": "11", "latitude": 42.9715, "longitude": 2.3553},
    "1110": {"name": "CORBIERES CENTRALES", "dept": "11", "latitude": 42.96, "longitude": 2.6969},
    "1111": {"name": "VALLEE DE L'ORBIEU", "dept": "11", "latitude": 43.0332, "longitude": 2.5861},
    "1112": {"name": "VALLEE DU LAUQUET", "dept": "11", "latitude": 43.0849, "longitude": 2.3767},
    "1113": {"name": "CABARDES", "dept": "11", "latitude": 43.3304, "longitude": 2.3096},
    "1114": {"name": "CONTREFORTS OUEST MONTAGNE NOIRE", "dept": "11", "latitude": 43.3564, "longitude": 2.0453},
    "1115": {"name": "MALEPERE", "dept": "11", "latitude": 43.1647, "longitude": 2.1944},
    "1116": {"name": "RAZES-HAUTE VALLEE", "dept": "11", "latitude": 43.0057, "longitude": 2.1254},
    "1117": {"name": "CHALABRAIS", "dept": "11", "latitude": 42.9781, "longitude": 2.0331},
    "1118": {"name": "PIEGE - LAURAGAIS", "dept": "11", "latitude": 43.2762, "longitude": 1.8904},
    "1119": {"name": "BASSES PLAINES", "dept": "11", "latitude": 43.2113, "longitude": 2.9312},
    "1120": {"name": "MONTAGNE NOIRE", "dept": "11", "latitude": 43.3808, "longitude": 2.3143},
    "1121": {"name": "PAYS DE SAULT", "dept": "11", "latitude": 42.7809, "longitude": 2.109},
    "1122": {"name": "ÎLE DE SAINTE-LUCIE", "dept": "11", "latitude": 43.0505, "longitude": 3.0427},
    "1123": {"name": "CAVAYERE GAUCHE", "dept": "11", "latitude": 43.1831, "longitude": 2.4161},
    # ── 13 ─────────────────────────────────────────────────────────────
    "131": {"name": "Alpilles", "dept": "13", "latitude": 43.7414, "longitude": 4.8702},
    "132": {"name": "Arbois", "dept": "13", "latitude": 43.4944, "longitude": 5.3048},
    "133": {"name": "Calanques", "dept": "13", "latitude": 43.2347, "longitude": 5.4494},
    "134": {"name": "Cap Canaille", "dept": "13", "latitude": 43.1914, "longitude": 5.5854},
    "135": {"name": "Castillon", "dept": "13", "latitude": 43.4555, "longitude": 4.9981},
    "136": {"name": "Chaine des Cotes", "dept": "13", "latitude": 43.6911, "longitude": 5.2807},
    "137": {"name": "Chambremont", "dept": "13", "latitude": 43.6716, "longitude": 4.834},
    "138": {"name": "Collines de Gardanne", "dept": "13", "latitude": 43.4526, "longitude": 5.4984},
    "139": {"name": "Concors", "dept": "13", "latitude": 43.637, "longitude": 5.6399},
    "1310": {"name": "Cote Bleue", "dept": "13", "latitude": 43.3695, "longitude": 5.1817},
    "1311": {"name": "Etoile", "dept": "13", "latitude": 43.3906, "longitude": 5.4351},
    "1312": {"name": "Garlaban", "dept": "13", "latitude": 43.318, "longitude": 5.5051},
    "1313": {"name": "Grand Caunet", "dept": "13", "latitude": 43.2423, "longitude": 5.6193},
    "1314": {"name": "Lançon", "dept": "13", "latitude": 43.5666, "longitude": 5.1313},
    "1315": {"name": "Les Roques", "dept": "13", "latitude": 43.6677, "longitude": 5.1667},
    "1316": {"name": "Montagnette", "dept": "13", "latitude": 43.8673, "longitude": 4.7346},
    "1317": {"name": "Montaiguet", "dept": "13", "latitude": 43.4845, "longitude": 5.4567},
    "1318": {"name": "Pont de Rhaud", "dept": "13", "latitude": 43.5851, "longitude": 5.0509},
    "1319": {"name": "Quatre Termes", "dept": "13", "latitude": 43.6111, "longitude": 5.2518},
    "1320": {"name": "Regagnas", "dept": "13", "latitude": 43.4687, "longitude": 5.6601},
    "1321": {"name": "Rougadou", "dept": "13", "latitude": 43.8398, "longitude": 4.9084},
    "1322": {"name": "Sainte-Baume", "dept": "13", "latitude": 43.3364, "longitude": 5.6983},
    "1323": {"name": "Sainte-Victoire", "dept": "13", "latitude": 43.5516, "longitude": 5.6193},
    "1324": {"name": "Sulauze", "dept": "13", "latitude": 43.5593, "longitude": 5.0298},
    "1325": {"name": "Trevaresse", "dept": "13", "latitude": 43.6393, "longitude": 5.3789},
    "1326": {"name": "Lunard", "dept": "13", "latitude": 43.6322, "longitude": 5.2045},
    # ── 17 ─────────────────────────────────────────────────────────────
    "171": {"name": "Secteur 1 – Îles et littoral", "dept": "17", "latitude": 45.9221, "longitude": -1.1895},
    "172": {"name": "Secteur 2 – Saintonge et Aunis", "dept": "17", "latitude": 45.8239, "longitude": -0.6698},
    "173": {"name": "Secteur 3 – Forêt de la Lande et estuaire", "dept": "17", "latitude": 45.3853, "longitude": -0.8359},
    "174": {"name": "Secteur 4 – Double Saintongeaise", "dept": "17", "latitude": 45.2492, "longitude": -0.2858},
    # ── 20 ─────────────────────────────────────────────────────────────
    "201": {"name": "FILITOSA", "dept": "20", "latitude": 41.7483, "longitude": 8.8711},
    "202": {"name": "COTI CHIAVARI", "dept": "20", "latitude": 41.7779, "longitude": 8.7836},
    "203": {"name": "POZZO DI BORGO", "dept": "20", "latitude": 41.9774, "longitude": 8.7001},
    "204": {"name": "PUNTA D'ARCO", "dept": "20", "latitude": 42.0622, "longitude": 8.6508},
    "205": {"name": "VALLE MALA", "dept": "20", "latitude": 42.148, "longitude": 8.6366},
    "206": {"name": "CAPO ROSSO", "dept": "20", "latitude": 42.2359, "longitude": 8.5724},
    "207": {"name": "PIANA", "dept": "20", "latitude": 42.2618, "longitude": 8.6653},
    "208": {"name": "VALLE D'OSE", "dept": "20", "latitude": 42.3486, "longitude": 8.6834},
    "209": {"name": "PORTO", "dept": "20", "latitude": 42.2785, "longitude": 8.7291},
    "211": {"name": "LONCA - AITONE - SERRIERA", "dept": "20", "latitude": 42.2859, "longitude": 8.8105},
    "212": {"name": "FALASORMA", "dept": "20", "latitude": 42.4173, "longitude": 8.7247},
    "213": {"name": "BONIFATO", "dept": "20", "latitude": 42.4439, "longitude": 8.8687},
    "214": {"name": "TARTAGINE - MELAJA", "dept": "20", "latitude": 42.4939, "longitude": 8.9749},
    "215": {"name": "FANGO", "dept": "20", "latitude": 42.3878, "longitude": 8.7758},
    "216": {"name": "REGINO", "dept": "20", "latitude": 42.5932, "longitude": 8.983},
    "217": {"name": "OSTRICONI", "dept": "20", "latitude": 42.6397, "longitude": 9.0766},
    "218": {"name": "AGRIATES OUEST", "dept": "20", "latitude": 42.684, "longitude": 9.1311},
    "2024": {"name": "BAVELLA", "dept": "20", "latitude": 41.8157, "longitude": 9.2435},
    "2026": {"name": "CAVU", "dept": "20", "latitude": 41.7308, "longitude": 9.2784},
    "2113": {"name": "VERGHELLU", "dept": "20", "latitude": 42.2052, "longitude": 9.1147},
    "2114": {"name": "MANGANELLU", "dept": "20", "latitude": 42.1706, "longitude": 9.1084},
    "2115": {"name": "RESTANICA", "dept": "20", "latitude": 42.2475, "longitude": 9.069},
    "2117": {"name": "TAVIGNANO", "dept": "20", "latitude": 42.298, "longitude": 9.0833},
    "2120": {"name": "PINIA", "dept": "20", "latitude": 42.029, "longitude": 9.4673},
    "2122": {"name": "VAL D'ESU", "dept": "20", "latitude": 42.2858, "longitude": 9.4891},
    "2127": {"name": "MARANA", "dept": "20", "latitude": 42.562, "longitude": 9.5076},
    "2128": {"name": "SAN PETRONE", "dept": "20", "latitude": 42.3995, "longitude": 9.3512},
    "2129": {"name": "AGRIATES EST", "dept": "20", "latitude": 42.6951, "longitude": 9.2201},
    "2130": {"name": "PIANELLO", "dept": "20", "latitude": 42.2882, "longitude": 9.3402},
    # ── 26 ─────────────────────────────────────────────────────────────
    "261": {"name": "Nord vallée du Rhône", "dept": "26", "latitude": 45.0568, "longitude": 4.9604},
    "262": {"name": "Royans Vercors", "dept": "26", "latitude": 44.9785, "longitude": 5.2891},
    "263": {"name": "Vallée de la Drôme", "dept": "26", "latitude": 44.7303, "longitude": 5.0934},
    "264": {"name": "Haut-Diois", "dept": "26", "latitude": 44.5772, "longitude": 5.4851},
    "265": {"name": "Sud vallée du Rhône", "dept": "26", "latitude": 44.6409, "longitude": 4.887},
    "266": {"name": "Pays de Dieulefit Hte Roanne Oule", "dept": "26", "latitude": 44.4958, "longitude": 5.2396},
    "267": {"name": "Nyonsais", "dept": "26", "latitude": 44.3852, "longitude": 5.1764},
    "268": {"name": "Hautes-Baronnies", "dept": "26", "latitude": 44.298, "longitude": 5.4988},
    "269": {"name": "Uchaux-Barry", "dept": "26", "latitude": 44.3168, "longitude": 4.7709},
    "2610": {"name": "Ventoux-Toulourenc", "dept": "26", "latitude": 44.1843, "longitude": 5.2536},
    # ── 30 ─────────────────────────────────────────────────────────────
    "301": {"name": "CAUSSE AIGOUAL", "dept": "30", "latitude": 44.1039, "longitude": 3.498},
    "302": {"name": "SUD CEVENNES", "dept": "30", "latitude": 43.9961, "longitude": 3.7915},
    "303": {"name": "NORD CEVENNES", "dept": "30", "latitude": 44.2494, "longitude": 4.0205},
    "304": {"name": "GARDON VIDOURLE", "dept": "30", "latitude": 43.9262, "longitude": 4.0899},
    "305": {"name": "VAL DE CEZE", "dept": "30", "latitude": 44.2238, "longitude": 4.3846},
    "306": {"name": "GARRIGUES", "dept": "30", "latitude": 43.9288, "longitude": 4.4172},
    "307": {"name": "COSTIERES PETITE CAMARGUE", "dept": "30", "latitude": 43.6872, "longitude": 4.3151},
    "308": {"name": "GARD RHODANIEN", "dept": "30", "latitude": 44.087, "longitude": 4.6543},
    # ── 34 ─────────────────────────────────────────────────────────────
    "341": {"name": "SOMAIL-ESPINOUSE-MONTS D'ORB", "dept": "34", "latitude": 43.606, "longitude": 2.9734},
    "342": {"name": "ESCANDORGUE ET LARZAC", "dept": "34", "latitude": 43.7663, "longitude": 3.2844},
    "343": {"name": "GANGEOIS", "dept": "34", "latitude": 43.8821, "longitude": 3.666},
    "344": {"name": "GARRIGUES ET PINEDES EST HERAULTAIS", "dept": "34", "latitude": 43.7388, "longitude": 3.8647},
    "345": {"name": "COLLINES CENTRE HERAULT", "dept": "34", "latitude": 43.5936, "longitude": 3.3283},
    "346": {"name": "MINERVOIS ET SAINT-CHINIANAIS", "dept": "34", "latitude": 43.4079, "longitude": 2.9157},
    "347": {"name": "PLAINE VITICOLE COEUR HERAULT", "dept": "34", "latitude": 43.4143, "longitude": 3.3644},
    "348": {"name": "GARDIOLE", "dept": "34", "latitude": 43.4937, "longitude": 3.7656},
    "349": {"name": "PLAINE VITICOLE EST HERAULTAIS", "dept": "34", "latitude": 43.5855, "longitude": 3.9928},
    # ── 42 ─────────────────────────────────────────────────────────────
    "421": {"name": "Plaine Roannaise", "dept": "42", "latitude": 46.1039, "longitude": 4.0722},
    "422": {"name": "Monts du Lyonnais", "dept": "42", "latitude": 45.6966, "longitude": 4.3592},
    "423": {"name": "Monts du Beaujolais", "dept": "42", "latitude": 46.069, "longitude": 4.2882},
    "424": {"name": "Plateau de Neulise", "dept": "42", "latitude": 45.8953, "longitude": 4.148},
    "425": {"name": "Monts du Forez", "dept": "42", "latitude": 45.642, "longitude": 3.9318},
    "426": {"name": "Plaine du Forez", "dept": "42", "latitude": 45.6321, "longitude": 4.1852},
    "427": {"name": "Monts du Jarez - Bassin Stéphanois", "dept": "42", "latitude": 45.4518, "longitude": 4.4093},
    "428": {"name": "Vallée du Rhône", "dept": "42", "latitude": 45.4087, "longitude": 4.6789},
    "429": {"name": "Monts du Pilat", "dept": "42", "latitude": 45.3855, "longitude": 4.5492},
    # ── 66 ─────────────────────────────────────────────────────────────
    "661": {"name": "CAPCIR", "dept": "66", "latitude": 42.5976, "longitude": 2.0863},
    "662": {"name": "CERDAGNE", "dept": "66", "latitude": 42.4705, "longitude": 1.9892},
    "663": {"name": "CONFLENT", "dept": "66", "latitude": 42.5519, "longitude": 2.3789},
    "664": {"name": "FENOUILLEDES", "dept": "66", "latitude": 42.7561, "longitude": 2.4933},
    "665": {"name": "ASPRES", "dept": "66", "latitude": 42.6074, "longitude": 2.6631},
    "666": {"name": "VALLESPIR", "dept": "66", "latitude": 42.4348, "longitude": 2.5855},
    "667": {"name": "ROUSSILLON", "dept": "66", "latitude": 42.6653, "longitude": 2.8715},
    "668": {"name": "ALBERES", "dept": "66", "latitude": 42.5028, "longitude": 3.0315},
    "669": {"name": "CORBIERES", "dept": "66", "latitude": 42.8465, "longitude": 2.8252},
    # ── 81 ─────────────────────────────────────────────────────────────
    "811": {"name": "Grésigne et Causses", "dept": "81", "latitude": 44.0202, "longitude": 1.8319},
    "812": {"name": "Ségala et Monts d'Alban", "dept": "81", "latitude": 43.9472, "longitude": 2.3927},
    "813": {"name": "Monts de Lacaune", "dept": "81", "latitude": 43.6702, "longitude": 2.6329},
    "814": {"name": "Sidobre Vallée du Thoré", "dept": "81", "latitude": 43.5135, "longitude": 2.4173},
    "815": {"name": "Montagne Noire", "dept": "81", "latitude": 43.4682, "longitude": 2.1837},
    "816": {"name": "Plaines", "dept": "81", "latitude": 43.6845, "longitude": 1.942},
    # ── 83 ─────────────────────────────────────────────────────────────
    "831": {"name": "MONTS TOULONNAIS", "dept": "83", "latitude": 43.1495, "longitude": 5.9691},
    "832": {"name": "SAINTE BAUME", "dept": "83", "latitude": 43.3039, "longitude": 5.8643},
    "833": {"name": "HAUT VAR", "dept": "83", "latitude": 43.6749, "longitude": 6.2201},
    "834": {"name": "CORNICHE DES MAURES", "dept": "83", "latitude": 43.1979, "longitude": 6.4716},
    "835": {"name": "MAURES", "dept": "83", "latitude": 43.3061, "longitude": 6.4258},
    "836": {"name": "CENTRE VAR", "dept": "83", "latitude": 43.4475, "longitude": 6.1843},
    "837": {"name": "PLATEAU DE CANJUERS", "dept": "83", "latitude": 43.6743, "longitude": 6.551},
    "838": {"name": "ESTEREL", "dept": "83", "latitude": 43.5238, "longitude": 6.816},
    "839": {"name": "ILES D'HYERES", "dept": "83", "latitude": 43.0039, "longitude": 6.386},
    # ── 84 ─────────────────────────────────────────────────────────────
    "841": {"name": "Massif de Bollène-Uchaux", "dept": "84", "latitude": 44.2494, "longitude": 4.8153},
    "842": {"name": "Massif des collines du pays Voconces", "dept": "84", "latitude": 44.2526, "longitude": 5.097},
    "843": {"name": "Massif du mont Ventoux", "dept": "84", "latitude": 44.1793, "longitude": 5.2891},
    "844": {"name": "Massif de Rasteau - Cairanne", "dept": "84", "latitude": 44.242, "longitude": 4.966},
    "845": {"name": "Massif de l'enclave des Papes", "dept": "84", "latitude": 44.3643, "longitude": 4.9818},
    "846": {"name": "Massif des collines de basse Durance", "dept": "84", "latitude": 43.834, "longitude": 4.9934},
    "847": {"name": "Massif de la plaine du Comtat", "dept": "84", "latitude": 44.0205, "longitude": 4.9575},
    "848": {"name": "Massif de Cadenet - Villelaure", "dept": "84", "latitude": 43.7386, "longitude": 5.3789},
    "849": {"name": "Massif de la vallée du Rhône", "dept": "84", "latitude": 43.9902, "longitude": 4.8087},
    "8410": {"name": "Massif du petit Luberon", "dept": "84", "latitude": 43.8188, "longitude": 5.2471},
    "8411": {"name": "Massif du grand Luberon", "dept": "84", "latitude": 43.8548, "longitude": 5.5457},
    "8412": {"name": "Massif des dentelles de Montmirail", "dept": "84", "latitude": 44.1611, "longitude": 5.0601},
    "8413": {"name": "Massif des monts de Vaucluse", "dept": "84", "latitude": 43.9926, "longitude": 5.2974},
    "8414": {"name": "Massif de la vallée d'Apt", "dept": "84", "latitude": 43.9015, "longitude": 5.3855},
    "8415": {"name": "Massif du Ventoux Sommet", "dept": "84", "latitude": 44.1738, "longitude": 5.2789},
}

# ── Per-department massif index ─────────────────────────────────────────────────
# Pre-computed for fast lookups: dept → list of massif_ids
MASSIFS_BY_DEPT: dict[str, list[str]] = {}
for _m_id, _m_info in MASSIFS.items():
    _dept = str(_m_info["dept"])
    MASSIFS_BY_DEPT.setdefault(_dept, []).append(_m_id)
