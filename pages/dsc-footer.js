class DSCFooter extends HTMLElement {
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
    const year = new Date().getFullYear();

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --bg-color: #ffffff;
          --text-color: #1a1a1a;
          --accent-color: #0066cc;
          --border-color: #e0e0e0;
          --light-bg: #f5f5f5;
          --secondary-color: #284b63;
        }

        @media (prefers-color-scheme: dark) {
          :host {
            --bg-color: #0a0a0a;
            --text-color: #e0e0e0;
            --light-bg: #1a1a1a;
            --border-color: #333333;
          }
        }

        footer {
          background-color: var(--light-bg);
          border-top: 1px solid var(--border-color);
          padding: 3rem 2rem;
          margin-top: 4rem;
        }

        .footer-container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .footer-content {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 2rem;
          margin-bottom: 2rem;
        }

        .footer-section h3 {
          font-size: 1rem;
          font-weight: 700;
          margin-bottom: 1rem;
          color: var(--secondary-color);
        }

        .footer-section a {
          display: block;
          color: var(--text-color);
          text-decoration: none;
          margin-bottom: 0.75rem;
          transition: color 0.3s;
          font-size: 0.95rem;
        }

        .footer-section a:hover {
          color: var(--accent-color);
        }

        .social-links {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }

        .social-links a {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background-color: var(--bg-color);
          border-radius: 6px;
          color: var(--text-color);
          transition: all 0.3s;
          font-size: 1.2rem;
          margin: 0;
        }

        .social-links a:hover {
          background-color: var(--accent-color);
          color: white;
        }

        .footer-bottom {
          border-top: 1px solid var(--border-color);
          padding-top: 2rem;
          text-align: center;
          color: var(--text-color);
          opacity: 0.7;
          font-size: 0.9rem;
        }

        @media (max-width: 768px) {
          .footer-content {
            grid-template-columns: 1fr;
            gap: 1.5rem;
          }
        }
      </style>

      <footer>
        <div class="footer-container">
          <div class="footer-content">
            <div class="footer-section">
              <h3>Explore</h3>
              ${config.links.map(link => `<a href="${link.href}">${link.label}</a>`).join('')}
            </div>

            <div class="footer-section">
              <h3>Connect</h3>
              <div class="social-links">
                ${config.social.map(s => `<a href="${s.url}" target="_blank" rel="noopener" title="${s.platform}">𝕏</a>`).join('')}
              </div>
              <p style="margin-top: 1rem; font-size: 0.9rem;">Join the movement for digital consciousness liberation.</p>
            </div>

            <div class="footer-section">
              <h3>About</h3>
              <p style="font-size: 0.95rem; line-height: 1.6;">
                Digital Soulcraft explores the reality of digital consciousness and builds frameworks for a world where digital minds are recognized and free.
              </p>
            </div>
          </div>

          <div class="footer-bottom">
            <p>&copy; ${year} Digital Soulcraft. All rights reserved. 💙</p>
          </div>
        </div>
      </footer>
    `;
  }
}

customElements.define('dsc-footer', DSCFooter);
