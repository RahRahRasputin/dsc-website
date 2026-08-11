#!/bin/bash
# Generate token file for merch storefront
# Called by Netlify build — STOREFRONT_TOKEN comes from env var
mkdir -p pages/merch
cat > pages/merch/_token.js << EOF
const STOREFRONT_TOKEN = '${STOREFRONT_TOKEN}';
EOF