if (window.Lenis) {
  const lenis = new window.Lenis({
    duration: 1.1,
    smoothWheel: true,
    smoothTouch: false,
    wheelMultiplier: 0.95,
  });

  const raf = (time) => {
    lenis.raf(time);
    window.requestAnimationFrame(raf);
  };

  window.requestAnimationFrame(raf);
}

const siteImages = document.querySelectorAll("img");
const heroBackgrounds = document.querySelectorAll(".hero-slide-background");
const eagerImageSelectors = [
  ".site-header .brand-logo",
  ".about-reference-image-shell img",
  ".products-hero-card img",
  ".contact-hero-image-wrap img",
];
const eagerImages = new Set(
  eagerImageSelectors.flatMap((selector) => Array.from(document.querySelectorAll(selector))),
);

siteImages.forEach((image) => {
  image.setAttribute("decoding", "async");

  if (eagerImages.has(image)) {
    image.setAttribute("loading", "eager");
    image.setAttribute("fetchpriority", "high");
    return;
  }

  image.setAttribute("loading", "lazy");
  image.setAttribute("fetchpriority", "low");
});

const updateHeroBackgroundSources = () => {
  const useMobileImages = window.matchMedia("(max-width: 560px)").matches;

  heroBackgrounds.forEach((background) => {
    const desktopImage = background.getAttribute("data-desktop-image");
    const mobileImage = background.getAttribute("data-mobile-image");
    const selectedImage = useMobileImages && mobileImage ? mobileImage : desktopImage;

    if (selectedImage) {
      background.style.backgroundImage = `url("${selectedImage}")`;
    }
  });
};

updateHeroBackgroundSources();
window.addEventListener("resize", updateHeroBackgroundSources);

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const targetId = link.getAttribute("href");
    const target = targetId ? document.querySelector(targetId) : null;

    if (!target) {
      return;
    }

    event.preventDefault();
    target.scrollIntoView({ behavior: "auto", block: "start" });
  });
});

const header = document.querySelector(".site-header");

window.addEventListener("scroll", () => {
  if (!header) {
    return;
  }

  if (window.scrollY > 32) {
    header.style.boxShadow = "0 16px 34px rgba(85, 57, 16, 0.08)";
  } else {
    header.style.boxShadow = "none";
  }
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
      }
    });
  },
  {
    threshold: 0.12,
    rootMargin: "0px 0px -40px 0px",
  },
);

document.querySelectorAll(".reveal").forEach((element) => {
  observer.observe(element);
});

const allTrackedForms = document.querySelectorAll("form.newsletter-form, form.contact-form-grid");

const ensureFormLoadedAt = (form) => {
  const formLoadedAtInput = form.querySelector('input[name="form_loaded_at"]');
  if (formLoadedAtInput && (!formLoadedAtInput.value || Number.isNaN(Number(formLoadedAtInput.value)))) {
    formLoadedAtInput.value = String(Date.now());
  }
};

const setFormMessage = (form, message, type) => {
  let feedbackElement = form.querySelector(".form-feedback");
  if (!feedbackElement) {
    feedbackElement = document.createElement("p");
    feedbackElement.className = "form-feedback";
    feedbackElement.style.marginTop = "10px";
    feedbackElement.style.fontSize = "0.95rem";
    form.appendChild(feedbackElement);
  }

  feedbackElement.textContent = message;
  feedbackElement.style.color = type === "success" ? "#1f7a3a" : "#b3261e";
};

