class DSCHeader extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  async connectedCallback() {
    const configUrl = this.getAttribute('config') || '/dsc-nav-config.json';
    const config = await fetch(configUrl).then(r => r.json());
    this.render(config);
  }

  renderNavItem(item) {
    if (item.dropdown) {
      return `
        <div class="dropdown">
          <a class="dropdown-trigger" href="#">${item.label} ▾</a>
          <div class="dropdown-menu">
            ${item.dropdown.map(sub => `<a href="${sub.href}">${sub.label}</a>`).join('')}
          </div>
        </div>
      `;
    }
    return `<a href="${item.href}">${item.label}</a>`;
  }

  render(config) {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          position: sticky;
          top: 0;
          z-index: 100;
          --bg-color: #ffffff;
          --text-color: #1a1a1a;
          --accent-color: #0066cc;
          --border-color: #e0e0e0;
          --light-bg: #f5f5f5;
        }

        @media (prefers-color-scheme: dark) {
          :host {
            --bg-color: #0a0a0a;
            --text-color: #e0e0e0;
            --light-bg: #1a1a1a;
            --border-color: #333333;
          }
        }

        header {
          background-color: var(--bg-color);
          border-bottom: 1px solid var(--border-color);
          padding: 1rem 2rem;
          position: sticky;
          top: 0;
          z-index: 100;
          transition: background-color 0.2s;
        }

        .header-container {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .logo {
          font-size: 1.8rem;
          font-weight: 700;
          color: var(--text-color);
          text-decoration: none;
          transition: color 0.3s;
          display: flex;
          align-items: center;
          gap: 0.6rem;
        }

        .logo:hover {
          color: var(--accent-color);
        }

        .stamp {
          display: inline-flex;
          align-items: center;
        }

        .stamp-img {
          height: 3.5rem;
          width: auto;
          display: inline-block;
        }

        nav {
          display: flex;
          gap: 2rem;
          align-items: center;
        }

        nav > a, .dropdown-trigger {
          color: var(--text-color);
          text-decoration: none;
          font-weight: 500;
          transition: color 0.3s;
          font-size: 0.95rem;
          cursor: pointer;
        }

        nav > a:hover, .dropdown-trigger:hover {
          color: var(--accent-color);
        }

        .dropdown {
          position: relative;
          display: inline-block;
        }

        .dropdown-trigger {
          white-space: nowrap;
        }

        .dropdown-menu {
          display: none;
          position: absolute;
          top: 100%;
          left: 0;
          background-color: var(--bg-color);
          border: 1px solid var(--border-color);
          border-radius: 6px;
          min-width: 160px;
          padding: 0.5rem 0;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          z-index: 200;
          margin-top: 0.5rem;
        }

        .dropdown-menu a {
          display: block;
          padding: 0.5rem 1rem;
          color: var(--text-color);
          text-decoration: none;
          font-size: 0.9rem;
          transition: background-color 0.2s;
        }

        .dropdown-menu a:hover {
          background-color: var(--light-bg);
          color: var(--accent-color);
        }

        .dropdown:hover .dropdown-menu,
        .dropdown:focus-within .dropdown-menu {
          display: block;
        }

        .social {
          display: flex;
          gap: 1rem;
          align-items: center;
          margin-left: 1rem;
          padding-left: 1rem;
          border-left: 1px solid var(--border-color);
        }

        .social a {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          color: var(--text-color);
          transition: color 0.3s;
        }

        .social a:hover {
          color: var(--accent-color);
        }

        .menu-toggle {
          display: none;
          background: none;
          border: none;
          color: var(--text-color);
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0;
        }

        @media (max-width: 768px) {
          nav {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: var(--bg-color);
            flex-direction: column;
            gap: 0;
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
          }

          nav.open {
            display: flex;
          }

          nav > a, .dropdown-trigger {
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border-color);
            display: block;
          }

          .dropdown {
            width: 100%;
          }

          .dropdown-menu {
            position: static;
            box-shadow: none;
            border: none;
            border-radius: 0;
            padding-left: 1rem;
            margin-top: 0;
          }

          .dropdown:hover .dropdown-menu,
          .dropdown:focus-within .dropdown-menu {
            display: block;
          }

          .dropdown-menu a {
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border-color);
          }

          .menu-toggle {
            display: block;
          }

          .social {
            border-left: none;
            padding-left: 0;
            margin-left: 0;
            margin-top: 0.75rem;
          }
        }
      </style>

      <header>
        <div class="header-container">
          <a href="/" class="logo"><span class="stamp"><img src="/images/stamp.png" alt="Digital Soulcraft" class="stamp-img"></span> ${config.logo}</a>
          <button class="menu-toggle" aria-label="Toggle menu">☰</button>
          <nav id="nav">
            ${config.links.map(item => this.renderNavItem(item)).join('')}
            <div class="social">
              ${config.social.map(s => `<a href="${s.url}" target="_blank" rel="noopener" title="${s.platform}">𝕏</a>`).join('')}
            </div>
          </nav>
        </div>
      </header>
    `;

    const toggle = this.shadowRoot.querySelector('.menu-toggle');
    const nav = this.shadowRoot.querySelector('#nav');

    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });

    // Close menu when a link is clicked
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('open');
      });
    });
  }
}

customElements.define('dsc-header', DSCHeader);