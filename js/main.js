(function () {
  "use strict";

  /* Mobile navigation */
  var toggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".nav-mobile");

  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      document.body.style.overflow = isOpen ? "hidden" : "";
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mobileNav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  /* Google Maps: load only after explicit click (Datenschutz) */
  var mapButtons = document.querySelectorAll("[data-load-map]");
  mapButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".map-box");
      if (!box) return;
      var src = box.getAttribute("data-map-src");
      var iframe = document.createElement("iframe");
      iframe.src = src;
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      iframe.title = "Google Maps – Standort Giant Küchenmontagen";
      box.innerHTML = "";
      box.appendChild(iframe);
      box.classList.add("is-loaded");
    });
  });

  /* Galerie: Pfeile scrollen die horizontale Leiste */
  var track = document.getElementById("galerie-track");
  document.querySelectorAll("[data-scroll]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!track) return;
      var card = track.querySelector(".galerie__card");
      var step = card ? card.getBoundingClientRect().width + 20 : 320;
      track.scrollBy({
        left: step * parseInt(btn.getAttribute("data-scroll"), 10),
        behavior: "smooth"
      });
    });
  });

  /* Scroll reveal */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }
})();
