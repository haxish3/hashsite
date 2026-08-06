import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowUpRight,
  Eye,
  Gamepad2,
  Code2,
  Headphones,
  Music2,
  Radio,
} from "lucide-react";
import "./styles.css";

const API = ["localhost", "127.0.0.1"].includes(window.location.hostname)
  ? "http://localhost:8000"
  : "https://api.hwsh.rest";

const links = {
  github: "https://github.com/haxish3",
  discord: "https://discord.com/users/822992602643038208",
  spotify: "https://open.spotify.com/user/a89uuvy1gdjuyllb5ym9hk8yo",
  roblox: "https://www.roblox.com/users/2856836334/profile",
};

const fallback = {
  discord: {
    username: "haxish3",
    global_name: "hwsh",
    avatar: "https://cdn.discordapp.com/embed/avatars/0.png",
  },
  spotify: { playing: false },
  roblox: { playing: false },
};

async function request(path) {
  const response = await fetch(`${API}${path}`);
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.json();
}

function usePresence() {
  const [data, setData] = useState({ ...fallback, visits: null });

  useEffect(() => {
    let active = true;
    const loadProfile = async () => {
      const [discord, visits] = await Promise.allSettled([
        request("/discord"),
        request("/visit"),
      ]);
      if (!active) return;
      setData((old) => ({
        ...old,
        discord: discord.status === "fulfilled" ? discord.value : fallback.discord,
        visits: visits.status === "fulfilled" ? visits.value.visits : null,
      }));
    };
    const loadLive = async () => {
      try {
        const live = await request("/live");
        if (active) setData((old) => ({ ...old, ...live }));
      } catch {
        if (active) setData((old) => ({ ...old, spotify: fallback.spotify, roblox: fallback.roblox }));
      }
    };

    loadProfile();
    loadLive();
    const interval = window.setInterval(loadLive, 10_000);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  return data;
}

function formatTime(seconds = 0) {
  const minutes = Math.floor(seconds / 60);
  if (minutes < 1) return "agora";
  if (minutes < 60) return `há ${minutes}m`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `há ${hours}h`;
  return `há ${Math.floor(hours / 24)}d`;
}

function formatDuration(seconds = 0) {
  const minutes = Math.floor((seconds % 3600) / 60);
  const hours = Math.floor(seconds / 3600);
  return hours ? `${hours}h ${minutes}m` : `${minutes} min`;
}

function formatClock(seconds = 0) {
  const safeSeconds = Math.max(0, Math.floor(seconds));
  const minutes = Math.floor(safeSeconds / 60);
  const rest = safeSeconds % 60;
  return `${minutes}:${String(rest).padStart(2, "0")}`;
}

function SocialLink({ href, icon: Icon, label }) {
  return (
    <a className="social-link" href={href} target="_blank" rel="noreferrer" aria-label={label} title={label}>
      <Icon size={18} strokeWidth={1.8} />
    </a>
  );
}

function SpotifyCard({ spotify }) {
  const hasTrack = spotify?.track || spotify?.artist;
  const progress = spotify?.progress;
  const [currentTime, setCurrentTime] = useState(progress?.current || 0);

  useEffect(() => {
    setCurrentTime(progress?.current || 0);
  }, [spotify?.track, progress?.current]);

  useEffect(() => {
    if (!spotify?.playing || !progress?.total) return undefined;
    const timer = window.setInterval(() => {
      setCurrentTime((current) => Math.min(current + 1, progress.total));
    }, 1000);
    return () => window.clearInterval(timer);
  }, [spotify?.playing, spotify?.track, progress?.total]);

  const percent = progress?.total
    ? Math.min(100, (currentTime / progress.total) * 100)
    : 0;

  return (
    <section className="panel spotify-panel" style={{ "--glow": spotify?.color || "transparent" }}>
      <div className="section-head">
        <span>{spotify?.playing ? "ouvindo agora" : "última música"}</span>
        <i />
        {spotify?.playing ? (
          <b className="live"><Radio size={12} /> ao vivo</b>
        ) : hasTrack ? (
          <small>{formatTime(spotify?.elapsed)}</small>
        ) : null}
      </div>

      {hasTrack ? (
        <div className="media-row">
          <img className="cover" src={spotify.album_cover} alt={`Capa de ${spotify.track || "música"}`} />
          <div className="media-copy">
            <a className="track" href={spotify.track_url || links.spotify} target="_blank" rel="noreferrer">
              {spotify.track || "faixa desconhecida"}
              <ArrowUpRight size={14} />
            </a>
            <p>{spotify.artist || "artista desconhecido"}</p>
            {spotify.playing && progress?.total ? (
              <div className="progress-wrap">
                <div className="progress"><span style={{ width: `${percent}%` }} /></div>
                <div className="timestamps"><span>{formatClock(currentTime)}</span><span>{formatClock(progress.total)}</span></div>
              </div>
            ) : (
              <span className="via">reproduzido via Spotify</span>
            )}
          </div>
        </div>
      ) : (
        <div className="empty-state"><Music2 size={18} /> nenhuma música por aqui</div>
      )}
    </section>
  );
}

function RobloxCard({ roblox }) {
  const playing = Boolean(roblox?.playing);
  return (
    <section className="panel game-panel" style={{ "--glow": roblox?.Rcolor || "transparent" }}>
      {playing ? (
        <div className="game-row">
          <img className="game-cover" src={roblox.image_url} alt="Capa do jogo" />
          <div className="game-copy">
            <span className="eyebrow"><Gamepad2 size={13} /> jogando agora</span>
            <h2>{roblox.game || "Roblox"}</h2>
            <p><i className="online-dot" /> online há {formatDuration(roblox.elapse_sec)}</p>
          </div>
          <a className="join" href={roblox.join_link || links.roblox} target="_blank" rel="noreferrer">
            entrar <ArrowUpRight size={15} />
          </a>
        </div>
      ) : (
        <div className="game-row offline">
          <div className="game-placeholder"><Gamepad2 size={21} /></div>
          <div className="game-copy"><span className="eyebrow">roblox</span><h2>offline</h2></div>
          <a className="join quiet" href={links.roblox} target="_blank" rel="noreferrer">perfil <ArrowUpRight size={15} /></a>
        </div>
      )}
    </section>
  );
}

function App() {
  const { discord, spotify, roblox, visits } = usePresence();
  const displayName = discord?.global_name || discord?.username || "hwsh";

  return (
    <main className="page-shell">
      <div className="noise" />
      <header className="topbar">
        <a className="brand" href="/">hwsh<span>.</span></a>
        <div className="visits"><Eye size={15} /> {visits == null ? "—" : visits.toLocaleString("pt-BR")}</div>
      </header>

      <div className="content">
        <section className="intro">
          <div className="avatar-wrap"><img src={discord?.avatar || fallback.discord.avatar} alt={displayName} /></div>
          <div>
            <span className="available"><i /> online por aí</span>
            <h1>{displayName}</h1>
            <p>@{discord?.username || "haxish3"} · backend, música e umas ideia torta.</p>
          </div>
        </section>

        <section className="social-row" aria-label="Redes sociais">
          <SocialLink href={links.github} icon={Code2} label="GitHub" />
          <SocialLink href={links.discord} icon={Radio} label="Discord" />
          <SocialLink href={links.spotify} icon={Headphones} label="Spotify" />
          <span className="social-line" />
          <span className="location">brasil · 03:00 utc</span>
        </section>

        <div className="activity-grid">
          <SpotifyCard spotify={spotify} />
          <RobloxCard roblox={roblox} />
        </div>
      </div>

      <footer>
        <span className="fate" tabIndex="0" aria-label="não era pra acontecer. mas aconteceu.">
          <span className="fate-before">não era pra acontecer.</span>
          <span className="fate-after" aria-hidden="true">mas aconteceu.</span>
        </span>
        <a href={links.github} target="_blank" rel="noreferrer">github.com/haxish3 <ArrowUpRight size={12} /></a>
      </footer>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
