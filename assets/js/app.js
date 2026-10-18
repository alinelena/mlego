/* global window, document */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", () => {
    setupThemeSwitcher();
    setupFloatingMenu();
    setupParallax();
    setupScrollReveal();
    setupCatalogSearch();
    setupCodeCopy();
    setupLightbox();
  });

  /* ==========================================================================
     Color Theme Switcher
     ========================================================================== */
  function setupThemeSwitcher() {
    const themeToggleBtn = document.getElementById("corner-theme-toggle");
    const themePanel = document.getElementById("corner-theme-panel");
    const menuToggleBtn = document.getElementById("corner-menu-toggle");
    const menuPanel = document.getElementById("corner-menu-panel");
    const themeActiveBadge = document.getElementById("theme-active-name");

    const themeNames = {
      default: "Cyber Cyan",
      nord: "Nord Frost",
      dracula: "Dracula",
      monokai: "Monokai Pro",
      gruvbox: "Gruvbox Retro",
      catppuccin: "Catppuccin",
      solarized: "Solarized",
    };

    function applyTheme(themeId) {
      if (!themeNames[themeId]) themeId = "default";
      document.documentElement.setAttribute("data-theme", themeId);
      try {
        localStorage.setItem("mlego-theme", themeId);
      } catch (e) {}

      if (themeActiveBadge) {
        themeActiveBadge.textContent = themeNames[themeId];
      }

      // Update active states on all theme buttons (both in popup and menu)
      document.querySelectorAll(".theme-option-btn, .theme-swatch-pill").forEach((btn) => {
        const id = btn.getAttribute("data-theme-id");
        btn.classList.toggle("active", id === themeId);
      });
    }

    // Initialize from storage or attribute
    const currentTheme = document.documentElement.getAttribute("data-theme") || "default";
    applyTheme(currentTheme);

    // Toggle theme panel
    if (themeToggleBtn && themePanel) {
      themeToggleBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const expanded = themeToggleBtn.getAttribute("aria-expanded") === "true";
        themeToggleBtn.setAttribute("aria-expanded", !expanded);
        themePanel.classList.toggle("show", !expanded);

        // Close menu panel if open
        if (menuPanel && menuToggleBtn) {
          menuToggleBtn.setAttribute("aria-expanded", "false");
          menuPanel.classList.remove("show");
        }
      });

      document.addEventListener("click", (e) => {
        if (!themePanel.contains(e.target) && !themeToggleBtn.contains(e.target)) {
          themeToggleBtn.setAttribute("aria-expanded", "false");
          themePanel.classList.remove("show");
        }
      });
    }

    // Close theme panel if menu is opened
    if (menuToggleBtn && themePanel && themeToggleBtn) {
      menuToggleBtn.addEventListener("click", () => {
        themeToggleBtn.setAttribute("aria-expanded", "false");
        themePanel.classList.remove("show");
      });
    }

    // Click handler for all theme option buttons
    document.querySelectorAll(".theme-option-btn, .theme-swatch-pill").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const themeId = btn.getAttribute("data-theme-id");
        if (themeId) {
          applyTheme(themeId);
        }
      });
    });
  }

  /* ==========================================================================
     Floating Corner Navigation Menu
     ========================================================================== */
  function setupFloatingMenu() {
    const toggleBtn = document.getElementById("corner-menu-toggle");
    const panel = document.getElementById("corner-menu-panel");
    const themeToggleBtn = document.getElementById("corner-theme-toggle");
    const themePanel = document.getElementById("corner-theme-panel");

    if (!toggleBtn || !panel) return;

    toggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = toggleBtn.getAttribute("aria-expanded") === "true";
      toggleBtn.setAttribute("aria-expanded", !expanded);
      panel.classList.toggle("show", !expanded);

      // Close theme panel if open
      if (themePanel && themeToggleBtn) {
        themeToggleBtn.setAttribute("aria-expanded", "false");
        themePanel.classList.remove("show");
      }
    });

    document.addEventListener("click", (e) => {
      if (!panel.contains(e.target) && !toggleBtn.contains(e.target)) {
        toggleBtn.setAttribute("aria-expanded", "false");
        panel.classList.remove("show");
      }
    });

    // Submenu toggles (Keyboards, POS Conversions, Mice, Guides)
    panel.querySelectorAll(".corner-nav-group-toggle-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const expanded = btn.getAttribute("aria-expanded") === "true";
        btn.setAttribute("aria-expanded", !expanded);
        const group = btn.closest(".corner-nav-group");
        if (group) {
          const subpanel = group.querySelector(".corner-subnav-panel");
          if (subpanel) {
            subpanel.classList.toggle("show", !expanded);
          }
        }
      });
    });
  }

  /* ==========================================================================
     Parallax & Scroll Reveal
     ========================================================================== */
  function setupParallax() {
    const parallaxWindows = document.querySelectorAll(".parallax-window");
    if (!parallaxWindows.length) return;

    function updateParallax() {
      const scrollY = window.scrollY;
      const windowH = window.innerHeight;

      parallaxWindows.forEach((win) => {
        const bg = win.querySelector(".parallax-bg");
        if (!bg) return;
        const rect = win.getBoundingClientRect();
        if (rect.top < windowH && rect.bottom > 0) {
          const speed = parseFloat(win.dataset.parallaxSpeed || "0.4");
          const offset = (rect.top - windowH / 2) * speed;
          bg.style.transform = `translate3d(0, ${offset}px, 0)`;
        }
      });
    }

    window.addEventListener("scroll", updateParallax, { passive: true });
    updateParallax();
  }

  function setupScrollReveal() {
    const revealSections = document.querySelectorAll(".reveal-section");
    if (!revealSections.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      { threshold: 0.08 }
    );

    revealSections.forEach((sec) => observer.observe(sec));
  }

  /* ==========================================================================
     Search & Filtering on Catalog Pages
     ========================================================================== */
  function setupCatalogSearch() {
    const searchInput = document.getElementById("search-input");
    if (!searchInput) return;

    searchInput.addEventListener("input", (e) => {
      const query = e.target.value.trim().toLowerCase();
      const cards = document.querySelectorAll(".card-item");

      cards.forEach((card) => {
        const text = (card.getAttribute("data-search") || "").toLowerCase();
        if (!query || text.includes(query)) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });
    });
  }

  /* ==========================================================================
     Code Block Copy Buttons
     ========================================================================== */
  function setupCodeCopy() {
    document.querySelectorAll(".modal-article-body pre, main pre").forEach((pre) => {
      if (pre.querySelector(".btn-copy")) return;
      const copyBtn = document.createElement("button");
      copyBtn.className = "btn btn-sm btn-dark position-absolute top-0 end-0 m-2 border border-secondary border-opacity-25 text-info btn-copy";
      copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
      copyBtn.title = "Copy code";
      copyBtn.style.zIndex = "5";

      copyBtn.addEventListener("click", () => {
        const code = pre.querySelector("code") ? pre.querySelector("code").innerText : pre.innerText;
        navigator.clipboard.writeText(code);
        copyBtn.innerHTML = '<i class="bi bi-check2 text-success"></i>';
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
        }, 2000);
      });

      pre.style.position = "relative";
      pre.appendChild(copyBtn);
    });

    // Make article images zoomable
    document.querySelectorAll(".modal-article-body img, main article img").forEach((img) => {
      img.style.cursor = "zoom-in";
      img.addEventListener("click", () => window.openLightbox(img.src));
    });
  }

  /* ==========================================================================
     Lightbox Image Zoom
     ========================================================================== */
  function setupLightbox() {
    const overlay = document.getElementById("lightbox-overlay");
    if (!overlay) return;

    overlay.addEventListener("click", () => {
      overlay.classList.remove("show");
    });
  }

  window.openLightbox = function (src) {
    const overlay = document.getElementById("lightbox-overlay");
    const img = document.getElementById("lightbox-img");
    if (!overlay || !img) return;

    img.src = src;
    overlay.classList.add("show");
  };
})();
