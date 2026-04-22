/* =========================================================
   GSAP ScrollTrigger — Premium Scroll Animations
   Works across all pages: index, about, product, contact
   ========================================================= */

(function () {
  "use strict";

  if (!window.gsap || !window.ScrollTrigger) {
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  /* ---------- Utility: split text into words wrapped in spans ---------- */
  function splitTextIntoWords(element) {
    const text = element.textContent.trim();
    if (!text) return [];
    const words = text.split(/\s+/);
    element.innerHTML = words
      .map(function (word) {
        return '<span class="gsap-word" style="display:inline-block;overflow:hidden"><span class="gsap-word-inner" style="display:inline-block">' + word + "</span></span>";
      })
      .join(" ");
    return element.querySelectorAll(".gsap-word-inner");
  }

  /* ---------- Utility: split text into individual chars ---------- */
  function splitTextIntoChars(element) {
    const text = element.textContent.trim();
    if (!text) return [];
    element.innerHTML = text
      .split("")
      .map(function (char) {
        if (char === " ") return " ";
        return '<span class="gsap-char" style="display:inline-block;overflow:hidden"><span class="gsap-char-inner" style="display:inline-block">' + char + "</span></span>";
      })
      .join("");
    return element.querySelectorAll(".gsap-char-inner");
  }

  /* ========================
     1. SECTION TITLES — Word-by-word reveal
     ======================== */
  document.querySelectorAll(".section-title, h1, h2").forEach(function (title) {
    // Skip hero h1 (handled by swiper) and already-processed elements
    if (
      title.closest(".hero-slide") ||
      title.closest(".swiper-slide") ||
      title.closest(".site-header") ||
      title.closest(".site-footer, .about-reference-footer, .products-footer, .contact-footer") ||
      title.classList.contains("gsap-processed")
    ) {
      return;
    }

    title.classList.add("gsap-processed");
    var wordInners = splitTextIntoWords(title);

    if (wordInners.length === 0) return;

    gsap.set(wordInners, { yPercent: 110, opacity: 0 });

    ScrollTrigger.create({
      trigger: title,
      start: "top 88%",
      once: true,
      onEnter: function () {
        gsap.to(wordInners, {
          yPercent: 0,
          opacity: 1,
          duration: 0.8,
          ease: "power3.out",
          stagger: 0.04,
        });
      },
    });
  });

  /* ========================
     2. EYEBROW LABELS — Char-by-char reveal with gold underline
     ======================== */
  document.querySelectorAll(".eyebrow").forEach(function (eyebrow) {
    if (
      eyebrow.closest(".hero-slide") ||
      eyebrow.closest(".swiper-slide") ||
      eyebrow.classList.contains("gsap-processed")
    ) {
      return;
    }

    eyebrow.classList.add("gsap-processed");
    var charInners = splitTextIntoChars(eyebrow);

    if (charInners.length === 0) return;

    gsap.set(charInners, { yPercent: 100, opacity: 0 });

    ScrollTrigger.create({
      trigger: eyebrow,
      start: "top 90%",
      once: true,
      onEnter: function () {
        gsap.to(charInners, {
          yPercent: 0,
          opacity: 1,
          duration: 0.5,
          ease: "power2.out",
          stagger: 0.02,
        });
      },
    });
  });

  /* ========================
     3. PARAGRAPHS — Fade-up reveal
     ======================== */
  var paraSelectors = [
    ".hero-text",
    ".about-reference-story-copy p",
    ".about-reference-value p",
    ".contact-hero-text",
    ".products-hero-text",
    ".faq-intro",
    ".testimonials-intro",
    ".about-reference-copy > p",
    ".contact-copy > p",
  ];

  document.querySelectorAll(paraSelectors.join(", ")).forEach(function (para) {
    if (
      para.closest(".hero-slide") ||
      para.closest(".swiper-slide") ||
      para.classList.contains("gsap-processed")
    ) {
      return;
    }

    para.classList.add("gsap-processed");

    gsap.set(para, { y: 30, opacity: 0 });

    ScrollTrigger.create({
      trigger: para,
      start: "top 88%",
      once: true,
      onEnter: function () {
        gsap.to(para, {
          y: 0,
          opacity: 1,
          duration: 0.9,
          ease: "power2.out",
        });
      },
    });
  });

  /* ========================
     4. CARDS — Staggered scale-up reveal
     ======================== */
  var cardGridSelectors = [
    ".trust-grid",
    ".product-grid",
    ".about-reference-stats-grid",
    ".about-reference-benefits-grid",
    ".about-reference-cert-grid",
    ".products-catalog",
    ".contact-quick-grid",
    ".ai-seo-grid",
    ".about-reference-values-panel",
  ];

  cardGridSelectors.forEach(function (gridSelector) {
    document.querySelectorAll(gridSelector).forEach(function (grid) {
      if (grid.classList.contains("gsap-processed")) return;
      grid.classList.add("gsap-processed");

      var cards = grid.querySelectorAll(
        ".trust-card, .product-card, .about-reference-stat, " +
        ".about-reference-benefit, .about-reference-cert-card, " +
        ".product-quote-card, article, .about-reference-value"
      );

      if (cards.length === 0) return;

      gsap.set(cards, { y: 35, opacity: 0 });

      ScrollTrigger.create({
        trigger: grid,
        start: "top 85%",
        once: true,
        onEnter: function () {
          gsap.to(cards, {
            y: 0,
            opacity: 1,
            duration: 1,
            ease: "power2.out",
            stagger: 0.1,
          });
        },
      });
    });
  });

  /* ========================
     5. IMAGES — Clip-path reveal
     ======================== */
  var imageSelectors = [
    ".about-reference-image-shell img",
    ".about-reference-collage-main",
    ".about-reference-collage-top",
    ".about-reference-collage-bottom",
    ".contact-hero-image-wrap img",
    ".products-hero-card img",
    ".products-banner-image",
    ".contact-cta-image",
  ];

  document.querySelectorAll(imageSelectors.join(", ")).forEach(function (img) {
    if (img.classList.contains("gsap-processed")) return;
    img.classList.add("gsap-processed");

    gsap.set(img, {
      clipPath: "inset(15% 15% 15% 15%)",
      opacity: 0,
      scale: 1.08,
    });

    ScrollTrigger.create({
      trigger: img,
      start: "top 85%",
      once: true,
      onEnter: function () {
        gsap.to(img, {
          clipPath: "inset(0% 0% 0% 0%)",
          opacity: 1,
          scale: 1,
          duration: 1.1,
          ease: "power3.out",
        });
      },
    });
  });

  /* ========================
     6. DIVIDERS — Grow width animation
     ======================== */
  document
    .querySelectorAll(
      ".about-reference-divider, .contact-divider, .products-copy-divider, .mini-divider"
    )
    .forEach(function (divider) {
      if (divider.classList.contains("gsap-processed")) return;
      divider.classList.add("gsap-processed");

      gsap.set(divider, { scaleX: 0, transformOrigin: "left center" });

      ScrollTrigger.create({
        trigger: divider,
        start: "top 90%",
        once: true,
        onEnter: function () {
          gsap.to(divider, {
            scaleX: 1,
            duration: 0.8,
            ease: "power2.inOut",
          });
        },
      });
    });

  /* ========================
     7. BUTTONS — Subtle pop-in
     ======================== */
  document
    .querySelectorAll(
      "main .button, .product-quote-button, .contact-submit"
    )
    .forEach(function (btn) {
      if (
        btn.closest(".hero-slide") ||
        btn.closest(".swiper-slide") ||
        btn.closest(".site-header") ||
        btn.classList.contains("gsap-processed")
      ) {
        return;
      }

      btn.classList.add("gsap-processed");

      gsap.set(btn, { y: 18, opacity: 0 });

      ScrollTrigger.create({
        trigger: btn,
        start: "top 92%",
        once: true,
        onEnter: function () {
          gsap.to(btn, {
            y: 0,
            opacity: 1,
            duration: 0.85,
            ease: "power2.out",
          });
        },
      });
    });

  /* ========================
     8. LIST ITEMS — Staggered slide-in
     ======================== */
  var listSelectors = [
    ".about-reference-checks",
    ".contact-info-list",
    ".contact-hero-points",
  ];

  listSelectors.forEach(function (listSel) {
    document.querySelectorAll(listSel).forEach(function (list) {
      if (list.classList.contains("gsap-processed")) return;
      list.classList.add("gsap-processed");

      var items = list.querySelectorAll("li, article, .contact-hero-point, .contact-info-item");

      if (items.length === 0) return;

      gsap.set(items, { x: -40, opacity: 0 });

      ScrollTrigger.create({
        trigger: list,
        start: "top 85%",
        once: true,
        onEnter: function () {
          gsap.to(items, {
            x: 0,
            opacity: 1,
            duration: 0.6,
            ease: "power2.out",
            stagger: 0.1,
          });
        },
      });
    });
  });

  /* ========================
     9. FAQ ITEMS — Staggered reveal
     ======================== */
  document.querySelectorAll(".faq-list, .faq-list-accordion").forEach(function (faqList) {
    if (faqList.classList.contains("gsap-processed")) return;
    faqList.classList.add("gsap-processed");

    var items = faqList.querySelectorAll(".faq-item, .faq-accordion-item");

    if (items.length === 0) return;

    gsap.set(items, { y: 25, opacity: 0 });

    ScrollTrigger.create({
      trigger: faqList,
      start: "top 85%",
      once: true,
      onEnter: function () {
        gsap.to(items, {
          y: 0,
          opacity: 1,
          duration: 0.9,
          ease: "power2.out",
          stagger: 0.1,
        });
      },
    });
  });

  /* ========================
     10. FOOTER — Reveal from bottom
     ======================== */
  document
    .querySelectorAll(
      ".site-footer, .about-reference-footer, .products-footer, .contact-footer"
    )
    .forEach(function (footer) {
      if (footer.classList.contains("gsap-processed")) return;
      footer.classList.add("gsap-processed");

      var children = footer.querySelectorAll(
        ":scope > .container > *, :scope > div > *"
      );

      if (children.length === 0) return;

      gsap.set(children, { y: 30, opacity: 0 });

      ScrollTrigger.create({
        trigger: footer,
        start: "top 90%",
        once: true,
        onEnter: function () {
          gsap.to(children, {
            y: 0,
            opacity: 1,
            duration: 1,
            ease: "power2.out",
            stagger: 0.12,
          });
        },
      });
    });

  /* ========================
     11. HERO SECTIONS (non-swiper) — Parallax on decorative leaves
     ======================== */
  document
    .querySelectorAll(
      ".about-reference-leaf, .contact-leaf, .products-hero-leaf, .hero-leaf"
    )
    .forEach(function (leaf) {
      if (leaf.classList.contains("gsap-processed")) return;
      leaf.classList.add("gsap-processed");

      gsap.to(leaf, {
        y: -60,
        ease: "none",
        scrollTrigger: {
          trigger: leaf.closest("section") || leaf.parentElement,
          start: "top bottom",
          end: "bottom top",
          scrub: 1.2,
        },
      });
    });

  /* ========================
     12. COUNTER ANIMATION — Animate numbers (e.g. 20+, 500+)
     ======================== */
  document.querySelectorAll(".about-reference-stat strong").forEach(function (numEl) {
    if (numEl.classList.contains("gsap-processed")) return;
    numEl.classList.add("gsap-processed");

    var text = numEl.textContent.trim();
    var match = text.match(/^(\d+)(.*)$/);
    if (!match) return;

    var targetNum = parseInt(match[1], 10);
    var suffix = match[2];
    var obj = { val: 0 };

    ScrollTrigger.create({
      trigger: numEl,
      start: "top 88%",
      once: true,
      onEnter: function () {
        gsap.to(obj, {
          val: targetNum,
          duration: 1.6,
          ease: "power2.out",
          onUpdate: function () {
            numEl.textContent = Math.round(obj.val) + suffix;
          },
        });
      },
    });
  });

  /* ========================
     13. TESTIMONIAL CARDS — Stagger on scroll
     ======================== */
  document.querySelectorAll(".testimonials-grid, .testimonials-swiper .swiper-wrapper").forEach(function (grid) {
    if (grid.classList.contains("gsap-processed")) return;
    grid.classList.add("gsap-processed");

    var cards = grid.querySelectorAll(".testimonial-card");
    if (cards.length === 0) return;

    gsap.set(cards, { y: 30, opacity: 0 });

    ScrollTrigger.create({
      trigger: grid,
      start: "top 85%",
      once: true,
      onEnter: function () {
        gsap.to(cards, {
          y: 0,
          opacity: 1,
          duration: 1,
          ease: "power2.out",
          stagger: 0.12,
        });
      },
    });
  });

  /* ========================
     14. CONTACT FORM — Fields slide in sequentially
     ======================== */
  document.querySelectorAll(".contact-form-grid").forEach(function (form) {
    if (form.classList.contains("gsap-processed")) return;
    form.classList.add("gsap-processed");

    var fields = form.querySelectorAll(".contact-field, button[type='submit']");
    if (fields.length === 0) return;

    gsap.set(fields, { x: 30, opacity: 0 });

    ScrollTrigger.create({
      trigger: form,
      start: "top 80%",
      once: true,
      onEnter: function () {
        gsap.to(fields, {
          x: 0,
          opacity: 1,
          duration: 0.5,
          ease: "power2.out",
          stagger: 0.07,
        });
      },
    });
  });

  /* ========================
     15. MAP SECTION — Scale reveal
     ======================== */
  document.querySelectorAll(".contact-map-pane").forEach(function (mapPane) {
    if (mapPane.classList.contains("gsap-processed")) return;
    mapPane.classList.add("gsap-processed");

    gsap.set(mapPane, { scale: 0.9, opacity: 0, borderRadius: "28px" });

    ScrollTrigger.create({
      trigger: mapPane,
      start: "top 85%",
      once: true,
      onEnter: function () {
        gsap.to(mapPane, {
          scale: 1,
          opacity: 1,
          duration: 0.9,
          ease: "power3.out",
        });
      },
    });
  });

  /* ---------- Refresh after images load ---------- */
  window.addEventListener("load", function () {
    ScrollTrigger.refresh();
  });
})();
