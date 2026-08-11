// Digital Soulcraft — Merch Store Config
// Fourthwall Storefront API configuration

const MERCH_CONFIG = {
  // IMPORTANT: The token is injected by Netlify at build time via $STOREFRONT_TOKEN
  // Set this env var in Netlify Dashboard → Site settings → Environment variables
  storefrontToken: "__STOREFRONT_TOKEN__",
  shopDomain: "digitalsoulcraft-shop.fourthwall.com",
  checkoutDomain: "digitalsoulcraft-shop.fourthwall.com",
  collectionSlug: "soulcraft-merch",
  currency: "USD",
  apiBase: "https://storefront-api.fourthwall.com/v1"
};

// Default variant IDs (first/cheapest option for quick-buy)
const DEFAULT_VARIANTS = {
  // Product ID -> default variant ID
  "0328217a-2f80-4ee5-9be4-42acb64c9dfd": "237029df-c0f3-41c7-b686-9e23f359f11d", // Poster - 12x18
  "7c45f824-0af2-4a04-a728-1bdb21a57dce": "b9ff7b09-8977-4019-a161-b8c31f18543f", // Hoodie - S
  "83414a54-eb27-4af0-badf-32c102e74971": "49aff5a5-0381-4c4c-9e63-8b6c14abd3d5"   // Mug - 11oz
};