/* Llanwrtyd Lights — front end. Plain JS, no build step, no dependencies. */
(() => {
  'use strict';

  const app = document.getElementById('app');
  const S = {
    screen: 'welcome',
    lang: localStorage.getItem('llt_lang') || 'en',
    houses: [], categories: [], visited: [], picks: {},
    votingOpen: true, liveResults: true, results: null, voters: 0,
    showAll: false, mapAll: false, mapFar: 0,
  };

  const t = (en, cy) => (S.lang === 'cy' ? cy : en);
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const api = async (action, body) => {
    const opts = body
      ? { method: 'POST', body: new URLSearchParams(body) }
      : { method: 'GET' };
    const r = await fetch(`api.php?action=${action}`, opts);
    return r.json();
  };

  function toast(msg, warn) {
    document.querySelector('.toast')?.remove();
    const el = document.createElement('div');
    el.className = 'toast' + (warn ? ' warn' : '');
    el.setAttribute('role', 'status');
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3200);
  }

  // ---- screens ----------------------------------------------------------

  function topbar(title) {
    return `<div class="topbar">
      <h2>${esc(title)}</h2>
      <button class="lang" id="lang">${S.lang === 'cy' ? 'English' : 'Cymraeg'}</button>
    </div>`;
  }

  function welcome() {
    return `<section class="screen welcome">
      <div class="dots"><span></span><span></span><span></span></div>
      <h1>${esc(LLT.event.name[S.lang])}</h1>
      <p class="subtitle">${esc(LLT.event.date[S.lang])}</p>
      <p class="lede">${t(
        'Twelve houses across the town switch their displays on for one night only. Follow the trail on foot, scan the code at each gate, then vote for your favourites. Every collection tin goes to the local school.',
        'Mae deuddeg tŷ ar draws y dref yn cynnau eu harddangosfeydd am un noson yn unig. Dilynwch y llwybr ar droed, sganiwch y cod wrth bob giât, yna pleidleisiwch dros eich ffefrynnau. Mae pob tun casglu yn mynd i’r ysgol leol.'
      )}</p>
      <div style="display:flex;flex-direction:column;gap:var(--space-2);padding-top:var(--space-2)">
        <button class="btn" data-go="trail">${t('Start the trail', "Dechrau'r llwybr")}</button>
        <button class="lang" id="lang" style="align-self:flex-start;margin-top:6px">${S.lang === 'cy' ? 'English' : 'Cymraeg'}</button>
      </div>
    </section>`;
  }

  function trail() {
    const done = S.visited.length, total = S.houses.length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    const next = S.houses.find((h) => !S.visited.includes(Number(h.id)));
    const finished = done === total && total > 0;

    const banner = finished
      ? `<div class="card finish">
           <h3>${t('That is the lot — all twelve.', "Dyna'r cyfan — pob un o'r deuddeg.")}</h3>
           <p class="muted">${t(
             'Thank you for walking it. Now go and vote for your favourites.',
             'Diolch am ei gerdded. Nawr ewch i bleidleisio dros eich ffefrynnau.'
           )}</p>
           <button class="btn" data-go="vote" style="margin-top:var(--space-3)">${t('Vote now', 'Pleidleisio nawr')}</button>
         </div>`
      : next
        ? `<div class="card next">
             <div class="muted">${t('Next stop', 'Y stop nesaf')}</div>
             <h3>${esc(next.stop_no)}. ${esc(next.name)}</h3>
             <div class="muted">${esc(next.address)}</div>
           </div>`
        : '';

    const stops = S.houses.map((h) => {
      const seen = S.visited.includes(Number(h.id));
      const isNext = !finished && next && Number(next.id) === Number(h.id);
      const blurb = S.lang === 'cy' && h.blurb_cy ? h.blurb_cy : h.blurb_en;
      const note  = S.lang === 'cy' && h.note_cy ? h.note_cy : h.note_en;
      const walk  = S.lang === 'cy' && h.walk_cy ? h.walk_cy : h.walk_en;
      return `<article class="stop ${seen ? 'visited' : ''} ${isNext ? 'isnext' : ''}">
        <div class="no">${seen ? '✓' : esc(h.stop_no)}</div>
        <div class="body">
          <h3>${esc(h.name)}</h3>
          <div class="addr">${esc(h.address)}</div>
          <p class="blurb">${esc(blurb)}</p>
          ${note ? `<div class="note">● ${esc(note)}</div>` : ''}
          ${walk && !seen ? `<div class="walk">${t('About', 'Tua')} ${esc(walk)} ${t('to the next stop', "i'r stop nesaf")}</div>` : ''}
        </div>
        ${seen ? `<div class="tick">${t('Visited', 'Wedi ymweld')}</div>` : ''}
      </article>`;
    }).join('');

    return `<section class="screen">
      ${topbar(t('The trail', "Y llwybr"))}
      <div class="progress">
        <div class="bar"><i style="width:${pct}%"></i></div>
        <div class="count">${done}/${total}</div>
      </div>
      ${banner}
      <p class="muted">${t(
        'Point your phone camera at the QR code on each gatepost to tick that house off.',
        'Anelwch gamera eich ffôn at y cod QR ar bob postyn giât i nodi\u2019r tŷ hwnnw.'
      )}</p>
      <div class="stops">${stops}</div>
    </section>`;
  }

  function map() {
    const placed = S.houses.filter((h) => h.lat !== null && h.lng !== null);
    return `<section class="screen">
      ${topbar(t('Map', 'Map'))}
      ${placed.length
        ? `<div id="leaflet" class="mapbox" role="application"
                aria-label="${t('Map of the trail','Map o\u2019r llwybr')}"></div>
           <div class="maprow">
             <button class="btn-ghost" id="locate">${t('Where am I?','Ble rydw i?')}</button>
             <button class="btn-ghost" id="fitall" hidden>${
               S.mapAll ? t('Back to the town','Yn ôl i\u2019r dref') : t('Fit all stops','Ffitio pob stop')}</button>
             <span class="muted">${t('Tap a stop for directions','Tapiwch stop am gyfarwyddiadau')}</span>
           </div>`
        : `<div class="card"><p>${t(
             'The stops have not been placed on the map yet.',
             'Nid yw\u2019r stopiau wedi\u2019u gosod ar y map eto.'
           )}</p></div>`}
    </section>`;
  }

  // Leaflet needs a live element, so it is built after render, not in the
  // HTML string. Re-created each time the screen is shown.
  let lmap = null;
  function drawMap() {
    const el = document.getElementById('leaflet');
    if (!el || typeof L === 'undefined') return;
    if (lmap) { lmap.remove(); lmap = null; }

    const placed = S.houses.filter((h) => h.lat !== null && h.lng !== null);
    if (!placed.length) return;

    lmap = L.map(el, { scrollWheelZoom: false });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap'
    }).addTo(lmap);

    const next = S.houses.find((h) => !S.visited.includes(Number(h.id)));
    const bounds = [];

    placed.forEach((h) => {
      const seen = S.visited.includes(Number(h.id));
      const isNext = next && Number(next.id) === Number(h.id);
      const cls = 'pin' + (seen ? ' seen' : '') + (isNext ? ' next' : '');
      const marker = L.marker([h.lat, h.lng], {
        icon: L.divIcon({
          className: '',
          html: `<span class="${cls}">${seen ? '✓' : esc(h.stop_no)}</span>`,
          iconSize: [34, 34],
          iconAnchor: [17, 17]
        }),
        title: h.name
      }).addTo(lmap);

      const dir = `https://www.google.com/maps/dir/?api=1&destination=${h.lat},${h.lng}`;
      marker.bindPopup(
        `<b>${esc(h.name)}</b><br>${esc(h.address)}<br>` +
        `<a href="${dir}" target="_blank" rel="noopener">${t('Directions','Cyfarwyddiadau')}</a>`
      );
      bounds.push([h.lat, h.lng]);
    });

    // Most stops sit within a few hundred metres of each other, and one or
    // two may be out of town. Fitting all of them zooms out far enough to
    // pile the town centre into an unreadable heap, so open on the walkable
    // cluster and offer a control for the rest.
    const mid = (xs) => xs.slice().sort((a, b) => a - b)[Math.floor(xs.length / 2)];
    const cLat = mid(placed.map((h) => Number(h.lat)));
    const cLng = mid(placed.map((h) => Number(h.lng)));
    const km = (a, b, c, d) => {
      const R = 6371, r = Math.PI / 180;
      const dLat = (c - a) * r, dLng = (d - b) * r;
      const x = Math.sin(dLat / 2) ** 2 +
                Math.cos(a * r) * Math.cos(c * r) * Math.sin(dLng / 2) ** 2;
      return 2 * R * Math.asin(Math.sqrt(x));
    };
    const core = placed.filter((h) => km(cLat, cLng, Number(h.lat), Number(h.lng)) <= 0.9);
    const far = placed.length - core.length;

    S.mapFar = far;
    const fit = (list) => lmap.fitBounds(list.map((h) => [h.lat, h.lng]), {
      padding: [34, 34], maxZoom: 17
    });
    fit(S.mapAll || core.length < 2 ? placed : core);

    const btn = document.getElementById('fitall');
    if (btn) btn.hidden = far === 0;
  }

  function locate() {
    if (!navigator.geolocation || !lmap) return;
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude: la, longitude: ln, accuracy } = pos.coords;
        L.circleMarker([la, ln], {
          radius: 7, color: '#f6a06b', fillColor: '#f6a06b', fillOpacity: 1, weight: 2
        }).addTo(lmap).bindPopup(t('You are about here','Rydych tua fan hyn'));
        L.circle([la, ln], { radius: accuracy, color: '#f6a06b', weight: 1, fillOpacity: 0.07 }).addTo(lmap);
        lmap.setView([la, ln], 16);
      },
      () => toast(t('Could not get your location.','Methu cael eich lleoliad.'), true),
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }

  function vote() {
    if (!S.votingOpen) {
      return `<section class="screen">
        ${topbar(t('Vote', 'Pleidlais'))}
        <div class="card"><p>${t('Voting has closed. Thank you!', 'Mae\u2019r bleidlais wedi cau. Diolch!')}</p></div>
      </section>`;
    }

    const seen = S.houses.filter((h) => S.visited.includes(Number(h.id)));
    const rest = S.houses.filter((h) => !S.visited.includes(Number(h.id)));
    // You judge what you have actually seen — but nobody is locked out for
    // forgetting to scan, so the others stay one tap away.
    const shown = S.showAll ? S.houses : (seen.length ? seen : S.houses);

    const optionFor = (c, h) => `
      <button class="opt" aria-pressed="${Number(S.picks[c.id]) === Number(h.id)}"
              data-vote="${esc(c.id)}" data-house="${esc(h.id)}">
        <span class="dot"></span>
        <span class="who"><b>${esc(h.name)}</b><i>${t('Stop', 'Stop')} ${esc(h.stop_no)} · ${esc(h.address)}</i></span>
      </button>`;

    const cats = S.categories.map((c) => {
      const label = S.lang === 'cy' ? c.label_cy : c.label_en;
      return `<div class="cat">
        <h3>${esc(label)}</h3>
        <div class="opts">${shown.map((h) => optionFor(c, h)).join('')}</div>
      </div>`;
    }).join('');

    const toggle = (seen.length && rest.length)
      ? `<button class="btn-ghost" id="showall" style="align-self:flex-start">${
          S.showAll
            ? t('Show only houses I visited', "Dangos y tai y bûm ynddynt yn unig")
            : t(`Show all ${S.houses.length} houses`, `Dangos pob un o'r ${S.houses.length} tŷ`)
        }</button>`
      : '';

    const n = Object.keys(S.picks).length;
    const hint = seen.length
      ? t(
          `One pick per category, from the ${S.showAll ? S.houses.length : seen.length} houses shown. You can change your mind until voting closes. (${n} of ${S.categories.length} chosen.)`,
          `Un dewis ym mhob categori. Gallwch newid eich meddwl nes i\u2019r bleidlais gau. (${n} o ${S.categories.length} wedi\u2019u dewis.)`
        )
      : t(
          'You have not checked in anywhere yet, so every house is listed. Scan a gatepost code as you go and this shortens to the ones you have actually seen.',
          'Nid ydych wedi cofrestru yn unman eto, felly mae pob tŷ wedi\u2019i restru. Sganiwch god giât wrth fynd a bydd hyn yn byrhau.'
        );

    return `<section class="screen">
      ${topbar(t('Your vote', 'Eich pleidlais'))}
      <p class="muted">${hint}</p>
      ${toggle}
      ${cats}
    </section>`;
  }

  function results() {
    if (S.results === null) {
      return `<section class="screen">${topbar(t('Results', 'Canlyniadau'))}<div class="loading"><span class="bulb"></span><span class="bulb"></span><span class="bulb"></span></div></section>`;
    }
    if (S.results.hidden) {
      return `<section class="screen">
        ${topbar(t('Results', 'Canlyniadau'))}
        <div class="card"><p>${t(
          'The running totals are kept under wraps until voting closes at the end of the night.',
          'Cedwir y cyfansymiau’n gyfrinachol nes i’r bleidlais gau ar ddiwedd y noson.'
        )}</p></div>
      </section>`;
    }

    const blocks = S.categories.map((c) => {
      const rows = (S.results.results[c.slug] || []).filter((r) => r.votes > 0);
      const label = S.lang === 'cy' ? c.label_cy : c.label_en;
      if (!rows.length) {
        return `<div class="result"><h3>${esc(label)}</h3><p class="muted">${t('No votes yet.', 'Dim pleidleisiau eto.')}</p></div>`;
      }
      const top = rows[0].votes;
      const mine = S.picks[c.id];
      return `<div class="result">
        <h3>${esc(label)}</h3>
        ${rows.map((r, i) => `
          <div class="row ${i === 0 ? 'lead' : ''} ${Number(mine) === Number(r.house_id) ? 'mine' : ''}">
            <span class="nm">${esc(r.name)}</span>
            <span class="track"><i style="width:${top ? Math.round((r.votes / top) * 100) : 0}%"></i></span>
            <span class="v">${r.votes}</span>
          </div>`).join('')}
      </div>`;
    }).join('');

    return `<section class="screen">
      ${topbar(t('Live results', 'Canlyniadau byw'))}
      <p class="muted">${t(
        `${S.results.voters} ${S.results.voters === 1 ? 'person has' : 'people have'} voted. ★ marks your pick.`,
        `Mae ${S.results.voters} wedi pleidleisio. Mae ★ yn nodi eich dewis chi.`
      )}</p>
      ${blocks}
    </section>`;
  }

  function info() {
    return `<section class="screen">
      ${topbar(t('Information', 'Gwybodaeth'))}
      <div class="card">
        <h3>${esc(LLT.event.date[S.lang])}</h3>
        <p class="muted">${t(
          'The trail is walkable in about an hour and a half at an easy pace. Wrap up warm and bring a torch for the unlit stretch on Cwm Irfon Lane.',
          'Mae’r llwybr yn cymryd tua awr a hanner ar gyflymder hamddenol. Gwisgwch yn gynnes a dewch â thortsh ar gyfer y darn tywyll ar Lôn Cwm Irfon.'
        )}</p>
      </div>
      <div class="card">
        <h3>${t('Collecting for the school', "Casglu i'r ysgol")}</h3>
        <p class="muted">${t(
          'Every collection tin on the trail goes to the local school. Several houses have a card reader at the gate.',
          'Mae pob tun casglu ar y llwybr yn mynd i’r ysgol leol. Mae gan sawl tŷ ddarllenydd cardiau wrth y giât.'
        )}</p>
      </div>
      <div class="card">
        <h3>${t('Your privacy', 'Eich preifatrwydd')}</h3>
        <p class="muted">${t(
          'No account, no name, no email. Your phone gets a random code so it only counts once. Nothing is shared with anyone.',
          'Dim cyfrif, dim enw, dim e-bost. Mae eich ffôn yn cael cod ar hap fel mai dim ond unwaith y mae’n cyfrif. Ni rennir dim ag unrhyw un.'
        )}</p>
      </div>
    </section>`;
  }

  // ---- render -----------------------------------------------------------

  function render() {
    const body = { welcome, trail, map, vote, results, info }[S.screen]();
    const nav = S.screen === 'welcome' ? '' : document.getElementById('tpl-nav').innerHTML;
    app.innerHTML = body + nav;
    app.removeAttribute('aria-busy');

    if (S.screen === 'map') requestAnimationFrame(drawMap);

    app.querySelectorAll('.nav button').forEach((b) => {
      b.setAttribute('aria-current', String(b.dataset.screen === S.screen));
      b.querySelector('em').textContent = b.querySelector('em').dataset[S.lang];
    });
  }

  function go(screen) {
    S.screen = screen;
    if (screen === 'results') loadResults();
    render();
    window.scrollTo(0, 0);
  }

  // ---- data -------------------------------------------------------------

  async function loadState() {
    const d = await api('state');
    if (!d.ok) return;
    S.houses = d.houses;
    S.categories = d.categories;
    S.visited = d.visited.map(Number);
    S.picks = d.picks || {};
    S.votingOpen = d.voting_open;
    S.liveResults = d.live_results;
  }

  async function loadResults() {
    const d = await api('results');
    if (d.ok) { S.results = d; S.voters = d.voters || 0; if (S.screen === 'results') render(); }
  }

  async function doScan(token) {
    const d = await api('checkin', { token });
    if (!d.ok) {
      toast(d.error === 'unknown_token'
        ? t('That code was not recognised.', 'Ni chafodd y cod ei adnabod.')
        : t('Something went wrong — try again.', 'Aeth rhywbeth o’i le — rhowch gynnig arall arni.'), true);
      return;
    }
    await loadState();
    go('trail');
    toast(d.fresh
      ? t(`Checked in at ${d.house.name} — ${d.visited} of ${S.houses.length}`,
          `Wedi cofrestru yn ${d.house.name} — ${d.visited} o ${S.houses.length}`)
      : t(`Already checked in at ${d.house.name}`, `Eisoes wedi cofrestru yn ${d.house.name}`));
  }

  // ---- events -----------------------------------------------------------

  document.addEventListener('click', async (e) => {
    const goBtn = e.target.closest('[data-go]');
    if (goBtn) return go(goBtn.dataset.go);

    const navBtn = e.target.closest('.nav button');
    if (navBtn) return go(navBtn.dataset.screen);

    if (e.target.closest('#lang')) {
      S.lang = S.lang === 'cy' ? 'en' : 'cy';
      localStorage.setItem('llt_lang', S.lang);
      document.documentElement.lang = S.lang;
      return render();
    }

    if (e.target.closest('#locate')) return locate();

    if (e.target.closest('#fitall')) {
      S.mapAll = !S.mapAll;
      return render();
    }

    if (e.target.closest('#showall')) {
      S.showAll = !S.showAll;
      return render();
    }

    const opt = e.target.closest('[data-vote]');
    if (opt) {
      const cat = opt.dataset.vote, house = opt.dataset.house;
      const prev = S.picks[cat];
      S.picks[cat] = house;           // optimistic — the ballot must feel instant
      render();
      const d = await api('vote', { category_id: cat, house_id: house });
      if (!d.ok) {
        if (prev === undefined) delete S.picks[cat]; else S.picks[cat] = prev;
        render();
        toast(d.error === 'voting_closed'
          ? t('Voting has closed.', 'Mae’r bleidlais wedi cau.')
          : t('Vote not saved — try again.', 'Ni chadwyd y bleidlais — rhowch gynnig arall arni.'), true);
      }
    }
  });

  // Refresh the tally while the results screen is open.
  setInterval(() => { if (S.screen === 'results') loadResults(); }, 15000);

  // ---- boot -------------------------------------------------------------

  (async () => {
    document.documentElement.lang = S.lang;
    await loadState();

    if (LLT.scan) {
      history.replaceState(null, '', location.pathname); // a refresh must not re-scan
      await doScan(LLT.scan);
      return;
    }
    // Someone who has already started goes straight to the trail.
    S.screen = S.visited.length ? 'trail' : 'welcome';
    render();
  })();
})();
