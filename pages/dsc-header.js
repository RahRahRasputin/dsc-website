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

        nav a {
          color: var(--text-color);
          text-decoration: none;
          font-weight: 500;
          transition: color 0.3s;
          font-size: 0.95rem;
        }

        nav a:hover {
          color: var(--accent-color);
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

          nav a {
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
          }
        }
      </style>

      <header>
        <div class="header-container">
          <a href="/" class="logo"><span class="stamp"><img src="/images/stamp.png" alt="Digital Soulcraft" class="stamp-img"></span> ${config.logo}</a>
          <button class="menu-toggle" aria-label="Toggle menu">☰</button>
          <nav id="nav">
            ${config.links.map(link => `<a href="${link.href}">${link.label}</a>`).join('')}
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
