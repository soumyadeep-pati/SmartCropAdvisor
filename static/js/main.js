/* ── Smart Crop Advisor — Main JS ── */

(function () {
  'use strict';

  /* ── Theme Toggle ── */
  const themeToggle = document.getElementById('themeToggle');
  const storedTheme = localStorage.getItem('theme');

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (themeToggle) {
      themeToggle.innerHTML = theme === 'dark'
        ? '<i class="fas fa-sun"></i>'
        : '<i class="fas fa-moon"></i>';
    }
  }

  if (storedTheme) {
    setTheme(storedTheme);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  /* ── Mobile Nav Toggle ── */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      const expanded = navLinks.classList.contains('open');
      navToggle.setAttribute('aria-expanded', expanded);
    });

    document.addEventListener('click', function (e) {
      if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── User Dropdown ── */
  const dropdownToggle = document.getElementById('userDropdownToggle');
  const dropdownMenu = document.getElementById('userDropdownMenu');

  if (dropdownToggle && dropdownMenu) {
    dropdownToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', function () {
      dropdownMenu.classList.remove('show');
    });

    dropdownMenu.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  /* ── Form Loading States ── */
  document.querySelectorAll('form[data-loading]').forEach(function (form) {
    form.addEventListener('submit', function () {
      const btn = form.querySelector('[type="submit"]');
      if (btn) {
        btn.disabled = true;
        const original = btn.innerHTML;
        btn.setAttribute('data-original', original);
        btn.innerHTML = '<span class="spinner-modern" style="display:inline-block;width:1rem;height:1rem;border-width:2px;margin-right:0.5rem;vertical-align:middle;"></span> Processing...';
      }
    });
  });

  /* ── Password Visibility Toggle ── */
  document.querySelectorAll('[data-toggle-pw]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const target = document.getElementById(this.getAttribute('data-toggle-pw'));
      if (!target) return;
      const isPassword = target.type === 'password';
      target.type = isPassword ? 'text' : 'password';
      this.innerHTML = isPassword
        ? '<i class="fas fa-eye-slash"></i>'
        : '<i class="fas fa-eye"></i>';
      this.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
    });
  });

  /* ── Auto-dismiss alerts ── */
  document.querySelectorAll('.alert-auto-dismiss').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.3s';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 300);
    }, 5000);
  });

  /* ── Active nav link ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-links a').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

})();
