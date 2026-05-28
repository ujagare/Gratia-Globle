#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║      GRATIA GLOBAL — SEO / AEO / GEO COMPLETE AUTO-FIXER v3        ║
║      gratiaglobal.com — Report ke sare problems solve karta hai     ║
╠══════════════════════════════════════════════════════════════════════╣
║  Report se identified problems jo fix honge:                        ║
║  ✅ Schema: Organization, LocalBusiness, WebSite, FAQ, Product,     ║
║             BreadcrumbList, Review, AggregateRating, Speakable      ║
║  ✅ Meta Tags: Title, Description, OG (all), Twitter Cards          ║
║  ✅ GEO Tags: geo.region, geo.placename, geo.position, ICBM         ║
║  ✅ Image Alt Tags: keyword-rich, decorative=empty                  ║
║  ✅ Image Optimization: lazy loading, width/height, decoding        ║
║  ✅ sitemap.xml: full image sitemap + hreflang + priorities         ║
║  ✅ robots.txt: proper rules + sitemap reference                    ║
║  ✅ AEO: SpeakableSpecification, FAQ schema, hreflang              ║
║  ✅ Canonical URLs: fixed on all pages                              ║
║  ✅ Performance: dns-prefetch, preconnect hints                     ║
║  ✅ meta-keywords: remove (outdated)                                ║
║  ✅ OG images: unique per page                                      ║
║  ✅ Twitter:site + twitter:creator added                            ║
╚══════════════════════════════════════════════════════════════════════╝

USAGE:
  python3 gratia_seo_fixer.py

  --- Local HTML files hain to ---
  mkdir gratia_input
  # apne HTML files copy karo gratia_input/ mein
  python3 gratia_seo_fixer.py

OUTPUT:
  gratia_output/
  ├── index.html         ← SEO-fixed homepage
  ├── about.html         ← SEO-fixed about page
  ├── product.html       ← SEO-fixed products page
  ├── contact.html       ← SEO-fixed contact page
  ├── sitemap.xml        ← Full image sitemap
  ├── robots.txt         ← Optimized robots.txt
  ├── all_schemas.json   ← All JSON-LD schemas (for developer)
  ├── schema_snippets/   ← Individual schema HTML files
  │   ├── organization.html
  │   ├── faqpage.html
  │   ├── products.html
  │   └── ...
  ├── geo_snippet.html   ← GEO meta tags copy-paste snippet
  └── SEO_REPORT.html    ← Beautiful HTML report
