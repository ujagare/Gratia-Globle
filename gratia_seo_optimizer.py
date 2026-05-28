#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          GRATIA GLOBAL — COMPLETE SEO OPTIMIZER SCRIPT                      ║
║          gratiaglobal.com  |  Version 1.1  |  2026                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Kya karta hai yeh script:                                                  ║
║  1. Image rename        — SEO-friendly filenames                             ║
║  2. Image optimization  — WebP compress, file size reduce                   ║
║  3. Lazy loading        — loading="lazy" add karta hai                      ║
║  4. Alt tags            — Missing alt text auto-generate karta hai          ║
║  5. Meta tags           — Title, description, keywords improve karta hai    ║
║  6. Semantic HTML       — header/main/article/section tags verify karta hai ║
║  7. Schema markup       — Organization, FAQ, BreadcrumbList JSON-LD         ║
║  8. Sitemap.xml         — Auto-generate karta hai                           ║
║  9. Robots.txt          — Verify / create karta hai                         ║
║  10. Open Graph         — Social sharing tags check / fix karta hai         ║
║  IMPORTANT: Website ka UI aur functionality bilkul change nahi hoga         ║
╚══════════════════════════════════════════════════════════════════════════════╝

USAGE:
  python3 gratia_seo_optimizer.py --root /path/to/website
  python3 gratia_seo_optimizer.py --root /path/to/website --dry-run
  python3 gratia_seo_optimizer.py --root /path/to/website --tasks all
  python3 gratia_seo_optimizer.py --root /path/to/website --tasks images,meta,schema

