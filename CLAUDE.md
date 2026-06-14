# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Mentor AI — a site with two parts:

- **Root (`/`)** — a marketing/landing page (`index.html`, "Mentor AI — Stop Being Average").
- **`character-ai/`** — the actual chat app: users pick an AI persona (Andrew Tate, Gary Vee, Dan Pena, Tai Lopez, plus a few Slovenian mentors) and chat with it in that persona's voice. Vanilla HTML/CSS/JS, zero build step, zero frontend dependencies.

## Running locally

```bash
# .env lives under character-ai/ (root server.py reads character-ai/.env)
echo "API_KEY=gsk_your_groq_key_here" > character-ai/.env
echo "PROVIDER=groq" >> character-ai/.env
echo "MODEL=llama-3.3-70b-versatile" >> character-ai/.env

python server.py        # serves the whole repo on http://localhost:9876 (or python server.py <port>)
```

Do NOT open `index.html` directly via `file://` — CORS blocks the LLM API calls. Always use `server.py`.

## Architecture

- **`index.html`** (root) — landing page, inline `<style>`/`<script>`, no LLM calls.
- **`server.py`** (root) — local dev server for the whole repo. Subclasses `SimpleHTTPRequestHandler`, reads `character-ai/.env`, and injects `window.__ENV__ = {...}` into the root `index.html` on the fly (via `</head>` replacement). Also exposes `GET /__env` returning the same env as JSON.
- **`character-ai/index.html`** — the chat app. This is the file to edit for chat UI/logic changes.
- **`character-ai/characters.json`** — defines each mentor persona (id, name, tag, avatar, color, tone, greetings, system prompt). Editable without touching code.
- **`character-ai/voicelines.json`, `character-ai/suggestions.json`, `character-ai/book-recommendations.json`** — supplementary persona content (extra lines, suggested prompts, book recs) loaded by the chat app.
- **`character-ai/avatars/`** — persona avatar images referenced from `characters.json`.
- **`character-ai/server.py`** — standalone dev server for just the chat app (same env-injection approach as root `server.py`, but reads `.env` from its own directory).
- **`api/env.js`** — Vercel serverless function equivalent of the `/__env` endpoint, used in production (reads `process.env`, returns JSON with CORS header).
- **`vercel.json`** (root) — routes `/api/env` to `api/env.js`; everything else served as static files.
- **`VOICELINES/`** — source text files for persona voicelines/Q&A used to build `character-ai/voicelines.json`.

### Chat app runtime flow (`character-ai/index.html`)

1. `init()` resolves config in priority order: `window.__ENV__` (server inject) → `/api/env` (Vercel) → `/__env` (local fallback) → values already in `localStorage`.
2. Settings (`apiKey`, `provider`, `model`, `customBaseUrl`, `customModelName`, `theme`) are persisted to `localStorage` (keys prefixed `mentor_*`) and edited via the settings modal (`saveSettings()`).
3. Each character keeps its own conversation history, persisted in `localStorage` under `CONV_KEY`, keyed by character id (`getConversation`/`saveConversation`/`loadConversation`/`clearConversation`).
4. Sending a message (`sendMessage()` → `callWithRetry()` → `callAPI()`) builds an OpenAI-compatible `chat/completions` request and hits the selected provider's endpoint (Groq, OpenRouter, Gemini, OpenAI, or a custom OpenAI-compatible base URL). API keys are stored client-side only and sent directly from the browser to the provider.
5. Custom avatars can be set per-character and are persisted in `localStorage` under `AVATAR_KEY` (`saveAvatar`/`getAvatar`/`setAvatar`/`editAvatar`).

## Editing personas

Persona behavior lives entirely in `character-ai/characters.json` — each entry has `id`, `name`, `tag`, `avatar`, `emoji`, `color`, `tone`, `greeting` (array), and `prompt` (the system prompt sent to the LLM). Changes take effect on page reload, no code changes needed.

## Deployment

Deployed on Vercel. Production config (`API_KEY`, `PROVIDER`, `MODEL`, `THEME`) is set as Vercel environment variables and served via `api/env.js`.
