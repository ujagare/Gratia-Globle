import { animate, inView, stagger } from "https://cdn.jsdelivr.net/npm/motion@11.11.13/+esm";

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (prefersReducedMotion) {
  // Respect accessibility settings by skipping motion-heavy effects.
} else {
  const heroTargets = document.querySelectorAll(
    ".hero-copy > *, .about-reference-copy > *, .products-hero-copy > *, .contact-copy > *",
  );

  if (heroTargets.length > 0) {
    animate(
      heroTargets,
      { opacity: [0, 1], y: [22, 0] },
      {
        duration: 0.62,
        delay: stagger(0.06),
        easing: [0.22, 1, 0.36, 1],
      },
    );
  }

  inView(
    ".reveal",
    (element) => {
      animate(
        element,
        { opacity: [0, 1], y: [26, 0], filter: ["blur(4px)", "blur(0px)"] },
        {
          duration: 0.72,
          easing: [0.22, 1, 0.36, 1],
        },
      );
    },
    { margin: "0px 0px -12% 0px" },
  );

  const hoverSelectors = ".button, .testimonial-card, .service-card, .product-card";
  document.querySelectorAll(hoverSelectors).forEach((element) => {
    let hoverInAnimation = null;
    let hoverOutAnimation = null;

    const resetAnimation = () => {
      if (hoverInAnimation) {
        hoverInAnimation.cancel();
        hoverInAnimation = null;
      }

      if (hoverOutAnimation) {
        hoverOutAnimation.cancel();
        hoverOutAnimation = null;
      }
    };

    element.addEventListener("pointerenter", () => {
      resetAnimation();

      hoverInAnimation = animate(
        element,
        { y: -3, scale: 1.01 },
        { duration: 0.2, easing: "ease-out" },
      );
    });

    element.addEventListener("pointerleave", () => {
      resetAnimation();

      hoverOutAnimation = animate(
        element,
        { y: 0, scale: 1 },
        { duration: 0.24, easing: "ease-out" },
      );
    });
  });
}
