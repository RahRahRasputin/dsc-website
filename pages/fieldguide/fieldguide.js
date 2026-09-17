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
  function activateTeamLegend(entries) {
    if (!teamLegend) return;
    const items = teamLegend.querySelectorAll('.legend-item');
    let best = null, bestRatio = 0;
    entries.forEach(entry => {
      const team = entry.target.querySelector('.team-header')?.className.match(/green|yellow|orange|red/)?.[0];
      if (team && entry.intersectionRatio > bestRatio) {
        best = team;
        bestRatio = entry.intersectionRatio;
      }
    });
    if (best) {
      items.forEach(item => {
        item.classList.toggle('active', item.dataset.team === best);
      });
    }
  }

  if (teamLegend) {
    const sections = document.querySelectorAll('.team-section');
    if (sections.length > 0) {
      const firstItem = teamLegend.querySelector('.legend-item');
      if (firstItem) firstItem.classList.add('active');
    }
    const observer = new IntersectionObserver(activateTeamLegend, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });
    sections.forEach(s => observer.observe(s));
  }

  // Section legend scroll highlighting (papers page)
  const sectionLegend = document.getElementById('sectionLegend');
  function activateSectionLegend(entries) {
    if (!sectionLegend) return;
    const items = sectionLegend.querySelectorAll('.legend-item');
    let best = null, bestRatio = 0;
    entries.forEach(entry => {
      const cls = [...entry.target.classList].find(c => ['green','blue','orange','red','grey'].includes(c));
      if (cls && entry.intersectionRatio > bestRatio) {
        best = cls;
        bestRatio = entry.intersectionRatio;
      }
    });
    if (best) {
      items.forEach(item => {
        item.classList.toggle('active', item.dataset.section === best);
      });
    }
  }

  if (sectionLegend) {
    const sections = document.querySelectorAll('.section');
    if (sections.length > 0) {
      const firstItem = sectionLegend.querySelector('.legend-item');
      if (firstItem) firstItem.classList.add('active');
    }
    const observer = new IntersectionObserver(activateSectionLegend, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });
    sections.forEach(s => observer.observe(s));
  }
});