const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");
const Module = require("module");

function addNodePath(modulePath) {
  if (!fs.existsSync(modulePath)) return;
  const current = process.env.NODE_PATH ? process.env.NODE_PATH.split(path.delimiter) : [];
  if (!current.includes(modulePath)) {
    process.env.NODE_PATH = [modulePath, ...current].join(path.delimiter);
    Module._initPaths();
  }
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (firstError) {
    const runtimeNodeModules = path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules"
    );

    addNodePath(runtimeNodeModules);

    const pnpmDir = path.join(runtimeNodeModules, ".pnpm");
    if (fs.existsSync(pnpmDir)) {
      const playwrightPkg = fs
        .readdirSync(pnpmDir)
        .find((name) => /^playwright@\d/.test(name));
      if (playwrightPkg) {
        addNodePath(path.join(pnpmDir, playwrightPkg, "node_modules"));
      }
    }

    try {
      return require("playwright");
    } catch {
      const fallback = path.join(runtimeNodeModules, "playwright", "index.js");
      if (fs.existsSync(fallback)) {
        return require(fallback);
      }
    }

    console.error("Playwright não foi encontrado.");
    console.error("Instale Playwright no ambiente Node ou execute com o NODE_PATH do runtime Codex.");
    throw firstError;
  }
}

function walk(dir, results = []) {
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, results);
    if (entry.isFile() && entry.name === "arte.html") results.push(full);
  }
  return results;
}

async function launchBrowser(chromium) {
  const candidates = [
    { channel: "msedge" },
    { channel: "chrome" },
    { executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" },
    { executablePath: "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe" },
    { executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" },
    { executablePath: "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" },
    {},
  ];

  const errors = [];
  for (const candidate of candidates) {
    try {
      if (candidate.executablePath && !fs.existsSync(candidate.executablePath)) continue;
      return await chromium.launch({ headless: true, ...candidate });
    } catch (error) {
      errors.push(error.message);
    }
  }

  throw new Error(`Não foi possível abrir Edge, Chrome ou Chromium do Playwright.\n${errors.join("\n")}`);
}

(async () => {
  const { chromium } = loadPlaywright();
  const base = path.resolve(__dirname, "..");
  const outDir = path.join(base, "07_exportacao", "png");
  fs.mkdirSync(outDir, { recursive: true });

  const htmlFiles = [
    ...walk(path.join(base, "01_posts_feed")),
    ...walk(path.join(base, "02_carrosseis")),
    ...walk(path.join(base, "03_stories")),
  ];

  const browser = await launchBrowser(chromium);
  const page = await browser.newPage({ viewport: { width: 1280, height: 2200 }, deviceScaleFactor: 1 });

  let count = 0;
  for (const file of htmlFiles) {
    await page.goto(pathToFileURL(file).href, { waitUntil: "load" });
    await page.waitForTimeout(250);
    const frames = await page.locator(".creative-frame").all();

    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      const name = await frame.getAttribute("data-export-name");
      const fallbackName = `${path.basename(path.dirname(file))}_${String(i + 1).padStart(2, "0")}.png`;
      const outputPath = path.join(outDir, name || fallbackName);
      await frame.screenshot({ path: outputPath });
      count += 1;
    }
  }

  await browser.close();
  console.log(`Exportação concluída: ${count} PNGs em ${outDir}`);
})();
