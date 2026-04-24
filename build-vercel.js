const fs = require("fs");
const path = require("path");

const rootDir = __dirname;
const outDir = path.join(rootDir, "public");

const copyEntries = [
  "index.html",
  "about.html",
  "contact.html",
  "product.html",
  "privacy.html",
  "terms.html",
  "styles.css",
  "script.js",
  "gsap-scroll-animations.js",
  "motion-init.js",
  "robots.txt",
  "sitemap.xml",
  "assets",
];

const ensureCleanDir = (dirPath) => {
  fs.rmSync(dirPath, { recursive: true, force: true });
  fs.mkdirSync(dirPath, { recursive: true });
};

const copyEntry = (entryName) => {
  const sourcePath = path.join(rootDir, entryName);
  const targetPath = path.join(outDir, entryName);

  if (!fs.existsSync(sourcePath)) {
    return;
  }

  fs.cpSync(sourcePath, targetPath, { recursive: true });
};

ensureCleanDir(outDir);
copyEntries.forEach(copyEntry);

console.log("Static site copied to /public for Vercel.");
