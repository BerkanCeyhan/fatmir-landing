#!/usr/bin/env node
/**
 * Bildstrecke für die Fatmir-Landingpage mit Nano Banana 2 (gemini-3.1-flash-image).
 * SOP: brain/agency/sops/nano-banana.md
 *
 * Nutzung:  node scripts/gen-fatmir-bilder.mjs            (alles)
 *           node scripts/gen-fatmir-bilder.mjs icons-a    (einzelne Jobs)
 *
 * Ausgabe:  gen/<name>.raw  (Rohbytes, Endung wird danach in Python normalisiert)
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, resolve, extname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUTDIR = resolve(ROOT, "gen");

function loadKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY.trim();
  const env = readFileSync(resolve(ROOT, ".env"), "utf8");
  const m = env.match(/^\s*GEMINI_API_KEY\s*=\s*(.+)\s*$/m);
  if (!m) throw new Error("GEMINI_API_KEY nicht in .env gefunden");
  return m[1].replace(/^["']|["']$/g, "").trim();
}

// Immer gemini-3.1-flash-image (Nano Banana 2). Kein Fallback auf andere Modelle.
const MODELS = ["gemini-3.1-flash-image"];
const SEED = 730512;

// ---------------------------------------------------------------- Stilblöcke

const ILLU_STYLE =
  "Flat editorial vector illustration, bold simplified shapes with confident even outlines. " +
  "Strictly limited palette of exactly four colours and nothing else: warm off white RGB 251,248,244 " +
  "for the background, near black RGB 23,20,15 for all outlines and dark areas, saturated signal " +
  "orange RGB 240,80,30 as the single dominant accent, and warm sand RGB 234,222,206 for secondary " +
  "surfaces. Even, flat fills with a very fine paper grain. No photorealism, no gradients, no glow, " +
  "no drop shadows, no three dimensional rendering, no isometric perspective. " +
  "No text, no letters, no numbers, no logos, no watermark, no captions anywhere in the image.";

const FACE =
  "The attached photograph shows the man to be depicted. Keep his recognisable features exactly: " +
  "man in his late thirties, short dark brown hair swept up at the front, neatly trimmed dark stubble " +
  "beard along the jaw and a moustache, warm medium skin tone, thick dark eyebrows, wide open friendly " +
  "smile showing teeth, and a black and cream varsity jacket with striped cuffs. " +
  "Do not invent a different person, do not change his hair, beard or jacket.";

// ------------------------------------------------------------------ Job-Liste

const JOBS = [
  {
    name: "icons-a",
    aspect: "1:1",
    prompt:
      "A single flat graphic showing exactly nine separate pictogram icons arranged in a strict 3 by 3 " +
      "grid, three rows and three columns, evenly spaced, all nine at the same visual size. " +
      "Every icon is drawn in one single solid colour, pure black RGB 0,0,0, in a bold geometric " +
      "line style with one uniform stroke weight of roughly one fiftieth of the image width and " +
      "rounded stroke caps. No fills in any other colour, no shading, no gradient, no enclosing box " +
      "or circle behind an icon, no grid lines, no separators, no frames. " +
      "Each icon is centred in its own cell and occupies about fifty five percent of that cell. " +
      "Row one from left to right: a megaphone seen from the side pointing to the upper right; " +
      "a line chart rising to the right with three round data points on the line; " +
      "an upright smartphone with a play triangle centred on its screen and two small hearts floating " +
      "up from its top right corner. " +
      "Row two from left to right: a shopping bag with two round handles; " +
      "a target of three concentric circles with a single arrow standing in the centre; " +
      "two hands clasped in a handshake seen from the side. " +
      "Row three from left to right: a film camera on a three legged tripod; " +
      "a trophy cup with two handles on a rectangular base; " +
      "a calendar sheet with a small clock overlapping its lower right corner. " +
      "CRITICAL: the entire background is a pure, perfectly uniform chroma key green, exact RGB " +
      "0,255,0, filling every pixel that is not icon linework. No gradient, no vignette, no texture, " +
      "no shadow, no reflection. Nothing inside the icons is green. " +
      "Every icon keeps a clear margin of at least twelve percent of its cell to all cell edges, " +
      "nothing is cropped by the frame. " +
      "No text, no letters, no numbers, no captions, no watermark anywhere. Square 1:1 composition.",
  },
  {
    name: "hero-fatmir",
    aspect: "4:5",
    refs: ["img/award-swa-flex.webp"],
    prompt:
      FACE +
      " Photorealistic studio portrait of exactly this man, standing, turned slightly to his left, " +
      "looking straight into the camera with the same wide confident smile. His right arm is raised " +
      "in a relaxed victory gesture at shoulder height, his left hand is open and gesturing outward " +
      "as if mid sentence. Energetic, warm, welcoming posture. " +
      "He stands in front of a completely plain, evenly lit warm off white studio background, RGB " +
      "251,248,244, with no props, no furniture, no stage, no trophy, no letters and no signage. " +
      "Bright, soft, even daylight from the front left, gentle falloff, no hard shadows on the " +
      "background, no coloured light, no purple or blue cast, no neon. " +
      "Natural skin texture with visible pores and fine lines, no beauty retouching, no skin " +
      "smoothing, no plastic look, no HDR, no lens flare. " +
      "Vertical 4:5 composition, the man is cropped at mid thigh and occupies the right two thirds " +
      "of the frame with clear empty background on the left third. " +
      "No text, no letters, no numbers, no logo, no watermark anywhere.",
  },
  {
    name: "illu-live",
    aspect: "4:3",
    refs: ["img/award-swa-flex.webp"],
    prompt:
      FACE +
      " Draw him as a flat illustrated character in the style described below, not as a photograph. " +
      ILLU_STYLE +
      " He stands behind a low table in a bright room, turned towards a smartphone that is mounted " +
      "on a small tripod in the left third of the frame and films him. He holds a plain product box " +
      "up towards the phone with his right hand and points at it with his left hand, mouth open mid " +
      "sentence, weight on the front foot, energetic posture. " +
      "On the phone screen a simplified vertical live stream view is visible: a small solid circle in " +
      "its top left corner and three floating heart shapes rising from its lower edge. " +
      "Behind him on the right, three stacked parcel boxes and one simple shelf rack. " +
      "Landscape 4:3 composition, the man occupies the centre right at about seventy percent of the " +
      "image height, the phone on its tripod occupies the left quarter at about forty percent of the " +
      "image height.",
  },
  {
    name: "illu-marketing",
    aspect: "4:3",
    prompt:
      ILLU_STYLE +
      " One large simplified analytics panel floats slightly tilted in the centre of the frame, " +
      "showing a single line rising to the right with four round data points and, behind it, three " +
      "vertical bars of increasing height. Where labels would be, only short plain horizontal strokes, " +
      "never readable characters. " +
      "Around the panel three smaller floating cards connected to it by thin lines: upper left a " +
      "horseshoe magnet attracting three small circles, lower left a target of three concentric " +
      "circles with one arrow in the centre, right a rounded speech bubble containing three dots. " +
      "Landscape 4:3 composition, the analytics panel occupies the middle half of the frame and the " +
      "three small cards sit clear of all edges.",
  },
  {
    name: "illu-handel",
    aspect: "4:3",
    prompt:
      ILLU_STYLE +
      " A simplified shop facade with a striped awning stands in the left third of the frame. " +
      "A gentle dotted arc runs from the shop across the lower half of the frame to the right third, " +
      "where a large open cardboard parcel stands with a shopping bag, a shoe box and a small bottle " +
      "rising out of it. " +
      "Above the arc three small floating markers evenly spaced: a rounded payment card seen from the " +
      "front, a delivery van seen from the side, and a five pointed star. " +
      "Landscape 4:3 composition, the shop facade and the parcel are the same visual weight and both " +
      "keep a clear margin to the frame edges.",
  },
  {
    name: "illu-award-1",
    aspect: "16:9",
    refs: ["img/award-swa-flex.webp"],
    prompt:
      "The attached photograph is the scene to redraw. " +
      FACE +
      " Redraw this exact scene as a flat illustration in the style described, keeping his pose " +
      "precisely: he faces the viewer, his right arm is bent upwards in a flexed victory pose with a " +
      "closed fist, his left hand holds a tall rectangular award trophy up beside his head, and he is " +
      "smiling broadly. " +
      ILLU_STYLE +
      " The trophy is a simple upright rectangular slab rendered in the signal orange. Behind him a " +
      "plain flat wall with no writing and no signage of any kind. " +
      "Landscape 16:9 composition, the man is cropped at the waist and centred, occupying about " +
      "eighty percent of the image height.",
  },
  {
    name: "illu-award-2",
    aspect: "16:9",
    refs: ["img/award-swa-ok.webp"],
    prompt:
      "The attached photograph is the scene to redraw. " +
      FACE +
      " Redraw this exact scene as a flat illustration in the style described, keeping his pose " +
      "precisely: he sits relaxed in an armchair leaning slightly forward, smiling, his right hand " +
      "raised beside his face making an approving ring gesture with thumb and index finger touching " +
      "and the other three fingers extended, while his left hand rests on a tall rectangular award " +
      "trophy standing on his lap. " +
      ILLU_STYLE +
      " The trophy is a simple upright rectangular slab rendered in the signal orange. Behind him " +
      "two more empty armchairs suggested with a few plain shapes, and nothing else. " +
      "Landscape 16:9 composition, the man is centred and occupies about eighty percent of the " +
      "image height.",
  },
  {
    name: "illu-coaching",
    aspect: "4:3",
    prompt:
      ILLU_STYLE +
      " An open laptop stands in the centre left of the frame, its screen showing one large play " +
      "triangle inside a rounded rectangle and, below it, three short plain horizontal strokes that " +
      "stand in for a lesson list, never readable characters. " +
      "To the right of the laptop an upright smartphone on a small stand shows a simplified vertical " +
      "live stream with one small solid circle in its top left corner and two heart shapes rising " +
      "from its lower edge. " +
      "Between and slightly above the two devices, three small numbered step circles connected by a " +
      "thin dotted line rising to the right, the circles empty with no digits inside. " +
      "Landscape 4:3 composition, laptop and smartphone stand on one common flat surface line in the " +
      "lower third and both keep a clear margin to the frame edges.",
  },
  {
    name: "hero-wide",
    aspect: "16:9",
    refs: ["gen/hero-fatmir.png"],
    prompt:
      "The attached image is a photograph of a man standing in front of a plain warm off white studio " +
      "background. Reproduce this man EXACTLY as he appears in it: same face, same hair, same beard, " +
      "same black and cream varsity jacket, same raised right hand making a victory sign, same open " +
      "left hand gesturing outward, same smile, same body proportions, same lighting and shading on " +
      "him. Do not redraw him, do not restyle him, do not change his pose, do not mirror him, do not " +
      "change his clothing and do not change his size relative to his surroundings. " +
      "Place him unchanged inside the right third of a much wider frame, and extend the plain warm off " +
      "white studio background, RGB 251,248,244, seamlessly to his left and to his right so that it " +
      "fills the entire frame edge to edge with no visible seam, no join line, no border, no frame, " +
      "no vignette and no colour shift. The left two thirds of the frame are completely empty " +
      "background with nothing in them at all. " +
      "Keep the same soft even daylight and the same faint contact shadow close behind him. " +
      "CRITICAL framing: his whole body from the top of his raised hand down to his hips is fully " +
      "visible inside the frame. Nothing of him touches or is cut by the right edge: between his " +
      "right shoulder and sleeve and the right edge of the frame there is at least ten percent of " +
      "the image width of empty background. The top of his raised hand keeps at least eight percent " +
      "of the image height of empty background above it. Only his legs below the hips are cropped by " +
      "the bottom edge. He is smaller in the frame than in the attached image, so that all this " +
      "empty background fits around him. Horizontal 16:9 composition. " +
      "No text, no letters, no numbers, no logo, no watermark, no props, no furniture, no plants.",
  },
  {
    name: "hero-studio",
    aspect: "16:9",
    refs: ["gen/hero-fatmir.png"],
    prompt:
      "The attached image shows the man to photograph. Keep him exactly: same face, same short dark " +
      "hair, same trimmed dark beard, same warm skin tone, same wide friendly smile, same black and " +
      "cream varsity jacket with striped cuffs, same body proportions. Do not invent a different " +
      "person and do not change his clothing. " +
      "Photorealistic full length photograph of this man standing inside a real photo studio. " +
      "CRITICAL framing: his ENTIRE body is inside the frame, from the top of his raised hand down to " +
      "the soles of his shoes. Nothing is cropped by any edge. There is at least six percent of the " +
      "image height of empty space above his hand and at least four percent below his shoes, and at " +
      "least eight percent of the image width between his body and the right edge. " +
      "He stands on the right hand side, his body centred on the vertical line at about seventy two " +
      "percent of the image width, facing the camera, smiling, right arm raised in a relaxed victory " +
      "gesture, left hand open and gesturing outward, weight relaxed on one leg. " +
      "The studio is clearly visible as a room, not as a plain white cut out: a wide seamless paper " +
      "backdrop in warm light beige curves down into a smooth studio floor with a visible soft " +
      "horizon line behind him, one large soft light from the front left shapes him and casts a soft " +
      "contact shadow around his shoes, and the backdrop darkens gently towards the upper corners and " +
      "the right edge. " +
      "The left half of the frame is empty, uncluttered backdrop, evenly and brightly lit in a light " +
      "warm beige so that dark text placed over it stays easy to read. No furniture, no lighting " +
      "equipment, no props, no plants and no other people inside the frame. " +
      "Warm natural colour, gentle contrast, soft even daylight quality, no HDR, no lens flare, no " +
      "coloured gels, no purple or blue cast, no vignette burnt into the corners. Natural skin " +
      "texture with pores and fine lines, no beauty retouching, no skin smoothing. " +
      "Horizontal 16:9 composition. No text, no letters, no numbers, no logo, no watermark.",
  },
];

// ----------------------------------------------------------------- Ausführung

const MIME = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };

function inlineRef(relPath) {
  const abs = resolve(ROOT, relPath);
  const mimeType = MIME[extname(abs).toLowerCase()];
  if (!mimeType) throw new Error("Unbekannter Referenztyp: " + relPath);
  return { inlineData: { mimeType, data: readFileSync(abs).toString("base64") } };
}

async function callModel(key, model, parts, aspectRatio, withTuning) {
  const body = {
    contents: [{ parts }],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig: { aspectRatio },
      ...(withTuning ? { temperature: 0.15, seed: SEED } : {}),
    },
  };
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,
    {
      method: "POST",
      headers: { "content-type": "application/json", "x-goog-api-key": key },
      body: JSON.stringify(body),
    }
  );
  if (!res.ok) {
    const text = await res.text();
    const err = new Error(`HTTP ${res.status}: ${text.slice(0, 300)}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

async function run() {
  const key = loadKey();
  const only = process.argv.slice(2);
  mkdirSync(OUTDIR, { recursive: true });

  for (const job of JOBS) {
    if (only.length && !only.some((o) => job.name.startsWith(o))) continue;

    const parts = [];
    for (const r of job.refs ?? []) parts.push(inlineRef(r));
    parts.push({ text: job.prompt });

    let data;
    try {
      data = await callModel(key, MODELS[0], parts, job.aspect, true);
    } catch (e) {
      if (e.status !== 400) throw e;
      console.warn(`${job.name}: 400 mit seed/temperature, wiederhole ohne`);
      data = await callModel(key, MODELS[0], parts, job.aspect, false);
    }

    const part = (data.candidates?.[0]?.content?.parts ?? []).find((p) => p.inlineData?.data);
    if (!part) {
      console.error(`${job.name}: kein Bild in der Antwort`, JSON.stringify(data).slice(0, 300));
      continue;
    }
    const buf = Buffer.from(part.inlineData.data, "base64");
    const out = resolve(OUTDIR, `${job.name}.raw`);
    writeFileSync(out, buf);
    console.log(`${job.name}: ${(buf.length / 1024).toFixed(0)} KB (${part.inlineData.mimeType}) -> gen/${job.name}.raw`);
  }
}

run().catch((e) => {
  console.error(String(e.message || e));
  process.exit(1);
});
