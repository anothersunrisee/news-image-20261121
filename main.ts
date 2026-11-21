// news-image-20261121 entry (Node 22, standard library only).
// The image is entry.png beside this file: a dense newspaper front page
// summing up the world news of Saturday 21 November 2026
// (Russia strikes + missiles in Poland, AI sell-off correction,
// ICJ Myanmar genocide ruling). The program copies it to the output dir.
// The image is drawn by draw_frontpage.py (Python PIL) and committed as-is,
// so the entrypoint is a deterministic byte-for-byte copy.
//
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// The program runs twice and both runs must write the same bytes,
// so this is a plain copy: no timestamps, no randomness, no network.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
copyFileSync(source, join(outDir, 'entry.png'));
