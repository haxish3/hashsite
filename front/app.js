const HOSTNAME_MAP = {
  "localhost": "http://localhost:8000",
  "127.0.0.1": "http://localhost:8000",
};

const API_BASE = HOSTNAME_MAP[window.location.hostname] || "https://api.hwsh.rest";

const FALLBACK = {
  discord: {
    username: "hash",
    global_name: "hash",
    avatar: "https://cdn.discordapp.com/embed/avatars/0.png",
  },
  spotify: {
    playing: false,
  },
  roblox: {
    online: false,
  },
  visitas: 6767,
};

const SOCIAL_LINKS = {
  discord: "https://discord.com/users/822992602643038208",
  roblox: "https://www.roblox.com/users/2856836334/profile",
  spotify: "https://open.spotify.com/user/a89uuvy1gdjuyllb5ym9hk8yo?si=537c922ad38542d1",
  github: "https://github.com/haxish3",
};

async function get(url) {
  const res = await fetch(url, { method: "GET" });
  if (!res.ok) throw new Error(`GET ${url} ${res.status}`);
  return res.json();
}

async function post(url) {
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) throw new Error(`POST ${url} ${res.status}`);
  return res.json();
}

async function loadDiscord() {
  try {
    const data = await get(`${API_BASE}/discord`);
    return data;
  } catch {
    return FALLBACK.discord;
  }
}

