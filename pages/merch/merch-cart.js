// Digital Soulcraft — Storefront Cart & Checkout
// Handles cart creation, item management, and checkout redirect

const MERCH = {
  // Config
  config: MERCH_CONFIG,

  // Direct checkout — no cart needed, uses products= parameter
  buyNow(variantId, quantity = 1) {
    const url = `https://${this.config.checkoutDomain}/cart/checkout?products=${variantId}:${quantity}&currency=${this.config.currency}`;
    window.location.href = url;
  },

  // Fetch products from Storefront API
  async fetchProducts() {
    const url = `${this.config.apiBase}/collections/${this.config.collectionSlug}/products?storefront_token=${this.config.storefrontToken}&pageSize=20`;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      const data = await res.json();
      return data.results || [];
    } catch (err) {
      console.error("Failed to fetch products:", err);
      return [];
    }
  },

  // Render product cards into a container
  renderProducts(products, containerId = "merch-grid") {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!products || products.length === 0) {
      container.innerHTML = `
        <div class="coming-soon-banner">
          <h2>🛍️ Loading Products...</h2>
          <p>If products don't appear, check back soon or visit our <a href="https://${this.config.shopDomain}" target="_blank" style="color: var(--accent-color); font-weight: 600;">shop directly</a>.</p>
        </div>`;
      return;
    }

    container.innerHTML = products.map(product => {
      const defaultImg = product.images?.[0]?.transformedUrl || "";
      const thumbImg = product.images?.[0]?.transformedUrl || "";
      const hasMultipleVariants = product.variants && product.variants.length > 1;
      const firstVariant = product.variants?.[0];

      // Determine category from product name
      let category = "Merch";
      const name = product.name.toLowerCase();
      if (name.includes("hoodie") || name.includes("shirt") || name.includes("tee")) category = "Apparel";
      else if (name.includes("mug") || name.includes("cup")) category = "Drinkware";
      else if (name.includes("poster") || name.includes("print")) category = "Posters";

      const price = firstVariant?.unitPrice?.value || 0;
      const variantId = firstVariant?.id || "";

      return `
        <div class="merch-card">
          <div class="merch-image" style="background: linear-gradient(135deg, #2d2d2d 0%, #1a1a2e 100%);">
            ${thumbImg ? `<img src="${thumbImg}" alt="${this._escapeHtml(product.name)}" style="width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;" loading="lazy">` : `<div class="merch-image-text">📦</div>`}
          </div>
          <div class="merch-content">
            <div class="merch-category">${category}</div>
            <h2 class="merch-title">${this._escapeHtml(product.name)}</h2>
            <p class="merch-description">${this._escapeHtml(this._stripHtml(product.description || ""))}</p>
            ${hasMultipleVariants ? `
              <div class="merch-variants">
                <label class="variant-label" for="variant-${product.id}">Size:</label>
                <select class="variant-select" id="variant-${product.id}" data-product-id="${product.id}">
                  ${product.variants.map(v => `
                    <option value="${v.id}">${this._escapeHtml(v.attributes?.size?.name || v.name)} — $${v.unitPrice?.value?.toFixed(2)}</option>
                  `).join("")}
                </select>
              </div>
            ` : ""}
            <div class="merch-footer">
              <span class="merch-price">$${price.toFixed(2)}</span>
              <button class="merch-buy-btn" 
                data-variant-id="${variantId}" 
                data-product-id="${product.id}"
                ${hasMultipleVariants ? `data-has-variants="true"` : ""}
                onclick="MERCH.handleBuy(this)">
                Buy Now
              </button>
            </div>
          </div>
        </div>
      `;
    }).join("");

    // Hide the "Coming Soon" banner if it exists
    const banner = document.getElementById("coming-soon-banner");
    if (banner) banner.style.display = "none";
  },

  // Handle Buy button click
  handleBuy(button) {
    const productId = button.dataset.productId;
    const hasVariants = button.dataset.hasVariants === "true";

    let variantId = button.dataset.variantId;
    if (hasVariants) {
      const select = document.getElementById(`variant-${productId}`);
      if (select) variantId = select.value;
    }

    if (variantId) {
      this.buyNow(variantId);
    }
  },

  // Initialise the merch page
  async init(containerId = "merch-grid") {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Show loading state
    container.innerHTML = `
      <div class="coming-soon-banner">
        <h2>🔄 Loading Products...</h2>
        <p>Fetching from Fourthwall...</p>
      </div>`;

    const products = await this.fetchProducts();
    this.renderProducts(products, containerId);
  },

  // Helpers
  _stripHtml(html) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  },

  _escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
};