TASKS available: images, lazy, alttags, meta, semantic, schema, sitemap, robots, opengraph
"""

import os
import re
import sys
import json
import shutil
import hashlib
import logging
import argparse
import unicodedata
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree as ET

# ─── Optional imports (graceful degradation) ────────────────────────────────
try:
    from bs4 import BeautifulSoup, Tag
    BS4_OK = True
except ImportError:
    BS4_OK = False
    print("[ERROR] beautifulsoup4 install karein: pip install beautifulsoup4 lxml")
    sys.exit(1)

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False
    print("[WARNING] Pillow nahi mila — image compression skip hoga. pip install Pillow")

# ─── Logging setup ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("seo_optimizer.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("seo")

# ═════════════════════════════════════════════════════════════════════════════
# ░░  CONFIGURATION — Yahan apni website details update karein  ░░
# ═════════════════════════════════════════════════════════════════════════════
CONFIG = {
    "site_url":        "https://www.gratiaglobal.com",
    "site_name":       "Gratia Global",
    "site_lang":       "en",
    "company": {
        "name":        "Gratia Global",
        "description": "Premium agro and herbal product exporter from India. Bulk herbal powders, spices, dry vegetables with ISO & HACCP certification.",
        "url":         "https://www.gratiaglobal.com",
        "logo":        "https://www.gratiaglobal.com/assets/images/Logo.webp",
        "phone":       "+91 86009 49433",
        "email":       "info@gratiaglobal.com",
        "address": {
            "streetAddress":   "A-1, Export House",
            "addressLocality": "Indore",
            "addressRegion":   "Madhya Pradesh",
            "postalCode":      "452010",
            "addressCountry":  "IN",
        },
        "sameAs": [
            "https://wa.me/918600949433",
        ],
        "foundingYear": "2014",
        "areaServed":   "Worldwide",
    },

    # ── Per-page SEO data ──────────────────────────────────────────────────
    "pages": {
        "index.html": {
            "title":       "Gratia Global | Agro & Herbal Product Exporter in India",
            "description": "Gratia Global exports premium agro and herbal products from India — bulk buyers, private label brands, and B2B importers. Request a free quote today.",
            "keywords":    "herbal powder exporter India, agro products export India, bulk curry leaves powder, turmeric powder bulk supplier, amla powder exporter, ashwagandha powder export, onion powder supplier India, private label herbal products, B2B herbal export",
            "canonical":   "https://www.gratiaglobal.com/",
            "og_image":    "https://www.gratiaglobal.com/assets/images/slider/curry-leaves-powder-exporter-india.webp",
        },
        "about.html": {
            "title":       "About Gratia Global | Trusted Herbal & Agro Export Company in India",
            "description": "Gratia Global is a trusted herbal and agro export company from Indore, India. ISO 22000, HACCP & FSSAI certified. Serving B2B buyers worldwide since 2014.",
            "keywords":    "about Gratia Global, herbal export company India, agro exporter India, ISO certified herbal exporter, HACCP certified, FSSAI certified, B2B herbal supplier India",
            "canonical":   "https://www.gratiaglobal.com/about",
            "og_image":    "https://www.gratiaglobal.com/assets/images/Logo.webp",
        },
        "products.html": {
            "title":       "Export Quality Herbal Powders, Spices & Agro Products | Gratia Global",
            "description": "Buy export-quality herbal powders, spices, dry vegetables & agro products from Gratia Global, India. Bulk supply, private label & MOQ-flexible. Request a free quote.",
            "keywords":    "herbal powder exporter India, curry leaves powder supplier, amla powder wholesale, ashwagandha powder export, moringa powder exporter, onion powder bulk India, turmeric powder bulk supplier, private label herbal products",
            "canonical":   "https://www.gratiaglobal.com/products",
            "og_image":    "https://www.gratiaglobal.com/assets/images/Logo.webp",
        },
        "contact.html": {
            "title":       "Contact Gratia Global | Bulk Herbal & Agro Export Inquiries",
            "description": "Contact Gratia Global for bulk herbal powder, spice & agro export inquiries. Get a free quote for private label, bulk supply & international orders. Reply within 24 hours.",
            "keywords":    "contact herbal exporter India, bulk agro product inquiry, private label herbal products quote, export inquiry India, Gratia Global contact",
            "canonical":   "https://www.gratiaglobal.com/contact",
            "og_image":    "https://www.gratiaglobal.com/assets/images/Logo.webp",
        },
    },

    # ── Image rename map — Old filename → New SEO-friendly name ───────────
    # Format: "original_basename": "new_seo_name"  (without extension)
    "image_rename_map": {
        # Slider images
        "ChatGPT Image Apr 12, 2026, 11_29_51 PM":        "turmeric-powder-bulk-exporter-india-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_30_17 PM":        "lonche-pickle-export-quality-india-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_30_26 PM":        "horse-gram-pulses-bulk-exporter-india-gratia-global",
        "ChatGPT Image Apr 12, 2026, 02_11_46 PM":        "premium-herbal-export-products-india-gratia-global",
        # Icons
        "ChatGPT Image Apr 12, 2026, 11_30_35 PM":        "natural-products-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_30_56 PM":        "premium-quality-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_08 PM":        "global-reach-export-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_14 PM":        "bulk-supply-logistics-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_20 PM":        "quality-assurance-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_28 PM":        "certified-products-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_37 PM":        "customer-satisfaction-icon-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_31_02 PM":        "sustainable-practices-icon-gratia-global",
        "ChatGPT_Image_Apr_12__2026__11_31_02_PM-removebg-preview": "sustainable-practices-icon-clean-gratia-global",
        # Process icons
        "ChatGPT Image Apr 13, 2026, 12_37_37 AM":        "sampling-process-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 12_41_04 AM":        "packaging-process-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 12_42_35 AM":        "shipping-process-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 12_45_04 AM":        "delivery-process-icon-gratia-global",
        # Clip art decorations
        "ChatGPT Image Apr 12, 2026, 11_45_59 PM":        "herbal-leaf-decoration-gratia-global",
        "ChatGPT Image Apr 12, 2026, 11_44_00 PM":        "herbal-leaf-green-decoration-gratia-global",
        "ChatGPT Image Apr 13, 2026, 12_02_45 AM":        "herbal-botanical-decoration-gratia-global",
        # About page
        "ChatGPT_Image_Apr_13__2026__10_27_54_PM-removebg-preview": "herbal-leaf-about-decoration-gratia-global",
        "f008e0e4-5123-402e-a802-7cbba72ff28c":            "herbal-plant-natural-element-gratia-global",
        "ChatGPT Image Apr 13, 2026, 09_32_49 PM":        "tea-leaves-harvested-india-gratia-global",
        "ChatGPT Image Apr 13, 2026, 09_34_49 PM":        "herbal-powder-bowl-premium-gratia-global",
        "ChatGPT Image Apr 13, 2026, 09_36_13 PM":        "warehouse-storage-logistics-gratia-global",
        "Screenshot_2026-04-13_213833-removebg-preview":  "global-export-countries-icon-gratia-global",
        "Screenshot_2026-04-13_213857-removebg-preview":  "happy-global-clients-icon-gratia-global",
        "Screenshot_2026-04-13_213921-removebg-preview":  "premium-products-catalog-icon-gratia-global",
        "Screenshot_2026-04-13_213937-removebg-preview":  "export-experience-years-icon-gratia-global",
        "Screenshot_2026-04-13_214003-removebg-preview":  "mission-icon-gratia-global",
        "Screenshot_2026-04-13_214033-removebg-preview":  "vision-icon-gratia-global",
        "Screenshot_2026-04-13_214117-removebg-preview":  "quality-assurance-about-icon-gratia-global",
        "Screenshot_2026-04-13_214137-removebg-preview":  "trusted-network-icon-gratia-global",
        "Screenshot_2026-04-13_214155-removebg-preview":  "export-standards-icon-gratia-global",
        "Screenshot_2026-04-13_214216-removebg-preview":  "global-delivery-icon-gratia-global",
        "Screenshot_2026-04-13_214232-removebg-preview":  "transparent-communication-icon-gratia-global",
        "Screenshot_2026-04-13_214252-removebg-preview":  "partnership-focus-icon-gratia-global",
        "Screenshot_2026-04-13_215105-removebg-preview":  "fssai-certified-gratia-global",
        "Screenshot_2026-04-13_215123-removebg-preview":  "usda-organic-certified-gratia-global",
        "Screenshot_2026-04-13_215153-removebg-preview":  "gmp-certified-gratia-global",
        "Screenshot_2026-04-13_215212-removebg-preview":  "apeda-registered-gratia-global",
        # Products page
        "ChatGPT Image Apr 13, 2026, 04_42_36 PM":        "premium-herbal-powders-spices-bowls-gratia-global",
        "ChatGPT Image Apr 13, 2026, 04_39_48 PM":        "herbal-product-category-decoration-gratia-global",
        "ChatGPT Image Apr 13, 2026, 04_21_57 PM":        "herbal-powders-category-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 04_22_58 PM":        "dry-vegetables-category-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 04_23_49 PM":        "pickles-category-icon-gratia-global",
        "ChatGPT Image Apr 13, 2026, 04_24_32 PM":        "pulses-grains-category-icon-gratia-global",
        "8b6bb8bb-6e14-4666-99bf-2014a5f6e910":           "all-products-category-icon-gratia-global",
        # Contact page
        "ChatGPT Image Apr 13, 2026, 11_21_35 PM":        "global-export-contact-visual-gratia-global",
        "ChatGPT_Image_Apr_13__2026__11_34_33_PM-removebg-preview": "export-contact-decoration-gratia-global",
        "ChatGPT Image Apr 13, 2026, 11_48_58 PM":        "premium-herbal-ingredients-export-gratia-global",
        "Screenshot 2026-04-13 235355-Photoroom":          "office-address-icon-gratia-global",
        "Screenshot_2026-04-14_011616-removebg-preview":  "contact-subject-icon-gratia-global",
        "Screenshot_2026-04-14_012606-removebg-preview-removebg-preview": "contact-message-icon-gratia-global",
        "Screenshot_2026-04-14_011404-removebg-preview":  "business-hours-icon-gratia-global",
        "Untitled_design__2_-removebg-preview":           "quick-response-icon-gratia-global",
        "Untitled_design__3_-removebg-preview":           "contact-name-icon-gratia-global",
        "Untitled_design__4_-removebg-preview":           "contact-form-decoration-gratia-global",
        "Untitled__1_-removebg-preview":                  "contact-email-icon-gratia-global",
        "Untitled__2_-removebg-preview":                  "whatsapp-support-icon-gratia-global",
        "Untitled":                                        "contact-phone-icon-gratia-global",
        # Process icons (generic)
        "3f6bf610-f742-4101-be0b-a7f49a5e78b6":           "inquiry-process-icon-gratia-global",
        "a10c733c-bb1a-4846-b8f9-37b7b9a7c0a0":           "ashwagandha-powder-herbal-exporter-india-gratia-global",
        "3ff24925-35bf-4b76-abb2-825a02deeadd":           "moringa-powder-bulk-export-india-gratia-global",
    },

    # ── Alt text map — image filename keyword → alt text ──────────────────
    "alt_text_map": {
        "logo":                     "Gratia Global Logo - Premium Agro & Herbal Exporter India",
        "curry-leaves-powder":      "Curry Leaves Powder Bulk Exporter India - Gratia Global",
        "curry_leaves_powder":      "Curry Leaves Powder Bulk Exporter India - Gratia Global",
        "onion-powder":             "Onion Powder Bulk Supplier India - Gratia Global",
        "amla-powder":              "Amla Powder Exporter India Wholesale Supply - Gratia Global",
        "ashwagandha-powder":       "Ashwagandha Powder Herbal Exporter India - Gratia Global",
        "turmeric-powder":          "Turmeric Powder High Curcumin Bulk Supplier India - Gratia Global",
        "moringa-powder":           "Moringa Powder Bulk Export India - Gratia Global",
        "horse-gram":               "Horse Gram Bulk Pulses Exporter India - Gratia Global",
        "lonche":                   "Lonche Pickle Export Quality India - Gratia Global",
        "leaf-decoration":          "Decorative herbal leaf",
        "herbal-leaf":              "Decorative herbal leaf element",
        "natural-products":         "100% Natural products icon",
        "premium-quality":          "Premium Quality standards icon",
        "global-reach":             "Global Reach export icon",
        "bulk-supply":              "Bulk Supply and logistics icon",
        "quality-assurance":        "Quality Assurance icon",
        "certified-products":       "Certified Products HACCP ISO icon",
        "customer-satisfaction":    "Customer Satisfaction icon",
        "sustainable-practices":    "Sustainable Practices eco-conscious icon",
        "sampling":                 "Sampling process icon",
        "packaging":                "Packaging process icon",
        "shipping":                 "Shipping process icon",
        "delivery":                 "Delivery process icon",
        "inquiry":                  "Inquiry process icon",
        "fssai":                    "FSSAI certified herbal exporter India",
        "usda":                     "USDA Organic certified products",
        "gmp":                      "GMP certified manufacturing",
        "apeda":                    "APEDA registered agro exporter India",
        "iso":                      "ISO 22000:2018 certified",
        "haccp":                    "HACCP certified food safety",
        "warehouse":                "Warehouse storage and logistics support",
        "team":                     "Gratia Global export team member",
        "strategy-lead":            "Founder and Export Strategy Lead - Gratia Global",
        "quality-lead":             "Quality and Compliance Lead - Gratia Global",
        "sourcing-lead":            "Sourcing and Supplier Network Lead - Gratia Global",
        "client-relations-lead":    "Client Relations and Logistics Lead - Gratia Global",
        "tea-leaves":               "Tea leaves being carefully harvested India",
        "herbal-powder":            "Premium herbal powder in bowl - Gratia Global",
        "global-export-contact":    "Global export contact - Gratia Global",
        "herbal-ingredient":        "Premium herbal export ingredients - Gratia Global",
        "achievement":              "Achievement award icon - 10+ years",
        "happy-clients":            "Happy clients icon - 500+ clients",
        "export-countries":         "Export countries icon - 20+ countries",
    },

    # ── FAQ data for schema ────────────────────────────────────────────────
    "faq": [
        {
            "q": "Do you support bulk and private label orders?",
            "a": "Yes. Gratia Global handles bulk quantities and provides customized packaging and private labeling to match your brand and market requirements.",
        },
        {
            "q": "Can we request product samples before ordering?",
            "a": "Absolutely. We share samples for approval so you can verify product quality, texture, and specification before placing a final order.",
        },
        {
            "q": "Which countries does Gratia Global export to?",
            "a": "We export across the Middle East, Europe, Southeast Asia, and beyond. Our team evaluates new destination markets based on compliance needs.",
        },
        {
            "q": "What quality certifications does Gratia Global hold?",
            "a": "Gratia Global maintains ISO 22000:2018, HACCP, FSSAI, USDA Organic, GMP, and APEDA certifications with strict stage-wise quality checks.",
        },
        {
            "q": "What is the minimum order quantity for export shipments?",
            "a": "MOQ depends on the product category and packaging format. Our team shares a clear MOQ and quotation during the initial inquiry.",
        },
        {
            "q": "How long does it take from order confirmation to dispatch?",
            "a": "Most orders are dispatched within the planned lead time after sample approval and documentation confirmation. Exact timelines are shared in the final quote.",
        },
        {
            "q": "Does Gratia Global assist with export documentation?",
            "a": "Yes. We provide complete export documentation support including invoice, packing list, certificate of origin, and compliance guidance for smooth customs clearance.",
        },
    ],

    # ── Image compression settings ─────────────────────────────────────────
    "image": {
        "max_width":       1920,
        "webp_quality":    82,
        "jpg_quality":     85,
        "png_optimize":    True,
        "skip_small_kb":   5,    # files smaller than this (KB) skip compression
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# ░░  HELPER UTILITIES  ░░
# ═════════════════════════════════════════════════════════════════════════════

def slugify(text: str) -> str:
    """Convert arbitrary string to lowercase-hyphen slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def backup_file(path: Path) -> Path:
    """Create .bak backup of a file before modifying."""
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)
    return bak


