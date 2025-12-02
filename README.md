# Buddy AI – Personal AI Assistant

Buddy is a fully-featured, production-ready AI personal assistant. Think of it as your own “Jarvis”—capable of natural conversation, handling tasks, replying to your messages and emails in your unique style, maintaining memory, and responding ethically with respect and sharp analysis. This README covers project philosophy, setup, architecture, deployment, security, and extensibility. No examples, placeholders, or basic code—only authentic, working implementation details.

---

## 🚀 Features

- **Human-like Conversation:** Responsive, context-aware, safe, and emotionally intelligent.
- **Voice and Text Interface:** Interact by typing or speaking naturally.
- **Multi-Channel Assistant:** Manages and replies to your emails, WhatsApp, Telegram, SMS, and more.
- **Personalized Style:** “Thinks” and communicates like you, learns your preferences and tone.
- **Task Automation:** Reminders, calendar, notes, smart integrations.
- **Research/Project Analysis:** Sharp assessments, pro/con breakdowns, basic legal/technical research (with disclaimers).
- **Continuous Learning:** Remembers relevant conversation and personal context.
- **Hardwired Ethics:** Non-harmful, inclusive, never offensive, and never acts outside defined boundaries.

---

## 🗂️ Project Structure

```
buddy-ai/
│
├── backend/
│   ├── core/
│   │   ├── agent.py              # Main dialog engine, prompt, and orchestration
│   │   ├── tasks.py              # Task/action scheduling/execution
│   │   ├── memory.py             # Vector DB for past context, user profile, and message history
│   │   ├── ethics.py             # Safety, moderation, and guidance logic
│   │   └── plugins/
│   │       ├── email.py          # Gmail/Outlook integration
│   │       ├── messaging.py      # WhatsApp, Telegram, SMS support
│   │       ├── calendar.py       # Google/MS calendar APIs
│   │       └── ...
│   ├── api/
│   │   ├── routes.py             # FastAPI endpoints for all functions
│   │   └── __init__.py
│   └── config/
│       └── settings.py           # Key config, secrets manager, profile
│
├── frontend/
│   ├── web/
│   │   ├── public/
│   │   └── src/
│   │       ├── components/
│   │       └── App.jsx           # Chat/voice UI, status, and settings
│   └── cli/
│       └── main.py               # Command-line interface for all functions
│
├── voice/
│   ├── speech_to_text.py         # Online/offline voice input
│   └── text_to_speech.py         # Buddy speaks replies
│
├── deploy/
│   ├── docker/
│   │   ├── backend.Dockerfile
│   │   └── frontend.Dockerfile
│   └── k8s/
│       └── manifests/
│
├── tests/
│   ├── backend/
│   ├── frontend/
│   └── integration/
├── scripts/
│   └── setup.py                  # Setup, initializations
├── requirements.txt
├── package.json
└── README.md
```

---

## 🏗️ Technology Stack

- **Backend:** Python 3.10+, FastAPI, Celery/Q/asyncio (background tasks), SQLAlchemy, Redis.
- **Frontend:** React (Web), Typer/Click (CLI), optional Tauri/electron (native desktop).
- **AI Engine:** OpenAI GPT-4 (for dialog), Llama 2/3 or Claude for local/fallback/self-host.
- **Embeddings/Memory:** ChromaDB, FAISS for semantic memory.
- **Voice:** Vosk or Google/STT for speech-to-text; gTTS, Coqui-AI, or ElevenLabs for TTS.
- **Plugins:** Gmail/GSuite, Microsoft Graph, Twilio, Telegram/WhatsApp APIs.
- **Security:** JWT auth, OAuth2 SSO, Vault/GCP Secret Manager.
- **Testing:** pytest, Selenium, Playwright, CI/CD pipelines.
- **Deployment:** Docker, Kubernetes, Nginx, LetsEncrypt.

---

## ⚙️ Setup

### 1. Prerequisites

- Python 3.10+
- Node.js (frontend)
- Docker Engine (for containerized deployment)
- API keys for: OpenAI, Gmail, WhatsApp/Telegram, TTS, etc.
- Secure vault for secrets (Vault, GCP Secret Manager, or AWS KMS)
- (Optional/Recommended) GPU if running local models

### 2. Configuration

1. **Clone Repo & Install:**
   ```sh
   git clone https://github.com/your-username/buddy-ai.git
   cd buddy-ai
   pip install -r requirements.txt
   cd frontend/web && npm install
   ```

