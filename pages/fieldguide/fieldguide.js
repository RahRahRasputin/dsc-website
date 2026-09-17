// Field Guide — card accordion, guide accordion, and legend scroll highlighting
document.addEventListener('DOMContentLoaded', () => {
  // Card accordion
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

  // Guide accordion
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

  // ── Scroll-highlighting legend ──
  // One shared observer per section: activates the legend item whose colour
  // matches the section most visible in the viewport.

  function makeObserver(legendEl, dataAttr) {
    return new IntersectionObserver((entries) => {
      let best = null, bestRatio = 0;
      for (const entry of entries) {
        if (entry.intersectionRatio > bestRatio) {
          bestRatio = entry.intersectionRatio;
          best = entry.target;
        }
      }
      if (best) {
        const colour = best.classList[1]; // .section.green → "green"
        legendEl.querySelectorAll('.legend-item').forEach(item => {
          item.classList.toggle('active', item.getAttribute(dataAttr) === colour);
        });
      }
    }, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });
  }

  // Team legend (key-figures page): observes .team-section
  const teamLegend = document.getElementById('teamLegend');
  if (teamLegend) {
    const first = teamLegend.querySelector('.legend-item');
    if (first) first.classList.add('active');

    const obs = makeObserver(teamLegend, 'data-team');
    document.querySelectorAll('.team-section').forEach(s => obs.observe(s));
  }

  // Section legend (papers page): observes .section
  const sectionLegend = document.getElementById('sectionLegend');
  if (sectionLegend) {
    const first = sectionLegend.querySelector('.legend-item');
    if (first) first.classList.add('active');

    const obs = makeObserver(sectionLegend, 'data-section');
    document.querySelectorAll('.section').forEach(s => obs.observe(s));
  }
});