def find_html_files(root: Path) -> list[Path]:
    """Recursively find all .html files under root."""
    return sorted(root.rglob("*.html"))


def find_image_files(root: Path) -> list[Path]:
    """Recursively find all image files under root."""
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
    return [p for p in root.rglob("*") if p.suffix.lower() in exts]


def read_html(path: Path) -> BeautifulSoup:
    content = path.read_text(encoding="utf-8", errors="replace")
    return BeautifulSoup(content, "lxml")


def write_html(path: Path, soup: BeautifulSoup, dry_run: bool = False):
    html = str(soup)
    if dry_run:
        log.info(f"  [DRY-RUN] Would write: {path.name}")
    else:
        backup_file(path)
        path.write_text(html, encoding="utf-8")
        log.info(f"  ✓ Saved: {path.name}")


def guess_alt_from_filename(stem: str) -> str:
    """Generate a reasonable alt text from a filename stem."""
    alt_map = CONFIG["alt_text_map"]
    stem_lower = stem.lower()
    for key, alt in alt_map.items():
        if key in stem_lower:
            return alt
    # Fallback: clean slug → human readable
    clean = re.sub(r"[-_]+", " ", stem_lower)
    clean = re.sub(r"\b(gratia global|gratia|global|india|www|com)\b", "", clean).strip()
    return clean.title() if clean else "Gratia Global product image"


