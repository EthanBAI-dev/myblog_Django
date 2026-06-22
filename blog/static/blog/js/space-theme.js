/**
 * Quiet Cosmos — Spiral Galaxy Three.js
 * Adapted from s_v6 (WarpDrive-Frontend-Styles)
 * A static spiral galaxy with gentle rotation and mouse parallax.
 * No star tunnel, no warp, no planets — just the quiet cosmos.
 */
(function () {
  'use strict';

  const badge = document.getElementById('debug-badge');
  function showDebug(msg) {
    console.error(msg);
    if (badge) { badge.textContent = msg; badge.classList.add('show'); }
  }

  if (!window.THREE) {
    showDebug('Three.js not loaded.');
    return;
  }
  if (!window.WebGLRenderingContext) {
    showDebug('WebGL not supported.');
    return;
  }

  const isMobile = window.innerWidth < 768;
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const mount = document.getElementById('scene-root');

  // Params
  const P = {
    galaxyRadius: isMobile ? 650 : 1000,
    coreRadius: isMobile ? 120 : 200,
    armCount: 2,
    armWinding: 3.2,
    armWidth: isMobile ? 100 : 160,
    starCount: prefersReduced ? 5000 : (isMobile ? 10000 : 25000),
    dustRatio: 0.35,
    diskThickness: isMobile ? 16 : 26,
    rotSpeed: prefersReduced ? 0.00006 : 0.00018,
    armStarRatio: 0.7,
    camDist: isMobile ? 800 : 1200,
    camHeight: isMobile ? 350 : 500,
    tiltX: -0.21,
    tiltZ: 0.15,
    driftX: isMobile ? 5 : 10,
    driftY: isMobile ? 3 : 6,
  };

  let scn, cam, ren;
  let galGrp, galRotGrp, bgPts, glowC, glowH, ambG;
  let aid = null;
  const mo = { tx: 0, ty: 0, cx: 0, cy: 0 };
  const clock = new THREE.Clock();

  function starColor(tmp) {
    const t = THREE.MathUtils.clamp((tmp - 1000) / 9000, 0, 1);
    return new THREE.Color(
      THREE.MathUtils.lerp(1.0, 0.55, t),
      THREE.MathUtils.lerp(0.35, 0.88, t),
      THREE.MathUtils.lerp(0.10, 1.0, t)
    );
  }

  function makeGalaxy() {
    const sp = [], sc = [], dp = [], dc = [], bp = [], bc = [];
    const { galaxyRadius: GR, coreRadius: CR, armCount: ARM_N, armWinding: ARM_WIND,
            armWidth: ARM_WIDTH, starCount: NSTAR, dustRatio: DRAT,
            diskThickness: THK, armStarRatio: ASR } = P;

    for (let i = 0; i < NSTAR; i++) {
      const isBulge = Math.random() < 0.08 && i > NSTAR * 0.1;
      const r = isBulge
        ? Math.pow(Math.random(), 2.5) * CR
        : CR + Math.pow(Math.random(), 0.7) * (GR - CR);

      let x, z, tmp;

      if (isBulge) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const rad = r;
        x = Math.sin(phi) * Math.cos(theta) * rad;
        z = Math.sin(phi) * Math.sin(theta) * rad * 0.7;
        const y = Math.cos(phi) * rad * 0.6;
        tmp = 8000 + Math.random() * 2000;
        const col = starColor(tmp);
        bp.push(x, y, z); bc.push(col.r, col.g, col.b);
        continue;
      }

      const isOnArm = Math.random() < ASR;
      const isDust = !isOnArm && Math.random() < DRAT;

      let angle;
      if (isOnArm) {
        const armIdx = Math.floor(Math.random() * ARM_N);
        const armAngleOffset = (Math.PI * 2 / ARM_N) * armIdx;
        const t = r / GR;
        const spiralAngle = armAngleOffset + ARM_WIND * Math.PI * 2 * Math.pow(t, 0.6);
        const spread = (Math.random() - 0.5) * ARM_WIDTH * (0.3 + 0.7 * t);
        const spreadAngle = (Math.random() - 0.5) * 0.25;
        angle = spiralAngle + spreadAngle;
        x = Math.cos(angle) * (r + spread);
        z = Math.sin(angle) * (r + spread);
      } else {
        angle = Math.random() * Math.PI * 2;
        const rr = CR + Math.random() * (GR - CR);
        x = Math.cos(angle) * rr;
        z = Math.sin(angle) * rr;
      }

      const y = (Math.random() - 0.5) * THK * (0.2 + 0.8 * (r / GR));
      tmp = 3000 + 6000 * (1 - r / GR) + (Math.random() - 0.5) * 2000;
      const col = starColor(tmp);

      if (isDust) {
        const d = col.clone().multiplyScalar(0.3 + Math.random() * 0.15);
        dp.push(x, y, z); dc.push(d.r, d.g, d.b);
      } else {
        sp.push(x, y, z); sc.push(col.r, col.g, col.b);
      }
    }

    function makePoints(pos, col, size, op) {
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(pos), 3));
      g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(col), 3));
      const tex = (function () {
        const c = document.createElement('canvas'); c.width = 48; c.height = 48;
        const ctx = c.getContext('2d');
        const gr = ctx.createRadialGradient(24, 24, 0, 24, 24, 24);
        gr.addColorStop(0, 'rgba(255,255,255,1)');
        gr.addColorStop(0.2, 'rgba(255,255,255,0.85)');
        gr.addColorStop(0.5, 'rgba(220,225,255,0.25)');
        gr.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = gr; ctx.fillRect(0, 0, 48, 48);
        return new THREE.CanvasTexture(c);
      })();
      return new THREE.Points(g, new THREE.PointsMaterial({
        size: size || 1.5, map: tex, transparent: true, opacity: op || 0.95,
        vertexColors: true, depthWrite: false, sizeAttenuation: true,
        blending: THREE.AdditiveBlending
      }));
    }

    const g = new THREE.Group();
    g.add(makePoints(sp, sc, 1.6, 0.95));
    g.add(makePoints(dp, dc, 0.8, 0.30));
    g.add(makePoints(bp, bc, 1.8, 0.85));
    return g;
  }

  function makeBackgroundStars(n) {
    const p = [], c = [];
    for (let i = 0; i < n; i++) {
      p.push((Math.random() - 0.5) * 6000, (Math.random() - 0.5) * 4000, -2000 - Math.random() * 3500);
      const v = 0.5 + Math.random() * 0.5;
      c.push(v, v, v);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(p), 3));
    g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(c), 3));
    const tex = (function () {
      const c = document.createElement('canvas'); c.width = 24; c.height = 24;
      const ctx = c.getContext('2d');
      const gr = ctx.createRadialGradient(12, 12, 0, 12, 12, 12);
      gr.addColorStop(0, 'rgba(255,255,255,1)');
      gr.addColorStop(0.5, 'rgba(200,200,255,0.2)');
      gr.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = gr; ctx.fillRect(0, 0, 24, 24);
      return new THREE.CanvasTexture(c);
    })();
    return new THREE.Points(g, new THREE.PointsMaterial({
      size: isMobile ? 1.6 : 2.2, map: tex, transparent: true, opacity: 0.8,
      vertexColors: true, depthWrite: false, sizeAttenuation: true,
      blending: THREE.AdditiveBlending
    }));
  }

  function glowTexture(type) {
    const sz = 512;
    const c = document.createElement('canvas'); c.width = sz; c.height = sz;
    const ctx = c.getContext('2d');
    const radius = sz / 2 * 0.82;
    const gr = ctx.createRadialGradient(sz / 2, sz / 2, 0, sz / 2, sz / 2, radius);
    if (type === 'core') {
      gr.addColorStop(0, 'rgba(255,248,235,0.50)');
      gr.addColorStop(0.12, 'rgba(255,240,220,0.28)');
      gr.addColorStop(0.35, 'rgba(220,210,200,0.08)');
      gr.addColorStop(0.85, 'rgba(0,0,0,0)');
      gr.addColorStop(1, 'rgba(0,0,0,0)');
    } else if (type === 'halo') {
      gr.addColorStop(0, 'rgba(240,235,255,0.10)');
      gr.addColorStop(0.3, 'rgba(200,210,255,0.06)');
      gr.addColorStop(0.65, 'rgba(160,180,240,0.02)');
      gr.addColorStop(0.85, 'rgba(0,0,0,0)');
      gr.addColorStop(1, 'rgba(0,0,0,0)');
    } else {
      gr.addColorStop(0, 'rgba(200,215,255,0.04)');
      gr.addColorStop(0.4, 'rgba(170,195,255,0.02)');
      gr.addColorStop(0.85, 'rgba(0,0,0,0)');
      gr.addColorStop(1, 'rgba(0,0,0,0)');
    }
    ctx.fillStyle = gr; ctx.fillRect(0, 0, sz, sz);
    const tex = new THREE.CanvasTexture(c);
    tex.premultiplyAlpha = false;
    return tex;
  }

  function rebuildGalaxy() {
    if (!scn) return;
    if (galGrp) { scn.remove(galGrp); }

    galGrp = new THREE.Group();
    galGrp.rotation.x = P.tiltX;
    galGrp.rotation.z = P.tiltZ;

    galRotGrp = new THREE.Group();
    galGrp.add(galRotGrp);

    galRotGrp.add(makeGalaxy());

    glowC = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTexture('core'), transparent: true, opacity: 0.8,
      depthWrite: false, blending: THREE.AdditiveBlending, premultipliedAlpha: false
    }));
    glowC.scale.set(isMobile ? 140 : 220, isMobile ? 140 : 220, 1);
    galRotGrp.add(glowC);

    glowH = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTexture('halo'), transparent: true, opacity: 0.2,
      depthWrite: false, blending: THREE.AdditiveBlending, premultipliedAlpha: false
    }));
    glowH.scale.set(isMobile ? 500 : 800, isMobile ? 500 : 800, 1);
    galRotGrp.add(glowH);

    scn.add(galGrp);
  }

  function init() {
    scn = new THREE.Scene();
    cam = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 1, 10000);
    cam.position.set(0, P.camHeight, P.camDist);
    cam.lookAt(0, 0, 0);

    ren = new THREE.WebGLRenderer({
      antialias: !isMobile, alpha: true, powerPreference: 'high-performance'
    });
    ren.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    ren.setSize(window.innerWidth, window.innerHeight);
    ren.setClearColor(0x000000, 0);
    mount.innerHTML = '';
    mount.appendChild(ren.domElement);

    bgPts = makeBackgroundStars(prefersReduced ? 600 : (isMobile ? 1000 : 2000));
    scn.add(bgPts);

    ambG = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTexture('amb'), transparent: true, opacity: 1,
      depthWrite: false, blending: THREE.AdditiveBlending, premultipliedAlpha: false
    }));
    ambG.scale.set(isMobile ? 1200 : 2000, isMobile ? 1200 : 2000, 1);
    ambG.position.set(0, 0, -400);
    scn.add(ambG);

    rebuildGalaxy();
  }

  function animate() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const el = clock.elapsedTime;

    mo.cx += (mo.tx - mo.cx) * 0.035;
    mo.cy += (mo.ty - mo.cy) * 0.035;

    cam.position.x = mo.cx * P.driftX;
    cam.position.y = P.camHeight - mo.cy * P.driftY;
    cam.position.z = P.camDist + mo.cy * 2;
    cam.lookAt(0, 0, 0);

    if (galRotGrp) galRotGrp.rotation.y += P.rotSpeed;

    if (glowC) {
      const p = 1 + Math.sin(el * 0.7) * 0.02;
      glowC.scale.set((isMobile ? 140 : 220) * p, (isMobile ? 140 : 220) * p, 1);
    }
    if (glowH) {
      const p = 1 + Math.cos(el * 0.5) * 0.015;
      glowH.scale.set((isMobile ? 500 : 800) * p, (isMobile ? 500 : 800) * p, 1);
    }

    ren.render(scn, cam);
    aid = requestAnimationFrame(animate);
  }

  function onResize() {
    if (!cam || !ren) return;
    cam.aspect = window.innerWidth / window.innerHeight;
    cam.updateProjectionMatrix();
    ren.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    ren.setSize(window.innerWidth, window.innerHeight);
  }

  function onPointerMove(e) {
    mo.tx = (e.clientX / window.innerWidth) * 2 - 1;
    mo.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }

  try {
    init();
    animate();
    window.addEventListener('resize', onResize);
    window.addEventListener('mousemove', onPointerMove, { passive: true });
    window.addEventListener('beforeunload', function () {
      if (aid) cancelAnimationFrame(aid);
      window.removeEventListener('resize', onResize);
      window.removeEventListener('mousemove', onPointerMove);
    });
  } catch (err) {
    showDebug('Three.js init failed: ' + (err && err.message ? err.message : err));
  }
})();
