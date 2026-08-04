// Field Guide — card accordion, guide accordion, and team legend scroll highlighting
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

  // Team legend scroll highlighting
  const legend = document.getElementById('teamLegend');
  if (legend) {
    const sections = document.querySelectorAll('.team-section');
    const items = legend.querySelectorAll('.legend-item');

    // Mark first as active by default
    if (items.length > 0) items[0].classList.add('active');

    const observer = new IntersectionObserver((entries) => {
      let visible = null;
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible = entry.target;
        }
      });
      if (visible) {
        const team = visible.querySelector('.team-header')?.className.match(/green|yellow|orange|red/)?.[0];
        if (team) {
          items.forEach(item => {
            item.classList.toggle('active', item.dataset.team === team);
          });
        }
      }
    }, { threshold: 0.3 });

    sections.forEach(s => observer.observe(s));
  }
});