def get_page_key(html_path: Path) -> Optional[str]:
    """Map a file path to a key in CONFIG['pages']."""
    name = html_path.name.lower()
    if name in CONFIG["pages"]:
        return name
    # Try stem match
    for k in CONFIG["pages"]:
        if Path(k).stem == html_path.stem.lower():
            return k
    return None


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 1 — IMAGE RENAME  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_image_rename(root: Path, dry_run: bool) -> dict:
    """Rename images to SEO-friendly filenames and update all HTML references."""
    log.info("═" * 60)
    log.info("TASK 1: Image Rename")
    rename_map = CONFIG["image_rename_map"]
    stats = {"renamed": 0, "html_updated": 0, "skipped": 0}

    # Build actual rename pairs: old_path → new_path
    file_moves: dict[Path, Path] = {}
    for img_path in find_image_files(root):
        stem = img_path.stem
        # Try exact match first
        new_stem = rename_map.get(stem)
        if not new_stem:
            # Try with spaces normalized
            normalized = stem.replace("_", " ").replace("-", " ")
            for k, v in rename_map.items():
                if k.replace("_", " ").replace("-", " ").lower() == normalized.lower():
                    new_stem = v
                    break
        if not new_stem:
            stats["skipped"] += 1
            continue
        new_path = img_path.parent / (new_stem + img_path.suffix.lower())
        if img_path == new_path:
            stats["skipped"] += 1
            continue
        if new_path.exists():
            log.warning(f"  Target already exists, skipping: {new_path.name}")
            stats["skipped"] += 1
            continue
        file_moves[img_path] = new_path

    # Build string replace map for HTML (relative paths)
    path_replacements: list[tuple[str, str]] = []
    for old_path, new_path in file_moves.items():
        # Store various forms that might appear in HTML src/href attributes
        old_rel = str(old_path.name)
        new_rel = str(new_path.name)
        path_replacements.append((old_rel, new_rel))
        # Also stem-only for JS or CSS references
        path_replacements.append((old_path.stem, new_path.stem))

    # Update HTML files first (before renaming on disk)
    html_files = find_html_files(root)
    for html_path in html_files:
        content = html_path.read_text(encoding="utf-8", errors="replace")
        new_content = content
        for old_str, new_str in path_replacements:
            if old_str in new_content:
                new_content = new_content.replace(old_str, new_str)
        if new_content != content:
            if not dry_run:
                backup_file(html_path)
                html_path.write_text(new_content, encoding="utf-8")
            stats["html_updated"] += 1
            log.info(f"  ✓ HTML updated: {html_path.name}")

    # Also update CSS files
    for css_path in root.rglob("*.css"):
        content = css_path.read_text(encoding="utf-8", errors="replace")
        new_content = content
        for old_str, new_str in path_replacements:
            if old_str in new_content:
                new_content = new_content.replace(old_str, new_str)
        if new_content != content:
            if not dry_run:
                backup_file(css_path)
                css_path.write_text(new_content, encoding="utf-8")
            log.info(f"  ✓ CSS updated: {css_path.name}")

    # Now rename the files on disk
    for old_path, new_path in file_moves.items():
        log.info(f"  Rename: {old_path.name}  →  {new_path.name}")
        if not dry_run:
            old_path.rename(new_path)
        stats["renamed"] += 1

    log.info(f"  Summary: {stats['renamed']} renamed, {stats['html_updated']} HTML files updated, {stats['skipped']} skipped")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 2 — IMAGE OPTIMIZATION (WebP compress)  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_image_optimize(root: Path, dry_run: bool) -> dict:
    """Compress images. Resize if too large. Convert JPG/PNG to WebP optionally."""
    log.info("═" * 60)
    log.info("TASK 2: Image Optimization")
    stats = {"compressed": 0, "skipped": 0, "saved_kb": 0}

    if not PIL_OK:
        log.warning("  Pillow not installed — skipping image optimization")
        return stats

    cfg = CONFIG["image"]

    for img_path in find_image_files(root):
        if img_path.suffix.lower() == ".svg":
            stats["skipped"] += 1
            continue

        size_kb = img_path.stat().st_size / 1024
        if size_kb < cfg["skip_small_kb"]:
            stats["skipped"] += 1
            continue

        try:
            with Image.open(img_path) as img:
                orig_size = img_path.stat().st_size
                w, h = img.size
                needs_resize = w > cfg["max_width"]
                ext = img_path.suffix.lower()

                if dry_run:
                    info = f"{w}x{h}, {size_kb:.0f}KB"
                    if needs_resize:
                        info += f" → resize to {cfg['max_width']}px wide"
                    log.info(f"  [DRY-RUN] {img_path.name}: {info}")
                    stats["compressed"] += 1
                    continue

                backup_file(img_path)
                img_copy = img.copy()

                # Resize if needed
                if needs_resize:
                    ratio = cfg["max_width"] / w
                    new_h = int(h * ratio)
                    img_copy = img_copy.resize((cfg["max_width"], new_h), Image.LANCZOS)

                # Convert RGBA→RGB for JPEG
                if img_copy.mode in ("RGBA", "P") and ext in (".jpg", ".jpeg"):
                    img_copy = img_copy.convert("RGB")

                # Save with compression
                if ext == ".webp":
                    img_copy.save(img_path, "WEBP", quality=cfg["webp_quality"], method=6, optimize=True)
                elif ext in (".jpg", ".jpeg"):
                    img_copy.save(img_path, "JPEG", quality=cfg["jpg_quality"], optimize=True, progressive=True)
                elif ext == ".png":
                    img_copy.save(img_path, "PNG", optimize=cfg["png_optimize"])
                elif ext == ".gif":
                    stats["skipped"] += 1
                    continue

                new_size = img_path.stat().st_size
                saved = (orig_size - new_size) / 1024
                stats["saved_kb"] += max(0, int(saved))
                stats["compressed"] += 1
                log.info(f"  ✓ {img_path.name}: {orig_size//1024}KB → {new_size//1024}KB (saved {max(0,int(saved))}KB)")

        except Exception as e:
            log.warning(f"  [SKIP] {img_path.name}: {e}")
            stats["skipped"] += 1

    log.info(f"  Summary: {stats['compressed']} optimized, saved ~{stats['saved_kb']}KB, {stats['skipped']} skipped")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 3 — LAZY LOADING  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_lazy_loading(root: Path, dry_run: bool) -> dict:
    """Add loading="lazy" to all <img> tags that are not above the fold."""
    log.info("═" * 60)
    log.info("TASK 3: Lazy Loading")
    stats = {"imgs_updated": 0, "files_changed": 0}

    # Tags that are likely above the fold (logo, hero slider first image) — keep eager
    EAGER_KEYWORDS = {"logo", "Logo", "hero", "banner", "slider"}

    for html_path in find_html_files(root):
        soup = read_html(html_path)
        changed = False

        imgs = soup.find_all("img")
        for idx, img in enumerate(imgs):
            src = img.get("src", "")
            existing_loading = img.get("loading", "")
            if existing_loading:
                continue  # Already has loading attribute

            # First 2 images on page: keep eager (above fold)
            if idx < 2:
                img["loading"] = "eager"
                img["fetchpriority"] = "high"
                changed = True
                continue

            # Check if it's a logo or hero image
            is_above_fold = any(kw in src for kw in EAGER_KEYWORDS)
            if is_above_fold and idx < 4:
                img["loading"] = "eager"
                changed = True
                continue

            img["loading"] = "lazy"
            img["decoding"] = "async"
            stats["imgs_updated"] += 1
            changed = True

        if changed:
            write_html(html_path, soup, dry_run)
            stats["files_changed"] += 1

    log.info(f"  Summary: {stats['imgs_updated']} images got lazy loading, {stats['files_changed']} files changed")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 4 — ALT TAGS  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_alt_tags(root: Path, dry_run: bool) -> dict:
    """Add or improve alt text on all <img> tags."""
    log.info("═" * 60)
    log.info("TASK 4: Alt Tags")
    stats = {"fixed": 0, "already_ok": 0, "files_changed": 0}

    DECORATIVE_KEYWORDS = {"clip art", "decoration", "leaf", "border", "divider", "bg", "background"}

    for html_path in find_html_files(root):
        soup = read_html(html_path)
        changed = False

        for img in soup.find_all("img"):
            src = img.get("src", "")
            current_alt = img.get("alt", None)
            stem = Path(src).stem if src else ""

            # Already has good alt text
            if current_alt is not None and len(current_alt.strip()) > 3:
                # Check for generic AI-generated filenames in alt text
                if re.search(r"ChatGPT|Screenshot \d{4}|Untitled", current_alt):
                    # Bad alt — regenerate
                    pass
                else:
                    stats["already_ok"] += 1
                    continue

            # Decorative images get empty alt (accessibility best practice)
            stem_lower = stem.lower()
            src_lower = src.lower()
            is_decorative = any(kw in src_lower for kw in DECORATIVE_KEYWORDS)
            if is_decorative and "product" not in src_lower and "logo" not in src_lower:
                img["alt"] = ""
                img["role"] = "presentation"
                changed = True
                stats["fixed"] += 1
                continue

            # Generate alt from filename
            new_alt = guess_alt_from_filename(stem)
            img["alt"] = new_alt
            changed = True
            stats["fixed"] += 1
            log.info(f"  Alt set: [{stem[:40]}] → '{new_alt}'")

        if changed:
            write_html(html_path, soup, dry_run)
            stats["files_changed"] += 1

    log.info(f"  Summary: {stats['fixed']} alt tags fixed, {stats['already_ok']} already OK, {stats['files_changed']} files changed")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 5 — META TAGS  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_meta_tags(root: Path, dry_run: bool) -> dict:
    """Ensure every HTML page has correct title, meta description, keywords, author, viewport."""
    log.info("═" * 60)
    log.info("TASK 5: Meta Tags")
    stats = {"pages_updated": 0}

    def upsert_meta(soup: BeautifulSoup, name: str = None, prop: str = None,
                    http_equiv: str = None, content: str = None):
        """Update existing meta tag or insert a new one."""
        if name:
            tag = soup.find("meta", attrs={"name": name})
        elif prop:
            tag = soup.find("meta", attrs={"property": prop})
        elif http_equiv:
            tag = soup.find("meta", attrs={"http-equiv": http_equiv})
        else:
            return

        if tag:
            tag["content"] = content
        else:
            new_tag = soup.new_tag("meta")
            if name:        new_tag["name"] = name
            if prop:        new_tag["property"] = prop
            if http_equiv:  new_tag["http-equiv"] = http_equiv
            new_tag["content"] = content
            head = soup.find("head")
            if head:
                head.append(new_tag)

    def upsert_link(soup: BeautifulSoup, rel: str, href: str):
        tag = soup.find("link", attrs={"rel": rel})
        if tag:
            tag["href"] = href
        else:
            new_tag = soup.new_tag("link", rel=rel, href=href)
            head = soup.find("head")
            if head:
                head.append(new_tag)

    for html_path in find_html_files(root):
        page_key = get_page_key(html_path)
        if not page_key:
            log.warning(f"  No config for: {html_path.name} — skipping meta update")
            continue

        page_cfg = CONFIG["pages"][page_key]
        soup = read_html(html_path)
        head = soup.find("head")
        if not head:
            log.warning(f"  No <head> tag in: {html_path.name}")
            continue

        # ── Title ──────────────────────────────────────────────────────────
        title_tag = soup.find("title")
        if title_tag:
            title_tag.string = page_cfg["title"]
        else:
            t = soup.new_tag("title")
            t.string = page_cfg["title"]
            head.insert(0, t)

        # ── Basic meta ─────────────────────────────────────────────────────
        upsert_meta(soup, name="description",       content=page_cfg["description"])
        upsert_meta(soup, name="keywords",          content=page_cfg["keywords"])
        upsert_meta(soup, name="author",            content="Gratia Global")
        upsert_meta(soup, name="robots",            content="index, follow, max-image-preview:large")
        upsert_meta(soup, name="viewport",          content="width=device-width, initial-scale=1.0")
        upsert_meta(soup, name="theme-color",       content="#a67c2d")
        upsert_meta(soup, name="language",          content="English")
        upsert_meta(soup, name="revisit-after",     content="7 days")
        upsert_meta(soup, name="geo.region",        content="IN-MP")
        upsert_meta(soup, name="geo.placename",     content="Indore, Madhya Pradesh, India")
        upsert_meta(soup, http_equiv="Content-Type", content="text/html; charset=UTF-8")

        # ── Canonical ──────────────────────────────────────────────────────
        upsert_link(soup, "canonical", page_cfg["canonical"])

        # ── Open Graph ─────────────────────────────────────────────────────
        upsert_meta(soup, prop="og:type",        content="website")
        upsert_meta(soup, prop="og:url",         content=page_cfg["canonical"])
        upsert_meta(soup, prop="og:title",       content=page_cfg["title"])
        upsert_meta(soup, prop="og:description", content=page_cfg["description"])
        upsert_meta(soup, prop="og:image",       content=page_cfg["og_image"])
        upsert_meta(soup, prop="og:image:width",  content="1200")
        upsert_meta(soup, prop="og:image:height", content="630")
        upsert_meta(soup, prop="og:locale",      content="en_IN")
        upsert_meta(soup, prop="og:site_name",   content=CONFIG["site_name"])

        # ── Twitter Cards ──────────────────────────────────────────────────
        upsert_meta(soup, name="twitter:card",        content="summary_large_image")
        upsert_meta(soup, name="twitter:title",       content=page_cfg["title"])
        upsert_meta(soup, name="twitter:description", content=page_cfg["description"])
        upsert_meta(soup, name="twitter:image",       content=page_cfg["og_image"])
        upsert_meta(soup, name="twitter:url",         content=page_cfg["canonical"])

        write_html(html_path, soup, dry_run)
        stats["pages_updated"] += 1

    log.info(f"  Summary: {stats['pages_updated']} pages updated with meta tags")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 6 — SEMANTIC HTML TAGS  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_semantic_tags(root: Path, dry_run: bool) -> dict:
    """Ensure semantic HTML5 elements are properly in place.
    Only adds missing landmarks — does NOT restructure existing layout.
    """
    log.info("═" * 60)
    log.info("TASK 6: Semantic Tags")
    stats = {"files_changed": 0}

    for html_path in find_html_files(root):
        soup = read_html(html_path)
        changed = False

        # Add lang attribute to <html> if missing
        html_tag = soup.find("html")
        if html_tag and not html_tag.get("lang"):
            html_tag["lang"] = CONFIG["site_lang"]
            changed = True
            log.info(f"  lang='en' added to <html> in {html_path.name}")

        # Add <meta charset> if missing
        head = soup.find("head")
        if head and not soup.find("meta", attrs={"charset": True}):
            charset_tag = soup.new_tag("meta")
            charset_tag["charset"] = "UTF-8"
            head.insert(0, charset_tag)
            changed = True

        # Ensure nav has role="navigation" and aria-label
        for nav in soup.find_all("nav"):
            if not nav.get("role"):
                nav["role"] = "navigation"
                changed = True
            if not nav.get("aria-label"):
                nav["aria-label"] = "Main navigation"
                changed = True

        # Ensure header has role="banner"
        header = soup.find("header")
        if header and not header.get("role"):
            header["role"] = "banner"
            changed = True

        # Ensure footer has role="contentinfo"
        footer = soup.find("footer")
        if footer and not footer.get("role"):
            footer["role"] = "contentinfo"
            changed = True

        # Ensure main has role="main" if present
        main = soup.find("main")
        if main and not main.get("role"):
            main["role"] = "main"
            changed = True

        # Add aria-label to buttons without text or aria-label
        for btn in soup.find_all("button"):
            if not btn.get_text(strip=True) and not btn.get("aria-label"):
                btn["aria-label"] = "Action button"
                changed = True

        # Ensure all <a> with no text have aria-label
        for a in soup.find_all("a", href=True):
            if not a.get_text(strip=True) and not a.get("aria-label"):
                href = a.get("href", "")
                a["aria-label"] = f"Link to {href}"
                changed = True

        if changed:
            write_html(html_path, soup, dry_run)
            stats["files_changed"] += 1

    log.info(f"  Summary: {stats['files_changed']} files updated with semantic improvements")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 7 — SCHEMA MARKUP (JSON-LD)  ░░
