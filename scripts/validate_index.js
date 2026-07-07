#!/usr/bin/env node
/**
 * JS smoke-check for index.html.
 *
 * The dashboard is a single file whose entire UI is driven by one `const DATA = {...}`
 * object literal. A single syntax error there (see the 2026-07-03 and 2026-07-07
 * auto-sync incidents) blanks the whole live site with no other symptom. This script
 * extracts that object, evaluates it in an isolated VM, and asserts the shape is sane.
 *
 * Run locally:   node scripts/validate_index.js
 * In CI it gates the GitHub Pages deploy, so a broken DATA block never ships.
 * Exits non-zero (and prints why) on any problem.
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const INDEX = path.join(__dirname, "..", "index.html");

function fail(msg) {
  console.error("❌ index.html validation FAILED: " + msg);
  process.exit(1);
}

const html = fs.readFileSync(INDEX, "utf8");

const anchor = html.indexOf("const DATA");
if (anchor === -1) fail("could not find `const DATA` in index.html");

// Balance-match the DATA object literal starting at its first `{`.
const start = html.indexOf("{", anchor);
if (start === -1) fail("no opening `{` after `const DATA`");
let depth = 0, end = -1;
for (let i = start; i < html.length; i++) {
  const c = html[i];
  if (c === "{") depth++;
  else if (c === "}") { depth--; if (depth === 0) { end = i; break; } }
}
if (end === -1) fail("unbalanced braces — DATA object never closes");

const literal = html.slice(start, end + 1);

let DATA;
try {
  DATA = vm.runInNewContext("(" + literal + ")", Object.create(null), { timeout: 2000 });
} catch (e) {
  fail("DATA object does not parse as valid JS — " + e.message);
}

const p = DATA && DATA.participants;
if (!Array.isArray(p)) fail("DATA.participants is not an array");
if (p.length === 0) fail("DATA.participants is empty");

const seen = new Set();
for (const [i, part] of p.entries()) {
  const at = `participants[${i}]`;
  if (typeof part !== "object" || part === null) fail(`${at} is not an object`);
  if (typeof part.id !== "number") fail(`${at} has non-numeric id (${JSON.stringify(part.id)})`);
  if (seen.has(part.id)) fail(`duplicate id ${part.id} at ${at}`);
  seen.add(part.id);
  if (typeof part.name !== "string" || !part.name.trim()) fail(`${at} (id ${part.id}) has no name`);
  if (part.quotes != null && !Array.isArray(part.quotes)) fail(`${at} (${part.name}) quotes is not an array`);
  if (part.gaps != null && !Array.isArray(part.gaps)) fail(`${at} (${part.name}) gaps is not an array`);
  if (part.services != null && !Array.isArray(part.services)) fail(`${at} (${part.name}) services is not an array`);
}

console.log(`✅ index.html OK — ${p.length} participants, ids 1..${Math.max(...seen)}, all unique.`);
