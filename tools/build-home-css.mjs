import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceFiles = [
  "assets/css/main.css",
  "assets/css/mediaquery.css",
  "assets/css/cookies.css",
  "assets/css/site-v2.css",
  "assets/css/motion.css",
  "assets/css/hero-background.css",
  "assets/css/soulcont-brand.css",
];

const sections = [];

for (const relativePath of sourceFiles) {
  const absolutePath = path.join(repositoryRoot, relativePath);
  const source = await readFile(absolutePath, "utf8");
  const normalized = source
    .replace(/^\uFEFF/, "")
    .replace(/^@charset\s+["']UTF-8["'];?\s*/i, "")
    .replace(/[ \t]+$/gm, "");

  sections.push(`/* Source: ${relativePath} */\n${normalized.trim()}\n`);
}

const output = `@charset "UTF-8";\n\n${sections.join("\n")}`;
const outputPath = path.join(repositoryRoot, "assets/css/home.bundle.css");

await writeFile(outputPath, output, "utf8");
console.log(`Generated ${path.relative(repositoryRoot, outputPath)} (${Buffer.byteLength(output)} bytes)`);
