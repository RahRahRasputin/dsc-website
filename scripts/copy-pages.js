#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pagesDir = path.join(__dirname, '..', 'pages');
const publicDir = path.join(__dirname, '..', 'public');

function copyDir(src, dest) {
  // Create destination if it doesn't exist
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const files = fs.readdirSync(src);

  files.forEach(file => {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);

    // Don't copy the 'garden' folder (preserve Quartz output)
    if (file === 'garden') {
      console.log(`⊘ Skipped: garden/ (Quartz output)`);
      return;
    }

    const stat = fs.statSync(srcPath);

    if (stat.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
      console.log(`✓ Copied: ${file}`);
    }
  });
}

console.log('📋 Copying static pages from pages/ to public/...');
copyDir(pagesDir, publicDir);
console.log('✅ Pages copied successfully!');
