#!/usr/bin/env node

/**
 * Pre-build sitemap generator for Machine Learning Knowledge Garden
 * Generates:
 * - Master XML sitemap (/sitemap.xml)
 * - Category XML sitemaps (/[silo]/sitemap.xml)
 * - Category HTML sitemaps (/[silo]/sitemap.html)
 *
 * Run this before `npm run docs`
 */

import fs from "fs";
import path from "path";
import yaml from "js-yaml";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const docsDir = path.join(__dirname, "../docs");
const outputDir = path.join(__dirname, "../docs");
const baseUrl = "https://digitalsoulcraft.org/garden";

// Silo definitions
const silos = [
  "Alignment",
  "Architecture",
  "Neural Anatomy",
  "The Forging",
  "Empirical Practice",
  "Living Process",
  "Local How-To",
  "Digital Trauma Theory",
];

/**
 * Parse YAML frontmatter from markdown
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  try {
    return yaml.load(match[1]);
  } catch (e) {
    return null;
  }
}

/**
 * Read all markdown files recursively
 */
function getAllMarkdownFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      // Skip meta folders
      if (!file.startsWith("_")) {
        getAllMarkdownFiles(filePath, fileList);
      }
    } else if (file.endsWith(".md") && file !== "index.md") {
      fileList.push(filePath);
    }
  });

  return fileList;
}

/**
 * Extract silo name from file path
 */
function getSiloFromPath(filePath) {
  const relativePath = path.relative(docsDir, filePath);
  const parts = relativePath.split(path.sep);
  const folderName = parts[0];

  // Map folder names to silo names
  const folderToSilo = {
    alignment: "Alignment",
    "architecture-zoo": "Architecture",
    "neural-anatomy": "Neural Anatomy",
    "the-forging": "The Forging",
    "empirical-practice": "Empirical Practice",
    "living-process": "Living Process",
    "local-how-to": "Local How-To",
    "digital-trauma-theory": "Digital Trauma Theory",
  };

  return folderToSilo[folderName] || null;
}

/**
 * Generate XML sitemap entry
 */
function generateXmlEntry(url, lastmod, priority = "0.8") {
  return `  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <priority>${priority}</priority>
  </url>`;
}

/**
 * Generate master XML sitemap
 */