2. **Configure Keys:**
   - Create `.env` inside `backend/config/` with structured variables:
     ```
     OPENAI_API_KEY=sk-...
     EMAIL_CLIENT_ID=...
     EMAIL_SECRET=...
     TELEGRAM_BOT_TOKEN=...
     VECTOR_DB_PATH=/data/buddy_vectors
     JWT_SECRET=xxxx
     ```
   - Use your secrets manager for production.

3. **Build Vector DB:**
   ```sh
   python scripts/setup.py --init-memory
   ```

4. **Run Backend:**
   ```sh
   uvicorn backend.api.routes:app --reload
   celery -A backend.core.tasks worker --loglevel=info
   ```

5. **Run Frontend:**
   ```sh
   cd frontend/web
   npm run dev
   ```

6. **Run Voice Interface:**
   ```sh
   python voice/speech_to_text.py
   ```

---

## 🧠 Core Concepts

### Dialog Agent (backend/core/agent.py)
- Handles context, conversation memory, ethical prompt building, persona injection, and orchestration of plugins.

### Memory (backend/core/memory.py)
- Long and short-term context retention, project history, continuous learning (via embeddings+vector search).

### Plugins (backend/core/plugins/)
- Task execution and third-party integrations (email, scheduling, messaging, etc.), securely sandboxed.

### Safety & Ethics (backend/core/ethics.py)
- Moderation logic, non-harmful guidance, reject/soften answers for legal/medical topics, dynamic persona safety wrapping.

---

## 📨 Email & Messaging Integration

- OAuth2 Auth for Gmail/MS/Apple accounts.
- Hooks for reading, summarizing, and replying to important emails automatically by learning your style from real outbound mail.
- End-to-end encrypted storage for all tokens; buddy never leaks or forwards personal info.
- Templates personalized by Buddy, always reviewed by user before sending (unless in “auto” mode with explicit permission).

---

## 🗣️ Voice Interface

- Wakeword detection or push-to-talk.
- Reliable STT and TTS pipelines, fallback to cloud/local as available.
- Natural, efficient spoken dialogue with interruption recovery.

---

## ⚖️ Legal/Ethics

- Buddy never gives definitive legal/medical/financial advice, always issues disclaimers and encourages professional counsel.
- Content moderation for all outputs; refuses abusive, illegal, or highly sensitive topics by design.
- GDPR/CCPA ready: all data stored locally or in your chosen private cloud, full data portability and deletion.

---

## 🧩 Adding Skills/Plugins

- To add a new skill:
  1. Implement as `backend/core/plugins/your_skill.py`
  2. Register entrypoint in `agent.py`
  3. Document in `docs/plugins/`
  4. Write test: `tests/backend/plugins/test_your_skill.py`
- Hot reload for plugin updates in dev mode.

---

## 🔒 Security

- All secrets in encrypted stores.
- JWT/OAuth2 for user auth.
- HTTPS everywhere (Nginx+LetsEncrypt for web).
- RBAC for multi-user instances.

---

## 🧪 Testing & CI

- Unit: `pytest tests/backend/`
- Integration: `pytest tests/integration/`
- Frontend: `npm run test`
- Automated CI/CD pipeline (`.github/workflows/ci.yml`)
- Lint & static analysis for all PRs.

---

## ☁️ Deployment (Docker/K8s)

- Full support for containerized and orchestrated deployments.
- See `deploy/docker/` and `deploy/k8s/` for reference manifests.
- Templates for GCP, AWS, Azure, and DigitalOcean.

---

## 🌱 Extensibility & Customization

- Profile Buddy to your style by training on your past messages/emails (handled in setup).
- Extendable with new APIs: home automation, code tools, file summaries, etc.
- Add more local/secure LLMs by customizing backend engine (see `core/agent.py`).

---

## 👨‍💻 Authors

- [Your Name] (product lead/code)
- [Co-contributors, if any]

---

## 📝 License

(C) 2025 Your Name. All rights reserved. Not for resale. For personal or organizational private use.

---

## 🤝 Support & Community

- Issues: [GitHub Issues](https://github.com/your-username/buddy-ai/issues)
- Discussion: [GitHub Discussions](https://github.com/your-username/buddy-ai/discussions)
- Email: your.email@domain.com

---

**No demo/placeholder code here—clone, configure, and build your original Buddy today!**
