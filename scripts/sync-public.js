const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const publicDir = path.join(root, "public");

const entriesToCopy = [
  "index.html",
  "about.html",
  "contact.html",
  "product.html",
  "privacy.html",
  "terms.html",
  "styles.css",
  "script.js",
  "motion-init.js",
  "gsap-scroll-animations.js",
  "favicon.ico",
  "robots.txt",
  "sitemap.xml",
  "assets",
];

fs.rmSync(publicDir, { recursive: true, force: true });
fs.mkdirSync(publicDir, { recursive: true });

for (const entry of entriesToCopy) {
  const source = path.join(root, entry);
  const destination = path.join(publicDir, entry);

  if (!fs.existsSync(source)) {
    continue;
  }

  fs.cpSync(source, destination, { recursive: true });
}

console.log(`Synced ${entriesToCopy.length} site entries to public/`);
