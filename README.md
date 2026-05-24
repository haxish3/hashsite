# HashSite 🎵

Um site de perfil dinâmico que integra informações em tempo real do Discord, Spotify e Roblox. Exibe seu status atual, música que está ouvindo e jogo que está jogando, tudo em um único lugar elegante.

**[Visite o site →](https://hashsite.vercel.app)**

---

## ✨ Características

- **Discord Integration**: Mostra seu avatar, nome global e username do Discord
- **Spotify Now Playing**: Exibe a música que está ouvindo ou a última música tocada em tempo real
- **Roblox Game Status**: Mostra qual jogo do Roblox você está jogando e há quanto tempo está jogando
- **Live Updates**: Dados atualizados dinamicamente sem necessidade de recarregar a página
- **Design Responsivo**: Interface moderna e elegante que funciona em todos os dispositivos
- **Analytics**: Contador de visitantes do site

---

## 🛠️ Stack Tecnológico

### Frontend
- **JavaScript** (27.9%) - Lógica e interatividade
- **CSS** (26.9%) - Estilização moderna e responsiva
- **HTML** (22.1%) - Estrutura

### Backend
- **Python** (23.1%) - API com FastAPI
- **FastAPI** - Framework web rápido e moderno
- **Spotipy** - Integração com Spotify
- **Supabase** - Banco de dados e estatísticas

---

## 📦 Requisitos

### Backend
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

Copie `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

### 4. Executar Backend Localmente

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### 5. Executar Frontend

```bash
cd front
# Abra index.html em um servidor local ou navegador
```

---

## 📋 Dependências Backend

```
fastapi - Framework web
uvicorn[standard] - Servidor ASGI
spotipy - Integração Spotify
requests - Requisições HTTP
colorthief - Extração de cores
python-dotenv - Variáveis de ambiente
supabase - Cliente Supabase
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
1. Crie uma conta em [Supabase](https://supabase.com)
2. Crie um novo projeto
3. Configure as tabelas de banco de dados
4. Copie a URL e chave da API

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
│   ├── requirements.txt      # Dependências Python
│   ├── vercel.json          # Configuração Vercel
│   └── .env.example         # Exemplo de variáveis
├── front/
│   ├── index.html           # Página principal
│   ├── app.js               # Lógica da aplicação
│   └── styles.css           # Estilos
└── README.md
```

---

## 🌐 Deploy

O projeto está configurado para ser deployado no **Vercel**.

### Deploy Automático
1. Faça push para o repositório
2. Conecte o repositório no Vercel
3. Configure as variáveis de ambiente
4. Deploy automático será acionado

---

## 📊 Endpoints da API

- `GET /discord` - Dados do Discord
- `GET /spotify` - Dados do Spotify
- `GET /roblox` - Status do Roblox
- `GET /stats` - Estatísticas do site

---

## 🎨 Personalização

### Cores
As cores são extraídas dinamicamente das capas de álbum do Spotify usando `colorthief`

### Temas
Edite `styles.css` para personalizar cores, fontes e layout

---

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para grandes mudanças, abra uma issue primeiro para discutir o que você gostaria de mudar.

---

## 📞 Suporte

Encontrou um bug? Abra uma [issue](https://github.com/haxish3/hashsite/issues) ou entre em contato.

---

**Made with ❤️ by haxish3**

**[Visite o site →](https://hashsite.vercel.app)**
