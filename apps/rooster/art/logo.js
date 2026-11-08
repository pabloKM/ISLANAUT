// ROOSTER 3D wireframe logo: extruded pieces traced from the owner's rooster design,
// projected to SVG. roosterSVG({ry,rx,size,bg,glow,id}) returns an <svg> string.
(function (root) {
  const T = (x, y) => [(x - 360) / 100, -(y - 450) / 100]; // traced crop coords -> model units
  const PIECES = [
    { name: 'tail', z: [-1.0, -0.25], col: '#9FE3FF',
      pts: [[355,400],[533,192],[680,495],[578,500],[580,610]].map(p => T(...p)) },
    { name: 'head', z: [-0.55, 0.55], col: '#45B8F5',
      pts: [[182,62],[198,196],[238,212],[244,250],[355,400],[175,615],[162,505],[55,500],[100,283],[52,280],[72,262],[45,215],[95,222],[88,185]].map(p => T(...p)) },
    { name: 'body', z: [-0.35, 0.9], col: '#2D8CF0',
      pts: [[355,400],[580,610],[395,830],[175,615]].map(p => T(...p)) },
  ];
  const EYE = { c: T(172, 248), r: 0.34, z: 0.6, fill: 0.75 };

  function rot(p, ry, rx) {
    let [x, y, z] = p;
    const cy = Math.cos(ry), sy = Math.sin(ry);
    [x, z] = [x * cy + z * sy, -x * sy + z * cy];
    const cx = Math.cos(rx), sx = Math.sin(rx);
    [y, z] = [y * cx - z * sx, y * sx + z * cx];
    return [x, y, z];
  }

  function roosterSVG(o = {}) {
    const ry = o.ry ?? -0.22, rx = o.rx ?? 0.25, size = o.size ?? 512, id = o.id || 'rl';
    const D = 11;
    const raw = p => { const [x, y, z] = rot(p, ry, rx); const k = D / (D - z); return [x * k, y * k, z]; };
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    for (const pc of PIECES) for (const [x, y] of pc.pts) for (const z of pc.z) { const r = raw([x, y, z]); x0 = Math.min(x0, r[0]); x1 = Math.max(x1, r[0]); y0 = Math.min(y0, r[1]); y1 = Math.max(y1, r[1]); }
    const S = (o.scale ?? 0.8) * size / Math.max(x1 - x0, y1 - y0), mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
    const proj = p => { const r = raw(p); return [size / 2 + (r[0] - mx) * S, size / 2 - (r[1] - my) * S, r[2]]; };
    const segs = [], nodes = [];
    for (const pc of PIECES) {
      const n = pc.pts.length;
      const F = pc.pts.map(([x, y]) => [x, y, pc.z[1]]), B = pc.pts.map(([x, y]) => [x, y, pc.z[0]]);
      for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        segs.push([F[i], F[j], pc.col, 1]);
        segs.push([B[i], B[j], pc.col, 0.8]);
        segs.push([F[i], B[i], pc.col, 0.9]);
        nodes.push([F[i], pc.col], [B[i], pc.col]);
      }
      // faint depth rings between front and back faces give the wireframe its model feel
      if (o.mesh !== false) for (const f of [0.33, 0.66]) { const zz = pc.z[0] + (pc.z[1] - pc.z[0]) * f; for (let i = 0; i < n; i++) { const j = (i + 1) % n; segs.push([[pc.pts[i][0], pc.pts[i][1], zz], [pc.pts[j][0], pc.pts[j][1], zz], pc.col, 0.3]); } }
    }
    const sorted = segs.map(([a, b, c, w]) => { const A = proj(a), B2 = proj(b); return { A, B: B2, c, w, z: (A[2] + B2[2]) / 2 }; }).sort((p, q) => p.z - q.z);
    const zs = sorted.map(s => s.z), zmin = Math.min(...zs), zmax = Math.max(...zs);
    const op = z => 0.28 + 0.72 * (z - zmin) / ((zmax - zmin) || 1);
    const lw = (o.lw ?? 1) * size / 512;
    let lines = '';
    for (const s of sorted) {
      const a = op(s.z) * s.w;
      lines += `<line x1="${s.A[0].toFixed(1)}" y1="${s.A[1].toFixed(1)}" x2="${s.B[0].toFixed(1)}" y2="${s.B[1].toFixed(1)}" stroke="${s.c}" stroke-opacity="${a.toFixed(2)}" stroke-width="${((s.w > 0.5 ? 3.2 : 1.6) * lw * (0.7 + 0.5 * op(s.z))).toFixed(2)}" stroke-linecap="round"/>`;
    }
    let dots = '';
    for (const [p, c] of nodes) { const P = proj(p); dots += `<circle cx="${P[0].toFixed(1)}" cy="${P[1].toFixed(1)}" r="${(3.4 * lw).toFixed(1)}" fill="${c}" fill-opacity="${op(P[2]).toFixed(2)}"/>`; }
    // eye gauge: dim full track + bright 75% arc from 12 o'clock clockwise
    const ring = (f0, f1, r) => { let d = ''; const N = 72; for (let i = 0; i <= N; i++) { const t = f0 + (f1 - f0) * i / N, a = Math.PI / 2 - t * 2 * Math.PI; const P = proj([EYE.c[0] + r * Math.cos(a), EYE.c[1] + r * Math.sin(a), EYE.z]); d += (i ? 'L' : 'M') + P[0].toFixed(1) + ' ' + P[1].toFixed(1); } return d; };
    const ctr = proj([EYE.c[0], EYE.c[1], EYE.z]);
    const tip = (() => { const a = Math.PI / 2 - EYE.fill * 2 * Math.PI; return proj([EYE.c[0] + EYE.r * Math.cos(a), EYE.c[1] + EYE.r * Math.sin(a), EYE.z]); })();
    const eye = `<path d="${ring(0, 1, EYE.r)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="${(7 * lw).toFixed(1)}"/>`
      + `<path d="${ring(0, EYE.fill, EYE.r)}" fill="none" stroke="#FF8A3D" stroke-width="${(7 * lw).toFixed(1)}" stroke-linecap="round"/>`
      + `<line x1="${ctr[0].toFixed(1)}" y1="${ctr[1].toFixed(1)}" x2="${tip[0].toFixed(1)}" y2="${tip[1].toFixed(1)}" stroke="#FF8A3D" stroke-width="${(2.6 * lw).toFixed(1)}" stroke-linecap="round"/>`
      + `<circle cx="${ctr[0].toFixed(1)}" cy="${ctr[1].toFixed(1)}" r="${(5 * lw).toFixed(1)}" fill="#FFFFFF"/>`;
    const glow = o.glow !== false;
    const bg = o.bg === 'none' ? '' : `<radialGradient id="${id}g" cx="45%" cy="40%" r="75%"><stop offset="0" stop-color="#173A5E"/><stop offset="1" stop-color="#08111D"/></radialGradient>`;
    const filt = glow ? `<filter id="${id}f" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="${(5 * lw).toFixed(1)}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>` : '';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}"><defs>${bg}${filt}</defs>`
      + (bg ? `<rect width="${size}" height="${size}" fill="url(#${id}g)"/>` : '')
      + `<g${glow ? ` filter="url(#${id}f)"` : ''}>${lines}${dots}${eye}</g></svg>`;
  }
  root.roosterSVG = roosterSVG;
  if (typeof module !== 'undefined') module.exports = { roosterSVG };
})(typeof window !== 'undefined' ? window : globalThis);
