import json

with open('./custom_components/acces_massifs_fr/www/massifs_france.geojson', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

def get_centroid(geometry):
    coords = geometry.get('coordinates', [])
    flat_pts = []
    
    def extract_pts(c):
        if not c:
            return
        if isinstance(c[0], (int, float)):
            flat_pts.append((c[0], c[1]))
        else:
            for sub in c:
                extract_pts(sub)
    
    extract_pts(coords)
    if not flat_pts:
        return 43.5, 5.0
    avg_lng = sum(p[0] for p in flat_pts) / len(flat_pts)
    avg_lat = sum(p[1] for p in flat_pts) / len(flat_pts)
    return round(avg_lat, 4), round(avg_lng, 4)

massifs_dict = {}
for feat in geojson['features']:
    props = feat['properties']
    m_id = str(props['ID'])
    name = str(props['NOM_MASSIF'])
    dept = str(props['dept'])
    lat, lng = get_centroid(feat['geometry'])
    
    massifs_dict[m_id] = {
        'name': name,
        'dept': dept,
        'latitude': lat,
        'longitude': lng,
    }

print(f"Total massifs processed: {len(massifs_dict)}")

# Group by dept
by_dept = {}
for m_id, info in massifs_dict.items():
    d = info['dept']
    by_dept.setdefault(d, []).append((m_id, info))

for d in sorted(by_dept.keys()):
    print(f"Dept {d}: {len(by_dept[d])} massifs")

# Output const.py format
lines = ["MASSIFS: dict[str, dict[str, str | float]] = {"]
for d in sorted(by_dept.keys()):
    lines.append(f"    # ── {d} ─────────────────────────────────────────────────────────────")
    for m_id, info in sorted(by_dept[d], key=lambda x: (len(x[0]), x[0])):
        name = info['name'].replace('"', '\\"')
        lines.append(f'    "{m_id}": {{"name": "{name}", "dept": "{info["dept"]}", "latitude": {info["latitude"]}, "longitude": {info["longitude"]}}},')
lines.append("}")

with open('./tools/generated_massifs_const.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print("Generated ./tools/generated_massifs_const.py")