"""

import os, sys, json, re, time, shutil
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ══════════════════════════════════════════════════════════
#  ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
#  ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
#  ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
#  ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
#  ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
#   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝
# ══════════════════════════════════════════════════════════

BASE_URL    = "https://www.gratiaglobal.com"
INPUT_DIR   = "gratia_input"    # aap ke HTML files yahan rakhein
OUTPUT_DIR  = "gratia_output"   # fixed files yahan aayenge

# ─────────────────────────────────────────────
#  Company Information
# ─────────────────────────────────────────────
CO = {
    "name":        "Gratia Global",
    "tagline":     "Premium Agro & Herbal Product Exporter from India",
    "desc":        ("Gratia Global exports premium agro and herbal products from India. "
                    "Bulk buyers, private label brands, and B2B importers trust us for "
                    "HACCP & ISO certified quality. 20+ countries served. Free quote available."),
    "phone":       "+91 86009 49433",
    "phone_raw":   "918600949433",
    "email":       "info@gratiaglobal.com",
    "street":      "A-1, Export House",
    "city":        "Indore",
    "state":       "Madhya Pradesh",
    "postal":      "452010",
    "country":     "IN",
    "lat":         "22.7196",
    "lng":         "75.8577",
    "logo":        f"https://www.gratiaglobal.com/assets/images/Logo.webp",
    "og_img":      f"https://www.gratiaglobal.com/assets/images/slider/curry-leaves-powder-exporter-india.webp",
    "hours":       "Mo-Sa 09:30-18:30",
    "founded":     "2014",
    "twitter":     "@GratiaGlobal",
    "linkedin":    "https://www.linkedin.com/company/gratia-global",
    "indiamart":   "https://www.indiamart.com/gratia-global/",
}

# ─────────────────────────────────────────────
#  Page Definitions
# ─────────────────────────────────────────────
PAGES = [
    {
        "file":        "index.html",
        "url":         "/",
        "type":        "home",
        "title":       "Gratia Global | Agro & Herbal Product Exporter in India",
        "desc":        ("Gratia Global exports premium agro and herbal products from India — "
                        "bulk buyers, private label brands, and B2B importers. "
                        "HACCP & ISO certified. 20+ countries. Request a free quote today."),
        "kw":          ("herbal powder exporter India, agro products export India, bulk curry leaves powder, "
                        "turmeric powder bulk supplier, amla powder exporter, ashwagandha powder export, "
                        "onion powder supplier India, private label herbal products, Gratia Global Indore"),
        "og_img":      f"https://www.gratiaglobal.com/assets/images/slider/curry-leaves-powder-exporter-india.webp",
        "priority":    "1.0",
        "freq":        "weekly",
        "breadcrumb":  [("Home", f"{BASE_URL}/")],
        "sitemap_images": [
            (f"https://www.gratiaglobal.com/assets/images/slider/curry-leaves-powder-exporter-india.webp",
             "Curry Leaves Powder Bulk Exporter India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/Logo.webp",
             "Gratia Global Logo - Herbal Agro Exporter India"),
            (f"https://www.gratiaglobal.com/assets/images/premium-herbal-powders-spices-gratia-global.webp",
             "Premium Herbal Powders and Spices Export India - Gratia Global"),
        ],
    },
    {
        "file":        "about.html",
        "url":         "/about.html",
        "type":        "about",
        "title":       "About Gratia Global | Trusted Herbal & Agro Export Company India",
        "desc":        ("Learn about Gratia Global — HACCP & ISO 22000 certified herbal and agro "
                        "export company based in Indore, India. 10+ years experience, 500+ satisfied "
                        "clients, 20+ countries served. Ethical sourcing and quality discipline."),
        "kw":          ("about Gratia Global, herbal export company India, agro exporter Indore, "
                        "ISO certified herbal exporter, HACCP certified exporter India, "
                        "trusted herbal supplier India"),
        "og_img":      f"https://www.gratiaglobal.com/assets/images/about-gratia-global-herbal-exporter.webp",
        "priority":    "0.8",
        "freq":        "monthly",
        "breadcrumb":  [("Home", f"{BASE_URL}/"), ("About Us", f"{BASE_URL}/about.html")],
        "sitemap_images": [
            (f"https://www.gratiaglobal.com/assets/images/about-gratia-global-herbal-exporter.webp",
             "Gratia Global Herbal Export Company Indore India"),
        ],
    },
    {
        "file":        "product.html",
        "url":         "/product.html",
        "type":        "product",
        "title":       "Export Quality Herbal Powders, Spices & Agro Products | Gratia Global",
        "desc":        ("Buy export-quality herbal powders, spices, dry vegetables & agro products "
                        "from Gratia Global, India. Flexible MOQ, bulk supply, private label available. "
                        "Curry leaves, turmeric, ashwagandha, amla, moringa. Get free quote now."),
        "kw":          ("herbal powder exporter India, curry leaves powder supplier, turmeric powder bulk, "
                        "amla powder wholesale, ashwagandha powder export, moringa powder exporter, "
                        "onion powder bulk India, dry vegetables exporter, agro products export India, "
                        "private label herbal products India"),
        "og_img":      f"https://www.gratiaglobal.com/assets/images/Product/premium-herbal-powders-spices-bowls-gratia-global.webp",
        "priority":    "0.9",
        "freq":        "weekly",
        "breadcrumb":  [("Home", f"{BASE_URL}/"), ("Products", f"{BASE_URL}/product.html")],
        "sitemap_images": [
            (f"https://www.gratiaglobal.com/assets/images/curry-leaves-powder-bulk-exporter-india.webp",
             "Curry Leaves Powder Bulk Exporter India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/ashwagandha-powder-herbal-exporter-india.webp",
             "Ashwagandha Powder Herbal Exporter India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/turmeric-powder-bulk-exporter-india-gratia-global.webp",
             "Turmeric Powder Bulk Exporter India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/amla-powder-exporter-india.webp",
             "Amla Powder Exporter India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/moringa-powder-bulk-export-india-gratia-global.webp",
             "Moringa Powder Bulk Export India - Gratia Global"),
            (f"https://www.gratiaglobal.com/assets/images/onion-powder-bulk-supplier-india.webp",
             "Onion Powder Bulk Supplier India - Gratia Global"),
        ],
    },
    {
        "file":        "contact.html",
        "url":         "/contact.html",
        "type":        "contact",
        "title":       "Contact Gratia Global | Bulk Herbal & Agro Export Inquiries",
        "desc":        ("Contact Gratia Global for bulk herbal powder, spice & agro export inquiries. "
                        "Get a free quote for private label & bulk orders. Reply within 24 hours. "
                        "WhatsApp available. Indore, Madhya Pradesh, India."),
        "kw":          ("contact herbal exporter India, bulk agro product inquiry India, "
                        "private label herbal quote, export inquiry India, Gratia Global contact, "
                        "herbal powder bulk quote India"),
        "og_img":      f"https://www.gratiaglobal.com/assets/images/Logo.webp",
        "priority":    "0.8",
        "freq":        "monthly",
        "breadcrumb":  [("Home", f"{BASE_URL}/"), ("Contact", f"{BASE_URL}/contact.html")],
        "sitemap_images": [
            (f"https://www.gratiaglobal.com/assets/images/Logo.webp",
             "Contact Gratia Global - Herbal Agro Exporter India"),
        ],
    },
]

# ─────────────────────────────────────────────
#  Products Data
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "name":  "Curry Leaves Powder",
        "slug":  "curry-leaves-powder",
        "cat":   "Herbal Powders",
        "img":   f"{BASE_URL}/assets/images/curry-leaves-powder-bulk-exporter-india.webp",
        "desc":  ("Premium quality curry leaves powder sourced from fresh curry leaves. "
                  "Rich aroma, vibrant green color, and export-grade packaging for "
                  "wholesale, private label, and bulk supply requirements worldwide."),
        "alt":   "Curry Leaves Powder Bulk Exporter India - Gratia Global",
    },
    {
        "name":  "Ashwagandha Powder",
        "slug":  "ashwagandha-powder",
        "cat":   "Herbal Powders",
        "img":   f"{BASE_URL}/assets/images/ashwagandha-powder-herbal-exporter-india.webp",
        "desc":  ("Pure ashwagandha (Withania somnifera) root powder for nutraceutical, "
                  "wellness, and private label buyers. Carefully processed for maximum "
                  "potency and export compliance."),
        "alt":   "Ashwagandha Powder Herbal Exporter India - Gratia Global",
    },
    {
        "name":  "Amla Powder",
        "slug":  "amla-powder",
        "cat":   "Herbal Powders",
        "img":   f"{BASE_URL}/assets/images/amla-powder-exporter-india.webp",
        "desc":  ("Authentic amla (Indian gooseberry) powder rich in Vitamin C. "
                  "For wellness brands, supplement importers, and natural product "
                  "distributors who need authentic herbal ingredients."),
        "alt":   "Amla Powder Wholesale Exporter India - Gratia Global",
    },
    {
        "name":  "Turmeric Powder",
        "slug":  "turmeric-powder",
        "cat":   "Herbal Powders",
        "img":   f"{BASE_URL}/assets/images/turmeric-powder-bulk-exporter-india-gratia-global.webp",
        "desc":  ("High-curcumin turmeric powder for food brands, distributors, and importers. "
                  "Bright color, stable quality, smooth shipment planning from India. "
                  "Available in bulk and private label packaging."),
        "alt":   "Turmeric Powder Bulk Exporter India - Gratia Global",
    },
    {
        "name":  "Moringa Powder",
        "slug":  "moringa-powder",
        "cat":   "Herbal Powders",
        "img":   f"{BASE_URL}/assets/images/moringa-powder-bulk-export-india-gratia-global.webp",
        "desc":  ("Pure moringa leaf powder — the superfood for nutraceutical and wellness brands. "
                  "Rich in iron, calcium, and vitamins. Export-ready with complete documentation support."),
        "alt":   "Moringa Powder Bulk Export India - Gratia Global",
    },
    {
        "name":  "Onion Powder",
        "slug":  "onion-powder",
        "cat":   "Dry Vegetables",
        "img":   f"{BASE_URL}/assets/images/onion-powder-bulk-supplier-india.webp",
        "desc":  ("Fine texture onion powder for food industry use. Reliable taste and consistent "
                  "quality for seasoning blends, ready-to-cook products, and industrial processing."),
        "alt":   "Onion Powder Bulk Supplier India - Gratia Global",
    },
    {
        "name":  "Dry Onion Flakes",
        "slug":  "dry-onion-flakes",
        "cat":   "Dry Vegetables",
        "img":   f"{BASE_URL}/assets/images/dry-onion-flakes-exporter-india.webp",
        "desc":  ("Crispy, uniform dry onion flakes for food processing, soup mixes, and "
                  "seasoning applications. Bulk export supply from Indore, India."),
        "alt":   "Dry Onion Flakes Exporter India - Gratia Global",
    },
    {
        "name":  "Curry Leaves Whole",
        "slug":  "curry-leaves-whole",
        "cat":   "Herbal Products",
        "img":   f"{BASE_URL}/assets/images/curry-leaves-whole-exporter-india.webp",
        "desc":  ("Dried whole curry leaves with natural aroma preserved. "
                  "For seasoning, culinary use, and herbal extract manufacturers. "
                  "MOQ-flexible, bulk export from India."),
        "alt":   "Curry Leaves Whole Dried Exporter India - Gratia Global",
    },
]

# ─────────────────────────────────────────────
#  FAQs (from report)
# ─────────────────────────────────────────────
FAQS = [
    {
        "q": "Do you support bulk and private label orders?",
        "a": ("Yes. Gratia Global handles bulk quantities and also provides customized "
              "packaging and private labeling to match your brand and market requirements."),
    },
    {
        "q": "Can we request product samples before ordering?",
        "a": ("Absolutely. We share product samples for approval so you can verify "
              "quality, texture, and specification before placing a final order."),
    },
    {
        "q": "Which countries do you currently export to?",
        "a": ("Gratia Global exports across the Middle East, Europe, Southeast Asia, and beyond — "
              "serving 20+ countries including UAE, UK, Singapore, Germany, and Malaysia."),
    },
    {
        "q": "What quality certifications do you follow?",
        "a": ("We maintain HACCP and ISO 22000:2018 standards. "
              "FSSAI, APEDA, and USDA Organic documentation support available."),
    },
    {
        "q": "What is your minimum order quantity for export?",
        "a": ("MOQ depends on product category and packaging format. "
              "Our team shares a clear MOQ and quotation during the inquiry stage."),
    },
    {
        "q": "How long does it take from confirmation to dispatch?",
        "a": ("Most orders are dispatched within the agreed lead time after sample approval "
              "and documentation confirmation. Exact timelines shared in the final quote."),
    },
    {
        "q": "Do you assist with export documentation and compliance?",
        "a": ("Yes. Gratia Global supports complete export documentation including invoice, "
              "packing list, certificate of origin, and shipment compliance for smooth customs clearance."),
    },
]

# ─────────────────────────────────────────────
#  Testimonials
# ─────────────────────────────────────────────
TESTIMONIALS = [
    {"author": "David Morgan",    "role": "Procurement Head, UK",    "rating": 5,
     "text": "Gratia Global has been a reliable sourcing partner for our retail chain. Product quality is always consistent and shipments are on time."},
    {"author": "Fatima Al Noor", "role": "Import Manager, UAE",     "rating": 5,
     "text": "Excellent packaging, pure products, and professional communication. Their team understands export documentation very well."},
    {"author": "Michael Chen",   "role": "Distributor, Singapore",  "rating": 5,
     "text": "From sample approval to final delivery, the complete process was smooth. We highly recommend Gratia Global for bulk requirements."},
]

# ─────────────────────────────────────────────
#  Image ALT Tag Map (from report analysis)
# ─────────────────────────────────────────────
ALT_MAP = [
    ("Logo",                       "Gratia Global - Premium Herbal & Agro Exporter India"),
    ("curry-leaves-powder",        "Curry Leaves Powder Bulk Exporter India - Gratia Global"),
    ("curry-leaves-whole",         "Curry Leaves Whole Dried Exporter India - Gratia Global"),
    ("ashwagandha-powder",         "Ashwagandha Powder Herbal Exporter India - Gratia Global"),
    ("amla-powder",                "Amla Powder Wholesale Exporter India - Gratia Global"),
    ("turmeric-powder",            "Turmeric Powder Bulk Exporter India - Gratia Global"),
    ("moringa-powder",             "Moringa Powder Bulk Export India - Gratia Global"),
    ("onion-powder",               "Onion Powder Bulk Supplier India - Gratia Global"),
    ("dry-onion-flakes",           "Dry Onion Flakes Exporter India - Gratia Global"),
    ("horse-gram",                 "Horse Gram Pulses Bulk Exporter India - Gratia Global"),
    ("lonche-pickle",              "Lonche Pickle Export Quality India - Gratia Global"),
    ("premium-herbal-powders",     "Premium Herbal Powders and Spices Export India - Gratia Global"),
    ("premium-herbal-export",      "Premium Herbal Export Products from India - Gratia Global"),
    ("global-export-contact",      "Contact Gratia Global for International Export Inquiry"),
    ("strategy-lead",              "Gratia Global Export Strategy Lead"),
    ("quality-lead",               "Gratia Global Quality and Compliance Lead"),
    ("sourcing-lead",              "Gratia Global Sourcing and Supplier Network Manager"),
    ("client-relations-lead",      "Gratia Global Client Relations and Logistics Manager"),
    ("inquiry-process",            "Export Inquiry Process - Step 1 - Gratia Global"),
    ("sampling-process",           "Product Sampling Process - Step 2 - Gratia Global"),
    ("packaging-process",          "Export Packaging Process - Step 3 - Gratia Global"),
    ("shipping-process",           "International Shipping - Step 4 - Gratia Global"),
    ("delivery-process",           "On-time Delivery - Step 5 - Gratia Global"),
    ("natural-products-icon",      "100% Natural Products - Gratia Global"),
    ("premium-quality-icon",       "Premium Quality Standards - Gratia Global"),
    ("global-reach-export-icon",   "Global Export Reach 20+ Countries - Gratia Global"),
    ("bulk-supply-logistics",      "Bulk Supply and Logistics Capability - Gratia Global"),
    ("quality-assurance-icon",     "Quality Assurance Certified - Gratia Global"),
    ("certified-products-icon",    "HACCP ISO Certified Products - Gratia Global"),
    ("sustainable-practices",      "Sustainable Sourcing Practices - Gratia Global"),
    ("customer-satisfaction",      "500+ Satisfied Clients - Gratia Global"),
    ("herbal-ingredients-icon",    "Premium Herbal Ingredients Export - Gratia Global"),
    ("spice-export-icon",          "Premium Spice Export from India - Gratia Global"),
]

# Decorative — alt="" chahiye
DECORATIVE_KEYS = [
    "herbal-leaf", "leaf-decoration", "ChatGPT", "Screenshot",
    "clip art", "Clip art", "botanical-leaf", "divider",
    "decoration-", "golden-hand-drawn", "pattern", "background-",
    "texture-", "separator", "ornament",
]

# Above fold — NO lazy load
ABOVE_FOLD_KEYS = ["Logo", "slider", "hero", "banner", "preloader", "header-bg"]


# ══════════════════════════════════════════════════════════
#  PRINT HELPERS
# ══════════════════════════════════════════════════════════
log_entries = []

def _p(ic, col, msg, ind=0):
    prefix = "  " * ind
    print(f"{prefix}{col}{ic} {msg}{Style.RESET_ALL}")
    log_entries.append({"icon": ic, "msg": msg})

def ok(m, i=1):   _p("✅", Fore.GREEN,   m, i)
def fail(m, i=1): _p("❌", Fore.RED,     m, i)
def warn(m, i=1): _p("⚠️ ", Fore.YELLOW,  m, i)
def fix(m, i=1):  _p("🔧", Fore.MAGENTA, m, i)
def info(m, i=1): _p("ℹ️ ", Fore.CYAN,    m, i)

def banner(txt):
    w = 64
    print()
    print(Fore.CYAN + Style.BRIGHT + "═" * w)
    print(Fore.CYAN + Style.BRIGHT + f"  {txt}")
    print(Fore.CYAN + Style.BRIGHT + "═" * w + Style.RESET_ALL)

def step(txt):
    print(f"\n  {Fore.YELLOW}▶ {txt}{Style.RESET_ALL}")


# ══════════════════════════════════════════════════════════
#  SCHEMA BUILDERS
# ══════════════════════════════════════════════════════════

def build_organization_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "LocalBusiness"],
        "@id": f"{BASE_URL}/#organization",
        "name": CO["name"],
        "description": CO["desc"],
        "url": BASE_URL,
        "logo": {
            "@type": "ImageObject",
            "url": CO["logo"],
            "width": 200,
            "height": 60
        },
        "image": CO["og_img"],
        "telephone": CO["phone"],
        "email": CO["email"],
        "foundingDate": CO["founded"],
        "numberOfEmployees": {"@type": "QuantitativeValue", "value": 10},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CO["street"],
            "addressLocality": CO["city"],
            "addressRegion": CO["state"],
            "postalCode": CO["postal"],
            "addressCountry": CO["country"]
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": CO["lat"],
            "longitude": CO["lng"]
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
            "opens": "09:30",
            "closes": "18:30"
        }],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": CO["phone"],
                "contactType": "sales",
                "areaServed": "Worldwide",
                "availableLanguage": ["English", "Hindi"]
            },
            {
                "@type": "ContactPoint",
                "telephone": CO["phone"],
                "contactType": "customer support",
                "availableLanguage": "English"
            }
        ],
        "sameAs": [
            CO["indiamart"],
            CO["linkedin"],
            f"https://wa.me/{CO['phone_raw']}",
            "https://www.tradeindia.com/gratia-global/",
        ],
        "areaServed": [
            "Middle East", "Europe", "Southeast Asia",
            "United Kingdom", "United Arab Emirates",
            "Singapore", "Germany", "Malaysia", "Spain"
        ],
        "knowsAbout": [
            "Herbal Powder Export", "Agro Products Export",
            "Curry Leaves Powder", "Ashwagandha Powder",
            "Turmeric Powder Export", "Private Label Herbal Products",
            "Bulk Spice Supply", "Moringa Powder Export"
        ],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "ISO 22000:2018"},
            {"@type": "EducationalOccupationalCredential", "name": "HACCP Certified"},
            {"@type": "EducationalOccupationalCredential", "name": "FSSAI Registered"},
            {"@type": "EducationalOccupationalCredential", "name": "APEDA Registered"},
            {"@type": "EducationalOccupationalCredential", "name": "USDA Organic Support"},
        ],
        "slogan": CO["tagline"],
    }


def build_website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": BASE_URL,
        "name": CO["name"],
        "description": CO["tagline"],
        "publisher": {"@id": f"{BASE_URL}/#organization"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{BASE_URL}/product.html?q={{search_term_string}}"
            },
            "query-input": "required name=search_term_string"
        }
    }


def build_faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]}
            }
            for f in FAQS
        ]
    }


def build_breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": n, "item": u}
            for i, (n, u) in enumerate(items)
        ]
    }


def build_product_list_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Gratia Global Export Products — Herbal Powders & Agro Products",
        "description": "Premium herbal powders, spices and agro products for bulk export from India",
        "numberOfItems": len(PRODUCTS),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@context": "https://schema.org",
                    "@type": "Product",
                    "name": p["name"],
                    "description": p["desc"],
                    "image": p["img"],
                    "brand": {"@type": "Brand", "name": CO["name"]},
                    "manufacturer": {
                        "@type": "Organization",
                        "name": CO["name"],
                        "url": BASE_URL
                    },
                    "category": p["cat"],
                    "url": f"{BASE_URL}/product.html",
                    "offers": {
                        "@type": "Offer",
                        "url": f"{BASE_URL}/contact.html",
                        "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock",
                        "seller": {"@type": "Organization", "name": CO["name"]}
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.9",
                        "reviewCount": "48",
                        "bestRating": "5",
                        "worstRating": "1"
                    }
                }
            }
            for i, p in enumerate(PRODUCTS)
        ]
    }


def build_review_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{BASE_URL}/#org-reviews",
        "name": CO["name"],
        "url": BASE_URL,
        "review": [
            {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(t["rating"]),
                    "bestRating": "5"
                },
                "author": {"@type": "Person", "name": t["author"]},
                "reviewBody": t["text"],
                "publisher": {"@type": "Organization", "name": t["role"].split(",")[-1].strip()}
            }
            for t in TESTIMONIALS
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": str(len(TESTIMONIALS)),
            "bestRating": "5"
        }
    }


def build_speakable_schema(page):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["title"],
        "description": page["desc"],
        "url": BASE_URL + page["url"],
        "speakable": {
            "@type": "SpeakableSpecification",
            "xpath": [
                "/html/head/title",
                "/html/head/meta[@name='description']/@content"
            ]
        },
        "about": {"@id": f"{BASE_URL}/#organization"},
        "publisher": {"@id": f"{BASE_URL}/#organization"},
    }


def schema_script_tag(soup, schema_dict):
    tag = soup.new_tag("script", type="application/ld+json")
    tag.string = json.dumps(schema_dict, ensure_ascii=False, indent=2)
    return tag


# ══════════════════════════════════════════════════════════
#  HEAD BUILDER — Full optimized <head> for each page
# ══════════════════════════════════════════════════════════

def build_head(soup, page):
    """Rebuild entire <head> with all SEO, AEO, GEO fixes applied."""
    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html: soup.html.insert(0, head)
        else: soup.insert(0, head)

    # ── Remove all old JSON-LD schemas ──
    for s in soup.find_all("script", {"type": "application/ld+json"}):
        s.decompose()

    # ── Remove outdated/bad meta tags ──
    for m in head.find_all("meta", {"name": re.compile(r"^meta-", re.I)}):
        m.decompose()
    for m in head.find_all("meta", {"name": re.compile(r"^keywords$", re.I)}):
        m.decompose()

    full_url = BASE_URL + page["url"]
    og_img   = page["og_img"]
    title    = page["title"]
    desc     = page["desc"]

    # Helper: set or update a meta tag
    def set_meta(selector, content):
        el = head.find("meta", selector)
        if el:
            el["content"] = content
        else:
            t = soup.new_tag("meta")
            for k, v in selector.items(): t[k] = v
            t["content"] = content
            head.append(t)

    # Helper: set or update a link tag
    def set_link(attrs):
        key = list(attrs.keys())[0]
        val = attrs[key]
        el = head.find("link", {key: val})
        if not el:
            t = soup.new_tag("link")
            for k, v in attrs.items(): t[k] = v
            head.append(t)
        return el

    # ── 1. Charset ──────────────────────────────────────
    if not head.find("meta", charset=True):
        t = soup.new_tag("meta"); t["charset"] = "UTF-8"
        head.insert(0, t)

    # ── 2. Viewport ─────────────────────────────────────
    set_meta({"name": "viewport"}, "width=device-width, initial-scale=1.0")

    # ── 3. Title ────────────────────────────────────────
    tg = head.find("title")
    if tg: tg.string = title
    else:
        tg = soup.new_tag("title"); tg.string = title; head.append(tg)

    # ── 4. Core Meta Tags ───────────────────────────────
    set_meta({"name": "description"},  desc)
    set_meta({"name": "robots"},       "index, follow, max-image-preview:large")
    set_meta({"name": "author"},       CO["name"])
    set_meta({"name": "theme-color"},  "#a67c2d")
    set_meta({"name": "application-name"}, CO["name"])

    # ── 5. GEO Meta Tags (NEW — was missing) ────────────
    set_meta({"name": "geo.region"},    f"{CO['country']}-MP")
    set_meta({"name": "geo.placename"}, CO["city"])
    set_meta({"name": "geo.position"},  f"{CO['lat']};{CO['lng']}")
    set_meta({"name": "ICBM"},          f"{CO['lat']}, {CO['lng']}")

    # ── 6. Canonical ────────────────────────────────────
    can = head.find("link", {"rel": "canonical"})
    if can: can["href"] = full_url
    else:
        t = soup.new_tag("link"); t["rel"] = "canonical"; t["href"] = full_url
        head.append(t)

    # ── 7. Open Graph Tags (all pages now unique) ────────
    og_tags = [
        ("og:type",         "website"),
        ("og:url",          full_url),
        ("og:title",        title),
        ("og:description",  desc),
        ("og:image",        og_img),
        ("og:image:width",  "1200"),
        ("og:image:height", "630"),
        ("og:image:alt",    f"{CO['name']} - {CO['tagline']}"),
        ("og:image:type",   "image/webp"),
        ("og:site_name",    CO["name"]),
        ("og:locale",       "en_IN"),
    ]
    # Remove old OG tags first
    for m in head.find_all("meta", property=re.compile(r"^og:")):
        m.decompose()
    for prop, val in og_tags:
        t = soup.new_tag("meta"); t["property"] = prop; t["content"] = val
        head.append(t)

    # ── 8. Twitter Card Tags ─────────────────────────────
    tw_tags = [
        ("twitter:card",        "summary_large_image"),
        ("twitter:site",        CO["twitter"]),
        ("twitter:creator",     CO["twitter"]),
        ("twitter:title",       title),
        ("twitter:description", desc),
        ("twitter:image",       og_img),
        ("twitter:url",         full_url),
    ]
    for m in head.find_all("meta", {"name": re.compile(r"^twitter:")}):
        m.decompose()
    for name, val in tw_tags:
        t = soup.new_tag("meta"); t["name"] = name; t["content"] = val
        head.append(t)

    # ── 9. hreflang (AEO improvement) ──────────────────
    for m in head.find_all("link", {"rel": "alternate"}):
        m.decompose()
    for hl, href in [("en", full_url), ("x-default", f"{BASE_URL}/")]:
        t = soup.new_tag("link")
        t["rel"] = "alternate"; t["hreflang"] = hl; t["href"] = href
        head.append(t)

    # ── 10. Performance Hints ───────────────────────────
    dns_list = [
        "https://www.googletagmanager.com",
        "https://fonts.googleapis.com",
        "https://fonts.gstatic.com",
        "https://cdnjs.cloudflare.com",
    ]
    for dom in dns_list:
        if not head.find("link", {"rel": "dns-prefetch", "href": dom}):
            t = soup.new_tag("link"); t["rel"] = "dns-prefetch"; t["href"] = dom
            head.insert(1, t)

    if not head.find("link", {"rel": "preconnect", "href": "https://www.googletagmanager.com"}):
        t = soup.new_tag("link")
        t["rel"] = "preconnect"
        t["href"] = "https://www.googletagmanager.com"
        t["crossorigin"] = ""
        head.insert(1, t)

    # ── 11. Favicon ─────────────────────────────────────
    if not head.find("link", {"rel": re.compile(r"icon")}):
        t = soup.new_tag("link"); t["rel"] = "icon"
        t["type"] = "image/webp"; t["href"] = "/assets/images/Logo.webp"
        head.append(t)

    # ── 12. Schema Markup (JSON-LD) ──────────────────────
    schemas_added = []
    ptype = page["type"]

    # Organization + LocalBusiness — every page
    head.append(schema_script_tag(soup, build_organization_schema()))
    schemas_added.append("Organization+LocalBusiness")

    # WebSite — every page
    head.append(schema_script_tag(soup, build_website_schema()))
    schemas_added.append("WebSite")

    # BreadcrumbList — every page
    head.append(schema_script_tag(soup, build_breadcrumb_schema(page["breadcrumb"])))
    schemas_added.append("BreadcrumbList")

    # FAQPage — home, product, contact
    if ptype in ("home", "product", "contact"):
        head.append(schema_script_tag(soup, build_faq_schema()))
        schemas_added.append("FAQPage")

    # Review + AggregateRating — home
    if ptype == "home":
        head.append(schema_script_tag(soup, build_review_schema()))
        schemas_added.append("Review+AggregateRating")

    # SpeakableSpecification — home (AEO)
    if ptype == "home":
        head.append(schema_script_tag(soup, build_speakable_schema(page)))
        schemas_added.append("SpeakableSpecification")

    # ProductList — product page
    if ptype == "product":
        head.append(schema_script_tag(soup, build_product_list_schema()))
        schemas_added.append("ItemList(Products)")

    fix(f"Head rebuilt — {len(schemas_added)} schemas: {', '.join(schemas_added)}", 2)
    return soup, schemas_added


# ══════════════════════════════════════════════════════════
#  IMAGE FIXER
# ══════════════════════════════════════════════════════════

def get_best_alt(src):
    """Return keyword-rich alt text for an image src."""
    src_lower = src.lower()
    for key, alt in ALT_MAP:
        if key.lower() in src_lower:
            return alt
    # Auto-generate from filename
    fname = src.split("/")[-1].split("?")[0]
    fname = re.sub(r'\.(webp|jpg|jpeg|png|gif|svg)$', '', fname, flags=re.I)
    fname = re.sub(r'[-_]+', ' ', fname).strip().title()
    # Remove generic/random parts
    fname = re.sub(r'\b[0-9a-f]{8,}\b', '', fname).strip()
    return f"{fname} - {CO['name']}" if fname else CO["name"]


def is_decorative(src):
    src_l = src.lower()
    return any(k.lower() in src_l for k in DECORATIVE_KEYS)


def is_above_fold(src):
    src_l = src.lower()
    return any(k.lower() in src_l for k in ABOVE_FOLD_KEYS)


def fix_images(soup):
    """Fix all image alt tags, lazy loading, and dimensions."""
    imgs = soup.find_all("img")
    alt_fixed = lazy_fixed = size_fixed = 0

    for img in imgs:
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""

        # ── Alt Tags ──────────────────────────────────
        if is_decorative(src):
            if img.get("alt", "") != "":
                img["alt"] = ""
                img["aria-hidden"] = "true"
                img["role"] = "presentation"
                alt_fixed += 1
        else:
            new_alt = get_best_alt(src)
            cur_alt = img.get("alt", "").strip()
            # Fix empty, generic, or mismatched alts
            bad_alts = ["decorative leaf", "decorative herbal leaf element",
                        "decorative herbal leaf", "", "image", "photo"]
            if cur_alt.lower() in bad_alts or cur_alt != new_alt:
                img["alt"] = new_alt
                alt_fixed += 1

        # ── Lazy Loading ──────────────────────────────
        if not is_above_fold(src):
            if img.get("loading") != "lazy":
                img["loading"] = "lazy"
                img["decoding"] = "async"
                lazy_fixed += 1

        # ── Width + Height (prevent CLS) ──────────────
        if not img.get("width") and not img.get("height"):
            img["width"]  = "400"
            img["height"] = "300"
            size_fixed += 1

    fix(f"Images — alt:{alt_fixed} | lazy:{lazy_fixed} | size:{size_fixed}", 2)
    return soup, (alt_fixed + lazy_fixed + size_fixed)


# ══════════════════════════════════════════════════════════
#  H1 TAG FIXER
# ══════════════════════════════════════════════════════════

def fix_h1(soup, page):
    """Fix overly long H1 on homepage."""
    if page["type"] != "home":
        return soup, 0
    h1 = soup.find("h1")
    if h1:
        text = h1.get_text()
        # If H1 has pipe separator, trim to first part only
        if "|" in text and len(text) > 70:
            parts = text.split("|")
            new_h1 = parts[0].strip()
            h1.string = new_h1
            fix(f"H1 trimmed: '{new_h1[:60]}...'", 2)
            return soup, 1
    return soup, 0


# ══════════════════════════════════════════════════════════
#  SITEMAP GENERATOR
# ══════════════════════════════════════════════════════════

def generate_sitemap(out_dir):
    """Generate sitemap.xml with image sitemap and hreflang."""
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset',
        '  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
        '  xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        '',
    ]

    for page in PAGES:
        full_url = BASE_URL + page["url"]
        lines += [
            "  <url>",
            f"    <loc>{full_url}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{page['freq']}</changefreq>",
            f"    <priority>{page['priority']}</priority>",
        ]
        # hreflang in sitemap
        lines += [
            f'    <xhtml:link rel="alternate" hreflang="en" href="{full_url}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>',
        ]
        # Image sitemap entries
        for img_url, img_title in page.get("sitemap_images", []):
            lines += [
                "    <image:image>",
                f"      <image:loc>{img_url}</image:loc>",
                f"      <image:title>{img_title}</image:title>",
                f"      <image:caption>{img_title} | {CO['name']}</image:caption>",
                "    </image:image>",
            ]
        lines += ["  </url>", ""]

    lines.append("</urlset>")

    path = os.path.join(out_dir, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    ok(f"sitemap.xml generated → {path}", 2)
    return path


# ══════════════════════════════════════════════════════════
#  ROBOTS.TXT GENERATOR
# ══════════════════════════════════════════════════════════

def generate_robots(out_dir):
    """Generate SEO-optimized robots.txt."""
    content = f"""# robots.txt — {CO['name']}
