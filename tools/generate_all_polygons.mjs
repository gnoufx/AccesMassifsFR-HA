import fs from 'fs';
import path from 'path';
import { deserialize } from 'flatgeobuf/lib/mjs/geojson.js';

const fgbDir = './tools/fgb_downloads';
const deptFiles = [
  { dept: '04', file: 'massifs_04.fgb' },
  { dept: '06', file: 'massifs_06.fgb' },
  { dept: '07', file: 'massifs_07.fgb' },
  { dept: '11', file: 'massifs_11.fgb' },
  { dept: '13', file: 'massifs_13.fgb' },
  { dept: '17', file: 'massifs_17.fgb' },
  { dept: '20', file: 'massifs_20.fgb' },
  { dept: '26', file: 'massifs_26.fgb' },
  { dept: '30', file: 'massifs_30.fgb' },
  { dept: '34', file: 'massifs_34.fgb' },
  { dept: '42', file: 'massifs_42.fgb' },
  { dept: '66', file: 'massifs_66.fgb' },
  { dept: '81', file: 'massifs_81.fgb' },
  { dept: '83', file: 'massifs_83.fgb' },
  { dept: '84', file: 'massifs_84.fgb' },
];

const allFeatures = [];
const massifCatalog = {};

for (const { dept, file } of deptFiles) {
  const filePath = path.join(fgbDir, file);
  const bytes = fs.readFileSync(filePath);
  const uint8 = new Uint8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength);

  const iter = deserialize(uint8);
  let count = 0;
  for await (const feature of iter) {
    const rawProps = feature.properties || {};
    const rawId = rawProps.ID ?? rawProps.id ?? rawProps.CODE ?? rawProps.NUMERO;
    const rawName = rawProps.NOM_MASSIF || rawProps.nom_massif || rawProps.LIBELLE || rawProps.NOM || `Massif ${rawId}`;
    
    // Normalize ID as string
    const mId = String(rawId);
    
    // Normalize name
    let cleanName = String(rawName).trim();
    // Remove leading number prefixes like '8-GARDIOLE' or '1 - '
    cleanName = cleanName.replace(/^\d+\s*[-–]\s*/, '').trim();

    // Set normalized properties
    feature.properties = {
      ID: mId,
      id: mId,
      NOM_MASSIF: cleanName,
      dept: dept,
    };

    allFeatures.push(feature);
    massifCatalog[mId] = {
      name: cleanName,
      dept: dept,
      geomType: feature.geometry?.type
    };
    count++;
  }
  console.log(`Dept ${dept}: ${count} polygons added.`);
}

console.log(`\nTotal polygon features: ${allFeatures.length}`);

const geojsonOutput = {
  type: 'FeatureCollection',
  features: allFeatures,
};

const outputPath = './custom_components/acces_massifs_fr/www/massifs_france.geojson';
fs.writeFileSync(outputPath, JSON.stringify(geojsonOutput));
console.log(`Saved unified GeoJSON to ${outputPath} (${(fs.statSync(outputPath).size / 1024 / 1024).toFixed(2)} MB)`);

// Save massif catalog JSON for reference
fs.writeFileSync('./tools/massifs_catalog.json', JSON.stringify(massifCatalog, null, 2));
console.log(`Saved catalog of ${Object.keys(massifCatalog).length} massifs to ./tools/massifs_catalog.json`);
