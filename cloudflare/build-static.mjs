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
  "INSTAGRAM",
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
  const isReferenced =
    searchableText.includes(basename) || searchableText.includes(encodedBasename);

  if (isReferenced) selected.add(rel);
}

for (const file of [...selected].sort()) copy(file);

// Keep GitHub Pages URL behavior while html_handling remains "none".
// Explicit rules preserve indexed .html URLs and add the extensionless and
// trailing-slash forms that GitHub Pages currently serves.
const htmlFiles = walk(output).filter(
  (file) => path.extname(file).toLowerCase() === ".html",
);

const routes = [];

for (const file of htmlFiles) {
  const rel = path.relative(output, file).replaceAll(path.sep, "/");
  const isIndex = path.basename(rel).toLowerCase() === "index.html";

  if (isIndex) {
    const directory = path.posix.dirname(`/${rel}`);
    if (directory === "/") {
      routes.push({ from: "/", to: `/${rel}`, code: 200 });
      continue;
    }

    routes.push({ from: `${directory}/`, to: `/${rel}`, code: 200 });
    routes.push({ from: directory, to: `${directory}/`, code: 301 });
  } else {
    routes.push({
      from: `/${rel.replace(/\.html$/i, "")}`,
      to: `/${rel}`,
      code: 200,
    });
  }
}

const seen = new Map();
for (const route of routes) {
  const existing = seen.get(route.from);
  if (existing && existing.to !== route.to) {
    throw new Error(
      `Route conflict at "${route.from}": "${existing.to}" vs "${route.to}"`,
    );
  }
  seen.set(route.from, route);
}

const indexRoutes = [...seen.values()]
  .map((route) => `${route.from} ${route.to} ${route.code}`)
  .sort((a, b) => a.localeCompare(b));

if (indexRoutes.length > 2000) {
  throw new Error(
    `_redirects has ${indexRoutes.length} static rules; the limit is 2000`,
  );
}

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
