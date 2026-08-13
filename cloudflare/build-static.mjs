import fs from "node:fs";
import path from "node:path";

const [sourceArg, outputArg] = process.argv.slice(2);

if (!sourceArg || !outputArg) {
  throw new Error("Usage: node build-cloudflare-static.mjs <source> <output>");
}

const source = path.resolve(sourceArg);
const output = path.resolve(outputArg);
const allowedOutputRoot = `${path.resolve(process.cwd())}${path.sep}`;

if (!output.startsWith(allowedOutputRoot) || output === source) {
  throw new Error(`Refusing to replace output outside ${path.resolve(process.cwd())}`);
}

const publicRoots = [
  "Agradecimento",
  "BLOG",
  "cidades",
  "HTML",
  "landingpages",
  "servicos",
];

const rootFiles = [
  "404.html",
  "contatos.html",
  "index.html",
  "robots.txt",
  "site.webmanifest",
  "sitemap.xml",
];

const textExtensions = new Set([
  ".css",
  ".html",
  ".js",
  ".json",
  ".map",
  ".svg",
  ".txt",
  ".webmanifest",
  ".xml",
]);

const imageExtensions = new Set([
  ".avif",
  ".gif",
  ".ico",
  ".jpeg",
  ".jpg",
  ".png",
  ".webp",
]);

function walk(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

function relative(file) {
  return path.relative(source, file).replaceAll(path.sep, "/");
}

function copy(relativePath) {
  const from = path.join(source, ...relativePath.split("/"));
  const to = path.join(output, ...relativePath.split("/"));
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
}

fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output, { recursive: true });

const selected = new Set(rootFiles);

for (const publicRoot of publicRoots) {
  for (const file of walk(path.join(source, publicRoot))) {
    selected.add(relative(file));
  }
}

const assetFiles = walk(path.join(source, "assets"));
for (const file of assetFiles) {
  const extension = path.extname(file).toLowerCase();
  if (!imageExtensions.has(extension)) {
    selected.add(relative(file));
  }
}

const searchableText = [...selected]
  .filter((file) => textExtensions.has(path.extname(file).toLowerCase()))
  .map((file) => fs.readFileSync(path.join(source, ...file.split("/")), "utf8"))
  .join("\n");

for (const file of assetFiles) {
  const extension = path.extname(file).toLowerCase();
  if (!imageExtensions.has(extension)) continue;

  const rel = relative(file);
  const basename = path.basename(file);
  const encodedBasename = encodeURIComponent(basename);
  const isSoulcontAsset = rel.startsWith("assets/img/soulcont/");
  const isReferenced =
    searchableText.includes(basename) || searchableText.includes(encodedBasename);

  if (isSoulcontAsset || isReferenced) selected.add(rel);
}

for (const file of [...selected].sort()) copy(file);

const indexRoutes = walk(output)
  .filter((file) => path.basename(file).toLowerCase() === "index.html")
  .map((file) => {
    const rel = path.relative(output, file).replaceAll(path.sep, "/");
    const directory = path.posix.dirname(`/${rel}`);
    const route = directory === "/" ? "/" : `${directory}/`;
    return `${route} /${rel} 200`;
  })
  .sort((a, b) => a.localeCompare(b));

fs.writeFileSync(
  path.join(output, "_redirects"),
  `${indexRoutes.join("\n")}\n`,
  "utf8",
);

const files = walk(output);
const totalBytes = files.reduce((sum, file) => sum + fs.statSync(file).size, 0);

console.log(
  JSON.stringify(
    {
      files: files.length,
      totalBytes,
      redirects: indexRoutes.length,
      omittedRootFiles: fs
        .readdirSync(source, { withFileTypes: true })
        .filter((entry) => entry.isFile() && !selected.has(entry.name))
        .map((entry) => entry.name),
    },
    null,
    2,
  ),
);

