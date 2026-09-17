// Field Guide — card accordion, guide accordion, and legend scroll highlighting
document.addEventListener('DOMContentLoaded', () => {
  // Card accordion (existing)
  document.querySelectorAll('.card-wrapper').forEach(wrapper => {
    const card = wrapper.querySelector('.card');
    const detail = wrapper.querySelector('.card-detail');
    if (!card || !detail) return;

    function toggle() {
      const isOpen = detail.classList.toggle('open');
      card.classList.toggle('expanded', isOpen);
      card.setAttribute('aria-expanded', String(isOpen));
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

    if (items.length > 0) items[0].classList.add('active');

    const observer = new IntersectionObserver((entries) => {
      let visible = null;
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible = entry.target;
        }
      });
      if (visible) {
        const team = visible.querySelector('.team-header')?.className
          .match(/green|yellow|orange|red/)?.[0];
        if (team) {
          items.forEach(item => {
            item.classList.toggle('active', item.dataset.team === team);
          });
        }
      }
    }, { threshold: 0.3 });

    sections.forEach(s => observer.observe(s));
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
  }
});