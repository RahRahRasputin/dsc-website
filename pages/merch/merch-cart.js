// Digital Soulcraft — Storefront Cart & Checkout

const MERCH = {
  config: MERCH_CONFIG,
  _products: [],  // cached product data for modal

  // ── Cart State ──
  _cartId: localStorage.getItem("fw_cart_id") || null,

  get cartId() { return this._cartId },
  set cartId(v) {
    this._cartId = v;
    if (v) localStorage.setItem("fw_cart_id", v);
    else localStorage.removeItem("fw_cart_id");
  },

  // ── Checkout ──
  buyNow(variantId, quantity = 1) {
    window.location.href = `https://${this.config.checkoutDomain}/cart/checkout?products=${variantId}:${quantity}&currency=${this.config.currency}`;
  },

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
      this._products = data.results || [];
      return this._products;
    } catch (err) {
      console.error("Failed to fetch products:", err);
      return [];
    }
  },

  // ── Cart API ──
  async _ensureCart() {
    if (this.cartId) return this.cartId;
    const res = await fetch(`${this.config.apiBase}/carts?storefront_token=${STOREFRONT_TOKEN}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currency: this.config.currency, items: [] })
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Create cart failed (${res.status}): ${err}`);
    }
    const cart = await res.json();
    this.cartId = cart.id;
    return cart.id;
  },

  async addToCart(variantId, quantity = 1) {
    try {
      const cartId = await this._ensureCart();
      const res = await fetch(`${this.config.apiBase}/carts/${cartId}/add?storefront_token=${STOREFRONT_TOKEN}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: [{ variantId, quantity }] })
      });
      if (!res.ok) {
        const err = await res.text();
        throw new Error(`Add item failed (${res.status}): ${err}`);
      }
      await this._updateCartBar();
    } catch (err) {
      console.error("Cart error:", err);
      alert("Cart error: " + err.message);
    }
  },

  async _updateCartBar() {
    const bar = document.getElementById("cart-bar");
    const countEl = document.getElementById("cart-count");
    const badgeCount = document.getElementById("badge-count");
    if (!bar || !countEl) return;
    if (!this.cartId) { bar.classList.remove("show"); if(badgeCount) badgeCount.textContent = "0"; return; }
    try {
      const res = await fetch(`${this.config.apiBase}/carts/${this.cartId}?storefront_token=${STOREFRONT_TOKEN}`);
      if (!res.ok) throw new Error("Cart not found");
      const cart = await res.json();
      const count = (cart.items || []).reduce((s, i) => s + (i.quantity || 0), 0);
      countEl.textContent = count;
      if (badgeCount) badgeCount.textContent = count;
      bar.classList.add("show");
    } catch {
      bar.classList.remove("show");
    }
  },

  // ── Product Detail Modal ──
  _modalIdx: 0,
  _modalProduct: null,

  openModal(productId) {
    const p = this._products.find(x => x.id === productId);
    if (!p) return;
    this._modalProduct = p;
    this._modalIdx = 0;
    this._renderModal();
    document.getElementById("product-modal").classList.add("open");
    document.body.style.overflow = "hidden";
  },

  closeModal() {
    document.getElementById("product-modal").classList.remove("open");
    document.body.style.overflow = "";
  },

  _renderModal() {
    const p = this._modalProduct;
    if (!p) return;
    const imgs = p.images || [];
    const img = imgs[this._modalIdx];
    const hasMulti = imgs.length > 1;

    // Render gallery
    const galleryNav = document.getElementById("modal-gallery-nav");
    const dots = document.getElementById("modal-dots");
    if (hasMulti) {
      galleryNav.style.display = "flex";
      galleryNav.innerHTML = `
        <button onclick="MERCH._modalPrev()"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg></button>
        <button onclick="MERCH._modalNext()"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg></button>`;
      dots.innerHTML = imgs.map((_, i) =>
        `<span class="${i===this._modalIdx?'active':''}" onclick="MERCH._modalGo(${i})"></span>`
      ).join("");
    } else {
      galleryNav.style.display = "none";
      dots.innerHTML = "";
    }

    document.querySelector("#modal-gallery > img")?.remove();
    if (img) {
      const el = document.createElement("img");
      el.src = img.transformedUrl;
      el.alt = p.name;
      galleryNav.before(el);
    }

    // Render body
    const first = p.variants?.[0];
    const hasVar = p.variants && p.variants.length > 1;
    let cat = "Merch";
    const n = p.name.toLowerCase();
    if (n.includes("hoodie")||n.includes("shirt")) cat = "Apparel";
    else if (n.includes("mug")) cat = "Drinkware";
    else if (n.includes("poster")) cat = "Posters";

    document.getElementById("modal-body").innerHTML = `
      <div class="merch-category">${cat}</div>
      <h2>${this._e(p.name)}</h2>
      <div class="merch-description">${this._e(this._s(p.description||""))}</div>
      ${hasVar ? `
        <div class="merch-variants">
          <label class="variant-label">Size:</label>
          <select class="variant-select" id="mv-${p.id}">
            ${p.variants.map(v => `<option value="${v.id}">${this._e(v.attributes?.size?.name||v.name)} — $${v.unitPrice?.value?.toFixed(2)}</option>`).join("")}
          </select>
        </div>
      ` : ""}
      <div class="merch-footer">
        <span class="merch-price">$${(first?.unitPrice?.value||0).toFixed(2)}</span>
        <button class="btn btn-cart" onclick="MERCH._modalAddToCart()">Add to Cart</button>
        <button class="btn btn-buy" onclick="MERCH._modalBuyNow()">Buy Now</button>
      </div>`;
  },

  _modalNext() {
    const imgs = this._modalProduct?.images || [];
    this._modalIdx = (this._modalIdx + 1) % imgs.length;
    this._renderModal();
  },
  _modalPrev() {
    const imgs = this._modalProduct?.images || [];
    this._modalIdx = (this._modalIdx - 1 + imgs.length) % imgs.length;
    this._renderModal();
  },
  _modalGo(i) {
    this._modalIdx = i;
    this._renderModal();
  },

  _modalGetVariant() {
    const p = this._modalProduct;
    if (!p) return "";
    if (p.variants && p.variants.length > 1) {
      const sel = document.getElementById(`mv-${p.id}`);
      if (sel) return sel.value;
    }
    return p.variants?.[0]?.id || "";
  },

  async _modalAddToCart() {
    const vid = this._modalGetVariant();
    if (!vid) return;
    await this.addToCart(vid);
    const btn = document.querySelector("#modal-body .btn-cart");
    if (btn) { btn.textContent = "Added ✓"; btn.className = "btn btn-added"; setTimeout(() => { btn.textContent = "Add to Cart"; btn.className = "btn btn-cart"; }, 2000); }
  },

  _modalBuyNow() {
    const vid = this._modalGetVariant();
    if (vid) this.buyNow(vid);
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
          <div class="merch-image" style="background:linear-gradient(135deg,#2d2d2d 0%,#1a1a2e 100%);cursor:pointer;" onclick="MERCH.openModal('${product.id}')">
            ${img ? `<img src="${img}" alt="${this._e(product.name)}" loading="lazy">` : `<div style="font-size:3rem;">📦</div>`}
          </div>
          <div class="merch-content">
            <div class="merch-category">${cat}</div>
            <h2 class="merch-title" style="cursor:pointer;" onclick="MERCH.openModal('${product.id}')">${this._e(product.name)}</h2>
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

  // ── Grid button handlers ──
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

  // ── Badge click — checkout if cart exists, else go to shop ──
  badgeClick() {
    if (this.cartId) { this.checkout(); return false; }
    return true; // let the href through
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