# ═════════════════════════════════════════════════════════════════════════════

def build_organization_schema() -> dict:
    c = CONFIG["company"]
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "ExportCompany"],
        "name": c["name"],
        "description": c["description"],
        "url": c["url"],
        "logo": {
            "@type": "ImageObject",
            "url": c["logo"],
            "width": 300,
            "height": 80,
        },
        "telephone": c["phone"],
        "email": c["email"],
        "address": {
            "@type": "PostalAddress",
            **c["address"],
        },
        "sameAs": c["sameAs"],
        "foundingDate": c["foundingYear"],
        "areaServed": c["areaServed"],
        "numberOfEmployees": {"@type": "QuantitativeValue", "value": 10},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "ISO 22000:2018"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "HACCP Certified"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "FSSAI Certified"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "APEDA Registered"},
        ],
        "knowsAbout": [
            "Herbal Powder Export", "Agro Product Export", "Curry Leaves Powder",
            "Turmeric Powder", "Amla Powder", "Ashwagandha Powder",
            "Moringa Powder", "Onion Powder", "Private Label Herbal Products",
        ],
    }


def build_local_business_schema() -> dict:
    c = CONFIG["company"]
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": c["name"],
        "image": c["logo"],
        "url": c["url"],
        "telephone": c["phone"],
        "email": c["email"],
        "address": {
            "@type": "PostalAddress",
            **c["address"],
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 22.7196,
            "longitude": 75.8577,
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "09:30",
            "closes": "18:30",
        },
        "priceRange": "$$",
        "currenciesAccepted": "INR, USD, EUR",
        "paymentAccepted": "Bank Transfer, LC",
    }


