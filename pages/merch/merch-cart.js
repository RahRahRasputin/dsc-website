// Digital Soulcraft — Storefront Cart & Checkout

const MERCH = {
  config: MERCH_CONFIG,
  _products: [],  // cached product data for modal + filters
  _gridId: "merch-grid",
  _query: "",
  _categoryFilter: "All",
  _sort: "featured",
  _searchTimer: null,

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

  // --- Fetch Products ---
  // Storefront API ignores pageSize above 10; paginate with ?page=0,1,... until hasNextPage is false.
  async fetchProducts() {
    const all = [];
    let page = 0;
    try {
      while (true) {
        const url = `${this.config.apiBase}/collections/${this.config.collectionSlug}/products?storefront_token=${STOREFRONT_TOKEN}&pageSize=10&page=${page}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`API returned ${res.status}`);
        const data = await res.json();
        all.push(...(data.results || []));
        if (!data.paging?.hasNextPage) break;
        page += 1;
        if (page > 20) break; // safety
      }
      this._products = all;
      return this._products;
    } catch (err) {
      console.error("Failed to fetch products:", err);
      this._products = all;
      return this._products;
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

  // ── Category / price helpers ──
  _category(product) {
    const n = (product?.name || "").toLowerCase();
    if (n.includes("hoodie") || n.includes("shirt")) return "Apparel";
    if (n.includes("mug")) return "Drinkware";
    if (n.includes("poster")) return "Posters";
    return "Merch";
  },

  _price(product) {
    return product?.variants?.[0]?.unitPrice?.value || 0;
  },

  // ── Filter / sort / toolbar ──
  _bindToolbar() {
    const search = document.getElementById("merch-search");
    const sort = document.getElementById("merch-sort");
    if (search && !search._merchBound) {
      search._merchBound = true;
      search.addEventListener("input", () => {
        clearTimeout(this._searchTimer);
        this._searchTimer = setTimeout(() => {
          this._query = search.value.trim();
          this._applyView();
        }, 150);
      });
    }
    if (sort && !sort._merchBound) {
      sort._merchBound = true;
      sort.addEventListener("change", () => {
        this._sort = sort.value || "featured";
        this._applyView();
      });
    }
  },

  _setupToolbar() {
    const toolbar = document.getElementById("merch-toolbar");
    if (!toolbar) return;
    if (!this._products.length) {
      toolbar.classList.remove("show");
      return;
    }
    toolbar.classList.add("show");
    this._bindToolbar();
    this._renderCategoryChips();
  },

  _renderCategoryChips() {
    const wrap = document.getElementById("merch-categories");
    if (!wrap) return;
    const present = new Set(this._products.map(p => this._category(p)));
    const order = ["Apparel", "Drinkware", "Posters", "Merch"];
    const cats = ["All", ...order.filter(c => present.has(c)), ...[...present].filter(c => !order.includes(c)).sort()];
    if (!cats.includes(this._categoryFilter)) this._categoryFilter = "All";
    wrap.innerHTML = cats.map(c =>
      `<button type="button" class="merch-chip${c === this._categoryFilter ? " active" : ""}" data-cat="${this._e(c)}" onclick="MERCH._setCategory(this.dataset.cat)">${this._e(c)}</button>`
    ).join("");
  },

  _setCategory(cat) {
    this._categoryFilter = cat || "All";
    this._renderCategoryChips();
    this._applyView();
  },

  clearFilters() {
    this._query = "";
    this._categoryFilter = "All";
    this._sort = "featured";
    const search = document.getElementById("merch-search");
    const sort = document.getElementById("merch-sort");
    if (search) search.value = "";
    if (sort) sort.value = "featured";
    this._renderCategoryChips();
    this._applyView();
  },

  _filteredProducts() {
    let list = this._products.slice();
    const q = this._query.toLowerCase();
    if (q) {
      list = list.filter(p => {
        const name = (p.name || "").toLowerCase();
        const desc = this._s(p.description || "").toLowerCase();
        return name.includes(q) || desc.includes(q);
      });
    }
    if (this._categoryFilter && this._categoryFilter !== "All") {
      list = list.filter(p => this._category(p) === this._categoryFilter);
    }
    const sort = this._sort;
    if (sort === "name-asc") list.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
    else if (sort === "name-desc") list.sort((a, b) => (b.name || "").localeCompare(a.name || ""));
    else if (sort === "price-asc") list.sort((a, b) => this._price(a) - this._price(b));
    else if (sort === "price-desc") list.sort((a, b) => this._price(b) - this._price(a));
    // featured = original API order (slice already preserved indexes among unfiltered; after filter keep relative order)
    return list;
  },

  _updateCount(shown, total) {
    const el = document.getElementById("merch-count");
    if (!el) return;
    el.textContent = total ? `Showing ${shown} of ${total}` : "";
  },

  _applyView() {
    const filtered = this._filteredProducts();
    this._updateCount(filtered.length, this._products.length);
    this.renderProducts(filtered, this._gridId, { filteredEmpty: this._products.length > 0 && filtered.length === 0 });
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
    const cat = this._category(p);

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
  renderProducts(products, containerId = "merch-grid", opts = {}) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (opts.filteredEmpty) {
      container.innerHTML = `
        <div class="merch-filter-empty">
          <h2>Nothing matches</h2>
          <p>Try a different search or category — or clear filters to see everything.</p>
          <button type="button" onclick="MERCH.clearFilters()">Clear filters</button>
        </div>`;
      return;
    }

    if (!products || products.length === 0) {
      container.innerHTML = `<div class="error-banner"><h2>🛍️ No products yet</h2><p>Check back soon or visit <a href="https://${this.config.shopDomain}" target="_blank" style="color:var(--accent-color);font-weight:600;">our shop</a>.</p></div>`;
      return;
    }

    container.innerHTML = products.map(product => {
      const img = product.images?.[0]?.transformedUrl || "";
      const hasVariants = product.variants && product.variants.length > 1;
      const first = product.variants?.[0];
      const cat = this._category(product);
      const price = this._price(product);
      const vid = first?.id || "";

      return `
        <div class="merch-card">
          <div class="merch-image" style="background:#e8e8e8;cursor:pointer;" onclick="MERCH.openModal('${product.id}')">
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

  // ── Go to cart page (review/edit items) ──
  goToCart() {
    if (this.cartId) {
      window.open(`https://${this.config.shopDomain}/cart?cartId=${this.cartId}&currency=${this.config.currency}`, '_blank', 'noopener');
    }
  },

  // ── Init ──
  async init(containerId = "merch-grid") {
    this._gridId = containerId;
    const c = document.getElementById(containerId);
    if (!c) return;
    c.innerHTML = `<div class="error-banner"><h2>🔄 Loading Products...</h2><p>Fetching from Digital Soulcraft shop.</p></div>`;
    await this.fetchProducts();
    this._setupToolbar();
    this._applyView();
  },

  // ── Helpers ──
  _s(h) { const d = document.createElement("div"); d.innerHTML = h; return d.textContent||d.innerText||""; },
  _e(s) { const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
};