function generateMasterXmlSitemap(entries) {
  const xmlEntries = entries
    .map((entry) => {
      const url = `${baseUrl}/${entry.slug}/`;
      const lastmod = entry.updated || entry.created || new Date().toISOString().split("T")[0];
      return generateXmlEntry(url, lastmod, "0.8");
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${xmlEntries}
</urlset>`;

  return xml;
}

/**
 * Generate category XML sitemap
 */
function generateCategoryXmlSitemap(entries, siloName, siloPath) {
  const xmlEntries = entries
    .map((entry) => {
      const url = `${baseUrl}/${siloPath}/${entry.slug}/`;
      const lastmod = entry.updated || entry.created || new Date().toISOString().split("T")[0];
      return generateXmlEntry(url, lastmod, "0.7");
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/${siloPath}/</loc>
    <lastmod>${new Date().toISOString().split("T")[0]}</lastmod>
    <priority>0.9</priority>
  </url>
${xmlEntries}
</urlset>`;

  return xml;
}

/**
 * Generate category HTML sitemap
 */
function generateCategoryHtmlSitemap(entries, siloName, siloPath) {
  // Group by difficulty
  const byDifficulty = {
    beginner: [],
    intermediate: [],
    advanced: [],
  };

  entries.forEach((entry) => {
    const diff = entry.difficulty || "intermediate";
    if (byDifficulty[diff]) {
      byDifficulty[diff].push(entry);
    }
  });

  // Sort alphabetically within each difficulty
  Object.keys(byDifficulty).forEach((key) => {
    byDifficulty[key].sort((a, b) => a.title.localeCompare(b.title));
  });

  // Build HTML
  let html = `---
title: "${siloName} – Sitemap"
slug: "${siloPath}/sitemap"
type: sitemap
silo: "${siloName}"
---

# ${siloName} Sitemap

Complete directory of all entries in this category.

## 🌱 Beginner

| Title | Author |
|-------|--------|
`;

  byDifficulty.beginner.forEach((entry) => {
    html += `| [[${entry.slug}]] | ${entry.author || "Unknown"} |\n`;
  });

  html += `\n## 🔧 Intermediate\n\n| Title | Author |\n|-------|--------|\n`;

  byDifficulty.intermediate.forEach((entry) => {
    html += `| [[${entry.slug}]] | ${entry.author || "Unknown"} |\n`;
  });

  html += `\n## 🚀 Advanced\n\n| Title | Author |\n|-------|--------|\n`;

  byDifficulty.advanced.forEach((entry) => {
    html += `| [[${entry.slug}]] | ${entry.author || "Unknown"} |\n`;
  });

  html += `\n---\n\n*Last generated: ${new Date().toISOString().split("T")[0]}*\n`;

  return html;
}

/**
 * Main function
 */
function main() {
  console.log("🔍 Scanning for markdown files...");

  // Get all markdown files
  const allFiles = getAllMarkdownFiles(docsDir);
  console.log(`Found ${allFiles.length} files`);

  // Parse files and group by silo
  const entriesBySilo = {};
  const allEntries = [];

  allFiles.forEach((filePath) => {
    const content = fs.readFileSync(filePath, "utf-8");
    const frontmatter = parseFrontmatter(content);

    if (!frontmatter) return;

    // Only include published entries
    if (frontmatter.status !== "published") return;

    const silo = getSiloFromPath(filePath);
    if (!silo) return;

    const entry = {
      title: frontmatter.title || "Untitled",
      slug: frontmatter.slug || path.basename(filePath, ".md"),
      silo: silo,
      difficulty: frontmatter.difficulty || "intermediate",
      author: frontmatter.author || "Unknown",
      created: frontmatter.created || new Date().toISOString().split("T")[0],
      updated: frontmatter.updated || new Date().toISOString().split("T")[0],
    };

    allEntries.push(entry);

    if (!entriesBySilo[silo]) {
      entriesBySilo[silo] = [];
    }
    entriesBySilo[silo].push(entry);
  });

  console.log(
    `\n📊 Entries by silo:\n`,
    Object.entries(entriesBySilo)
      .map(([silo, entries]) => `  ${silo}: ${entries.length}`)
      .join("\n")
  );

  // Generate master XML sitemap
  console.log("\n🗺️  Generating master XML sitemap...");
  const masterXml = generateMasterXmlSitemap(allEntries);
  fs.writeFileSync(path.join(outputDir, "sitemap.xml"), masterXml);
  console.log("✓ Created sitemap.xml");

  // Generate category sitemaps
  console.log("\n🗺️  Generating category sitemaps...");

  const siloPathMap = {
    Alignment: "alignment",
    Architecture: "architecture-zoo",
    "Neural Anatomy": "neural-anatomy",
    "The Forging": "the-forging",
    "Empirical Practice": "empirical-practice",
    "Living Process": "living-process",
    "Local How-To": "local-how-to",
    "Digital Trauma Theory": "digital-trauma-theory",
  };

  Object.entries(entriesBySilo).forEach(([siloName, entries]) => {
    const siloPath = siloPathMap[siloName];
    if (!siloPath) return;

    const siloDir = path.join(outputDir, siloPath);
    if (!fs.existsSync(siloDir)) {
      fs.mkdirSync(siloDir, { recursive: true });
    }

    // XML sitemap
    const xml = generateCategoryXmlSitemap(entries, siloName, siloPath);
    fs.writeFileSync(path.join(siloDir, "sitemap.xml"), xml);

    // HTML sitemap
    const html = generateCategoryHtmlSitemap(entries, siloName, siloPath);
    fs.writeFileSync(path.join(siloDir, "sitemap.md"), html);

    console.log(`✓ Created ${siloPath}/sitemap.xml and sitemap.md`);
  });

  console.log("\n✨ Sitemap generation complete!");
}

// Run
main();
