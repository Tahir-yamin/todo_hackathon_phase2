# Evolution of Todo 🚀 (Hackathon II Submission)

**A Cloud-Native, AI-Agentic Task Manager built with Spec-Driven Development.**

## 🌟 The Vision
We moved beyond simple CRUD. This application features an **AI Agent** that lives inside your dashboard, understanding context and manipulating the database directly via MCP Tools, synced instantly with a reactive UI.

## 🏗️ Tech Stack (The "Clean Slate" Architecture)
* **Frontend:** Next.js 14 (App Router) + Tailwind CSS + Framer Motion (3D Visuals)
* **Backend:** Python FastAPI (REST API + AI Agent)
* **Database:** Neon Serverless PostgreSQL
* **ORM:** Prisma v5 (Stable)
* **Authentication:** BetterAuth with Prisma Adapter (Google/GitHub SSO + Email Verification)
* **AI Engine:** Anthropic/OpenAI via MCP (Model Context Protocol)

## ✨ Key Features
1. **Event-Driven UI Sync:** Chat with the AI ("Add a task to buy milk"), and the Kanban board updates *instantly* without a page refresh.
2. **Secure Authentication:**
   * OAuth 2.0 (Google & GitHub)
   * Mandatory Email Verification (with Dev-Interceptor for hackathon demoing)
3. **Floating 3D Command Center:** A "World Class" glassmorphic landing page.
4. **Spec-Driven Development:** Built following the `Specify -> Plan -> Task -> Implement` cycle using Claude Code.

## 🛠️ Local Setup

### Prerequisites
* Node.js v20+
* Python 3.10+
* PostgreSQL URL (Neon or Local)

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### 2. Frontend (Next.js)
```bash
cd frontend
# Important: Use Prisma v5 for stability
npm install
npx prisma generate
npx dotenv-cli -e .env.local -- npx prisma db push
npm run dev
```

### 3. Environment Variables
Create `.env.local` in the frontend directory:
```env
DATABASE_URL=your_neon_postgresql_url
BETTER_AUTH_SECRET=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
- Context-aware task management

**UI/UX:**
- Glassmorphic design with animated backgrounds
- Framer Motion 3D effects
- Responsive Kanban board with drag-and-drop

---

*Built for the Agentic AI Hackathon 2025.*
*Survived 12+ hours of OAuth debugging to emerge stronger.* 💪

<!-- Deployment: 2025-12-25 15:56 UTC+5 - OAuth Fixed, Email Verification Live, Auto-Refresh Implemented -->

<!-- Build trigger: 2025-12-25 16:29 -->
