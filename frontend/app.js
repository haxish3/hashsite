
const API_BASE = "http://localhost:8000";

// --- Dados hardcoded (fallback) ---
const FALLBACK = {
  discord: {
    username: "hash",
    global_name: "hash",
    avatar: "https://cdn.discordapp.com/embed/avatars/0.png",
  },
  spotify: {
    playing: true,
    track: "Música exemplo",
    artist: "Artista",
    album_cover: "https://placehold.co/64x64/1a1a2e/666?text=🎵",
    embed_url: "",
    progress: { current: 45, total: 180 },
  },
  roblox: {
    online: true,
    playing: true,
    game: "None",
    join_link: "None",
  },
  visitas: 42,
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
    const data = await get(`${API_BASE}/api/discord`);
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

async function loadSpotify() {
  try {
    const data = await get(`${API_BASE}/api/spotify`);
    return data;
  } catch {
    return FALLBACK.spotify;
  }
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function renderSpotify(data) {
  const headerLabel = document.getElementById("spotify-header-label");
  const livePill = document.getElementById("spotify-live-pill");
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
  const link = document.getElementById("spotify-link")
  const card = document.querySelector(".card");

  const hasTrack = data.track || data.artist;
  const playing = !!data.playing;

  if (!hasTrack) {
    body.hidden = true;
    empty.hidden = false;
    livePill.hidden = true;
    empty.querySelector(".spotify-empty-text").textContent = "Nenhuma música";
    headerLabel.textContent = "🎵 Spotify";
    return;
  }

  body.hidden = false;
  empty.hidden = true;
  livePill.hidden = !playing;

  headerLabel.textContent = playing ? "🎵 Ouvindo agora" : "🎵 Última música";
  cover.src = data.album_cover || FALLBACK.spotify.album_cover;
  cover.alt = data.track || "";
  track.textContent = data.track || "—";
  artist.textContent = data.artist || "—";
  link.href = data.track_url || "open.spotify.com"
  card.style.setProperty("--color", data.color);

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
    via.hidden = false;
    via.textContent = "Reproduzindo via Spotify";
  } else {
    via.hidden = true;
  }
}

async function loadRoblox() {
  try {
    const data = await get(`${API_BASE}/api/roblox`);
    return data;
  } catch {
    return FALLBACK.roblox;
  }
}

function renderRoblox(data) {
  const body = document.getElementById("roblox-body");
  const offline = document.getElementById("roblox-offline");
  const game = document.getElementById("roblox-game");
  const join = document.getElementById("roblox-join");
  const image = document.getElementById("roblox-icon");
  const Rcolor = document.querySelector(".card-roblox");
  const elapse = document.querySelector('.roblox-time');

  const online = !!data.online;
  const playing = !!data.playing;
  const gameName = data.game || "—";
  const joinLink = data.join_link || "#";
  const imageUrl = data.image_url || "";
  const time = data.elapse_sec || 0;

  if (!online || !playing) {
    body.hidden = true;
    offline.hidden = false;
    return;
  }

  body.hidden = false;
  offline.hidden = true;
  game.textContent = gameName;
  join.href = joinLink;
  image.src = imageUrl;
  join.hidden = false;
  Rcolor.style.setProperty("--Rcolor", data.Rcolor)
  elapse.textContent = formatTime(time)
}

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;

  if (h > 0) return `${h}h ${m}m`;
  else if (m > 0) return `${m} min`;
  else return `${s} sec`;
}

async function loadVisitas() {
  try {
    const data = await get(`${API_BASE}/api/visit`);
    return data.visits ?? FALLBACK.visitas;
  } catch {
    return FALLBACK.visitas;
  }
}

function renderVisitas(count) {
  const el = document.getElementById("visits-count");
  el.textContent = typeof count === "number" ? count.toLocaleString("pt-BR") : "—";
}

async function updateCardS() {
  const spotify = await loadSpotify()
  renderSpotify(spotify)
}

async function updateCardR() {
  const roblox = await loadRoblox()
  renderRoblox(roblox)
}

let intervalRoblox = null;
let intervalSpotify = null;

async function updateCards() {
  const roblox = await loadRoblox();

  if (roblox.playing) {
    if (intervalRoblox) clearInterval(intervalRoblox);
    intervalRoblox = setInterval(updateCardR, 60000);
  } else {
    if (intervalRoblox) {
      clearInterval(intervalRoblox);
      intervalRoblox = null;
    }
  }

  const spotify = await loadSpotify();

  if (spotify.playing) {
    if (intervalSpotify) clearInterval(intervalSpotify);
    intervalSpotify = setInterval(updateCardS, 1000);
  } else {
    if (intervalSpotify) {
      clearInterval(intervalSpotify);
      intervalSpotify = null;
    }
  }
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
  const [discord, spotify, roblox, visits] = await Promise.all([
    loadDiscord(),
    loadSpotify(),
    loadRoblox(),
    loadVisitas(),
  ]);

  renderDiscord(discord);
  renderSpotify(spotify);
  renderRoblox(roblox);
  renderVisitas(visits);
  applySocialLinks();

  updateCards()
}

init();
