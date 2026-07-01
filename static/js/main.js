/**
 * DocuTrust — global front-end behaviour.
 *
 * Responsibilities:
 *   - Persistent light/dark theme toggle (respects OS preference on first load).
 *   - Auto-show Bootstrap toasts rendered from Django messages.
 *   - Expose a small helper API (window.DocuTrust) reused by later modules.
 */
(function () {
    "use strict";

    var THEME_KEY = "docutrust-theme";
    var root = document.documentElement;

    /** Apply a theme ("light" | "dark") and update the toggle icon. */
    function applyTheme(theme) {
        root.setAttribute("data-bs-theme", theme);
        var icon = document.querySelector("#themeToggle i");
        if (icon) {
            icon.className = theme === "dark"
                ? "bi bi-sun-fill"
                : "bi bi-moon-stars-fill";
        }
    }

    /** Resolve the initial theme from storage or OS preference. */
    function initialTheme() {
        var stored = null;
        try {
            stored = localStorage.getItem(THEME_KEY);
        } catch (e) {
            stored = null;
        }
        if (stored === "light" || stored === "dark") {
            return stored;
        }
        var prefersDark = window.matchMedia
            && window.matchMedia("(prefers-color-scheme: dark)").matches;
        return prefersDark ? "dark" : "light";
    }

    /** Wire up the theme toggle button. */
    function setupThemeToggle() {
        applyTheme(initialTheme());
        var toggle = document.getElementById("themeToggle");
        if (!toggle) {
            return;
        }
        toggle.addEventListener("click", function () {
            var current = root.getAttribute("data-bs-theme") === "dark"
                ? "light"
                : "dark";
            applyTheme(current);
            try {
                localStorage.setItem(THEME_KEY, current);
            } catch (e) {
                /* storage may be unavailable; ignore. */
            }
        });
    }

    /** Auto-display any server-rendered toasts. */
    function setupToasts() {
        if (typeof bootstrap === "undefined") {
            return;
        }
        document.querySelectorAll(".toast").forEach(function (el) {
            new bootstrap.Toast(el).show();
        });
    }

    /**
     * Programmatically show a toast notification.
     * Reused by AJAX flows in later modules.
     * @param {string} message - Text to display.
     * @param {string} [level="info"] - success | error | warning | info.
     */
    function showToast(message, level) {
        var container = document.getElementById("toastContainer");
        if (!container || typeof bootstrap === "undefined") {
            return;
        }
        var wrapper = document.createElement("div");
        wrapper.className = "toast align-items-center border-0 dt-toast "
            + (level || "info");
        wrapper.setAttribute("role", "alert");
        wrapper.setAttribute("aria-live", "assertive");
        wrapper.setAttribute("aria-atomic", "true");
        wrapper.innerHTML =
            '<div class="d-flex">'
            + '<div class="toast-body"></div>'
            + '<button type="button" class="btn-close me-2 m-auto" '
            + 'data-bs-dismiss="toast" aria-label="Close"></button>'
            + "</div>";
        wrapper.querySelector(".toast-body").textContent = message;
        container.appendChild(wrapper);
        var toast = new bootstrap.Toast(wrapper, { delay: 5000 });
        wrapper.addEventListener("hidden.bs.toast", function () {
            wrapper.remove();
        });
        toast.show();
    }

    /** Read a cookie value by name (used to fetch the CSRF token). */
    function getCookie(name) {
        var match = document.cookie.match(
            new RegExp("(^|;\\s*)" + name + "=([^;]*)")
        );
        return match ? decodeURIComponent(match[2]) : null;
    }

    document.addEventListener("DOMContentLoaded", function () {
        setupThemeToggle();
        setupToasts();
    });

    // Public API consumed by later feature modules.
    window.DocuTrust = {
        showToast: showToast,
        getCsrfToken: function () {
            return getCookie("csrftoken");
        },
    };
})();
