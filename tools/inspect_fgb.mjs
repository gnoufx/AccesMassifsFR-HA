import fs from 'fs';
import path from 'path';
import { deserialize } from 'flatgeobuf/lib/mjs/geojson.js';

const fgbDir = './tools/fgb_downloads';
const files = fs.readdirSync(fgbDir).filter(f => f.endsWith('.fgb')).sort();

console.log(`Found ${files.length} FGB files to convert.`);

for (const file of files) {
  const filePath = path.join(fgbDir, file);
  const bytes = fs.readFileSync(filePath);
  const uint8 = new Uint8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength);

  try {
    const iter = deserialize(uint8);
    const features = [];
    for await (const feature of iter) {
      features.push(feature);
    }
    console.log(`\n=== ${file} ===`);
    console.log(`Features count: ${features.length}`);
    if (features.length > 0) {
      console.log('Sample properties:', features[0].properties);
      console.log('Sample geom type:', features[0].geometry?.type);
    }
  } catch (err) {
    console.error(`Error parsing ${file}:`, err);
  }
}
