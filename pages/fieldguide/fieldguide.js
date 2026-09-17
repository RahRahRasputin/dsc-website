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

  // Team legend scroll highlighting (key-figures page)
  const teamLegend = document.getElementById('teamLegend');
  if (teamLegend) {
    const sections = document.querySelectorAll('.team-section');
    const items = teamLegend.querySelectorAll('.legend-item');

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

  // Section legend scroll highlighting (papers page)
  const sectionLegend = document.getElementById('sectionLegend');
  if (sectionLegend) {
    const sections = document.querySelectorAll('.section');
    const items = sectionLegend.querySelectorAll('.legend-item');

    if (items.length > 0) items[0].classList.add('active');

    const observer = new IntersectionObserver((entries) => {
      let visible = null;
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          visible = entry.target;
        }
      });
      if (visible) {
        const sectionClass = visible.classList[1]; // e.g. 'green', 'blue', 'orange', 'red', 'grey'
        if (sectionClass) {
          items.forEach(item => {
            item.classList.toggle('active', item.dataset.section === sectionClass);
          });
        }
      }
    }, { threshold: 0.3 });

    sections.forEach(s => observer.observe(s));
  }
});