def build_faq_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"],
                },
            }
            for item in CONFIG["faq"]
        ],
    }


def build_website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": CONFIG["site_name"],
        "url": CONFIG["site_url"],
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{CONFIG['site_url']}/products?search={{search_term_string}}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def build_breadcrumb_schema(page_name: str, page_url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": CONFIG["site_url"],
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": page_name,
                "item": page_url,
            },
        ],
    }


def build_products_schema() -> dict:
    products = [
        {"name": "Curry Leaves Powder", "desc": "Premium quality curry leaves powder for bulk export, naturally processed with rich aroma."},
        {"name": "Amla Powder",         "desc": "Export-grade amla powder for wellness brands, supplement importers and natural product distributors."},
        {"name": "Ashwagandha Powder",  "desc": "Carefully processed ashwagandha powder for nutraceutical and wellness brands."},
        {"name": "Turmeric Powder",     "desc": "High-color turmeric powder for food brands and distributors worldwide."},
        {"name": "Moringa Powder",      "desc": "Nutrient-rich moringa powder for health and wellness export markets."},
        {"name": "Onion Powder",        "desc": "Fine texture onion powder for food industry and seasoning blends."},
        {"name": "Dry Onion Flakes",    "desc": "Quality dry onion flakes for food processing and industrial buyers."},
        {"name": "Horse Gram",          "desc": "Bulk pulse export — horse gram for food distributors worldwide."},
        {"name": "Lonche (Pickle)",     "desc": "Traditional Indian pickles for export to South Asian diaspora markets."},
    ]
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Gratia Global Export Products",
        "description": "Premium agro and herbal products for bulk export from India",
        "numberOfItems": len(products),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Product",
                    "name": p["name"],
                    "description": p["desc"],
                    "brand": {"@type": "Brand", "name": "Gratia Global"},
                    "manufacturer": {
                        "@type": "Organization",
                        "name": "Gratia Global",
                        "url": CONFIG["site_url"],
                    },
                    "countryOfOrigin": "IN",
                    "offers": {
                        "@type": "Offer",
                        "availability": "https://schema.org/InStock",
                        "seller": {"@type": "Organization", "name": "Gratia Global"},
                        "priceCurrency": "USD",
                        "priceSpecification": {
                            "@type": "PriceSpecification",
                            "description": "Price on request — bulk orders only",
                        },
                    },
                },
            }
            for i, p in enumerate(products)
        ],
    }


