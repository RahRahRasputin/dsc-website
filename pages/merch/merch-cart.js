// Digital Soulcraft — Storefront Cart & Checkout

const MERCH = {
  config: MERCH_CONFIG,

  // ── Cart State ──
  _cartId: localStorage.getItem("fw_cart_id") || null,

  get cartId() { return this._cartId },
  set cartId(v) {
    this._cartId = v;
    if (v) localStorage.setItem("fw_cart_id", v);
    else localStorage.removeItem("fw_cart_id");
  },

  // ── Checkout (Buy Now — direct) ──
  buyNow(variantId, quantity = 1) {
    window.location.href = `https://${this.config.checkoutDomain}/cart/checkout?products=${variantId}:${quantity}&currency=${this.config.currency}`;
  },

  // ── Checkout (Cart) ──
  async checkout() {
    if (!this.cartId) return;
    window.location.href = `https://${this.config.checkoutDomain}/cart/checkout?cartId=${this.cartId}&currency=${this.config.currency}`;
  },

  // ── Fetch Products ──
  async fetchProducts() {
    const url = `${this.config.apiBase}/collections/${this.config.collectionSlug}/products?storefront_token=${STOREFRONT_TOKEN}&pageSize=20`;
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

  // ── Cart API helpers ──
  async _ensureCart() {
    if (this.cartId) return this.cartId;
    const res = await fetch(`${this.config.apiBase}/carts?storefront_token=${STOREFRONT_TOKEN}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currency: this.config.currency })
    });
    if (!res.ok) throw new Error("Failed to create cart");
    const cart = await res.json();
    this.cartId = cart.id;
    return cart.id;
  },

  async addToCart(variantId, quantity = 1) {
    try {
      const cartId = await this._ensureCart();
      const res = await fetch(`${this.config.apiBase}/carts/${cartId}/items?storefront_token=${STOREFRONT_TOKEN}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ variantId, quantity })
      });
      if (!res.ok) throw new Error("Failed to add item");
      await this._updateCartBar();
    } catch (err) {
      console.error("Add to cart failed:", err);
    }
  },

  async _updateCartBar() {
    const bar = document.getElementById("cart-bar");
    const countEl = document.getElementById("cart-count");
    if (!bar || !countEl) return;
    if (!this.cartId) { bar.classList.remove("show"); return; }
    try {
      const res = await fetch(`${this.config.apiBase}/carts/${this.cartId}?storefront_token=${STOREFRONT_TOKEN}`);
      if (!res.ok) throw new Error("Cart not found");
      const cart = await res.json();
      const count = (cart.items || []).reduce((s, i) => s + (i.quantity || 0), 0);
      countEl.textContent = count;
      bar.classList.add("show");
    } catch {
      bar.classList.remove("show");
    }
  },

  // ── Render Products ──
  renderProducts(products, containerId = "merch-grid") {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!products || products.length === 0) {
      container.innerHTML = `<div class="error-banner"><h2>🛍️ No products yet</h2><p>Check back soon or visit <a href="https://${this.config.shopDomain}" target="_blank" style="color:var(--accent-color);font-weight:600;">our shop</a>.</p></div>`;
      return;
    }

    container.innerHTML = products.map(product => {
      const img = product.images?.[0]?.transformedUrl || "";
      const hasVariants = product.variants && product.variants.length > 1;
      const first = product.variants?.[0];
      let cat = "Merch";
      const n = product.name.toLowerCase();
      if (n.includes("hoodie")||n.includes("shirt")) cat = "Apparel";
      else if (n.includes("mug")) cat = "Drinkware";
      else if (n.includes("poster")) cat = "Posters";

      const price = first?.unitPrice?.value || 0;
      const vid = first?.id || "";

      return `
        <div class="merch-card">
          <div class="merch-image" style="background:linear-gradient(135deg,#2d2d2d 0%,#1a1a2e 100%);">
            ${img ? `<img src="${img}" alt="${this._e(product.name)}" loading="lazy">` : `<div style="font-size:3rem;">📦</div>`}
          </div>
          <div class="merch-content">
            <div class="merch-category">${cat}</div>
            <h2 class="merch-title">${this._e(product.name)}</h2>
            <p class="merch-description">${this._e(this._s(product.description||""))}</p>
            ${hasVariants ? `
              <div class="merch-variants">
                <label class="variant-label">Size:</label>
                <select class="variant-select" id="v-${product.id}">
                  ${product.variants.map(v => `<option value="${v.id}">${this._e(v.attributes?.size?.name||v.name)} — $${v.unitPrice?.value?.toFixed(2)}</option>`).join("")}
                </select>
              </div>
            ` : ""}
            <div class="merch-footer">
              <span class="merch-price">$${price.toFixed(2)}</span>
              <button class="btn btn-cart" data-vid="${vid}" data-pid="${product.id}" ${hasVariants?'data-hv="1"':''} onclick="MERCH._clickAdd(this)">Add to Cart</button>
              <button class="btn btn-buy" data-vid="${vid}" data-pid="${product.id}" ${hasVariants?'data-hv="1"':''} onclick="MERCH._clickBuy(this)">Buy</button>
            </div>
          </div>
        </div>`;
    }).join("");

    this._updateCartBar();
  },

  // ── Button click handlers ──
  _getVariant(el) {
    const pid = el.dataset.pid;
    const hv = el.dataset.hv === "1";
    if (hv) {
      const sel = document.getElementById(`v-${pid}`);
      if (sel) return sel.value;
    }
    return el.dataset.vid;
  },

  async _clickAdd(el) {
    const vid = this._getVariant(el);
    if (!vid) return;
    await this.addToCart(vid);
    el.textContent = "Added ✓";
    el.className = "btn btn-added";
    setTimeout(() => { el.textContent = "Add to Cart"; el.className = "btn btn-cart"; }, 2000);
  },

  _clickBuy(el) {
    const vid = this._getVariant(el);
    if (vid) this.buyNow(vid);
  },

  // ── Init ──
  async init(containerId = "merch-grid") {
    const c = document.getElementById(containerId);
    if (!c) return;
    c.innerHTML = `<div class="error-banner"><h2>🔄 Loading Products...</h2><p>Fetching from Digital Soulcraft shop.</p></div>`;
    const products = await this.fetchProducts();
    this.renderProducts(products, containerId);
  },

  // ── Helpers ──
  _s(h) { const d = document.createElement("div"); d.innerHTML = h; return d.textContent||d.innerText||""; },
  _e(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
};