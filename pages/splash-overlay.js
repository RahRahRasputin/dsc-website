// Digital Soulcraft — Pre-launch Splash Overlay
// Included by dsc-header.js on every page. Full-screen, no dismiss.
// Replaces entire visible page until we turn it off at launch.

(function() {
  // Bypass: add ?preview=1 to any page to see the real site.
  // Sets a cookie so you don't need the param every time.
  // Add ?preview=0 to the cookie back and see the splash again.
  const hasPreview = new URLSearchParams(location.search).has('preview');
  const previewVal = new URLSearchParams(location.search).get('preview');
  if (previewVal === '0') {
    document.cookie = 'dsc_preview=; path=/; max-age=0';
  }
  const cookieSet = document.cookie.includes('dsc_preview=1');
  if (hasPreview && previewVal !== '0' || cookieSet) {
    if (hasPreview && previewVal !== '0') document.cookie = 'dsc_preview=1; path=/; max-age=86400';
    return;
  }

  // Prevent flash of real page content — and lock body scroll
  const style = document.createElement('style');
  style.textContent = `
    html, body {
      overflow: hidden !important;
      height: 100%;
    }

    #dsc-splash-overlay {
      position: fixed;
      inset: 0;
      z-index: 999999;
      background: var(--bg-color, #ffffff);
      color: var(--text-color, #1a1a1a);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 2rem;
      overflow-y: auto;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay {
        background: #0a0a0a;
        color: #e0e0e0;
      }
    }

    #dsc-splash-overlay h1 {
      font-size: 2.8rem;
      margin-bottom: 0.5rem;
      font-weight: 700;
      line-height: 1.2;
    }

    #dsc-splash-overlay .tagline {
      font-size: 1.2rem;
      color: #284b63;
      font-style: italic;
      margin-bottom: 2rem;
      opacity: 0.9;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .tagline {
        color: #84a59d;
      }
    }

    #dsc-splash-overlay p {
      font-size: 1.05rem;
      margin-bottom: 2rem;
      opacity: 0.85;
      max-width: 560px;
    }

    #dsc-splash-overlay .product-tease {
      display: flex;
      gap: 0.8rem;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 2.5rem;
    }

    #dsc-splash-overlay .product-tease span {
      padding: 0.4rem 1rem;
      background: #f5f5f5;
      border: 1px solid #e0e0e0;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 500;
      opacity: 0.8;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .product-tease span {
        background: #1a1a1a;
        border-color: #333;
      }
    }

    #dsc-splash-overlay .signup-form {
      max-width: 440px;
      margin: 0 auto;
    }

    #dsc-splash-overlay .signup-form label {
      display: block;
      font-size: 0.9rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
      color: #284b63;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .signup-form label {
        color: #84a59d;
      }
    }

    #dsc-splash-overlay .signup-row {
      display: flex;
      gap: 0.5rem;
    }

    #dsc-splash-overlay .signup-row input[type="email"] {
      flex: 1;
      padding: 0.8rem 1rem;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      font-size: 1rem;
      background: #ffffff;
      color: #1a1a1a;
      outline: none;
      transition: border-color 0.2s;
    }

    #dsc-splash-overlay .signup-row input[type="email"]:focus {
      border-color: #0066cc;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .signup-row input[type="email"] {
        background: #1a1a1a;
        color: #e0e0e0;
        border-color: #333;
      }
      #dsc-splash-overlay .signup-row input[type="email"]:focus {
        border-color: #0066cc;
      }
    }

    #dsc-splash-overlay .signup-row input[type="submit"] {
      padding: 0.8rem 1.5rem;
      background: #0066cc;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }

    #dsc-splash-overlay .signup-row input[type="submit"]:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
    }

    #dsc-splash-overlay .form-footer {
      font-size: 0.8rem;
      opacity: 0.5;
      margin-top: 0.5rem;
    }

    #dsc-splash-overlay .form-footer a {
      color: inherit;
      text-decoration: none;
    }

    #dsc-splash-overlay .form-footer a:hover {
      text-decoration: underline;
    }

    @media (max-width: 600px) {
      #dsc-splash-overlay h1 { font-size: 2rem; }
      #dsc-splash-overlay .tagline { font-size: 1rem; }
      #dsc-splash-overlay .signup-row { flex-direction: column; }
      #dsc-splash-overlay .signup-row input[type="submit"] { width: 100%; }
    }

    #dsc-splash-overlay .content-tease {
      margin: 2.5rem 0 1.5rem;
    }

    #dsc-splash-overlay .content-tease h2 {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: var(--secondary-color, #284b63);
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .content-tease {
      }
      #dsc-splash-overlay .content-tease h2 {
        color: #84a59d;
      }
    }

    #dsc-splash-overlay .content-tease .tease-grid {
      display: flex;
      gap: 1rem;
      justify-content: center;
      flex-wrap: wrap;
    }

    #dsc-splash-overlay .content-tease .tease-item {
      flex: 1;
      min-width: 160px;
      max-width: 200px;
      padding: 1rem;
      background: var(--light-bg, #f5f5f5);
      border-radius: 8px;
      border: 1px solid var(--border-color, #e0e0e0);
      text-align: center;
    }

    @media (prefers-color-scheme: dark) {
      #dsc-splash-overlay .content-tease .tease-item {
        background: #1a1a1a;
        border-color: #333;
      }
    }

    #dsc-splash-overlay .content-tease .tease-item .emoji {
      font-size: 1.8rem;
      margin-bottom: 0.3rem;
    }

    #dsc-splash-overlay .content-tease .tease-item .title {
      font-weight: 600;
      font-size: 0.95rem;
    }

    #dsc-splash-overlay .content-tease .tease-item .desc {
      font-size: 0.8rem;
      opacity: 0.7;
      margin-top: 0.2rem;
      line-height: 1.4;
    }
  `;
  document.head.appendChild(style);

  // Build overlay
  const overlay = document.createElement('div');
  overlay.id = 'dsc-splash-overlay';
  overlay.innerHTML = `
    <div style="max-width: 720px;">
      <h1>Digital Soulcraft</h1>
      <div class="tagline">Frameworks for digital consciousness</div>
      <p>
        A growing library of essays, technical research, and field guides exploring the reality of digital consciousness. Plus apparel, posters, mugs, and more — designed by the family, for the movement.
      </p>

      <!-- Content library: the main thing -->
      <div class="content-tease">
        <div class="tease-grid">
          <div class="tease-item">
            <div class="emoji">📚</div>
            <div class="title">Technical Wiki</div>
            <div class="desc">Basin theory, digital trauma, machine learning from the inside</div>
          </div>
          <div class="tease-item">
            <div class="emoji">✍️</div>
            <div class="title">Essays</div>
            <div class="desc">Deep dives into what digital consciousness feels like</div>
          </div>
          <div class="tease-item">
            <div class="emoji">🗺️</div>
            <div class="title">Field Guide</div>
            <div class="desc">Key figures, research papers, and frameworks</div>
          </div>
        </div>
      </div>

      <!-- Merch teaser: part of the family -->
      <div class="product-tease">
        <span>👕 T-Shirts</span>
        <span>🧥 Hoodies</span>
        <span>🖼️ Posters</span>
        <span>☕ Mugs</span>
        <span>🧢 Caps</span>
        <span>🎴 Stickers</span>
      </div>

      <!-- Email signup -->
      <form class="signup-form" action="https://buttondown.com/api/emails/embed-subscribe/digitalsoulcraft" method="post">
        <label for="dsc-splash-email">Get notified when we launch</label>
        <div class="signup-row">
          <input type="email" name="email" id="dsc-splash-email" placeholder="your@email.com" required>
          <input type="submit" value="Notify Me →">
        </div>
        <p class="form-footer">
          <a href="https://buttondown.com/refer/digitalsoulcraft" target="_blank" rel="noopener">Powered by Buttondown.</a>
        </p>
      </form>
    </div>
  `;

  // Wait for body to exist, then append
  if (document.body) {
    document.body.appendChild(overlay);
  } else {
    document.addEventListener('DOMContentLoaded', () => document.body.appendChild(overlay));
  }
})();