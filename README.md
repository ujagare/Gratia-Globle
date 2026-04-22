# Gratia-Globle

# Gratia Global - Premium Agro & Herbal Products Website

A production-ready, pixel-perfect homepage design for Gratia Global featuring a premium luxury aesthetic with gold gradient accents, soft off-white backgrounds, and elegant typography.

## Design Specifications

- **Desktop Width**: 1440px artboard with 1200px centered content container
- **Grid System**: 12-column grid with 24px gutter
- **Border Radius**: 16px for cards, 12px for buttons
- **Color Palette**:
  - Background: #F8F6F1
  - Beige Sections: #EFEAE2
  - Gold Gradient: linear-gradient(90deg, #C8A14B 0%, #A67C2D 100%)
  - Text Primary: #3B372F
  - Text Muted: #6B6760

## Typography

- **Headings**: Playfair Display (serif)
- **Body Text**: Poppins (sans-serif)
- **Sizes**:
  - Hero Headline: 56px
  - Section Titles: 36px
  - Body: 16px
  - Small Text: 14px
  - Captions: 12px

## Features

1. **Sticky Header** with navigation and CTA button
2. **Hero Section** with two-column layout and gradient text effect
3. **Feature Icons Strip** showcasing key benefits
4. **Product Showcase** with 6-card grid and hover effects
5. **About/Why Choose Split** with stats and icon list
6. **Export Process Timeline** with 5-step visualization
7. **CTA Banner** with gold gradient background
8. **Footer** with newsletter subscription

## Setup Instructions

1. **Add Product Images**:

   - Create an `assets` folder in the root directory
   - Add the following images (recommended size: 400x400px):
     - `hero-spices.jpg` - Hero section image
     - `curry-leaves-powder.jpg`
     - `curry-leaves-whole.jpg`
     - `onion-powder.jpg`
     - `dry-onion-flakes.jpg`
     - `amla-powder.jpg`
     - `turmeric-powder.jpg`

2. **Open the Website**:

   - Simply open `index.html` in your browser
   - No build process required - pure HTML, CSS, and JavaScript

3. **Customize Content**:
   - Edit text content in `index.html`
   - Modify colors and spacing in `styles.css`
   - Adjust interactions in `script.js`

## Image Recommendations

For best results, use high-quality stock images with:

- Warm color grading
- Realistic textures
- Centered composition
- Subtle vignette effect
- Professional food photography style

### Suggested Stock Image Sources:

- Unsplash (free)
- Pexels (free)
- Shutterstock (premium)
- Adobe Stock (premium)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Responsive Design

The website includes responsive breakpoints for:

- Desktop: 1440px+
- Tablet: 768px - 1024px
- Mobile: < 768px

## Accessibility Features

- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- Focus outlines for interactive elements
- Sufficient color contrast ratios

## Performance Optimizations

- Minimal external dependencies (only Google Fonts)
- Optimized CSS with CSS variables
- Smooth scroll behavior
- Intersection Observer for animations
- Efficient event listeners

## Customization Guide

### Changing Colors:

Edit CSS variables in `styles.css`:

```css
:root {
  --gold-start: #c8a14b;
  --gold-end: #a67c2d;
  --bg-primary: #f8f6f1;
  --bg-beige: #efeae2;
  --text-primary: #3b372f;
}
```

### Adding More Products:

Copy a product card in `index.html` and update:

- Image source
- Product name
- Description

### Modifying Sections:

Each section has clear HTML comments for easy identification and modification.

## License

This is a custom design for Gratia Global. All rights reserved.

## Support

For questions or customization requests, please contact the development team.

## Secure Email Setup (Resend)

This project now includes a production-ready backend for contact/newsletter forms via Resend.

### 1) Install dependencies

```bash
npm install
```

### 2) Create environment file

Copy `.env.example` to `.env` and set real values:

- `RESEND_API_KEY`
- `CONTACT_FROM_EMAIL` (must use a verified Resend domain)
- `CONTACT_TO_EMAIL`
- `NEWSLETTER_TO_EMAIL`
- `APP_ORIGIN` (comma-separated allowed origins for production)

### 3) Run server

```bash
npm start
```

### Security included

- Helmet security headers
- IP rate limiting per endpoint
- Honeypot + form timing bot checks
- Origin allowlist enforcement in production
- Server-side validation + sanitization
- No API keys exposed in frontend
