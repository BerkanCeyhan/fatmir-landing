#!/usr/bin/env node
/**
 * Korrigiert illu-live.webp: die Person auf dem Handybildschirm bekommt denselben
 * Bart wie der Mann davor. Sonst bleibt das Bild unveraendert.
 * SOP: brain/agency/sops/nano-banana.md
 *
 *   node scripts/fix-live-bart.mjs
 *
 * Ausgabe: gen/illu-live-fix.raw
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function loadKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY.trim();
  const env = readFileSync(resolve(ROOT, ".env"), "utf8");
  const m = env.match(/^\s*GEMINI_API_KEY\s*=\s*(.+)\s*$/m);
  if (!m) throw new Error("GEMINI_API_KEY nicht in .env gefunden");
  return m[1].replace(/^["']|["']$/g, "").trim();
}

const MODEL = "gemini-3.1-flash-image";
const SEED = 730512;

const PROMPT =
  "Edit the attached flat vector illustration. Change exactly one detail and nothing else: " +
  "the small person shown on the smartphone screen inside the image is the same man as the large " +
  "man standing on the right, so give that small figure on the screen the identical neatly trimmed " +
  "dark stubble beard and moustache along the jaw that the large man has. " +
  "Everything else must stay pixel identical: same composition, same framing, same phone, tripod, " +
  "ring light, shelves, boxes, floating heart icons, same poses, same varsity jacket, same line " +
  "weights, same flat colour palette of warm off white, near black, signal orange and warm sand, " +
  "same paper grain. Do not redraw the scene, do not change any colours, do not add or remove any " +
  "object, no text, no letters, no numbers, no logos, no watermark.";

const res = await fetch(
  `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`,
  {
    method: "POST",
    headers: { "content-type": "application/json", "x-goog-api-key": loadKey() },
    body: JSON.stringify({
      contents: [{
        parts: [
          { inlineData: { mimeType: "image/webp", data: readFileSync(resolve(ROOT, "img2/illu-live.webp")).toString("base64") } },
          { text: PROMPT },
        ],
      }],
      generationConfig: {
        responseModalities: ["IMAGE"],
        imageConfig: { aspectRatio: "4:3" },
        temperature: 0.15,
        seed: SEED,
      },
    }),
  }
);

if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
const data = await res.json();
const part = (data.candidates?.[0]?.content?.parts ?? []).find((p) => p.inlineData?.data);
if (!part) throw new Error("Keine Bilddaten in der Antwort");
mkdirSync(resolve(ROOT, "gen"), { recursive: true });
const buf = Buffer.from(part.inlineData.data, "base64");
writeFileSync(resolve(ROOT, "gen/illu-live-fix.raw"), buf);
console.log(`${(buf.length / 1024).toFixed(0)} KB (${part.inlineData.mimeType}) -> gen/illu-live-fix.raw`);
