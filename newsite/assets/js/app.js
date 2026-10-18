/* global jsyaml, marked, bootstrap, window, document */

(function () {
  "use strict";

  // Section YAML data sources matching alin.elena.re architecture
  const DATA_FILES = {
    site: "data/site.yml",
    about: "data/about.yml",
    keyboards: "data/keyboards.yml",
    converted: "data/converted.yml",
    mice: "data/mice.yml",
    guides: "data/guides.yml",
    specs: "data/specs.yml",
  };

  const state = {
    data: {},
    docsById: new Map(),
    currentFilter: "all",
    currentSearchQuery: "",
    modalInstance: null,
    currentDocId: null,
  };

  // Configure marked options
  if (typeof marked !== "undefined") {
    marked.setOptions({
      gfm: true,
      breaks: false,
      headerIds: true,
      mangle: false,
    });
  }

  async function fetchYaml(path) {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to load ${path}: ${response.status}`);
    }
    const text = await response.text();
    return jsyaml.load(text);
  }

  async function loadAllData() {
    try {
      const results = await Promise.all(
        Object.entries(DATA_FILES).map(async ([key, path]) => {
          const val = await fetchYaml(path);
          return [key, val];
        })
      );
      state.data = Object.fromEntries(results);

      // Index items by ID for the reader modal
      ["keyboards", "converted", "mice", "guides"].forEach((key) => {
        const sec = state.data[key];
        if (sec && Array.isArray(sec.items)) {
          sec.items.forEach((item) => {
            state.docsById.set(item.id, item);
          });
        }
      });

      // Index About manifesto as 'home'
      if (state.data.about) {
        state.docsById.set("home", {
          id: "home",
          title: "mlego Overview & Manifesto",
          category: "overview",
          badge: "Overview",
          content: state.data.about.content || "",
        });
      }

      renderUI();
    } catch (err) {
      console.error("Error loading YAML data:", err);
    }
  }

  function renderUI() {
    setupFloatingMenu();
    setupParallax();
    setupScrollReveal();
    setupSearchAndFilters();

    renderAboutSection();
    renderKeyboardsSection();
    renderConvertedSection();
    renderMiceSection();
    renderGuidesSection();
    renderSpecsTable();

    setupLightbox();
    setupRouting();
    attachCardListeners();
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

    panel.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        toggleBtn.setAttribute("aria-expanded", "false");
        panel.classList.remove("show");
      });
    });

    // Section spy
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
     Section Renderers
     ========================================================================== */
  function renderAboutSection() {
    const about = state.data.about;
    if (!about) return;

    const statsContainer = document.getElementById("about-stats-container");
    if (statsContainer && Array.isArray(about.stats)) {
      statsContainer.innerHTML = about.stats
        .map(
          (s) => `
        <div class="col-6 col-lg-3">
          <div class="stat-card">
            <i class="bi ${s.icon} stat-icon" style="color: ${s.color};"></i>
            <div class="stat-count">${s.count}</div>
            <div class="stat-label">${s.label}</div>
          </div>
        </div>
      `
        )
        .join("");
    }
  }

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

  function renderKeyboardsSection() {
    const kbContainer = document.getElementById("keyboards-grid");
    const data = state.data.keyboards;
    if (kbContainer && data && Array.isArray(data.items)) {
      kbContainer.innerHTML = data.items.map(renderHardwareCard).join("");
    }
  }

  function renderConvertedSection() {
    const convContainer = document.getElementById("converted-grid");
    const data = state.data.converted;
    if (convContainer && data && Array.isArray(data.items)) {
      convContainer.innerHTML = data.items.map(renderHardwareCard).join("");
    }
  }

  function renderMiceSection() {
    const miceContainer = document.getElementById("mice-grid");
    const data = state.data.mice;
    if (miceContainer && data && Array.isArray(data.items)) {
      miceContainer.innerHTML = data.items.map(renderHardwareCard).join("");
    }
  }

  function renderGuidesSection() {
    const guidesContainer = document.getElementById("guides-grid");
    const data = state.data.guides;
    if (guidesContainer && data && Array.isArray(data.items)) {
      guidesContainer.innerHTML = data.items.map(renderGuideCard).join("");
    }
  }

  function renderSpecsTable() {
    const tableBody = document.getElementById("specs-table-body");
    const data = state.data.specs;
    if (!tableBody || !data || !Array.isArray(data.items)) return;

    tableBody.innerHTML = data.items
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

  function attachCardListeners() {
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
        const matchesCategory = state.currentFilter === "all" || cat === state.currentFilter;
        const matchesQuery = !state.currentSearchQuery || searchText.includes(state.currentSearchQuery.toLowerCase());

        if (matchesCategory && matchesQuery) {
          card.style.display = "";
        } else {
          card.style.display = "none";
        }
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.currentSearchQuery = e.target.value.trim();
        applyFilter();
      });
    }

    filterPills.forEach((pill) => {
      pill.addEventListener("click", () => {
        filterPills.forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");
        state.currentFilter = pill.getAttribute("data-filter") || "all";
        applyFilter();
      });
    });
  }

  /* ==========================================================================
     Document Reader Modal
     ========================================================================== */
  function openDoc(docId) {
    const item = state.docsById.get(docId);
    if (!item) {
      console.warn("Document not found:", docId);
      return;
    }

    state.currentDocId = docId;

    const modalEl = document.getElementById("docReaderModal");
    const titleEl = document.getElementById("docModalTitle");
    const metaEl = document.getElementById("docModalMeta");
    const bodyEl = document.getElementById("docModalBody");

    if (!modalEl || !titleEl || !bodyEl) return;

    titleEl.textContent = item.title;
    metaEl.innerHTML = `
      <span class="mlego-badge me-2">${item.badge || item.category || "Doc"}</span>
      ${item.mcu ? `<span class="badge bg-dark text-info border border-info border-opacity-25 me-2"><i class="bi bi-cpu me-1"></i>${item.mcu}</span>` : ""}
      ${item.firmware ? `<span class="badge bg-dark text-success border border-success border-opacity-25 me-2"><i class="bi bi-code-slash me-1"></i>${item.firmware}</span>` : ""}
      <span class="text-muted"><i class="bi bi-file-earmark-text me-1"></i>${item.id}.md</span>
    `;

    // Render markdown content from the section YAML
    const markdownContent = item.content || item.markdown || "No documentation content available.";
    if (typeof marked !== "undefined") {
      bodyEl.innerHTML = marked.parse(markdownContent);
    } else {
      bodyEl.textContent = markdownContent;
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

    if (!state.modalInstance) {
      state.modalInstance = new bootstrap.Modal(modalEl);
    }
    state.modalInstance.show();

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
        if (state.docsById.has(id)) {
          openDoc(id);
        }
      }
    }

    window.addEventListener("hashchange", handleHash);
    handleHash();
  }

  // Kickoff YAML data loading
  document.addEventListener("DOMContentLoaded", loadAllData);
})();
