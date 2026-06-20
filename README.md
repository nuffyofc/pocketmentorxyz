# 🧠 Mentor AI

**→ [pocketmentorxyz.vercel.app](https://pocketmentorxyz.vercel.app/)**

Chat with AI-powered mentors that talk in their own voice. Pick a character — Andrew Tate, Gary Vee, Dan Pena, Tai Lopez, and more — and get real advice, motivation, and zero fluff.

---

## How it works

1. **Pick a mentor** — select from the visual card grid on load
2. **Type your message** — the AI responds in that character's voice
3. **Switch anytime** — each mentor keeps its own conversation history
4. **No account needed** — chats and settings saved in your browser

---

## Run locally

```bash
git clone https://github.com/nuffyofc/pocketmentorxyz.git
cd pocketmentorxyz/character-ai

echo "API_KEY=gsk_your_groq_key_here" > .env
echo "PROVIDER=groq" >> .env
echo "MODEL=llama-3.3-70b-versatile" >> .env

python ../server.py
# → http://localhost:9876/character-ai/
```

> Opening `index.html` via `file://` won't work — use the server.

---

## Deploy on Vercel

1. Push repo to GitHub
2. Import at vercel.com → leave root directory as-is
3. Add environment variables:

| Name | Value |
|------|-------|
| `API_KEY` | your Groq / OpenRouter key |
| `PROVIDER` | `groq` |
| `MODEL` | `llama-3.3-70b-versatile` |

4. Deploy ✅

---

## Edit characters

Open `character-ai/characters.json` — change name, prompt, greeting, avatar, or color. Reload and it takes effect instantly, no code changes needed.

---

## Providers

Groq, OpenRouter, Google Gemini, OpenAI, or any custom OpenAI-compatible endpoint. Your key stays in your browser — never stored on any server.

---

## Built with vibe coding

This project was built across ~4 sessions of AI-assisted development using Claude Code. Around 800+ lines of logic, 10 mentor personas, a fully custom Python dev server with env injection, a visual mentor selection screen, Hustler's University lesson integration for Andrew Tate, dynamic context-aware suggestion buttons, avatar management, voice lines, book recommendations, a minigame, and Vercel deployment — all shipped without touching a framework or build tool. Zero npm. Zero webpack. Just HTML, CSS, vanilla JS, and Python.
