/* global marked, bootstrap, window, document */

(function () {
  "use strict";

  // Data storage
  let docsData = window.MLEGO_DATA || {};
  let currentFilter = "all";
  let currentSearchQuery = "";
  let modalInstance = null;
  let currentDocId = null;

  // Category order for navigation
  const CATEGORIES = [
    { id: "keyboards", name: "Keyboards", icon: "bi-keyboard", color: "#6cb670" },
    { id: "converted", name: "POS Conversions", icon: "bi-cpu", color: "#fbbf24" },
    { id: "mice", name: "Mice Liberation", icon: "bi-mouse", color: "#818cf8" },
    { id: "guides", name: "Hardware Guides", icon: "bi-journal-code", color: "#f472b6" },
  ];

  // Configure marked options
  if (typeof marked !== "undefined") {
    marked.setOptions({
      gfm: true,
      breaks: false,
      headerIds: true,
      mangle: false,
    });
  }

  // Fetch docs data if not loaded via script tag
  async function loadData() {
    if (Object.keys(docsData).length > 0) {
      initApp();
      return;
    }
    try {
      const res = await fetch("data/docs.json");
      if (res.ok) {
        docsData = await res.json();
      }
    } catch (e) {
      console.warn("Could not load data/docs.json dynamically, using bundle if available", e);
    }
    initApp();
  }

  function initApp() {
    setupFloatingMenu();
    setupParallax();
    setupScrollReveal();
    setupSearchAndFilters();
    renderAllSections();
    setupLightbox();
    setupRouting();
  }

  /* ==========================================================================
     Floating Corner Navigation Menu
     ========================================================================== */
  function setupFloatingMenu() {
    const toggleBtn = document.getElementById("corner-menu-toggle");
    const panel = document.getElementById("corner-menu-panel");
    const labelSpan = document.getElementById("corner-current-section");

    if (!toggleBtn || !panel) return;

    toggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const expanded = toggleBtn.getAttribute("aria-expanded") === "true";
      toggleBtn.setAttribute("aria-expanded", !expanded);
      panel.classList.toggle("show", !expanded);
    });

    document.addEventListener("click", (e) => {
      if (!panel.contains(e.target) && !toggleBtn.contains(e.target)) {
        toggleBtn.setAttribute("aria-expanded", "false");
        panel.classList.remove("show");
      }
    });

    // Close menu on link click
    panel.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        toggleBtn.setAttribute("aria-expanded", "false");
        panel.classList.remove("show");
      });
    });

    // Section scroll spy to update label
    const sections = document.querySelectorAll("section[id], header");
    window.addEventListener(
      "scroll",
      () => {
        let currentSec = "Menu";
        const scrollPos = window.scrollY + 180;

        sections.forEach((sec) => {
          const top = sec.offsetTop;
          const height = sec.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            const heading = sec.querySelector(".section-title") || sec.querySelector("h1");
            if (heading) {
              currentSec = heading.textContent.trim().split(" ")[0];
            } else if (sec.id === "hero") {
              currentSec = "Home";
            }
          }
        });

        if (labelSpan && currentSec) {
          labelSpan.textContent = currentSec.substring(0, 12);
        }
      },
      { passive: true }
    );
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
     Card Renderers
     ========================================================================== */
  function renderHardwareCard(item) {
    const badgeColorClass =
      item.category === "keyboards"
        ? "mlego-badge--green"
        : item.category === "converted"
        ? "mlego-badge--amber"
        : item.category === "mice"
        ? "mlego-badge--purple"
        : "";

    return `
      <div class="col-lg-4 col-md-6 mb-4 card-item" data-id="${item.id}" data-category="${item.category}" data-search="${(item.title + ' ' + (item.mcu || '') + ' ' + (item.badge || '') + ' ' + (item.summary || '')).toLowerCase()}">
        <div class="hardware-card">
          <div class="hardware-card-thumb-wrap">
            <img src="${item.image || 'pics/mlego.webp'}" alt="${item.title}" class="hardware-card-thumb" loading="lazy">
          </div>
          <div class="hardware-card-body">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <span class="mlego-badge ${badgeColorClass}">${item.badge || item.category}</span>
              ${item.keys ? `<span class="badge bg-dark text-secondary border border-secondary border-opacity-25">${item.keys} Keys</span>` : ""}
            </div>
            <h3 class="hardware-card-title">${item.title}</h3>
            <div class="hardware-card-specs">
              ${item.mcu ? `<span class="badge bg-dark text-info border border-info border-opacity-25"><i class="bi bi-cpu me-1"></i>${item.mcu}</span>` : ""}
              ${item.firmware ? `<span class="badge bg-dark text-success border border-success border-opacity-25"><i class="bi bi-code-slash me-1"></i>${item.firmware}</span>` : ""}
            </div>
            <p class="hardware-card-desc">${item.summary || ""}</p>
            <div class="mt-auto pt-2 border-top border-secondary border-opacity-25 d-flex align-items-center justify-content-between">
              <button type="button" class="btn btn-sm btn-ddmms-primary open-doc-btn" data-doc-id="${item.id}">
                <i class="bi bi-book me-1"></i> Read Notes
              </button>
              <button type="button" class="btn btn-sm btn-outline-secondary view-img-btn" data-img-src="${item.image}">
                <i class="bi bi-zoom-in"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderGuideCard(item) {
    return `
      <div class="col-lg-6 mb-4 card-item" data-id="${item.id}" data-category="${item.category}" data-search="${(item.title + ' ' + (item.badge || '') + ' ' + (item.summary || '')).toLowerCase()}">
        <div class="surface-card d-flex flex-row gap-3">
          <div class="d-none d-sm-block flex-shrink-0" style="width: 140px; height: 140px; border-radius: 0.75rem; overflow: hidden;">
            <img src="${item.image || 'pics/mlego.webp'}" alt="${item.title}" style="width: 100%; height: 100%; object-fit: cover;">
          </div>
          <div class="d-flex flex-column flex-grow-1">
            <div class="d-flex align-items-center justify-content-between mb-1">
              <span class="mlego-badge mlego-badge--purple">${item.badge || "Guide"}</span>
            </div>
            <h4 class="h5 text-white mb-2">${item.title}</h4>
            <p class="text-secondary small mb-3 flex-grow-1">${item.summary}</p>
            <div>
              <button type="button" class="btn btn-sm btn-ddmms-outline open-doc-btn" data-doc-id="${item.id}">
                <i class="bi bi-journal-text me-1"></i> Open Guide
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderAllSections() {
    // 1. Keyboards
    const kbContainer = document.getElementById("keyboards-grid");
    if (kbContainer) {
      const kbList = ["m66", "m65", "m60", "m60_split", "m48", "m20", "m8", "m4"]
        .map((id) => docsData[id])
        .filter(Boolean);
      kbContainer.innerHTML = kbList.map(renderHardwareCard).join("");
    }

    // 2. Converted POS
    const convertedContainer = document.getElementById("converted-grid");
    if (convertedContainer) {
      const convList = ["tipro8x16", "tipro8x12", "tipro8x4", "tiproansi-ortho", "tiproortho-ansi"]
        .map((id) => docsData[id])
        .filter(Boolean);
      convertedContainer.innerHTML = convList.map(renderHardwareCard).join("");
    }

    // 3. Mice
    const miceContainer = document.getElementById("mice-grid");
    if (miceContainer) {
      const miceList = ["prime"].map((id) => docsData[id]).filter(Boolean);
      miceContainer.innerHTML = miceList.map(renderHardwareCard).join("");
    }

    // 4. Guides
    const guidesContainer = document.getElementById("guides-grid");
    if (guidesContainer) {
      const guideList = ["assembly", "notenoughpins", "how_matrix_works_extra", "hand5x5"]
        .map((id) => docsData[id])
        .filter(Boolean);
      guidesContainer.innerHTML = guideList.map(renderGuideCard).join("");
    }

    // 5. Lineup Specs Table
    renderSpecsTable();

    // Attach card event listeners
    document.querySelectorAll(".open-doc-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const docId = btn.getAttribute("data-doc-id");
        if (docId) openDoc(docId);
      });
    });

    document.querySelectorAll(".view-img-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const src = btn.getAttribute("data-img-src");
        if (src) openLightbox(src);
      });
    });
  }

  function renderSpecsTable() {
    const tableBody = document.getElementById("specs-table-body");
    if (!tableBody) return;

    const list = [
      { id: "m66", name: "m66", layout: "5×14 Ortho", keys: "66", mcu: "RP2040 / nice!nano / XIAO", features: "Clickable Encoder, Per-Key RGB, Modular Display (OLED/E-Ink/Sharp/LCD)", firmware: "QMK & ZMK" },
      { id: "m65", name: "m65", layout: "5×13 Ortho", keys: "65", mcu: "STM32F401 / RP2040 / XIAO", features: "11 Hardware Revisions, Underglow RGB, Shift Register Matrix, E-Ink", firmware: "QMK & ZMK" },
      { id: "m60", name: "m60", layout: "5×12 Ortho", keys: "60", mcu: "STM32F401 / RP2040", features: "Preonic-style, Rotary encoder, RGB strip, OLED support", firmware: "QMK" },
      { id: "m60_split", name: "m60 Split", layout: "5×12 Split", keys: "60 (2×30)", mcu: "Dual STM32F401 / 411", features: "Dual 16×16 LEGO baseplates, Dual encoders, Underglow RGB", firmware: "QMK" },
      { id: "m48", name: "m48", layout: "4×12 Ortho", keys: "48", mcu: "STM32F401 / F411", features: "Planck-style compact, Rotary encoder, RGB strip", firmware: "QMK" },
      { id: "m20", name: "m20", layout: "5×4 Pad", keys: "20", mcu: "Raspberry Pi Pico (RP2040)", features: "Cherry MX & Kailh Choc v2, Rotary encoder, OLED", firmware: "QMK" },
      { id: "m8", name: "m8", layout: "2×4 Pad", keys: "8", mcu: "XIAO RP2040", features: "74HC595 + 74HC589 SPI Shift Registers, E-Ink, OLED", firmware: "QMK" },
      { id: "m4", name: "m4", layout: "2×2 Pad", keys: "4", mcu: "Seeed XIAO BLE / RP2040", features: "Wireless BLE, Shift register prototype, Compact macropad", firmware: "ZMK & QMK" },
      { id: "tipro8x16", name: "Tipro 8×16", layout: "8×16 POS", keys: "128", mcu: "STM32F401", features: "Polished steel plate, 74HC595 LED expander, MT3 keycaps", firmware: "QMK" },
      { id: "tipro8x12", name: "Tipro 8×12", layout: "8×12 POS", keys: "96", mcu: "STM32F401", features: "Daughterboard conversion, Shift register LEDs", firmware: "QMK" },
      { id: "tipro8x4", name: "Tipro 8×4", layout: "8×4 POS", keys: "32", mcu: "WeAct STM32G431", features: "Dedicated 32-key POS macropad module", firmware: "QMK" },
      { id: "prime", name: "SS Prime Mouse", layout: "5-Btn Mouse", keys: "5", mcu: "STM32F103", features: "PixArt PMW3389 sensor, SWD unlocked, UF2 bootloader", firmware: "QMK" },
    ];

    tableBody.innerHTML = list
      .map(
        (row) => `
        <tr>
          <td class="fw-bold text-white"><a href="#doc/${row.id}" class="text-info">${row.name}</a></td>
          <td><span class="mlego-badge">${row.layout}</span></td>
          <td><span class="badge bg-dark text-light border border-secondary border-opacity-25">${row.keys}</span></td>
          <td class="small text-secondary">${row.mcu}</td>
          <td class="small text-light">${row.features}</td>
          <td><span class="badge bg-dark text-success border border-success border-opacity-25">${row.firmware}</span></td>
          <td>
            <button type="button" class="btn btn-sm btn-ddmms-outline open-doc-btn py-1 px-2" data-doc-id="${row.id}">
              <i class="bi bi-file-text"></i> Docs
            </button>
          </td>
        </tr>
      `
      )
      .join("");
  }

  /* ==========================================================================
     Search & Filters
     ========================================================================== */
  function setupSearchAndFilters() {
    const searchInput = document.getElementById("search-input");
    const filterPills = document.querySelectorAll(".filter-pill");

    function applyFilter() {
      const cards = document.querySelectorAll(".card-item");
      cards.forEach((card) => {
        const cat = card.getAttribute("data-category");
        const searchText = card.getAttribute("data-search") || "";
        const matchesCategory = currentFilter === "all" || cat === currentFilter;
        const matchesQuery = !currentSearchQuery || searchText.includes(currentSearchQuery.toLowerCase());

        if (matchesCategory && matchesQuery) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        currentSearchQuery = e.target.value.trim();
        applyFilter();
      });
    }

    filterPills.forEach((pill) => {
      pill.addEventListener("click", () => {
        filterPills.forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");
        currentFilter = pill.getAttribute("data-filter") || "all";
        applyFilter();
      });
    });
  }

  /* ==========================================================================
     Document Reader Modal
     ========================================================================== */
  function openDoc(docId) {
    const item = docsData[docId];
    if (!item) {
      console.warn("Document not found:", docId);
      return;
    }

    currentDocId = docId;

    const modalEl = document.getElementById("docReaderModal");
    const titleEl = document.getElementById("docModalTitle");
    const metaEl = document.getElementById("docModalMeta");
    const bodyEl = document.getElementById("docModalBody");

    if (!modalEl || !titleEl || !bodyEl) return;

    titleEl.textContent = item.title;
    metaEl.innerHTML = `
      <span class="mlego-badge me-2">${item.badge || item.category}</span>
      ${item.mcu ? `<span class="badge bg-dark text-info border border-info border-opacity-25 me-2"><i class="bi bi-cpu me-1"></i>${item.mcu}</span>` : ""}
      ${item.firmware ? `<span class="badge bg-dark text-success border border-success border-opacity-25 me-2"><i class="bi bi-code-slash me-1"></i>${item.firmware}</span>` : ""}
      <span class="text-muted"><i class="bi bi-file-earmark-text me-1"></i>${item.id}.md</span>
    `;

    // Render Markdown
    if (typeof marked !== "undefined" && item.markdown) {
      bodyEl.innerHTML = marked.parse(item.markdown);
    } else {
      bodyEl.textContent = item.markdown || "No content available.";
    }

    // Attach click-to-zoom on images inside modal
    bodyEl.querySelectorAll("img").forEach((img) => {
      img.addEventListener("click", () => openLightbox(img.src));
    });

    // Add copy button to code blocks
    bodyEl.querySelectorAll("pre").forEach((pre) => {
      const copyBtn = document.createElement("button");
      copyBtn.className = "btn btn-sm btn-dark position-absolute top-0 end-0 m-2 border border-secondary border-opacity-25 text-info";
      copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
      copyBtn.title = "Copy code";
      copyBtn.addEventListener("click", () => {
        const codeText = pre.querySelector("code") ? pre.querySelector("code").innerText : pre.innerText;
        navigator.clipboard.writeText(codeText);
        copyBtn.innerHTML = '<i class="bi bi-check2"></i>';
        setTimeout(() => (copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>'), 2000);
      });
      pre.style.position = "relative";
      pre.appendChild(copyBtn);
    });

    if (!modalInstance) {
      modalInstance = new bootstrap.Modal(modalEl);
    }
    modalInstance.show();

    // Update URL hash
    window.location.hash = `doc/${docId}`;
  }

  /* ==========================================================================
     Lightbox Image Preview
     ========================================================================== */
  function setupLightbox() {
    const overlay = document.getElementById("lightbox-overlay");
    if (!overlay) return;

    overlay.addEventListener("click", () => {
      overlay.classList.remove("show");
    });
  }

  function openLightbox(src) {
    const overlay = document.getElementById("lightbox-overlay");
    const img = document.getElementById("lightbox-img");
    if (!overlay || !img) return;

    img.src = src;
    overlay.classList.add("show");
  }

  /* ==========================================================================
     URL Hash Routing
     ========================================================================== */
  function setupRouting() {
    function handleHash() {
      const hash = window.location.hash;
      if (hash.startsWith("#doc/")) {
        const id = hash.replace("#doc/", "");
        if (docsData[id]) {
          openDoc(id);
        }
      }
    }

    window.addEventListener("hashchange", handleHash);
    handleHash();
  }

  // Kickoff
  document.addEventListener("DOMContentLoaded", loadData);
})();

