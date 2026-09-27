/**
 * dsc-ad-slider.js — Skyscraper ad rotator for Digital Soulcraft
 *
 * Injects rotating ads into the sidebar slot created by dsc-header.js.
 * Config-driven: one JSON file for all ads, across the whole site.
 *
 * Usage:
 *   <script src="/dsc-ad-slider.js"></script>
 *
 * Config: /dsc-ads-config.json
 *   { "ads": [{ "image": "...", "url": "...", "alt": "..." }], "interval_ms": 8000 }
 */
(function () {
  // Only run on pages that have a sidebar slot
  const slot = document.getElementById('dsc-sidebar-slot');
  if (!slot) return;

  // Don't double-initialise
  if (slot.dataset.dscAdSlider === 'loaded') return;
  slot.dataset.dscAdSlider = 'loaded';

  // Empty the placeholder content
  slot.innerHTML = '';
  slot.style.display = '';          // undo any override
  slot.style.opacity = '1';
  slot.style.border = 'none';
  slot.style.alignItems = 'stretch';
  slot.style.overflow = 'hidden';

  // Remove the ::after pseudo-content
  const noPseudo = document.createElement('style');
  noPseudo.textContent = '.wiki-sidebar::after { content: none !important; }';
  document.head.appendChild(noPseudo);

  // --- Ad rotation state ---
  let ads = [];
  let index = 0;
  let timer = null;

  const link = document.createElement('a');
  link.target = '_blank';
  link.rel = 'noopener';
  link.style.display = 'block';
  link.style.width = '100%';
  link.style.height = '100%';

  const img = document.createElement('img');
  img.style.width = '100%';
  img.style.height = 'auto';
  img.style.display = 'block';
  img.style.borderRadius = '6px';
  img.style.transition = 'opacity 0.4s ease';

  link.appendChild(img);
  slot.appendChild(link);

  function showAd(i) {
    const ad = ads[i];
    if (!ad) return;
    img.style.opacity = '0';
    setTimeout(() => {
      img.src = ad.image;
      img.alt = ad.alt || '';
      link.href = ad.url;
      img.style.opacity = '1';
    }, 200);
  }

  function nextAd() {
    if (ads.length < 2) return;
    index = (index + 1) % ads.length;
    showAd(index);
  }

  function startRotation() {
    stopRotation();
    if (ads.length > 1) {
      timer = setInterval(nextAd, 8000); // default, overridden from config
    }
  }

  function stopRotation() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  // Pause on hover, resume on leave
  slot.addEventListener('mouseenter', stopRotation);
  slot.addEventListener('mouseleave', startRotation);

  // --- Load config ---
  const configUrl = slot.dataset.config || '/dsc-ads-config.json';

  fetch(configUrl)
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then(cfg => {
      ads = cfg.ads || [];
      if (ads.length === 0) {
        slot.innerHTML = '<p style="padding:1rem;text-align:center;font-size:0.8rem;opacity:0.4">Ads</p>';
        return;
      }
      // Update interval if provided
      if (cfg.interval_ms) {
        if (timer) clearInterval(timer);
        timer = setInterval(nextAd, cfg.interval_ms);
      }
      showAd(0);
      startRotation();
    })
    .catch(err => {
      // Silent fallback — just show the empty slot
      slot.innerHTML = '';
    });

})();