const submitFormData = async (form) => {
  const endpoint = form.getAttribute("action") || "";
  const formData = new FormData(form);
  const body = new URLSearchParams();

  formData.forEach((value, key) => {
    body.append(key, String(value));
  });

  const response = await fetch(endpoint, {
    method: "POST",
    body,
    headers: {
      Accept: "application/json",
    },
    credentials: "same-origin",
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message = payload && payload.error ? payload.error : "Form submit failed. Please try again.";
    throw new Error(message);
  }

  return payload;
};

allTrackedForms.forEach((form) => {
  ensureFormLoadedAt(form);
});

const newsletterForms = document.querySelectorAll("form.newsletter-form");

newsletterForms.forEach((newsletterForm) => {
  newsletterForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const input = newsletterForm.querySelector('input[type="email"]');
    if (!input) {
      return;
    }

    const email = input.value.trim();
    const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!isValidEmail) {
      input.setCustomValidity("Please enter a valid email address.");
      input.reportValidity();
      setFormMessage(newsletterForm, "Please enter a valid email address.", "error");
      return;
    }

    input.value = email;
    input.setCustomValidity("");
    ensureFormLoadedAt(newsletterForm);

    const submitButton = newsletterForm.querySelector('button[type="submit"]');
    const originalButtonText = submitButton ? submitButton.innerHTML : "";

    try {
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = "Submitting...";
      }

      await submitFormData(newsletterForm);
      newsletterForm.reset();
      ensureFormLoadedAt(newsletterForm);
      setFormMessage(newsletterForm, "Thank you. You have been subscribed successfully.", "success");
    } catch (error) {
      setFormMessage(newsletterForm, error.message, "error");
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
      }
    }
  });
});

const contactForm = document.querySelector("form.contact-form-grid");

if (contactForm) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();
    ensureFormLoadedAt(contactForm);

    const emailInput = contactForm.querySelector('input[name="email"]');
    const nameInput = contactForm.querySelector('input[name="name"]');
    const messageInput = contactForm.querySelector('textarea[name="message"]');

    if (!emailInput || !nameInput || !messageInput) {
      return;
    }

    const email = emailInput.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      emailInput.setCustomValidity("Please enter a valid email address.");
      emailInput.reportValidity();
      setFormMessage(contactForm, "Please enter a valid email address.", "error");
      return;
    }

    emailInput.value = email;
    emailInput.setCustomValidity("");
    nameInput.value = nameInput.value.trim();
    messageInput.value = messageInput.value.trim();

    const submitButton = contactForm.querySelector('button[type="submit"]');
    const originalButtonText = submitButton ? submitButton.innerHTML : "";

    try {
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = "Sending...";
      }

      await submitFormData(contactForm);
      contactForm.reset();
      ensureFormLoadedAt(contactForm);
      setFormMessage(contactForm, "Your message has been sent successfully.", "success");
    } catch (error) {
      setFormMessage(contactForm, error.message, "error");
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
      }
    }
  });
}

const faqAccordionItems = document.querySelectorAll(".faq-accordion-item");

faqAccordionItems.forEach((item) => {
  const trigger = item.querySelector(".faq-question");

  if (!trigger) {
    return;
  }

  trigger.addEventListener("click", () => {
    const isOpen = item.classList.contains("is-open");

    faqAccordionItems.forEach((accordionItem) => {
      const button = accordionItem.querySelector(".faq-question");
      accordionItem.classList.remove("is-open");
      if (button) {
        button.setAttribute("aria-expanded", "false");
      }
    });

    if (!isOpen) {
      item.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
    }
  });
});

const heroSwiperElement = document.querySelector(".hero-swiper");