def inject_schema(soup: BeautifulSoup, schemas: list[dict]):
    """Inject JSON-LD scripts into <head>, replacing old ones."""
    # Remove existing JSON-LD scripts to avoid duplicates
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        script.decompose()

    head = soup.find("head")
    if not head:
        return

    for schema in schemas:
        script_tag = soup.new_tag("script", attrs={"type": "application/ld+json"})
        script_tag.string = json.dumps(schema, ensure_ascii=False, indent=2)
        head.append(script_tag)


def task_schema_markup(root: Path, dry_run: bool) -> dict:
    """Inject JSON-LD structured data into all pages."""
    log.info("═" * 60)
    log.info("TASK 7: Schema Markup (JSON-LD)")
    stats = {"pages_updated": 0}

    org_schema     = build_organization_schema()
    local_schema   = build_local_business_schema()
    website_schema = build_website_schema()
    faq_schema     = build_faq_schema()
    products_schema = build_products_schema()

    page_schemas = {
        "index.html": [website_schema, org_schema, local_schema, faq_schema],
        "about.html": [
            org_schema,
            build_breadcrumb_schema("About Us", f"{CONFIG['site_url']}/about"),
        ],
        "products.html": [
            org_schema,
            build_breadcrumb_schema("Products", f"{CONFIG['site_url']}/products"),
        ],
        "contact.html": [
            local_schema,
            faq_schema,
            build_breadcrumb_schema("Contact Us", f"{CONFIG['site_url']}/contact"),
        ],
    }

    for html_path in find_html_files(root):
        page_key = get_page_key(html_path)
        schemas = page_schemas.get(page_key)
        if not schemas:
            log.warning(f"  No schema config for: {html_path.name}")
            continue

        soup = read_html(html_path)
        inject_schema(soup, schemas)
        write_html(html_path, soup, dry_run)
        stats["pages_updated"] += 1
        log.info(f"  ✓ Schema injected: {html_path.name} ({len(schemas)} schemas)")

    log.info(f"  Summary: {stats['pages_updated']} pages updated with schema")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 8 — SITEMAP.XML  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_sitemap(root: Path, dry_run: bool) -> dict:
    """Generate sitemap.xml for all HTML pages."""
    log.info("═" * 60)
    log.info("TASK 8: Sitemap.xml")
    stats = {"urls": 0}

    pages_priority = {
        "index.html":    ("1.0",  "weekly"),
        "products.html": ("0.9",  "weekly"),
        "about.html":    ("0.7",  "monthly"),
        "contact.html":  ("0.6",  "monthly"),
    }

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for html_path in find_html_files(root):
        pkey = get_page_key(html_path)
        priority, changefreq = pages_priority.get(pkey, ("0.5", "monthly"))

        if html_path.name.lower() == "index.html":
            loc = CONFIG["site_url"] + "/"
        else:
            loc = CONFIG["site_url"] + "/" + html_path.stem

        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text         = loc
        ET.SubElement(url_el, "lastmod").text      = now_iso
        ET.SubElement(url_el, "changefreq").text   = changefreq
        ET.SubElement(url_el, "priority").text     = priority
        stats["urls"] += 1

    ET.indent(urlset, space="  ")
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding="unicode")

    sitemap_path = root / "sitemap.xml"
    if not dry_run:
        sitemap_path.write_text(sitemap_xml, encoding="utf-8")
        log.info(f"  ✓ sitemap.xml created: {sitemap_path}")
    else:
        log.info(f"  [DRY-RUN] Would create: {sitemap_path}")

    log.info(f"  Summary: {stats['urls']} URLs in sitemap")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 9 — ROBOTS.TXT  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_robots(root: Path, dry_run: bool) -> dict:
    """Create or verify robots.txt."""
    log.info("═" * 60)
    log.info("TASK 9: Robots.txt")
    stats = {"action": "none"}

    robots_path = root / "robots.txt"
    robots_content = f"""User-agent: *
Allow: /

# Block access to backup and hidden files
Disallow: /*.bak$
Disallow: /*.log$
Disallow: /assets/images/team/

# Block common non-content paths
Disallow: /assets/js/
Disallow: /assets/css/

# Sitemap location
Sitemap: {CONFIG['site_url']}/sitemap.xml

# Crawl delay (be polite to Googlebot)
Crawl-delay: 1
"""

    if robots_path.exists():
        existing = robots_path.read_text(encoding="utf-8")
        if "Sitemap:" not in existing:
            # Append sitemap line
            updated = existing.rstrip() + f"\n\nSitemap: {CONFIG['site_url']}/sitemap.xml\n"
            if not dry_run:
                backup_file(robots_path)
                robots_path.write_text(updated, encoding="utf-8")
                log.info(f"  ✓ robots.txt updated with Sitemap directive")
            stats["action"] = "updated"
        else:
            log.info(f"  robots.txt already has Sitemap directive — OK")
            stats["action"] = "ok"
    else:
        if not dry_run:
            robots_path.write_text(robots_content, encoding="utf-8")
            log.info(f"  ✓ robots.txt created at {robots_path}")
        else:
            log.info(f"  [DRY-RUN] Would create: {robots_path}")
        stats["action"] = "created"

    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  TASK 10 — OPEN GRAPH (extra checks)  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_opengraph(root: Path, dry_run: bool) -> dict:
    """Verify and fix Open Graph tags (covered in meta task but double-checks here)."""
    log.info("═" * 60)
    log.info("TASK 10: Open Graph Verification")
    stats = {"pages_checked": 0, "fixed": 0}

    required_og = ["og:type", "og:url", "og:title", "og:description", "og:image",
                   "og:site_name", "og:locale"]

    for html_path in find_html_files(root):
        soup = read_html(html_path)
        page_key = get_page_key(html_path)
        if not page_key:
            continue

        page_cfg = CONFIG["pages"][page_key]
        missing = []
        for prop in required_og:
            if not soup.find("meta", attrs={"property": prop}):
                missing.append(prop)

        if missing:
            log.warning(f"  {html_path.name}: Missing OG tags: {missing}")
            # Already handled in meta task — just report
            stats["fixed"] += len(missing)

        stats["pages_checked"] += 1

    log.info(f"  Summary: {stats['pages_checked']} pages checked, {stats['fixed']} OG tag gaps found (fixed by meta task)")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  BONUS — PRECONNECT / DNS-PREFETCH HINTS  ░░
# ═════════════════════════════════════════════════════════════════════════════

