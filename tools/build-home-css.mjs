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

// index.html is the only page that loads home.bundle.css (every other page
// links main.css/site-v2.css/motion.css/etc directly, unbundled), so it is
// safe to drop top-level rules that index.html never uses -- doing so never
// touches the source files themselves, which stay served in full elsewhere.
//
// cookies.css, mediaquery.css and hero-background.css are always copied
// through untouched: cookies.css is almost entirely markup injected at
// runtime by cookies.js (innerHTML), so static analysis can't see its
// real usage, and the other two had zero unused top-level rules when this
// was last audited (tools/qa/css_usage_audit.py).
const unfilteredFiles = new Set([
  "assets/css/mediaquery.css",
  "assets/css/cookies.css",
  "assets/css/hero-background.css",
]);

const jsFiles = [
  "assets/js/menu.js",
  "assets/js/cookies.js",
  "assets/js/footer.js",
  "assets/js/motion.js",
  "assets/js/main.js",
  "assets/js/soulcont-brand.js",
];

const tokenPattern = /[.#][a-zA-Z_-][\w-]*/g;

async function collectUsedTokens() {
  const used = new Set();
  const htmlSource = await readFile(path.join(repositoryRoot, "index.html"), "utf8");

  for (const m of htmlSource.matchAll(/class="([^"]*)"/g)) {
    for (const token of m[1].split(/\s+/).filter(Boolean)) used.add("." + token);
  }
  for (const m of htmlSource.matchAll(/id="([^"]*)"/g)) {
    used.add("#" + m[1]);
  }

  for (const relativePath of jsFiles) {
    const jsSource = await readFile(path.join(repositoryRoot, relativePath), "utf8");

    for (const m of jsSource.matchAll(/classList\.(?:add|remove|toggle|contains)\(\s*['"]([^'"]+)['"]/g)) {
      used.add("." + m[1]);
    }
    for (const m of jsSource.matchAll(/querySelector(?:All)?\(\s*['"]([^'"]+)['"]/g)) {
      for (const t of m[1].match(tokenPattern) || []) used.add(t);
    }
    for (const m of jsSource.matchAll(/\.className\s*=\s*['"]([^'"]+)['"]/g)) {
      for (const token of m[1].split(/\s+/).filter(Boolean)) used.add("." + token);
    }
    for (const m of jsSource.matchAll(/getElementById\(\s*['"]([^'"]+)['"]/g)) {
      used.add("#" + m[1]);
    }
    // HTML injected via innerHTML/template literals: class="a b c"
    for (const m of jsSource.matchAll(/class=["']([^"']+)["']/g)) {
      for (const token of m[1].split(/\s+/).filter(Boolean)) used.add("." + token);
    }
    for (const m of jsSource.matchAll(/\bid=["']([^"']+)["']/g)) {
      used.add("#" + m[1]);
    }
  }

  return used;
}

// Removes unused top-level rules in place, preserving the order and
// whitespace of everything else. @-rules (@media, @supports, @keyframes,
// @font-face, ...) are always kept whole and never parsed internally.
function filterCss(css, used) {
  let out = "";
  let dropped = 0;
  const n = css.length;
  let i = 0;

  while (i < n) {
    if (css.startsWith("/*", i)) {
      const end = css.indexOf("*/", i) + 2;
      out += css.slice(i, end);
      i = end;
      continue;
    }

    if (css[i] === "@") {
      let j = i;
      let depth = 0;
      while (j < n) {
        if (css[j] === "{") {
          depth += 1;
        } else if (css[j] === "}") {
          depth -= 1;
          if (depth === 0) {
            j += 1;
            break;
          }
        } else if (css[j] === ";" && depth === 0) {
          j += 1;
          break;
        }
        j += 1;
      }
      out += css.slice(i, j);
      i = j;
      continue;
    }

    if (" \t\r\n".includes(css[i])) {
      out += css[i];
      i += 1;
      continue;
    }

    const brace = css.indexOf("{", i);
    const selector = css.slice(i, brace);
    let depth = 1;
    let k = brace + 1;
    while (depth > 0 && k < n) {
      if (css[k] === "{") depth += 1;
      else if (css[k] === "}") depth -= 1;
      k += 1;
    }
    const ruleText = css.slice(i, k);

    const tokens = selector.match(tokenPattern) || [];
    const keep = tokens.length === 0 || tokens.some((t) => used.has(t));
    if (keep) {
      out += ruleText;
    } else {
      dropped += ruleText.length;
    }
    i = k;
  }

  return { css: out, dropped };
}

const used = await collectUsedTokens();
const sections = [];
let totalDropped = 0;

for (const relativePath of sourceFiles) {
  const absolutePath = path.join(repositoryRoot, relativePath);
  const source = await readFile(absolutePath, "utf8");
  const normalized = source
    .replace(/^﻿/, "")
    .replace(/^@charset\s+["']UTF-8["'];?\s*/i, "")
    .replace(/[ \t]+$/gm, "");

  let filtered = normalized;
  let droppedForFile = 0;
  if (!unfilteredFiles.has(relativePath)) {
    const result = filterCss(normalized, used);
    filtered = result.css;
    droppedForFile = result.dropped;
    totalDropped += droppedForFile;
  }
  console.log(`${relativePath}: dropped ${droppedForFile} bytes of confirmed-unused top-level CSS`);

  sections.push(`/* Source: ${relativePath} */\n${filtered.trim()}\n`);
}

const output = `@charset "UTF-8";\n\n${sections.join("\n")}`;
const outputPath = path.join(repositoryRoot, "assets/css/home.bundle.css");

await writeFile(outputPath, output, "utf8");
console.log(`Generated ${path.relative(repositoryRoot, outputPath)} (${Buffer.byteLength(output)} bytes)`);
console.log(`Total bytes removed vs. plain concatenation: ${totalDropped}`);
