# HashSite 🎵

Um site de perfil dinâmico que integra informações em tempo real do Discord, Spotify e Roblox. Exibe seu status atual, música que está ouvindo e jogo que está jogando, tudo em um único lugar.

**[Visite o site →](https://hwsh.rest)**

---

## ✨ Características

- **Discord Integration**: Mostra seu avatar, nome global e username do Discord
- **Spotify Now Playing**: Exibe a música que está ouvindo ou a última música tocada em tempo real
- **Roblox Game Status**: Mostra qual jogo do Roblox você está jogando e há quanto tempo
- **Live Updates**: Dados atualizados dinamicamente sem necessidade de recarregar a página
- **Design Responsivo**: Interface moderna que funciona em todos os dispositivos
- **Analytics**: Contador de visitantes do site

---

## 🛠️ Stack Tecnológico

### Frontend
- **JavaScript** — Lógica e interatividade
- **CSS** — Estilização moderna e responsiva
- **HTML** — Estrutura

### Backend
- **FastAPI** — Framework web rápido e moderno
- **Spotipy** — Integração com Spotify
- **Supabase** — Banco de dados e estatísticas

---

## 📦 Requisitos

- Python 3.8+
- pip

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório `back/` com as seguintes variáveis:

```env
# Discord
DISCORD_BOT_TOKEN=seu_token_aqui
DISCORD_ID=seu_id_aqui

# Roblox
ROBLOX_COOKIE=seu_cookie_aqui
ROBLOX_USER_ID=seu_user_id_aqui

# Spotify
SPOTIFY_CLIENT=seu_client_aqui
SPOTIFY_SECRET=seu_secret_aqui
SPOTIFY_REDIRECT=http://localhost:8000/callback

# Supabase
SUPABASE_URL=sua_url_aqui
SUPABASE_KEY=sua_chave_aqui
```

---

## 🚀 Como Usar

### 1. Clonar o Repositório

```bash
git clone https://github.com/haxish3/hashsite.git
cd hashsite
```

### 2. Configurar Backend

```bash
cd back
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

### 4. Executar Backend Localmente

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### 5. Executar Frontend

Nas primeiras linhas do `front/app.js`, configure a URL da API:

```js
// linha 1 e 2
const API_BASE = "http://localhost:8000"; // descomente essa pra rodar local
// const API_BASE = "https://api.hwsh.rest"; // comente essa, ou troque pelo seu domínio
```

Depois abra `index.html` em um servidor local ou navegador.

---

## 📋 Dependências Backend

```
fastapi
uvicorn[standard]
spotipy
requests
colorthief
python-dotenv
supabase
```

---

## 🔑 Configurando as Integrações

### Discord Bot Token
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá para "Bot" e gere um token
4. Copie o token para `DISCORD_BOT_TOKEN`

### Spotify Credentials
1. Vá para [Spotify Developer](https://developer.spotify.com)
2. Crie uma aplicação
3. Copie `Client ID` e `Client Secret`
4. Configure a URL de redirect

### Roblox
1. Obtenha seu User ID no Roblox
2. Configure o cookie `.ROBLOSECURITY` (use a ferramenta de desenvolvedor)

### Supabase
1. Crie uma conta em [Supabase](https://supabase.com) e crie um novo projeto
2. Copie a URL e a chave `anon` do projeto em **Settings > API**
3. No **SQL Editor**, crie as três tabelas abaixo:

```sql
-- Estatísticas gerais e controle da API
create table stats (
  id int primary key,
  visits int default 0,
  api_enabled boolean default true
);
insert into stats (id, visits, api_enabled) values (1, 0, true);

-- Histórico da música atual do Spotify
create table music_history (
  id int primary key,
  track text,
  artist text,
  album text,
  image text,
  url text
);
insert into music_history (id) values (1);

-- Sessão de jogo atual do Roblox
create table game_session (
  id int primary key,
  "gameName" text,
  "startedAt" text
);
insert into game_session (id) values (1);
```

> Todas as tabelas trabalham com uma única linha de `id = 1` — o código sempre faz update nessa linha, nunca insere novas.

---

## 📁 Estrutura do Projeto

```
hashsite/
├── back/
│   ├── core/
│   │   ├── discord.py       # Integração Discord
│   │   ├── spotify.py       # Integração Spotify
│   │   ├── roblox.py        # Integração Roblox
│   │   ├── stats.py         # Estatísticas
│   │   ├── supabase.py      # Cliente Supabase
│   │   └── __init__.py
│   ├── main.py              # API principal
│   ├── config.py            # Configurações
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env.example
├── front/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── README.md
```

---

## 🌐 Deploy

O projeto está configurado para deploy no **Vercel**.

1. Faça push para o repositório
2. Conecte o repositório no Vercel
3. Configure as variáveis de ambiente
4. Deploy automático será acionado

---

## 📊 Endpoints da API

- `GET /discord` — Dados do Discord
- `GET /live` — Status do Spotify e Roblox em tempo real
- `GET /stats` — Estatísticas do site
- `POST /toggle?status=true|false` — Liga ou desliga a API (quando desligada, `/live` retorna vazio)

---

## 🎨 Personalização

As cores são extraídas dinamicamente das capas de álbum do Spotify via `colorthief`. Para customizar o visual, edite `front/styles.css`.

---

**Made with ❤️ by haxish3**
