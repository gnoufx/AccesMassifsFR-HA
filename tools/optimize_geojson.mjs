import fs from 'fs';

const raw = JSON.parse(fs.readFileSync('./custom_components/acces_massifs_fr/www/massifs_france.geojson', 'utf8'));

function roundCoords(coords, precision = 5) {
  if (!Array.isArray(coords)) return coords;
  if (typeof coords[0] === 'number') {
    return [
      Math.round(coords[0] * 10 ** precision) / 10 ** precision,
      Math.round(coords[1] * 10 ** precision) / 10 ** precision,
    ];
  }
  return coords.map(c => roundCoords(c, precision));
}

for (const feature of raw.features) {
  if (feature.geometry && feature.geometry.coordinates) {
    feature.geometry.coordinates = roundCoords(feature.geometry.coordinates, 5);
  }
}

const minified = JSON.stringify(raw);
fs.writeFileSync('./custom_components/acces_massifs_fr/www/massifs_france.geojson', minified);
const sizeMB = (fs.statSync('./custom_components/acces_massifs_fr/www/massifs_france.geojson').size / 1024 / 1024).toFixed(2);
console.log(`Optimized GeoJSON size: ${sizeMB} MB (precision: 5 decimals, ~1m resolution). Features count: ${raw.features.length}`);
