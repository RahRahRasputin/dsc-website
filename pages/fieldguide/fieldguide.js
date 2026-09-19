// Field Guide — card accordion, guide accordion, and legend scroll highlighting
document.addEventListener('DOMContentLoaded', () => {
  // Card accordion — at most one figure open at a time
  document.querySelectorAll('.card-wrapper').forEach(wrapper => {
    const card = wrapper.querySelector('.card');
    const detail = wrapper.querySelector('.card-detail');
    if (!card || !detail) return;

    function closeOthers() {
      document.querySelectorAll('.card-wrapper').forEach(other => {
        if (other === wrapper) return;
        const otherCard = other.querySelector('.card');
        const otherDetail = other.querySelector('.card-detail');
        if (!otherCard || !otherDetail) return;
        otherDetail.classList.remove('open');
        otherCard.classList.remove('expanded');
        otherCard.setAttribute('aria-expanded', 'false');
      });
    }

    function toggle() {
      const isOpen = detail.classList.toggle('open');
      card.classList.toggle('expanded', isOpen);
      card.setAttribute('aria-expanded', String(isOpen));
      if (isOpen) {
        closeOthers();
        // Wait for the collapse transition (300ms) to finish, then scroll
        // so the card stays anchored at the top of the viewport
        setTimeout(() => {
          const header = document.querySelector('dsc-header');
          const legend = document.getElementById('sectionLegend') || document.getElementById('teamLegend');
          let offset = header ? header.getBoundingClientRect().height + 16 : 80;
          if (legend) offset += legend.getBoundingClientRect().height + 8;
          const top = wrapper.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
        }, 360);
      }
    }

    card.addEventListener('click', toggle);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      }
    });
  });

  // Guide accordion (About This Guide)
  const guideToggle = document.querySelector('.guide-accordion-toggle');
  const guideContent = document.querySelector('.guide-accordion-content');
  if (guideToggle && guideContent) {
    guideToggle.addEventListener('click', () => {
      const isOpen = guideContent.classList.toggle('open');
      guideToggle.classList.toggle('open', isOpen);
      guideToggle.setAttribute('aria-expanded', String(isOpen));
    });
    guideToggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        guideToggle.click();
      }
    });
  }

  // ── Team legend scroll highlighting (key-figures) ──
  const legend = document.getElementById('teamLegend');
  if (legend) {
    const sections = document.querySelectorAll('.team-section');
    const items = legend.querySelectorAll('.legend-item');
    const colours = ['green', 'yellow', 'orange', 'red'];

    function navHeight() {
      const header = document.querySelector('dsc-header');
      const h = header ? header.getBoundingClientRect().height : 0;
      if (h > 0) {
        document.documentElement.style.setProperty('--dsc-header-height', `${Math.round(h)}px`);
      }
      return h;
    }

    function colourOf(section) {
      if (!section) return null;
      return colours.find(c => section.classList.contains(c))
        || colours.find(c => section.querySelector('.team-header')?.classList.contains(c))
        || null;
    }

    function setActive(cls) {
      if (!cls) return;
      items.forEach(item => {
        item.classList.toggle('active', item.dataset.team === cls);
      });
    }

    function updateTeamLegend() {
      navHeight();
      // Active team = last heading that has arrived just under the key.
      const line = legend.getBoundingClientRect().bottom + 32;
      let current = sections[0];
      for (let i = 0; i < sections.length; i++) {
        const marker = sections[i].querySelector('.team-header') || sections[i];
        if (marker.getBoundingClientRect().top <= line) current = sections[i];
      }
      setActive(colourOf(current));
    }

    if (items.length > 0) setActive(colourOf(sections[0]) || items[0].dataset.team);

    window.addEventListener('scroll', updateTeamLegend, { passive: true });
    window.addEventListener('resize', updateTeamLegend);

    const siteHeader = document.querySelector('dsc-header');
    if (siteHeader && typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(updateTeamLegend).observe(siteHeader);
    }

    navHeight();
    updateTeamLegend();

    // ── Make team legend items clickable to scroll to section ──
    items.forEach(item => {
      item.style.cursor = 'pointer';
      item.addEventListener('click', () => {
        const colour = item.dataset.team;
        const target = document.querySelector(`.team-section.${colour}`) ||
                       document.querySelector(`.team-header.${colour}`)?.closest('.team-section');
        if (!target) return;
        const header = document.querySelector('dsc-header');
        const offset = header ? header.getBoundingClientRect().height + 16 : 100;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    });
  }

  // ── Section legend scroll highlighting (papers) ──
  // Uses scroll-spy on section headers for instant, reliable switching
  const sectionLegend = document.getElementById('sectionLegend');
  if (sectionLegend) {
    const sections = document.querySelectorAll('.section');
    const items = sectionLegend.querySelectorAll('.legend-item');
    const colours = ['green', 'blue', 'orange', 'red', 'grey'];

    if (items.length > 0) items[0].classList.add('active');

    function updateSectionLegend() {
      const scrollY = window.scrollY + 100;  // look a bit past the top of viewport
      let activeIdx = 0;

      for (let i = 0; i < sections.length; i++) {
        if (sections[i].offsetTop <= scrollY) {
          activeIdx = i;
        }
      }

      const cls = [...sections[activeIdx].classList].find(c => colours.includes(c));
      if (cls) {
        items.forEach(item => {
          item.classList.toggle('active', item.dataset.section === cls);
        });
      }
    }

    window.addEventListener('scroll', updateSectionLegend, { passive: true });
    // Also fire on load in case the page loads mid-section
    updateSectionLegend();

    // ── Make legend items clickable to scroll to section ──
    items.forEach(item => {
      item.style.cursor = 'pointer';
      item.addEventListener('click', () => {
        const colour = item.dataset.section;
        const target = document.querySelector(`.section.${colour}`);
        if (!target) return;
        // Account for the fixed header
        const header = document.querySelector('dsc-header');
        const offset = header ? header.getBoundingClientRect().height + 16 : 100;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    });
  }
});