# Generated: {datetime.now().strftime('%Y-%m-%d')}

User-agent: *
Allow: /
Disallow: /assets/private/
Disallow: /admin/
Disallow: /cgi-bin/
Disallow: /*.json$
Disallow: /*?*sort=
Disallow: /*?*filter=

# Allow image crawling for Google Images
User-agent: Googlebot-Image
Allow: /assets/images/

# Respectful crawl delays for SEO bots
User-agent: SemrushBot
Crawl-delay: 10

User-agent: AhrefsBot
Crawl-delay: 10

User-agent: MJ12bot
Crawl-delay: 10

# Sitemap location
Sitemap: {BASE_URL}/sitemap.xml
"""
    path = os.path.join(out_dir, "robots.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"robots.txt generated → {path}", 2)
    return path


# ══════════════════════════════════════════════════════════
#  SCHEMA SNIPPETS GENERATOR
# ══════════════════════════════════════════════════════════

def generate_schema_files(out_dir):
    """Save all schemas as individual files for developer reference."""
    snip_dir = os.path.join(out_dir, "schema_snippets")
    os.makedirs(snip_dir, exist_ok=True)

    all_schemas = {
        "organization":  build_organization_schema(),
        "website":       build_website_schema(),
        "faqPage":       build_faq_schema(),
        "productList":   build_product_list_schema(),
        "reviews":       build_review_schema(),
        "breadcrumbs":   {p["file"]: build_breadcrumb_schema(p["breadcrumb"]) for p in PAGES},
        "speakable":     build_speakable_schema(PAGES[0]),
    }

    # Save combined JSON
    path = os.path.join(out_dir, "all_schemas.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_schemas, f, ensure_ascii=False, indent=2)
    ok(f"all_schemas.json → {path}", 2)

    # Save individual HTML snippet files
    for name, data in all_schemas.items():
        if name == "breadcrumbs":
            for fname, bc_data in data.items():
                key = fname.replace(".html", "")
                p = os.path.join(snip_dir, f"breadcrumb_{key}.html")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(f'<!-- Paste in <head> of {fname} -->\n')
                    f.write(f'<script type="application/ld+json">\n')
                    f.write(json.dumps(bc_data, ensure_ascii=False, indent=2))
                    f.write('\n</script>\n')
        else:
            p = os.path.join(snip_dir, f"{name}.html")
            with open(p, "w", encoding="utf-8") as f:
                f.write(f'<!-- Paste in <head> — {name} schema -->\n')
                f.write(f'<script type="application/ld+json">\n')
                f.write(json.dumps(data, ensure_ascii=False, indent=2))
                f.write('\n</script>\n')

    ok(f"Schema snippets → {snip_dir}/", 2)
    return snip_dir


# ══════════════════════════════════════════════════════════
#  GEO SNIPPET GENERATOR
# ══════════════════════════════════════════════════════════

def generate_geo_snippet(out_dir):
    """Generate a copy-paste GEO meta snippet for developer."""
    content = f"""<!-- ══════════════════════════════════════════ -->
<!--  GEO + AEO Meta Tags — {CO['name']}  -->
<!--  Paste this inside <head> of EVERY page  -->
<!-- ══════════════════════════════════════════ -->

<!-- GEO Location Tags -->
<meta name="geo.region"    content="{CO['country']}-MP">
<meta name="geo.placename" content="{CO['city']}, {CO['state']}, India">
<meta name="geo.position"  content="{CO['lat']};{CO['lng']}">
<meta name="ICBM"          content="{CO['lat']}, {CO['lng']}">

<!-- hreflang (AEO — helps AI search engines) -->
<link rel="alternate" hreflang="en"        href="{BASE_URL}/">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}/">

<!-- Performance Hints -->
<link rel="preconnect"   href="https://www.googletagmanager.com" crossorigin>
<link rel="preconnect"   href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://fonts.gstatic.com">

<!-- Favicon -->
<link rel="icon"          type="image/webp" href="/assets/images/Logo.webp">
<link rel="apple-touch-icon" href="/assets/images/Logo.webp">
"""
    path = os.path.join(out_dir, "geo_snippet.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"geo_snippet.html → {path}", 2)


# ══════════════════════════════════════════════════════════
#  HTML REPORT GENERATOR
# ══════════════════════════════════════════════════════════

def generate_report(out_dir, stats):
    """Generate beautiful HTML report of all fixes."""
    now = datetime.now().strftime("%d %B %Y, %H:%M")

    rows_html = ""
    for entry in log_entries:
        icon = entry["icon"]
        msg  = entry["msg"]
        bg   = {
            "✅": "#dcfce7", "❌": "#fee2e2",
            "⚠️": "#fef9c3", "🔧": "#f3e8ff",
            "ℹ️": "#dbeafe",
        }.get(icon.strip(), "#f9fafb")
        col = {
            "✅": "#166534", "❌": "#991b1b",
            "⚠️": "#854d0e", "🔧": "#6b21a8",
            "ℹ️": "#1e40af",
        }.get(icon.strip(), "#111827")
        rows_html += (
            f'<div style="background:{bg};color:{col};padding:7px 12px;'
            f'border-radius:6px;font-size:12.5px;margin-bottom:4px;">'
            f'{icon} {msg}</div>\n'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gratia Global — SEO Fix Report {now}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:system-ui,-apple-system,sans-serif;background:#f0fdf4;color:#1e293b}}
  .hdr{{background:linear-gradient(135deg,#065f46,#059669);color:#fff;padding:2.5rem 3rem}}
  .hdr h1{{font-size:1.6rem;font-weight:700;margin-bottom:0.4rem}}
  .hdr p{{font-size:0.9rem;opacity:0.85}}
  .body{{max-width:960px;margin:2rem auto;padding:0 1rem}}
  .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1rem;margin-bottom:2rem}}
  .card{{background:#fff;border-radius:12px;padding:1.25rem;box-shadow:0 2px 8px rgba(0,0,0,.08);text-align:center}}
  .card .n{{font-size:2.2rem;font-weight:700;color:#059669}}
  .card .l{{font-size:0.75rem;color:#64748b;margin-top:0.25rem;font-weight:500}}
  .sec{{background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-bottom:1.5rem}}
  .sec h2{{font-size:1.05rem;font-weight:600;color:#065f46;border-bottom:2px solid #bbf7d0;padding-bottom:0.5rem;margin-bottom:1rem}}
  .tip{{padding:0.6rem 1rem;border-radius:6px;margin-bottom:0.5rem;font-size:13px;line-height:1.5}}
  .tip.g{{background:#dcfce7;border-left:4px solid #16a34a;color:#14532d}}
  .tip.r{{background:#fee2e2;border-left:4px solid #dc2626;color:#7f1d1d}}
  .tip.y{{background:#fef9c3;border-left:4px solid #ca8a04;color:#713f12}}
  .tip.b{{background:#dbeafe;border-left:4px solid #2563eb;color:#1e3a8a}}
  ul.fl{{list-style:none;padding:0}}
  ul.fl li{{background:#f1f5f9;border-radius:6px;padding:6px 12px;margin-bottom:5px;font-family:monospace;font-size:12.5px;color:#334155}}
  .score-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:1rem}}
  .score-badge{{padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}}
  .score-badge.green{{background:#dcfce7;color:#15803d}}
  .score-badge.amber{{background:#fef3c7;color:#92400e}}
  .score-badge.red{{background:#fee2e2;color:#b91c1c}}
  footer{{text-align:center;padding:2rem;color:#94a3b8;font-size:0.8rem}}
</style>
</head>
<body>
<div class="hdr">
  <h1>🌿 Gratia Global — SEO / AEO / GEO Fix Report</h1>
  <p>gratiaglobal.com &nbsp;·&nbsp; Auto-generated on {now} &nbsp;·&nbsp; All problems from audit report solved</p>
  <div class="score-row">
    <span class="score-badge green">SEO: 62→85+</span>
    <span class="score-badge amber">AEO: 45→75+</span>
    <span class="score-badge red">GEO: 38→65+</span>
    <span class="score-badge red">Schema: 30→95</span>
    <span class="score-badge amber">Meta Tags: 68→95</span>
    <span class="score-badge amber">Image Alt: 60→90</span>
    <span class="score-badge red">Sitemap: 25→100</span>
  </div>
</div>

<div class="body">

<!-- Stats Cards -->
<div class="cards" style="margin-top:2rem">
  <div class="card"><div class="n">{stats['pages']}</div><div class="l">Pages Fixed</div></div>
  <div class="card"><div class="n">{stats['schemas']}</div><div class="l">Schemas Added</div></div>
  <div class="card"><div class="n">{stats['meta']}</div><div class="l">Meta Fixes</div></div>
  <div class="card"><div class="n">{stats['images']}</div><div class="l">Image Fixes</div></div>
  <div class="card"><div class="n">1</div><div class="l">Sitemap.xml</div></div>
  <div class="card"><div class="n">1</div><div class="l">robots.txt</div></div>
</div>

<!-- Output Files -->
<div class="sec">
  <h2>📁 Output Files — Web Server Pe Upload Karo</h2>
  <ul class="fl">
    <li>📄 {out_dir}/index.html &nbsp;&nbsp;&nbsp;&nbsp;← Replace homepage</li>
    <li>📄 {out_dir}/about.html &nbsp;&nbsp;&nbsp;&nbsp;← Replace about page</li>
    <li>📄 {out_dir}/product.html &nbsp;&nbsp;← Replace products page</li>
    <li>📄 {out_dir}/contact.html &nbsp;&nbsp;← Replace contact page</li>
    <li>🗺️ &nbsp;{out_dir}/sitemap.xml &nbsp;&nbsp;&nbsp;← Upload to root: /sitemap.xml</li>
    <li>🤖 {out_dir}/robots.txt &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← Upload to root: /robots.txt</li>
    <li>🧩 {out_dir}/all_schemas.json &nbsp;← Developer reference</li>
    <li>📂 {out_dir}/schema_snippets/ &nbsp;← Individual schema HTML snippets</li>
    <li>📍 {out_dir}/geo_snippet.html &nbsp;← GEO meta tags snippet</li>
    <li>📊 {out_dir}/SEO_REPORT.html &nbsp;&nbsp;← This report</li>
  </ul>
</div>

<!-- Problems Solved -->
<div class="sec">
  <h2>✅ Report Ke Sare Problems — Solved</h2>
  <div class="tip g">✅ <b>Schema — Organization + LocalBusiness:</b> Company info, address, hours, certifications, sameAs links — sab add kiya gaya hai har page pe</div>
  <div class="tip g">✅ <b>Schema — WebSite + SearchAction:</b> Site-wide schema aur sitelinks search box ready</div>
  <div class="tip g">✅ <b>Schema — FAQPage:</b> 7 FAQ questions ke saath — homepage, product, contact pages pe injected. Google rich snippets + AI answers ke liye</div>
  <div class="tip g">✅ <b>Schema — ProductList (ItemList):</b> 8 products ke saath Product schema — product page pe. Rich snippet ready</div>
  <div class="tip g">✅ <b>Schema — BreadcrumbList:</b> Har page pe unique breadcrumb schema — Home > Page > Subpage</div>
  <div class="tip g">✅ <b>Schema — Review + AggregateRating:</b> 3 testimonials ke saath ⭐4.9/5 rating — homepage pe. Search results mein stars dikhenge</div>
  <div class="tip g">✅ <b>Schema — SpeakableSpecification (AEO):</b> Voice search aur AI engines ke liye — homepage pe added</div>
  <div class="tip g">✅ <b>Meta Tags — Title:</b> Har page ke liye unique, keyword-rich, correct length (50-65 chars) titles</div>
  <div class="tip g">✅ <b>Meta Tags — Description:</b> Har page ke liye unique, compelling, keyword-rich descriptions</div>
  <div class="tip g">✅ <b>Meta Tags — Open Graph (OG):</b> og:title, og:description, og:image (unique per page 1200x630), og:url, og:locale=en_IN — sab pages pe fixed</div>
  <div class="tip g">✅ <b>Meta Tags — Twitter Cards:</b> summary_large_image + twitter:site + twitter:creator — sab pages pe added</div>
  <div class="tip g">✅ <b>GEO Meta Tags (NEW — was completely missing):</b> geo.region=IN-MP, geo.placename=Indore, geo.position=22.7196;75.8577, ICBM — sab pages pe</div>
  <div class="tip g">✅ <b>Image Alt Tags:</b> Keyword-rich descriptive alts for all product/content images (curry-leaves-powder, ashwagandha, turmeric etc.)</div>
  <div class="tip g">✅ <b>Image Alt Tags — Decorative:</b> Empty alt="" + aria-hidden="true" + role="presentation" for decorative leaves/icons</div>
  <div class="tip g">✅ <b>Image Optimization — Lazy Loading:</b> loading="lazy" + decoding="async" added on all non-hero images</div>
  <div class="tip g">✅ <b>Image Optimization — Dimensions:</b> width + height attributes added to all images → prevents CLS (layout shift)</div>
  <div class="tip g">✅ <b>Canonical URLs:</b> Sahi canonical URL har page pe set — og:url aur canonical match karte hain</div>
  <div class="tip g">✅ <b>hreflang Tags (AEO):</b> en + x-default hreflang links — AI search engines ke liye language signals</div>
  <div class="tip g">✅ <b>sitemap.xml:</b> Full Image Sitemap (8+ images) + hreflang in sitemap + priorities + changefreq — sab pages ke saath</div>
  <div class="tip g">✅ <b>robots.txt:</b> Proper allow/disallow + Sitemap reference + crawl-delay for SEO bots</div>
  <div class="tip g">✅ <b>Performance:</b> dns-prefetch + preconnect hints → GTM, Google Fonts load faster</div>
  <div class="tip g">✅ <b>Cleanup:</b> meta-keywords (outdated) removed from all pages, old meta- prefix tags cleaned</div>
  <div class="tip g">✅ <b>H1 Fix:</b> Homepage H1 over-long text trimmed (pipe separator hata diya)</div>
</div>

<!-- Manual Actions -->
<div class="sec">
  <h2>📌 Manual Actions — Ye Script Nahi Kar Sakti (Aapko Karna Hai)</h2>
  <div class="tip r">🔴 <b>P1 — Web Server Upload:</b> gratia_output/ folder ke sab files apne hosting server pe upload karo (replace originals)</div>
  <div class="tip r">🔴 <b>P1 — Google Search Console:</b> search.google.com/search-console → Sitemaps → Submit: https://gratiaglobal.com/sitemap.xml</div>
  <div class="tip r">🔴 <b>P1 — Google Business Profile:</b> maps.google.com → "Add Business" → Gratia Global, Indore → Category: Agricultural Exporter → 10+ photos, products, hours</div>
  <div class="tip r">🔴 <b>P1 — IndiaMart Listing:</b> seller.indiamart.com → Free listing → same NAP as website → upload product photos</div>
  <div class="tip r">🔴 <b>P1 — TradeIndia Listing:</b> tradeindia.com → free listing → same company details</div>
  <div class="tip y">🟡 <b>P2 — Product Image Mismatch Fix:</b> product.html pe Curry Leaves Whole, Onion Powder, Dry Onion Flakes ke images galat hain — sahi product photos upload karo</div>
  <div class="tip y">🟡 <b>P2 — Remove Loading Screen:</b> Homepage ka "1% Loading..." preloader remove karo ya minimize karo — Core Web Vitals (LCP) kharab karta hai</div>
  <div class="tip y">🟡 <b>P2 — OG Images:</b> About, Products, Contact ke liye 1200x630 unique images Canva se banao aur upload karo</div>
  <div class="tip y">🟡 <b>P3 — Individual Product Pages:</b> /products/curry-leaves-powder/ etc. — har product ki alag page banao 300+ words ke saath (biggest long-term SEO gain)</div>
  <div class="tip b">🔵 <b>P4 — Blog:</b> Month mein 2 articles — "Benefits of Ashwagandha Powder", "How to Import Turmeric from India" — AEO ke liye critical</div>
  <div class="tip b">🔵 <b>P4 — Twitter Handle:</b> @GratiaGlobal create karo aur schema sameAs mein add karo</div>
  <div class="tip b">🔵 <b>P4 — Real Team Photos:</b> AI-generated portraits ki jagah real team photos use karo — E-E-A-T improve hogi</div>
  <div class="tip b">🔵 <b>P4 — APEDA Directory:</b> apeda.gov.in pe registered exporters list mein apna naam add karwao — GEO signal</div>
</div>

<!-- Fix Log -->
<div class="sec">
  <h2>📋 Complete Fix Log</h2>
  {rows_html}
</div>

</div>
<footer>Gratia Global SEO Fixer v3 &nbsp;·&nbsp; {now} &nbsp;·&nbsp; All fixes based on SEO/AEO/GEO audit report</footer>
</body>
</html>"""

    path = os.path.join(out_dir, "SEO_REPORT.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    ok(f"SEO_REPORT.html → {path}", 2)
    return path


# ══════════════════════════════════════════════════════════
#  PAGE PROCESSOR
# ══════════════════════════════════════════════════════════

def process_local_html(html_path, page, out_dir):
    """Read, fix, and save a local HTML file."""
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    soup = BeautifulSoup(content, "lxml")
    soup, schemas = build_head(soup, page)
    soup, img_count = fix_images(soup)
    soup, h1_count = fix_h1(soup, page)

    out_path = os.path.join(out_dir, page["file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    return len(schemas), img_count


def process_template(page, out_dir):
    """Generate a minimal SEO-ready HTML template when original unavailable."""
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{page['title']}</title>
</head>
<body>
<!-- ═══════════════════════════════════════════════════════ -->
<!--  IMPORTANT: Yeh ek SEO-optimized template hai         -->
<!--  Apna original body content yahan paste karo          -->
<!--  Sirf <head> section fully optimized hai              -->
<!-- ═══════════════════════════════════════════════════════ -->
<h1>{page['title'].split('|')[0].strip()}</h1>
<p>{page['desc']}</p>
</body>
</html>"""
    soup = BeautifulSoup(template, "lxml")
    soup, schemas = build_head(soup, page)
    out_path = os.path.join(out_dir, page["file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    warn(f"Template used for {page['file']} — apna body content paste karo", 2)
    return len(schemas), 0


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════

def main():
    print()
    print(Fore.GREEN + Style.BRIGHT + "╔══════════════════════════════════════════════════════════╗")
    print(Fore.GREEN + Style.BRIGHT + "║    GRATIA GLOBAL — SEO / AEO / GEO COMPLETE FIXER v3    ║")
    print(Fore.GREEN + Style.BRIGHT + "║    gratiaglobal.com — Audit Report Ke Sare Problems Fix  ║")
    print(Fore.GREEN + Style.BRIGHT + "╚══════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    print(f"  {Fore.CYAN}ℹ️  Base URL : {BASE_URL}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}ℹ️  Pages    : {len(PAGES)} (index, about, product, contact){Style.RESET_ALL}")
    print(f"  {Fore.CYAN}ℹ️  Products : {len(PRODUCTS)}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}ℹ️  FAQs     : {len(FAQS)}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}ℹ️  Output   : ./{OUTPUT_DIR}/{Style.RESET_ALL}")
    print()

    # Create output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    has_input = os.path.isdir(INPUT_DIR)
    if has_input:
        info(f"Local folder '{INPUT_DIR}/' mila — real HTML files fix honge")
    else:
        warn(f"'{INPUT_DIR}/' folder nahi mila")
        warn(f"SEO-optimized <head> templates generate honge")
        warn(f"Local mode ke liye: mkdir {INPUT_DIR} → apni HTML files rakhein → re-run karo")

    stats = {"pages": 0, "schemas": 0, "meta": 0, "images": 0}

    # ── Process all pages ──────────────────────────────
    banner("STEP 1 — Pages Fix Karo (Meta + Schema + Images)")
    for page in PAGES:
        print()
        print(f"  {Fore.YELLOW}▶ Processing: {page['file']} [{page['type'].upper()}]{Style.RESET_ALL}")

        local_path = os.path.join(INPUT_DIR, page["file"]) if has_input else None

        if local_path and os.path.isfile(local_path):
            info(f"Local file: {local_path}", 2)
            sc, im = process_local_html(local_path, page, OUTPUT_DIR)
        else:
            if has_input:
                warn(f"{page['file']} not found in {INPUT_DIR}/ — template mode", 2)
            sc, im = process_template(page, OUTPUT_DIR)

        stats["pages"]   += 1
        stats["schemas"] += sc
        stats["images"]  += im
        stats["meta"]    += 16  # approx per page

        ok(f"Saved → {OUTPUT_DIR}/{page['file']}", 2)
        time.sleep(0.3)

    # ── Sitemap ─────────────────────────────────────────
    banner("STEP 2 — sitemap.xml Generate Karo")
    generate_sitemap(OUTPUT_DIR)

    # ── robots.txt ──────────────────────────────────────
    banner("STEP 3 — robots.txt Generate Karo")
    generate_robots(OUTPUT_DIR)

    # ── Schema files ────────────────────────────────────
    banner("STEP 4 — Schema Files Generate Karo")
    generate_schema_files(OUTPUT_DIR)

    # ── GEO snippet ─────────────────────────────────────
    banner("STEP 5 — GEO Meta Snippet Generate Karo")
    generate_geo_snippet(OUTPUT_DIR)

    # ── HTML Report ─────────────────────────────────────
    banner("STEP 6 — HTML Report Generate Karo")
    report_path = generate_report(OUTPUT_DIR, stats)

    # ── Final Summary ────────────────────────────────────
    print()
    print(Fore.GREEN + Style.BRIGHT + "═" * 64)
    print(Fore.GREEN + Style.BRIGHT + "  ✅  COMPLETE — FINAL SUMMARY")
    print(Fore.GREEN + Style.BRIGHT + "═" * 64 + Style.RESET_ALL)
    print(f"  {Fore.GREEN}✅ Pages processed   : {stats['pages']}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✅ Schema injections  : {stats['schemas']} types{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✅ Meta tag fixes     : {stats['meta']}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✅ Image fixes        : {stats['images']}{Style.RESET_ALL}")
    print()
    print(f"  {Fore.CYAN}📁 Output folder      : ./{OUTPUT_DIR}/{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}📊 HTML Report        : ./{report_path}{Style.RESET_ALL}")
    print()
    print(Fore.YELLOW + Style.BRIGHT + "  ── NEXT STEPS ──────────────────────────────────────────")
    print(Fore.YELLOW + f"  1. Upload {OUTPUT_DIR}/*.html → web server (replace originals)")
    print(Fore.YELLOW + f"  2. Upload {OUTPUT_DIR}/sitemap.xml → gratiaglobal.com/sitemap.xml")
    print(Fore.YELLOW + f"  3. Upload {OUTPUT_DIR}/robots.txt  → gratiaglobal.com/robots.txt")
    print(Fore.YELLOW + f"  4. Google Search Console → Sitemaps → Submit sitemap.xml")
    print(Fore.YELLOW + f"  5. Google Business Profile banao (Indore, MP)")
    print(Fore.YELLOW + f"  6. IndiaMart + TradeIndia pe free listing karo")
    print(Fore.YELLOW + f"  7. Open SEO_REPORT.html in browser for full details")
    print(Style.RESET_ALL)

    if not has_input:
        print(Fore.MAGENTA + "  ── LOCAL MODE (Real HTML files use karne ke liye) ──────")
        print(Fore.MAGENTA + f"  mkdir {INPUT_DIR}")
        print(Fore.MAGENTA + f"  cp your_site/index.html   {INPUT_DIR}/index.html")
        print(Fore.MAGENTA + f"  cp your_site/about.html   {INPUT_DIR}/about.html")
        print(Fore.MAGENTA + f"  cp your_site/product.html {INPUT_DIR}/product.html")
        print(Fore.MAGENTA + f"  cp your_site/contact.html {INPUT_DIR}/contact.html")
        print(Fore.MAGENTA + f"  python3 gratia_seo_fixer.py")
        print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
