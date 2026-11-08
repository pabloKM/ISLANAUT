// Builds the site's front page (index.html) from games/*/game.json and apps/*/app.json.
// No dependencies: runs on plain Node 18+.
//   node scripts/build-index.mjs            -> writes ./index.html
//   node scripts/build-index.mjs --out dir  -> writes dir/index.html
import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";

const root = new URL("..", import.meta.url).pathname;
const outArg = process.argv.indexOf("--out");
const outDir = outArg > -1 ? process.argv[outArg + 1] : root;
const esc = (s = "") =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// Reads every <kind>/<slug>/ folder that has an index.html, with metadata from <metaFile>.
function collect(kind, metaFile) {
  const base = join(root, kind), items = [];
  for (const slug of existsSync(base) ? readdirSync(base) : []) {
    const dir = join(base, slug);
    if (!statSync(dir).isDirectory() || !existsSync(join(dir, "index.html"))) continue;
    let meta = {};
    try { meta = JSON.parse(readFileSync(join(dir, metaFile), "utf8")); }
    catch { console.warn(`! ${kind}/${slug}: missing or bad ${metaFile}, using defaults`); }
    items.push({
      slug, kind,
      title: meta.title || slug,
      blurb: meta.blurb || "",
      date: meta.date || "",
      updated: meta.updated || meta.date || "",
      tags: meta.tags || [],
      controls: meta.controls || "",
      artifact: meta.artifact || "",
      thumb: existsSync(join(dir, "thumb.png")) ? `${kind}/${slug}/thumb.png`
           : existsSync(join(dir, "thumb.jpg")) ? `${kind}/${slug}/thumb.jpg` : "",
    });
  }
  return items.sort((a, b) => (b.updated || "").localeCompare(a.updated || "") || a.title.localeCompare(b.title));
}
const games = collect("games", "game.json");
const apps = collect("apps", "app.json");

const palette = ["#ff2e88", "#ffd400", "#ff5a1f", "#9be22d", "#b79cff", "#29c5ff"];
const card = (g, i) => `
  <a class="card" href="${esc(g.kind)}/${esc(g.slug)}/" style="--c:${palette[i % palette.length]}">
    <div class="thumb">${g.thumb ? `<img src="${esc(g.thumb)}" alt="" loading="lazy">` : `<span>${esc(g.title.slice(0, 1))}</span>`}</div>
    <div class="body">
      <h2>${esc(g.title)}</h2>
      ${g.blurb ? `<p>${esc(g.blurb)}</p>` : ""}
      <div class="meta">
        ${g.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join("")}
        ${g.updated ? `<span class="date">${esc(g.updated)}</span>` : ""}
      </div>
    </div>
  </a>`;

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ISLANAUT — PabloKM × Claude games and apps</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@600;800&display=swap" rel="stylesheet">
<style>
  :root { --ink:#141218; --paper:#fff7e6; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--paper); color:var(--ink); font-family:Nunito,system-ui,sans-serif;
         background-image: radial-gradient(#14121814 1.5px, transparent 1.5px); background-size: 18px 18px; }
  header { padding: 36px 20px 8px; text-align:center; }
  h1 { font-family:Bangers,Impact,sans-serif; font-size: clamp(48px, 12vw, 120px); letter-spacing:3px; margin:0; line-height:.9;
       color:#ffd400; -webkit-text-stroke: 4px var(--ink); paint-order: stroke fill; text-shadow: 6px 6px 0 #ff2e88, 10px 10px 0 var(--ink); transform: rotate(-3deg); }
  header p { font-weight:800; margin:18px 0 0; }
  main { max-width: 1100px; margin: 24px auto 60px; padding: 0 16px; display:grid; gap:22px;
         grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
  .card { display:flex; flex-direction:column; text-decoration:none; color:inherit; background:#fff; border:4px solid var(--ink);
          border-radius:14px; box-shadow: 7px 7px 0 var(--ink); overflow:hidden; transition: transform .12s, box-shadow .12s; }
  .card:hover, .card:focus-visible { transform: translate(-3px,-3px) rotate(-.6deg); box-shadow: 10px 10px 0 var(--ink); outline:none; }
  .card:active { transform: translate(4px,4px); box-shadow: 3px 3px 0 var(--ink); }
  .thumb { aspect-ratio: 16/10; background: var(--c); border-bottom:4px solid var(--ink); display:grid; place-items:center; overflow:hidden; }
  .thumb img { width:100%; height:100%; object-fit:cover; display:block; }
  .thumb span { font-family:Bangers,Impact,sans-serif; font-size:96px; color:#fff; -webkit-text-stroke:4px var(--ink); paint-order:stroke fill; text-shadow:5px 5px 0 var(--ink); }
  .body { padding: 12px 14px 14px; }
  h2 { font-family:Bangers,Impact,sans-serif; letter-spacing:1px; font-size: 30px; margin:0 0 4px; }
  .body p { margin:0 0 10px; font-weight:600; line-height:1.35; }
  .meta { display:flex; flex-wrap:wrap; gap:6px; align-items:center; font-size:13px; font-weight:800; }
  .tag { background: var(--ink); color:#fff; border-radius: 999px; padding: 2px 9px; }
  .date { margin-left:auto; opacity:.6; }
  .section { font-family:Bangers,Impact,sans-serif; letter-spacing:2px; font-size:40px; max-width:1100px; margin:36px auto -6px; padding:0 16px; }
  .empty { grid-column: 1/-1; text-align:center; font-weight:800; font-size:20px; padding:40px; }
  footer { text-align:center; padding: 0 0 40px; font-weight:800; opacity:.7; }
  footer a { color: inherit; }
</style>
</head>
<body>
<header>
  <h1>ISLANAUT</h1>
  <p>${games.length + apps.length} prototype${games.length + apps.length === 1 ? "" : "s"} by PabloKM × Claude. Tap one to try it.</p>
</header>
${apps.length ? `<h2 class="section">Games</h2>` : ""}
<main>
${games.length ? games.map(card).join("") : `<div class="empty">No games yet. The first one lands soon!</div>`}
</main>
${apps.length ? `<h2 class="section">Apps</h2>
<main>
${apps.map((a, i) => card(a, i + games.length)).join("")}
</main>` : ""}
<footer><a href="https://github.com/pabloKM/ISLANAUT">source on GitHub</a></footer>
</body>
</html>
`;

writeFileSync(join(outDir, "index.html"), html);
console.log(`index.html: ${games.length} game(s), ${apps.length} app(s)`);
