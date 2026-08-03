# HashSite �🎵

HashSite é um perfil pessoal que junta Discord, Spotify e Roblox em uma página leve e intuitiva. A ideia é mostrar sua presença online de forma simples: avatar do Discord, o que está tocando no Spotify e qual jogo do Roblox está ativo.

**Visite o site** ou execute localmente para testar o fluxo em tempo real.

---

## O que este projeto faz

- Mostra informações públicas do Discord do usuário
- Consulta a música atual ou a última música tocada no Spotify
- Verifica o status do Roblox e exibe o jogo em andamento
- Usa Supabase para armazenar histórico e estado do site
- Atualiza o frontend automaticamente sem precisar recarregar

---

## O que mudou recentemente

Este projeto recebeu melhorias importantes no backend para torná-lo mais confiável:

- Tratamento de erros para APIs externas do Discord, Spotify e Roblox
- Timeouts em requisições HTTP para evitar travamentos
- Retornos seguros com fallback quando algum serviço estiver indisponível
- Proteção extra no acesso ao Supabase para evitar falhas nas consultas

Essas mudanças deixam a API mais resistente e o site mais estável em produção.

---

## Tecnologias

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- FastAPI
- Requests
- Supabase
- Spotify API
- Discord API

---

## Como rodar localmente

1. Entre na pasta do backend:

```bash
cd back
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

4. Preencha as variáveis no `back/.env`.

5. Inicie o servidor:

```bash
uvicorn main:app --reload
```

O backend ficará disponível em `http://localhost:8000`.

---

## Configuração do frontend

No `front/app.js`, a URL da API é definida automaticamente para `localhost` ou para o domínio remoto. Se quiser rodar localmente, apenas certifique-se de que `API_BASE` aponte para `http://localhost:8000`.

---

## Variáveis de ambiente

Use `back/.env.example` como base. Algumas variáveis importantes:

- `API_SECRET`
- `DISCORD_BOT_TOKEN`
- `DISCORD_ID`
- `ROBLOX_COOKIE`
- `ROBLOX_USER_ID`
- `SPOTIFY_REFRESH_TOKEN`
- `SPOTIFY_CLIENT`
- `SPOTIFY_SECRET`
- `SUPABASE_URL`
- `SUPABASE_KEY`

---

## Observações

- O arquivo `.env` não deve ser comitado.
- Se alguma API estiver fora do ar, o backend retorna valores padrão ao frontend.
- O projeto foi pensado para funcionar bem em deployment simples e também localmente.

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
│   └── .env.example
├── front/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── README.md
```

---

## 📊 Endpoints da API

- `GET /discord` — Dados do Discord
- `GET /live` — Status do Spotify e Roblox em tempo real
- `GET /status` — Em produção
- `POST /toggle?status=true|false` — Liga ou desliga a API (quando desligada, `/live` retorna vazio)

---

## 🎨 Personalização

As cores são extraídas dinamicamente das capas de álbum do Spotify via `colorthief`. Para customizar o visual, edite `front/styles.css`.

---

**Made with ❤️ by haxish3**