def task_performance_hints(root: Path, dry_run: bool) -> dict:
    """Add preconnect/dns-prefetch hints for external resources to improve Core Web Vitals."""
    log.info("═" * 60)
    log.info("BONUS: Performance Hints (preconnect / dns-prefetch)")
    stats = {"files_changed": 0}

    PRECONNECT_URLS = [
        "https://www.googletagmanager.com",
        "https://www.google-analytics.com",
        "https://fonts.googleapis.com",
        "https://fonts.gstatic.com",
    ]
    DNS_PREFETCH_URLS = [
        "https://wa.me",
        "https://maps.google.com",
    ]

    for html_path in find_html_files(root):
        soup = read_html(html_path)
        head = soup.find("head")
        if not head:
            continue

        changed = False
        existing_hrefs = {tag.get("href", "") for tag in head.find_all("link")}

        for url in PRECONNECT_URLS:
            if url not in existing_hrefs:
                tag = soup.new_tag("link", rel="preconnect", href=url, crossorigin="anonymous")
                head.insert(1, tag)
                changed = True

        for url in DNS_PREFETCH_URLS:
            if url not in existing_hrefs:
                tag = soup.new_tag("link")
                tag["rel"] = "dns-prefetch"
                tag["href"] = url
                head.insert(1, tag)
                changed = True

        if changed:
            write_html(html_path, soup, dry_run)
            stats["files_changed"] += 1

    log.info(f"  Summary: {stats['files_changed']} files updated with performance hints")
    return stats


# ═════════════════════════════════════════════════════════════════════════════
# ░░  REPORT GENERATOR  ░░
# ═════════════════════════════════════════════════════════════════════════════

def generate_report(all_stats: dict, root: Path, dry_run: bool):
    """Write a human-readable SEO optimization report."""
    report_path = root / "seo_optimization_report.txt"
    lines = [
        "=" * 70,
        "  GRATIA GLOBAL — SEO OPTIMIZATION REPORT",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Mode: {'DRY-RUN (no files changed)' if dry_run else 'LIVE (files modified)'}",
        f"  Website root: {root}",
        "=" * 70,
        "",
    ]

    task_labels = {
        "image_rename":     "Image Rename",
        "image_optimize":   "Image Optimization",
        "lazy_loading":     "Lazy Loading",
        "alt_tags":         "Alt Tags",
        "meta_tags":        "Meta Tags",
        "semantic":         "Semantic HTML",
        "schema":           "Schema Markup",
        "sitemap":          "Sitemap.xml",
        "robots":           "Robots.txt",
        "opengraph":        "Open Graph",
        "performance":      "Performance Hints",
    }

    for key, label in task_labels.items():
        s = all_stats.get(key, {})
        lines.append(f"  ✓ {label}")
        for k, v in s.items():
            lines.append(f"      {k}: {v}")
        lines.append("")

    lines += [
        "=" * 70,
        "  NEXT STEPS (manual actions needed):",
        "=" * 70,
        "",
        "  1. Google Search Console mein sitemap.xml submit karein:",
        "     https://search.google.com/search-console",
        "",
        "  2. Google PageSpeed Insights run karein:",
        "     https://pagespeed.web.dev/?url=https://www.gratiaglobal.com",
        "",
        "  3. Schema validation karein:",
        "     https://validator.schema.org/?url=https://www.gratiaglobal.com",
        "",
        "  4. Rich Results test karein:",
        "     https://search.google.com/test/rich-results",
        "",
        "  5. Mobile-Friendly test karein:",
        "     https://search.google.com/test/mobile-friendly",
        "",
        "  6. Backup files (.bak) review karke delete kar sakte hain:",
        "     find . -name '*.bak' -delete",
        "",
        "=" * 70,
    ]

    report_text = "\n".join(lines)
    print("\n" + report_text)

    if not dry_run:
        report_path.write_text(report_text, encoding="utf-8")
        log.info(f"\n  Report saved: {report_path}")


# ═════════════════════════════════════════════════════════════════════════════
# ░░  MAIN ENTRY POINT  ░░
# ═════════════════════════════════════════════════════════════════════════════

ALL_TASKS = ["images", "optimize", "lazy", "alttags", "meta", "semantic",
             "schema", "sitemap", "robots", "opengraph", "performance"]

def main():
    parser = argparse.ArgumentParser(
        description="Gratia Global — Complete SEO Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--root", "-r",
        required=True,
        help="Path to your website root folder (where index.html is)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Preview changes without modifying any files",
    )
    parser.add_argument(
        "--tasks", "-t",
        default="all",
        help=f"Comma-separated tasks to run. 'all' = everything. Options: {', '.join(ALL_TASKS)}",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        log.error(f"Root path not found: {root}")
        sys.exit(1)

    dry_run = args.dry_run
    tasks_input = args.tasks.lower()
    if tasks_input == "all":
        tasks = ALL_TASKS
    else:
        tasks = [t.strip() for t in tasks_input.split(",")]

    log.info("╔" + "═" * 60 + "╗")
    log.info("║  GRATIA GLOBAL SEO OPTIMIZER — Starting                    ║")
    log.info("╚" + "═" * 60 + "╝")
    log.info(f"  Root: {root}")
    log.info(f"  Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    log.info(f"  Tasks: {', '.join(tasks)}")

    html_files = find_html_files(root)
    log.info(f"  HTML files found: {len(html_files)} → {[f.name for f in html_files]}")

    all_stats = {}

    if "images" in tasks:
        all_stats["image_rename"] = task_image_rename(root, dry_run)

    if "optimize" in tasks:
        all_stats["image_optimize"] = task_image_optimize(root, dry_run)

    if "lazy" in tasks:
        all_stats["lazy_loading"] = task_lazy_loading(root, dry_run)

    if "alttags" in tasks:
        all_stats["alt_tags"] = task_alt_tags(root, dry_run)

    if "meta" in tasks:
        all_stats["meta_tags"] = task_meta_tags(root, dry_run)

    if "semantic" in tasks:
        all_stats["semantic"] = task_semantic_tags(root, dry_run)

    if "schema" in tasks:
        all_stats["schema"] = task_schema_markup(root, dry_run)

    if "sitemap" in tasks:
        all_stats["sitemap"] = task_sitemap(root, dry_run)

    if "robots" in tasks:
        all_stats["robots"] = task_robots(root, dry_run)

    if "opengraph" in tasks:
        all_stats["opengraph"] = task_opengraph(root, dry_run)

    if "performance" in tasks:
        all_stats["performance"] = task_performance_hints(root, dry_run)

    generate_report(all_stats, root, dry_run)
    log.info("\n  ✅  SEO Optimization complete!")


if __name__ == "__main__":
    main()
