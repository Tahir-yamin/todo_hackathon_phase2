# 🚀 AI-Powered Todo Application - Hackathon Project

**Full-Stack Todo Application with AI Chatbot Integration**

[![Deployment](https://img.shields.io/badge/Deployed-Vercel-black)](https://phase2-six.vercel.app)
[![Phase III](https://img.shields.io/badge/Phase-III%20Complete-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Phases](#project-phases)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [AI Integration](#ai-integration)
- [Security](#security)
- [Documentation](#documentation)

---

## 🎯 Overview

A comprehensive todo management application that evolved from a simple console app to a cloud-native, AI-powered full-stack application. Built as part of a hackathon challenge using spec-driven development.

**Live Demo:** [https://phase2-six.vercel.app](https://phase2-six.vercel.app)

---

## ✨ Features

### Core Functionality
- ✅ **Full CRUD Operations** - Create, Read, Update, Delete tasks
- ✅ **User Authentication** - Secure login/signup with Better Auth
- ✅ **Multi-User Support** - Isolated task management per user
- ✅ **Task Organization** - Priorities, categories, due dates
- ✅ **Search & Filter** - Find tasks quickly
- ✅ **Kanban View** - Drag-and-drop task management

### AI-Powered Features (Phase III)
- 🤖 **Natural Language Processing** - Create tasks using plain English
- 📅 **Smart Date Extraction** - "tomorrow", "next Friday" → YYYY-MM-DD
- 🎯 **Priority Detection** - "urgent" → high priority automatically
- 🏷️ **Category Inference** - Task categorization from context
- 💬 **Conversational Interface** - Chat widget for task management
- ♾️ **Unlimited AI Quota** - Using OpenRouter + DeepSeek V3

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Auth:** Better Auth
- **State:** React Hooks
- **Deployment:** Vercel

### Backend
- **Framework:** FastAPI (Python)
- **ORM:** SQLModel
- **Database:** Neon PostgreSQL (Serverless)
- **AI:** OpenRouter API + DeepSeek V3
- **Auth:** JWT + Header-based

### Development
- **Spec-Driven:** Claude Code + Spec-Kit Plus
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions
- **Package Manager:** npm (frontend), pip (backend)

---

## 📈 Project Phases

### Phase I: Console Application ✅
**Goal:** Python command-line todo app with in-memory storage

**Completed:**
- Basic CRUD operations
- Task management via CLI
- Clean code architecture
- Project structure setup

**Technology:** Python 3.13+, UV package manager

---

### Phase II: Full-Stack Web Application ✅
**Goal:** Transform to modern web app with persistent storage

**Completed:**
- Next.js responsive frontend
- FastAPI REST API backend
- Neon PostgreSQL database
- Better Auth authentication
- User signup/login flows
- Multi-user task isolation

**Key Endpoints:**
```
GET    /api/{user_id}/tasks         - List all tasks
POST   /api/{user_id}/tasks         - Create task
PUT    /api/{user_id}/tasks/{id}    - Update task
DELETE /api/{user_id}/tasks/{id}    - Delete task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion
```

---

### Phase III: AI-Powered Chatbot ✅ (Current)
**Goal:** Add conversational AI for natural language task management

**Completed:**
- ✅ AI chatbot integration (OpenRouter + DeepSeek V3)
- ✅ Natural language task creation
- ✅ Smart metadata extraction (dates, priorities, categories)
- ✅ Stateless architecture with DB conversation persistence
- ✅ Function calling for task operations
- ✅ Auto-refresh UI after chat actions
- ✅ Multi-user support maintained
- ✅ Unlimited AI quota (free tier)

**AI Capabilities:**
- "Add task to buy milk tomorrow" → Creates task with due_date
- "List my urgent tasks" → Filters by high priority
- "Complete the groceries task" → Marks task as done
- "Delete old meetings" → Finds and removes matching tasks

**Chat API:**
```
POST /api/{user_id}/chat
{
  "conversation_id": 123,      // optional
  "message": "Add task..."      // required
}
```

---

### Phase IV: Kubernetes Deployment (Upcoming)
**Goal:** Deploy to local Kubernetes with Minikube

**Planned:**
- Docker containerization
- Helm charts
- Minikube local deployment
- kubectl-ai & kagent integration
- AIOps workflows

---

### Phase V: Cloud Production (Future)
**Goal:** Advanced cloud deployment

**Planned:**
- DigitalOcean Kubernetes / GKE / AKS
- Kafka event-driven architecture
- Dapr integration
- Advanced features (recurring tasks, reminders)

---

## 🚀 Getting Started

### Prerequisites

```bash
# Required
- Node.js 20+
- Python 3.13+
- PostgreSQL (or Neon account)
- OpenRouter API key (free)

# Optional
- Docker Desktop
- Vercel CLI
```

### Installation

**1. Clone Repository:**
```bash
git clone https://github.com/Tahir-yamin/todo_hackathon_phase2.git
cd todo_hackathon_phase2
```

**2. Backend Setup:**
```bash
cd phase2/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

**3. Frontend Setup:**
```bash
cd phase2/frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local
# Edit .env.local with your credentials
```

**4. Database Setup:**
- Create account at [Neon](https://neon.tech)
- Create new database
- Copy connection string to `.env` files

**5. AI Setup:**
- Sign up at [OpenRouter](https://openrouter.ai/)
- Create API key (free)
- Add to `backend/.env`: `OPENROUTER_API_KEY=sk-or-v1-...`

### Running Locally

**Terminal 1 - Backend:**
```bash
cd phase2/backend
python -m uvicorn main:app --reload --port 8002
```

**Terminal 2 - Frontend:**
```bash
cd phase2/frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:3002
- Backend API: http://localhost:8002
- API Docs: http://localhost:8002/docs

---

## 🌐 Deployment

### Vercel (Recommended for Frontend)

**Automatic Deployment:**
1. Push to GitHub `main` branch
2. GitHub Actions automatically deploys
3. Live at: https://phase2-six.vercel.app

**Manual Deployment:**
```bash
npm i -g vercel
cd phase2/frontend
vercel --prod
```

**Environment Variables (Vercel Dashboard):**
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `NEXT_PUBLIC_API_URL`

### Backend Deployment Options

- **Vercel:** Limited Python support
- **Railway:** [railway.app](https://railway.app)
- **Render:** [render.com](https://render.com)
- **Fly.io:** [fly.io](https://fly.io)

---

## 🤖 AI Integration

### OpenRouter Setup

**Why OpenRouter?**
- ✅ Free unlimited tier (DeepSeek V3)
- ✅ Access to 100+ AI models
- ✅ OpenAI SDK compatible
- ✅ Automatic model fallback
- ✅ Better rate limits

**Get API Key:**
1. Visit https://openrouter.ai/
2. Sign up (free)
3. Go to Keys → Create Key
4. Copy `sk-or-v1-...`
5. Add to `backend/.env`

### Supported Commands

```
"Add task to buy milk tomorrow"
"List all my pending tasks"
"Mark task 5 as complete"
"Delete the meeting task"
"Create urgent task to call John at 2pm"
"Show me high priority tasks"
```

### Migration from Gemini

**Previous:** Google Gemini API (20 req/day limit)  
**Current:** OpenRouter + DeepSeek V3 (unlimited free)

**Reason:** Hit quota limits during development. OpenRouter provides better free tier and reliability.

---

## 🔐 Security

### Best Practices Implemented

✅ **Environment Variables**
- All secrets in `.env` files (gitignored)
- `.env.example` templates provided
- No hardcoded credentials

✅ **API Key Management**
- Rotated exposed keys
- Secure storage
- Per-environment keys

✅ **Authentication**
- JWT token validation
- User isolation
- Header-based auth for development
- Cookie-based for production

✅ **Security Incident Response**
- Documented in `security-incident-report.md`
- Enhanced `.gitignore`
- Automated security checks

### Security Checklist

Before deploying:
- [ ] Rotate all API keys
- [ ] Update `.env` with production values
- [ ] Enable CORS only for production domains
- [ ] Use HTTPS everywhere
- [ ] Implement rate limiting
- [ ] Enable database SSL

---

## 📚 Documentation

### Main Docs
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment guide (GitHub Pages & Vercel)
- **[Security Incident Report](./security-incident-report.md)** - Security best practices
- **[AI Integration Skills Guide](./ai-integration-skills-guide.md)** - Reusable AI patterns
- **[Phase III Lessons Learned](./phase3-lessons-learned-complete.md)** - Complete journey (40+ pages)
- **[Requirements Verification](./phase3-requirements-verification.md)** - Spec compliance check

### Additional Resources
- **[MCP Server Implementation Guide](./mcp-server-implementation-guide.md)** - Future microservices architecture
- **[Vercel Deployment Walkthrough](./vercel-deployment-walkthrough.md)** - Step-by-step deployment

---

## 🎯 Hackathon Submission

**Project:** Todo Application Evolution  
**Phase:** III - AI Chatbot (Complete)  
**Points:** 200/200  
**Bonus Features:**
- Smart NLP extraction
- Multi-user support
- Auto-refresh UI
- Comprehensive documentation (40+ pages)

**Submission Links:**
- **GitHub:** https://github.com/Tahir-yamin/todo_hackathon_phase2
- **Live Demo:** https://phase2-six.vercel.app
- **Demo Video:** [90 seconds max]

---

## 👨‍💻 Developer

**Tahir Yamin**
- Email: tahiryamin2050@gmail.com
- GitHub: [@Tahir-yamin](https://github.com/Tahir-yamin)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Panaversity** - Hackathon organizers
- **OpenRouter** - AI API aggregation
- **Neon** - Serverless PostgreSQL
- **Vercel** - Deployment platform
- **Claude Code** - Spec-driven development assistant

---

## 🔄 Project Timeline

| Phase | Duration | Status | Completion Date |
|-------|----------|--------|----------------|
| Phase I | 1 week | ✅ Complete | Dec 7, 2025 |
| Phase II | 1 week | ✅ Complete | Dec 14, 2025 |
| Phase III | 1 week (23h dev time) | ✅ Complete | Dec 21, 2025 |
| Phase IV | TBD | 🔜 Upcoming | Jan 4, 2026 |
| Phase V | TBD | 📅 Planned | Jan 18, 2026 |

---

**⭐ Star this repo if you found it helpful!**

**🐛 Found a bug? Open an issue!**

**💡 Have suggestions? Submit a PR!**

---

<p align="center">
  <strong>Built with ❤️ for Panaversity Hackathon II</strong>
</p>