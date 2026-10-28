import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const [input, name, ratio = 'original'] = process.argv.slice(2);
if (!input || !name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) {
  console.error('Uso: node tools/optimize-images.mjs <foto-original> <nome-em-minusculas> [3:4|3:2|4:3|1:1|original]');
  process.exit(1);
}
const ratios = { '3:4': [3, 4], '3:2': [3, 2], '4:3': [4, 3], '1:1': [1, 1] };
if (ratio !== 'original' && !(ratio in ratios)) throw new Error(`Proporção inválida: ${ratio}`);

const outputDir = path.resolve('assets/img/soulcont');
const source = path.resolve(input);
if (!fs.statSync(source).isFile()) throw new Error('A entrada precisa ser um arquivo.');
if (source.startsWith(path.resolve('assets') + path.sep)) throw new Error('Mantenha os originais fora de assets/.');

const base = sharp(source).rotate(); // aplica orientação EXIF e remove os metadados na saída
const meta = await base.metadata();
const originalWidth = [5, 6, 7, 8].includes(meta.orientation) ? meta.height : meta.width;
const originalHeight = [5, 6, 7, 8].includes(meta.orientation) ? meta.width : meta.height;
const targetRatio = ratio === 'original' ? originalWidth / originalHeight : ratios[ratio][0] / ratios[ratio][1];
const cropWidth = Math.min(originalWidth, Math.floor(originalHeight * targetRatio));
const widths = [320, 640, 960, 1600].filter(width => width <= cropWidth);
if (!widths.length) widths.push(cropWidth);
const landscape = targetRatio >= 1;
const limit = landscape ? 90 * 1024 : 45 * 1024;
const budgetWidth = landscape ? 960 : 640;
const files = [];
for (const width of widths) {
  const height = Math.round(width / targetRatio);
  const filename = `${name}-${width}w.webp`;
  const destination = path.join(outputDir, filename);
  const result = await sharp(source).rotate().resize(width, height, { fit: 'cover', position: 'attention', withoutEnlargement: true }).webp({ quality: 76, effort: 6 }).toFile(destination);
  files.push({ width, height: result.height, filename, bytes: result.size });
  const budget = width === budgetWidth ? (result.size > limit ? `ACIMA da meta de ${limit / 1024} KB` : 'OK') : 'fora da largura de referência do orçamento';
  console.log(`${filename}: ${(result.size / 1024).toFixed(1)} KB ${budget}`);
}
const fallback = files.find(file => file.width === 640) ?? files.at(-1);
const srcset = files.map(file => `/assets/img/soulcont/${file.filename} ${file.width}w`).join(', ');
console.log(`\n<img src="/assets/img/soulcont/${fallback.filename}"\n  srcset="${srcset}"\n  sizes="(max-width: 640px) calc(100vw - 40px), 480px"\n  width="${fallback.width}" height="${fallback.height}"\n  alt="DESCREVA A FOTO" loading="lazy" decoding="async">`);
