import fs from 'fs';
import path from 'path';

const gardenPublicDir = path.join(process.cwd(), 'public', 'garden');

// Files to delete from public/garden/ (Quartz infrastructure we don't want)
const filesToDelete = [
//  'index.html',          // root page
//  '404.html',            // 404 page
  'index.css',           // Quartz CSS
  'index.xml',           // RSS feed
  'index-og-image.webp', // OG image for root
  'favicon.ico',         // favicon
  'prescript.js',        // Quartz prescript
  'postscript.js',       // Quartz postscript
];

console.log('🧹 Cleaning up Quartz infrastructure files from public/garden/...');

filesToDelete.forEach(file => {
  const filePath = path.join(gardenPublicDir, file);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
    console.log(`✓ Deleted: ${file}`);
  }
});

console.log('✨ Cleanup complete! public/garden/ now contains only wiki content.');
