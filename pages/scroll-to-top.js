// Scroll-to-Top Button
(function() {
  // Create button element
  const button = document.createElement('button');
  button.id = 'scroll-to-top';
  button.innerHTML = '↑';
  button.title = 'Back to top';

  // Add styles
  const style = document.createElement('style');
  style.textContent = `
    #scroll-to-top {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: var(--accent-color, #0066cc);
      color: white;
      border: none;
      font-size: 1.2rem;
      cursor: pointer;
      display: none;
      z-index: 99;
      transition: opacity 0.3s ease, transform 0.3s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    #scroll-to-top.show {
      display: block;
    }

    #scroll-to-top:hover {
      transform: translateY(-3px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    #scroll-to-top:active {
      transform: translateY(-1px);
    }

    @media (max-width: 640px) {
      #scroll-to-top {
        bottom: 1.5rem;
        right: 1.5rem;
        width: 35px;
        height: 35px;
        font-size: 1rem;
      }
    }
  `;

  document.head.appendChild(style);
  document.body.appendChild(button);

  // Show/hide button based on scroll position
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      button.classList.add('show');
    } else {
      button.classList.remove('show');
    }
  });

  // Scroll to top when clicked
  button.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
})();
