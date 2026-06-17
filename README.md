# 🧠 Mentor AI

**→ https://github.com/nuffyofc/pocketmentorxyz**

Chat with AI-powered mentors that talk in your style. Pick a character — Andrew Tate, Gary Vee, Dan Pena, Tai Lopez — and get advice, motivation, or just a conversation in their voice.

---

## How it works

1. **Pick a mentor** — scroll the character cards at the top
2. **Type your message** — the AI responds in that character's style (prompt from `characters.json`)
3. **Switch anytime** — each character keeps its own conversation history
4. **No account needed** — your chats and settings are saved in your browser (localStorage)

Characters are defined in `characters.json` — anyone can edit them without touching code.

---

## How to use (local)

```bash
# 1. Clone
git clone https://github.com/nuffyofc/pocketmentorxyz.git
cd pocketmentorxyz/character-ai

# 2. Add your API key
echo "API_KEY=gsk_your_groq_key_here" > .env
echo "PROVIDER=groq" >> .env
echo "MODEL=llama-3.3-70b-versatile" >> .env

# 3. Start local server
python server.py
# → Opens http://localhost:9876
```

> ⚠️ Opening `index.html` directly via `file://` will NOT work — CORS blocks API calls. Use the server.

---

## How to deploy on Vercel

1. Push this repo to GitHub: https://github.com/nuffyofc/pocketmentorxyz
2. Go to https://vercel.com → Import Git Repository
3. Leave **Root Directory** as the repo root (it serves the landing page, `character-ai/`, and `api/` via `vercel.json`)
4. Add these environment variables:

| Name | Value |
|------|-------|
| `API_KEY` | `gsk_...` |
| `PROVIDER` | `groq` |
| `MODEL` | `llama-3.3-70b-versatile` |
| `THEME` | `dark` |

5. Deploy ✅

---

## Edit characters

Open `characters.json` — each entry has:

```json
{
  "id": "tate",
  "name": "Andrew Tate",
  "tag": "Top G",
  "emoji": "🥋",
  "color": "#E11D48",
  "greeting": "What's up, nerd. Let's get you sorted.",
  "prompt": "You are Andrew Tate..."
}
```

Change the name, tag, greeting, or prompt — reload and it takes effect.

---

## Providers & models

Click ⚙ to switch between Groq, OpenRouter, Google Gemini, OpenAI, or a custom OpenAI-compatible endpoint. Your key is stored locally in your browser — never sent anywhere except the API provider.