function renderDiscord(data) {
  const avatar = document.getElementById("profile-avatar");
  const nameEl = document.getElementById("profile-name");
  const usernameEl = document.getElementById("profile-username");

  const avatarUrl = data.avatar || FALLBACK.discord.avatar;
  const globalName = data.global_name ?? data.username ?? FALLBACK.discord.global_name;
  const username = data.username ? `@${data.username}` : `@${FALLBACK.discord.username}`;

  avatar.src = avatarUrl;
  avatar.alt = globalName;
  nameEl.textContent = globalName;
  usernameEl.textContent = username;
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

async function renderSpotify(data, skipTransition = false) {
  const spotifyHeader = document.querySelector('.spotify-header');
  const spotifyBody = document.getElementById('spotify-body');
  const card = document.querySelector('.card');
  const headerLabel = document.getElementById("spotify-header-label");
  const livePill = document.getElementById("spotify-live-wrapper");
  const body = document.getElementById("spotify-body");
  const empty = document.getElementById("spotify-empty");
  const cover = document.getElementById("spotify-cover");
  const track = document.getElementById("spotify-track");
  const artist = document.getElementById("spotify-artist");
  const progressWrap = document.getElementById("spotify-progress-wrap");
  const progressFill = document.getElementById("spotify-progress-fill");
  const currentEl = document.getElementById("spotify-current");
  const totalEl = document.getElementById("spotify-total");
  const via = document.getElementById("spotify-via");
  const link = document.getElementById("spotify-link");
  const slapse = document.getElementById("spotify-elapsed-time")

  const hasTrack = data.track || data.artist;
  const playing = !!data.playing;

  const oldPlaying = spotifyCache ? !!spotifyCache.playing : null;
  const oldTrack = spotifyCache ? spotifyCache.track : null;
  const oldArtist = spotifyCache ? spotifyCache.artist : null;

  const playStateChanged = oldPlaying !== null && oldPlaying !== playing;
  const trackChanged = (oldTrack !== data.track) || (oldArtist !== data.artist);
  const wentToNotPlaying = playStateChanged && !playing;

  const updateContent = () => {
    if (!hasTrack) {
      body.hidden = true;
      empty.hidden = false;
      livePill.hidden = true;
      empty.querySelector(".spotify-empty-text").textContent = "Nenhuma música";
      headerLabel.textContent = "Spotify";
      card.style.setProperty("--color", "rgba(0, 0, 0, 0)");
      return;
    }

    body.hidden = false;
    empty.hidden = true;
    livePill.hidden = !playing;

    headerLabel.textContent = playing ? "Ouvindo agora" : "Última música";
    cover.src = data.album_cover || FALLBACK.spotify.album_cover;
    cover.alt = data.track || "";
    track.textContent = data.track || "—";
    artist.textContent = data.artist || "—";
    link.href = data.track_url || "open.spotify.com";
    card.style.setProperty("--color", data.color || "rgba(0, 0, 0, 0)");
    via.textContent = "Reproduzido via Spotify";
    slapse.textContent = SformatTime(data.elapsed) || "";

    const progress = data.progress;
    const hasProgress = progress && typeof progress.current === "number" && typeof progress.total === "number";

    if (hasProgress && progress.total > 0) {
      progressWrap.hidden = false;
      const pct = Math.min(100, (progress.current / progress.total) * 100);
      progressFill.style.width = `${pct}%`;
      currentEl.textContent = fmtTime(progress.current);
      totalEl.textContent = fmtTime(progress.total);
    } else {
      progressWrap.hidden = true;
    }

    if (playing) {
      via.hidden = true;
      slapse.hidden = true
    } else {
      slapse.hidden = false
      via.hidden = false;
    }
  };

  if (skipTransition || (!trackChanged && !playStateChanged)) {
    updateContent();
  } else {
    if (playStateChanged) {
      spotifyHeader.classList.add('header-transitioning');
    }
    if (trackChanged) {
      spotifyBody.classList.add('section-transitioning');
    }
    if (wentToNotPlaying) {
      spotifyBody.classList.add('header-transitioning');
    }

    await new Promise(resolve => requestAnimationFrame(resolve));
    await new Promise(resolve => setTimeout(resolve, 300));

    updateContent();

    await new Promise(resolve => requestAnimationFrame(resolve));

    spotifyHeader.classList.remove('header-transitioning');
    spotifyBody.classList.remove('section-transitioning');
    spotifyBody.classList.remove('header-transitioning');
  }
}

function SformatTime(sc) {
  const m = Math.floor(sc / 60);
  const h = Math.floor(m / 60);
  const d = Math.floor(h / 24);
  const mes = Math.floor(d / 30)


  if (sc < 60) return `agora`;
  if (m < 60) return `há ${m}m`;
  if (h < 24) return `há ${h}h`;
  if (d < 30) return `há ${d}d`;
  if (mes < 12) return `há ${mes} ${mes === 1 ? 'mês' : 'meses'}`;
  return `há 1a+`;
}

let spotifyCache = null;
let tickInterval = null;
let endTimeout = null;
let elapsedInterval = null;

function tickSpotify() {
  if (!spotifyCache || !spotifyCache.playing) return;
  if (!spotifyCache.progress) return;

  spotifyCache.progress.current += 1;

  if (spotifyCache.progress.current >= spotifyCache.progress.total) {
    stopSpotifyTimers();
    return;
  }

  const pct = Math.min(100, (spotifyCache.progress.current / spotifyCache.progress.total) * 100);
  document.getElementById("spotify-progress-fill").style.width = `${pct}%`;
  document.getElementById("spotify-current").textContent = fmtTime(spotifyCache.progress.current);
}

function tickElapsed() {
  if (!spotifyCache || spotifyCache.playing) return;
  if (typeof spotifyCache.elapsed !== 'number') return;

  spotifyCache.elapsed += 1;

  const elapseEl = document.getElementById("spotify-elapsed-time");
  if (elapseEl && !elapseEl.hidden) {
    elapseEl.textContent = SformatTime(spotifyCache.elapsed);
  }
}

function stopSpotifyTimers() {
  if (tickInterval) { clearInterval(tickInterval); tickInterval = null; }
  if (endTimeout) { clearTimeout(endTimeout); endTimeout = null; }
  if (elapsedInterval) { clearInterval(elapsedInterval); elapsedInterval = null; }
}


function startSpotifyTimers() {
  stopSpotifyTimers();

  if (spotifyCache && spotifyCache.playing) {
    tickInterval = setInterval(tickSpotify, 1000);
  } else if (spotifyCache && !spotifyCache.playing && spotifyCache.elapsed) {
    elapsedInterval = setInterval(tickElapsed, 1000);
  }
}


async function renderRoblox(data, skipTransition = false) {
  const robloxCard = document.querySelector(".card-roblox");
  const body = document.getElementById("roblox-body");
  const offline = document.getElementById("roblox-offline");
  const game = document.getElementById("roblox-game");
  const join = document.getElementById("roblox-join");
  const image = document.getElementById("roblox-icon");
  const Rcolor = document.querySelector(".card-roblox");
  const elapse = document.querySelector('.roblox-time');

  const playing = !!data.playing;
  const oldPlaying = robloxCache ? !!robloxCache.playing : null;
  const playStateChanged = oldPlaying !== null && oldPlaying !== playing;

  const updateContent = () => {
    if (!playing) {
      Rcolor.style.setProperty("--Rcolor", "rgba(0, 0, 0, 0)");
      body.hidden = true;
      offline.hidden = false;
      return;
    }

    body.hidden = false;
    offline.hidden = true;
    game.textContent = data.game || "—";
    join.href = data.join_link || "#";
    image.src = data.image_url || "";
    join.hidden = false;
    Rcolor.style.setProperty("--Rcolor", data.Rcolor || "rgba(0, 0, 0, 0)");
    elapse.textContent = formatTime(data.elapse_sec || 0);
  };

  if (skipTransition || !playStateChanged) {
    updateContent();
  } else {
    robloxCard.classList.add('section-transitioning');
    await new Promise(resolve => requestAnimationFrame(resolve));
    await new Promise(resolve => setTimeout(resolve, 300));
    updateContent();
    await new Promise(resolve => requestAnimationFrame(resolve));
    robloxCard.classList.remove('section-transitioning');
  }
}

function formatTime(seconds) {
  const m = Math.floor((seconds % 3600) / 60);
  const h = Math.floor(seconds / 3600);


  if (h > 0) return `${h}h ${m}m`;
  else return `${m} min`;
}

async function loadLive() {
  try {
    const data = await get(`${API_BASE}/live`);
    return data
  } catch {
    return {
      discord: FALLBACK.discord,
      roblox: FALLBACK.roblox
    };
  }
}

let liveInterval = null;
let robloxCache = null;

function spotifyDataChanged(oldData, newData) {
  if (!oldData && !newData) return false;
  if (!oldData || !newData) return true;

  return (
    oldData.track !== newData.track ||
    oldData.artist !== newData.artist ||
    oldData.album_cover !== newData.album_cover ||
    oldData.playing !== newData.playing
  );
}

function robloxDataChanged(oldData, newData) {
  if (!oldData && !newData) return false;
  if (!oldData || !newData) return true;

  return (
    oldData.game !== newData.game ||
    oldData.playing !== newData.playing ||
    oldData.image_url !== newData.image_url
  );
}

async function updateLive() {
  const live = await loadLive();

  const spotifyChanged = spotifyDataChanged(spotifyCache, live.spotify);
  if (spotifyChanged) {
    await renderSpotify(live.spotify, false);
    stopSpotifyTimers();
    if (live.spotify.playing && live.spotify.progress) {
      startSpotifyTimers();
    }
  }

  const robloxChanged = robloxDataChanged(robloxCache, live.roblox);
  if (robloxChanged) {
    await renderRoblox(live.roblox, false);
  }

  spotifyCache = live.spotify;
  robloxCache = live.roblox;
}

function startLivePolling() {
  if (liveInterval) clearInterval(liveInterval);

  liveInterval = setInterval(updateLive, 10000)
}

async function loadVisitas() {
  try {
    const data = await get(`${API_BASE}/visit`);
    return data.visits ?? FALLBACK.visitas;
  } catch {
    return FALLBACK.visitas;
  }
}

function renderVisitas(count) {
  const el = document.getElementById("visits-count");
  el.textContent = typeof count === "number" ? count.toLocaleString("pt-BR") : "—";
}

function applySocialLinks() {
  const discord = document.getElementById("social-discord");
  const roblox = document.getElementById("social-roblox");
  const spotify = document.getElementById("social-spotify");
  const github = document.getElementById("social-github");
  if (discord) discord.href = SOCIAL_LINKS.discord;
  if (roblox) roblox.href = SOCIAL_LINKS.roblox;
  if (spotify) spotify.href = SOCIAL_LINKS.spotify;
  if (github) github.href = SOCIAL_LINKS.github;
}

async function init() {
  const [discord, live, visits] = await Promise.all([
    loadDiscord(),
    loadLive(),
    loadVisitas(),
  ]);

  renderDiscord(discord);
  renderVisitas(visits);
  await renderSpotify(live.spotify, true);
  await renderRoblox(live.roblox, true);
  applySocialLinks();

  spotifyCache = live.spotify;
  robloxCache = live.roblox;
  startSpotifyTimers();
  startLivePolling();
}

init();