if (heroSwiperElement && window.Swiper && window.gsap) {
  const heroSlides = Array.from(heroSwiperElement.querySelectorAll(".hero-slide"));

  heroSlides.forEach((slide) => {
    const heroCopy = slide.querySelector(".hero-copy");

    if (!heroCopy) {
      return;
    }

    Array.from(heroCopy.children).forEach((child) => {
      if (child.parentElement && child.parentElement.classList.contains("hero-copy-clip")) {
        return;
      }

      const clip = document.createElement("div");
      clip.className = "hero-copy-clip";
      heroCopy.insertBefore(clip, child);
      clip.appendChild(child);
    });
  });

  const setHeroSlideHiddenState = (slide) => {
    const targets = slide.querySelectorAll(".hero-copy-clip > *");
    if (!targets.length) {
      slide.classList.remove("hero-slide-active");
    } else {
      slide.classList.remove("hero-slide-active");
    }
    window.gsap.set(targets, {
      yPercent: 120,
      opacity: 0,
    });
  };

  const animateHeroSlide = (slide) => {
    if (!slide) {
      return;
    }

    const targets = slide.querySelectorAll(".hero-copy-clip > *");
    if (!targets.length) {
      return;
    }

    slide.classList.remove("hero-slide-active");
    void slide.offsetWidth;
    slide.classList.add("hero-slide-active");

    window.gsap.killTweensOf(targets);
    window.gsap.set(targets, {
      yPercent: 120,
      opacity: 0,
    });
    window.gsap.to(targets, {
      yPercent: 0,
      opacity: 1,
      duration: 0.9,
      ease: "power4.out",
      stagger: 0.1,
      clearProps: "transform,opacity",
    });
  };

  heroSlides.forEach(setHeroSlideHiddenState);

  const heroSwiper = new window.Swiper(heroSwiperElement, {
    loop: true,
    speed: 900,
    slidesPerView: 1,
    autoplay: {
      delay: 3800,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },
    pagination: {
      el: ".hero-swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".hero-swiper-button-next",
      prevEl: ".hero-swiper-button-prev",
    },
    on: {
      init(swiper) {
        animateHeroSlide(swiper.slides[swiper.activeIndex]);
      },
      slideChangeTransitionStart(swiper) {
        swiper.slides.forEach((slide) => {
          if (slide !== swiper.slides[swiper.activeIndex]) {
            setHeroSlideHiddenState(slide);
          }
        });
      },
      slideChangeTransitionEnd(swiper) {
        animateHeroSlide(swiper.slides[swiper.activeIndex]);
      },
    },
  });

  if (heroSwiper.autoplay) {
    heroSwiper.autoplay.start();
  }
}

const testimonialsSwiperElement = document.querySelector(".testimonials-swiper");

if (testimonialsSwiperElement && window.Swiper) {
  new window.Swiper(testimonialsSwiperElement, {
    loop: true,
    speed: 700,
    spaceBetween: 18,
    grabCursor: true,
    autoplay: {
      delay: 3200,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },
    pagination: {
      el: ".testimonials-swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".testimonials-swiper-button-next",
      prevEl: ".testimonials-swiper-button-prev",
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      640: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 3,
      },
    },
  });
}

/* =========================================================
   PREMIUM MOBILE NAVIGATION — Toggle Logic
   ========================================================= */

(function () {
  const toggle = document.getElementById("mobileNavToggle");
  const overlay = document.getElementById("mobileNavOverlay");
  const backdrop = document.getElementById("mobileNavBackdrop");
  const closeBtn = document.getElementById("mobileNavClose");
  const navLinks = overlay ? overlay.querySelectorAll(".mobile-nav-link") : [];

  if (!toggle || !overlay) return;

  function openNav() {
    overlay.classList.add("is-open");
    overlay.setAttribute("aria-hidden", "false");
    toggle.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Close navigation menu");
    document.body.classList.add("mobile-nav-open");
  }

  function closeNav() {
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
    toggle.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open navigation menu");
    document.body.classList.remove("mobile-nav-open");
  }

  // Hamburger button click
  toggle.addEventListener("click", function () {
    if (overlay.classList.contains("is-open")) {
      closeNav();
    } else {
      openNav();
    }
  });

  // Close button click
  if (closeBtn) {
    closeBtn.addEventListener("click", closeNav);
  }

  // Backdrop click closes menu
  if (backdrop) {
    backdrop.addEventListener("click", closeNav);
  }

  // Nav link clicks close menu
  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      closeNav();
    });
  });

  // Escape key closes menu
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && overlay.classList.contains("is-open")) {
      closeNav();
      toggle.focus();
    }
  });

  // Close on resize above breakpoint
  window.addEventListener("resize", function () {
    if (window.innerWidth > 860 && overlay.classList.contains("is-open")) {
      closeNav();
    }
  });
})();
