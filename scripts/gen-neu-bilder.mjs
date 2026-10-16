#!/usr/bin/env node
/**
 * Bildstrecke fuer die Alternativseite /neu/ mit Nano Banana 2.1 (gemini-nano-banana-2.1).
 * Feine Linien, nur Ink, Creme und Signalrot #C32828. Kein Orange mehr.
 *
 * Nutzung:  GEMINI_API_KEY=... node scripts/gen-neu-bilder.mjs          (alles, je 2 Varianten)
 *           GEMINI_API_KEY=... node scripts/gen-neu-bilder.mjs neu-live (einzelne Jobs)
 *
 * Ausgabe:  gen/<name>-<variante>.raw
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve, extname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUTDIR = resolve(ROOT, "gen");
const MODEL = "gemini-nano-banana-2.1";
const VARIANTS = [410233, 905117];

const key = (process.env.GEMINI_API_KEY || "").trim();
if (!key) throw new Error("GEMINI_API_KEY fehlt");

const LINE =
  "Refined fine-line editorial illustration in the manner of a high-end magazine line drawing: " +
  "every contour is drawn with one thin, even hairline stroke of uniform weight, roughly one " +
  "three-hundredth of the image width, crisp and confident, no sketchy double lines. Generous " +
  "negative space and only a few deliberate details. ";

const NO =
  "Absolutely no orange, no coral, no salmon, no pink, no beige or grey fills. No shading, no " +
  "hatching, no gradients, no glow, no drop shadows, no paper texture, no 3D, no isometric " +
  "perspective. No text, no letters, no numbers, no logos, no watermark anywhere in the image.";

const LIGHT =
  LINE +
  "Strict palette and nothing else: the entire background is one flat warm off-white, RGB " +
  "245,242,236, edge to edge; all linework is deep ink, RGB 20,24,26; the only accent is a clear " +
  "signal red, RGB 195,40,40, used sparingly for a few flat filled shapes and a handful of red " +
  "hairlines. " + NO;

const DARK =
  LINE +
  "Strict palette and nothing else: the entire background is one flat deep ink black, RGB " +
  "20,24,26, edge to edge; all linework is warm off-white, RGB 245,242,236; the only accent is a " +
  "clear signal red, RGB 195,40,40, used sparingly for a few flat filled shapes and a handful of " +
  "red hairlines. " + NO;

const FACE =
  "The attached photograph shows the man to be depicted. Keep his recognisable features exactly: " +
  "man in his late thirties, short dark brown hair swept up at the front, neatly trimmed dark " +
  "stubble beard along the jaw and a moustache, thick dark eyebrows, wide open friendly smile, " +
  "and a varsity jacket with striped cuffs. Do not invent a different person. " +
  "Draw him as a line drawing in the style described below, not as a photograph. ";

const JOBS = [
  {
    name: "neu-live",
    aspect: "4:5",
    refs: ["img/award-swa-flex.webp"],
    prompt:
      FACE + DARK +
      " He stands in a small live stream studio, turned three quarters towards a smartphone that " +
      "is mounted upright on a slim tripod in the left third of the frame and films him. He holds " +
      "a plain unlabelled product box up towards the phone in his right hand and gestures openly " +
      "with his left hand, mouth open mid sentence, energetic and confident, weight on the front " +
      "foot. The product box is a flat red fill. On the phone screen: a tiny solid red circle in " +
      "its top left corner and three small red heart shapes floating up from the lower edge of the " +
      "screen. Behind him on the right, one ring light drawn as a single thin circle on a thin " +
      "stand. Portrait 4:5 composition: he is cropped at the hips and occupies the right sixty " +
      "percent of the frame at about eighty percent of the image height, phone and tripod stand in " +
      "the left third, clear margins on all sides.",
  },
  {
    name: "neu-handel",
    aspect: "4:3",
    prompt:
      LIGHT +
      " A small shop facade with a simple striped awning stands in the left third. A fine dotted " +
      "arc travels from the shop across the frame to the right third, where an open parcel box " +
      "stands with a shopping bag and a slim bottle rising out of it. Above the arc three small " +
      "floating markers, evenly spaced: a payment card seen from the front, a delivery van seen " +
      "from the side, a five-pointed star. The awning stripes and the shopping bag are flat red " +
      "fills, everything else is ink hairline. Landscape 4:3 composition, shop and parcel have " +
      "the same visual weight and keep a clear margin to all edges.",
  },
  {
    name: "neu-marketing",
    aspect: "4:3",
    prompt:
      LIGHT +
      " One large analytics panel floats slightly tilted in the centre: a thin line rises to the " +
      "right through four small dots, three thin vertical bars of increasing height stand behind " +
      "it, and where labels would be there are only short plain strokes. The rising line and its " +
      "last dot are red. Around the panel three small floating cards joined to it by hairlines: " +
      "upper left a horseshoe magnet attracting three small circles, lower left a target of three " +
      "concentric circles with one arrow in the centre whose innermost circle is filled red, right " +
      "a rounded speech bubble with three dots. Landscape 4:3 composition, the panel occupies the " +
      "middle half of the frame and the three cards keep clear of all edges.",
  },
  {
    name: "neu-coaching",
    aspect: "4:3",
    prompt:
      LIGHT +
      " An open laptop stands centre left, its screen showing one play triangle filled red inside " +
      "a rounded rectangle and below it three short plain strokes standing in for a lesson list. " +
      "To its right an upright smartphone on a small stand shows a vertical live stream with a tiny " +
      "solid red circle in its top left corner and two red hearts rising from its lower edge. " +
      "Between and slightly above the two devices three small empty circles linked by a fine dotted " +
      "line rise to the right, with no digits inside. Both devices stand on one common hairline " +
      "surface in the lower third and keep a clear margin to all edges. Landscape 4:3 composition.",
  },
  {
    name: "neu-award",
    aspect: "4:3",
    refs: ["img/award-swa-flex.webp"],
    prompt:
      "The attached photograph is the scene to redraw. " + FACE + LIGHT +
      " Redraw this exact scene and keep his pose precisely: he faces the viewer, his right arm is " +
      "bent upwards in a flexed victory pose with a closed fist, his left hand holds a tall " +
      "rectangular award trophy up beside his head, and he smiles broadly. The trophy is a plain " +
      "upright slab filled flat red. Behind him nothing but the flat background, no wall, no " +
      "writing, no signage. Landscape 4:3 composition, he is cropped at the waist, centred, and " +
      "occupies about eighty percent of the image height.",
  },
];

const MIME = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };

function inlineRef(relPath) {
  const abs = resolve(ROOT, relPath);
  return { inlineData: { mimeType: MIME[extname(abs).toLowerCase()], data: readFileSync(abs).toString("base64") } };
}

async function call(parts, aspectRatio, seed, extra) {
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`,
    {
      method: "POST",
      headers: { "content-type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify({
        contents: [{ parts }],
        generationConfig: {
          responseModalities: ["IMAGE"],
          imageConfig: { aspectRatio, ...(extra ? { imageSize: "2K" } : {}) },
          ...(extra ? { temperature: 0.4, seed } : {}),
        },
      }),
    }
  );
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

async function runJob(job, seed, idx) {
  const parts = [...(job.refs ?? []).map(inlineRef), { text: job.prompt }];
  let data;
  try {
    data = await call(parts, job.aspect, seed, true);
  } catch (e) {
    if (e.status !== 400) throw e;
    console.warn(`${job.name}: 400 mit Zusatzoptionen, wiederhole schlicht`);
    data = await call(parts, job.aspect, seed, false);
  }
  const part = (data.candidates?.[0]?.content?.parts ?? []).find((p) => p.inlineData?.data);
  if (!part) {
    console.error(`${job.name}-${idx}: kein Bild`, JSON.stringify(data).slice(0, 300));
    return;
  }
  const buf = Buffer.from(part.inlineData.data, "base64");
  writeFileSync(resolve(OUTDIR, `${job.name}-${idx}.raw`), buf);
  console.log(`${job.name}-${idx}: ${(buf.length / 1024).toFixed(0)} KB ${part.inlineData.mimeType}`);
}

const only = process.argv.slice(2);
mkdirSync(OUTDIR, { recursive: true });
const tasks = [];
for (const job of JOBS) {
  if (only.length && !only.some((o) => job.name.startsWith(o))) continue;
  VARIANTS.forEach((seed, i) => tasks.push(() => runJob(job, seed, i + 1)));
}
// drei gleichzeitig, damit das Kontingent nicht kippt
let next = 0;
await Promise.all(Array.from({ length: 3 }, async () => {
  while (next < tasks.length) {
    const t = tasks[next++];
    try { await t(); } catch (e) { console.error(String(e.message || e)); }
  }
}));
