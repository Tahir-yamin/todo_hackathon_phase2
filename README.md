# 🚀 AI-Powered Todo Application - Hackathon Project

**Production-Ready Cloud-Native Todo Application with AI Chatbot & Kubernetes Deployment**

[![Deployment](https://img.shields.io/badge/Deployed-Vercel-black)](https://phase2-six.vercel.app)
[![Phase](https://img.shields.io/badge/Phase-IV%20Complete-brightgreen)]()
[![Kubernetes](https://img.shields.io/badge/K8s-Ready-blue)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## 📋 Quick Links

- **Live Demo**: [https://phase2-six.vercel.app](https://phase2-six.vercel.app)
- **Phase IV Deployment Guide**: [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md)
- **Spec-Driven Process**: [`CLAUDE.md`](./CLAUDE.md)
- **Project Constitution**: [`CONSTITUTION.md`](./CONSTITUTION.md)
- **Spec History**: [`specs/phase4/SPECIFICATION-HISTORY.md`](./specs/phase4/SPECIFICATION-HISTORY.md)

---

## 🎯 Overview

A comprehensive todo management application that evolved from a simple console app to a **production-ready cloud-native application** deployed on Kubernetes. Built using **spec-driven development** with Claude Code.

**Evolution Path**: Console App → Web App → AI-Powered → **Cloud-Native (Kubernetes)** → Future: Cloud Production

---

## ✨ Features

### Core Functionality (Phase I-II)
- ✅ **Full CRUD Operations** - Create, Read, Update, Delete tasks
- ✅ **User Authentication** - Email, Google, GitHub OAuth
- ✅ **Multi-User Support** - Isolated task management
- ✅ **Task Organization** - Priorities, categories, due dates
- ✅ **Search & Filter** - Find tasks quickly
- ✅ **Kanban Board** - Drag-and-drop interface

### AI-Powered Features (Phase III)
- 🤖 **Natural Language Processing** - "Add task to buy milk tomorrow"
- 📅 **Smart Date Extraction** - Understands "next Friday", "in 2 days"
- 🎯 **Auto-Prioritization** - Detects urgency from context
- 🏷️ **Category Inference** - Automatic task categorization
- 💬 **Conversational Interface** - Chat widget for task management
- ♾️ **Unlimited AI** - Free tier with OpenRouter + DeepSeek V3

### Cloud-Native Features (Phase IV) ✨
- ☸️ **Kubernetes Orchestration** - Auto-healing, rolling updates
- 🐳 **Docker Containerization** - Multi-stage optimized builds
- 📦 **Helm Package Management** - Version-controlled deployments
- 🔧 **ConfigMaps** - Externalized configuration
- 🏥 **Health Probes** - Liveness & readiness checks
- 📊 **Resource Management** - CPU/memory limits & requests
- 🤖 **Gordon AI Integration** - Docker AI Agent for operations
- 📚 **Comprehensive Documentation** - 70,000+ words, 22 workflows

---

## 🛠️ Tech Stack

### Application
- **Frontend**: Next.js 15 (React, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python, SQLModel)
- **Database**: Neon PostgreSQL (Serverless)
- **AI**: OpenRouter + DeepSeek V3
- **Auth**: Better Auth (Email, Google, GitHub)

### Cloud-Native (Phase IV)
- **Containerization**: Docker (multi-stage builds)
- **Orchestration**: Kubernetes (Docker Desktop)
- **Package Manager**: Helm Charts
- **AI DevOps**: Gordon, kubectl-ai, kagent
- **Deployment**: Local K8s + Cloud (Vercel/Railway)

### Development
- **Methodology**: Spec-Driven Development
- **AI Assistant**: Claude Code + Spec-Kit Plus
- **Version Control**: Git + GitHub
- **Documentation**: 70,000+ words, 22 workflows

---

## 📈 Project Phases

### ✅ Phase I: Console Application (Complete)
**Duration**: 1 week | **Completion**: Dec 7, 2025

- Python CLI with in-memory storage
- Basic CRUD operations
- Clean code architecture

### ✅ Phase II: Full-Stack Web App (Complete)
**Duration**: 1 week | **Completion**: Dec 14, 2025

- Next.js responsive frontend
- FastAPI REST backend
- PostgreSQL database
- Better Auth authentication
- Multi-user support

### ✅ Phase III: AI-Powered Chatbot (Complete)
**Duration**: 1 week | **Completion**: Dec 21, 2025

- Natural language processing
- Smart metadata extraction
- Function calling for task ops
- Unlimited AI quota

### ✅ Phase IV: Kubernetes Deployment (Complete)
**Duration**: 2 weeks | **Completion**: Dec 30, 2025

**Implementation**:
- ✅ Multi-stage Docker builds (Frontend: 485MB, Backend: 245MB)
- ✅ Kubernetes manifests (3 deployments, 3 services)
- ✅ Helm charts (400+ lines values.yaml)
- ✅ ConfigMaps for configuration
- ✅ Health probes & resource limits
- ✅ Gordon AI tested & documented
- ✅ kubectl-ai/kagent guides

**Documentation** (70,000+ words):
- Deployment guide (15,000 words)
- Spec history (10,000 words)
- Gordon AI guide (8,000 words)
- 22 operational workflows
- Security audit procedures

**Access**:
- Local: `http://localhost:30000` (Kubernetes NodePort)
- Cloud: `https://phase2-six.vercel.app` (Vercel)

**Guides**:
- [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md) - Complete deployment
- [`specs/phase4/SPECIFICATION-HISTORY.md`](./specs/phase4/SPECIFICATION-HISTORY.md) - Spec evolution

### 📅 Phase V: Cloud Production (Planned)
**Target**: Jan 18, 2026

- Azure AKS / GKE deployment
- Kafka event-driven architecture
- Dapr integration
- Advanced features (recurring tasks, reminders)

---

## 🚀 Quick Start

### Prerequisites

**For Web App (Phase II-III)**:
```bash
- Node.js 20+
- Python 3.13+
- PostgreSQL (or Neon account)
- OpenRouter API key (free)
```

**For Kubernetes (Phase IV)**:
```bash
- Docker Desktop 4.53+ (with Kubernetes enabled)
- Helm 3.13+
- kubectl
```

### Installation & Running

**Web App (Phase II-III)**:
```bash
# Clone repository
git clone https://github.com/Tahir-yamin/todo_hackathon_phase2.git
cd todo_hackathon_phase2

# Backend
cd phase2/backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
python -m uvicorn main:app --reload --port 8002

# Frontend (new terminal)
cd phase2/frontend
npm install
cp .env.example .env.local  # Edit with your credentials
npm run dev

# Access: http://localhost:3002
```

**Kubernetes (Phase IV)**:
```bash
# See comprehensive guide:
phase4/MANUAL-OPERATIONS-GUIDE.md

# Quick deploy (if prereqs met):
cd phase4
helm install todo-chatbot ./helm/todo-chatbot

# Access: http://localhost:30000
```

---

## 📚 Documentation

### Main Documentation
| Document | Description | Words |
|----------|-------------|-------|
| [`README.md`](./README.md) | This file - project overview | 2,000 |
| [`CLAUDE.md`](./CLAUDE.md) | Spec-driven development process | 8,500 |
| [`CONSTITUTION.md`](./CONSTITUTION.md) | Project principles & architecture | 5,000 |

### Phase IV Documentation
| Document | Description | Words |
|----------|-------------|-------|
| [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md) | Complete deployment guide | 15,000 |
| [`phase4/docs/GORDON-AI-GUIDE.md`](./phase4/docs/GORDON-AI-GUIDE.md) | Docker AI Agent integration | 8,000 |
| [`phase4/docs/kubectl-ai-kagent-setup.md`](./phase4/docs/kubectl-ai-kagent-setup.md) | AIOps tools setup | 4,500 |
| [`phase4/docs/DEMO-VIDEO-SCRIPT.md`](./phase4/docs/DEMO-VIDEO-SCRIPT.md) | 90-second demo guide | 5,000 |
| [`specs/phase4/SPECIFICATION-HISTORY.md`](./specs/phase4/SPECIFICATION-HISTORY.md) | Complete spec evolution | 10,000 |
| [`.agent/workflows/`](./.agent/workflows/) | 22 operational workflows | 20,000+ |

### Additional Documentation  
- **Phase 3**: [`docs/phase3/`](./docs/phase3/) - Auth, security, deployment guides
- **Deployment**: [`docs/deployment/`](./docs/deployment/) - Vercel, Railway guides
- **Security**: [`.agent/workflows/security-audit.md`](./.agent/workflows/security-audit.md)

**Total Documentation**: 70,000+ words

---

## 🌐 Deployment

### Kubernetes (Phase IV)
```bash
# Local Kubernetes (Docker Desktop)
helm install todo-chatbot ./phase4/helm/todo-chatbot
kubectl get pods -n todo-chatbot

# Access: http://localhost:30000
```

### Cloud (Bonus)
- **Frontend**: Vercel (https://phase2-six.vercel.app)
- **Backend**: Railway (auto-deployed)

See [`docs/deployment/VERCEL_RAILWAY_FIX.md`](./docs/deployment/VERCEL_RAILWAY_FIX.md) for cloud deployment.

---

## 🔐 Security

### Implementation
- ✅ Zero exposed credentials (100% audit pass)
- ✅ SSH-based GitHub authentication
- ✅ Comprehensive `.gitignore` patterns
- ✅ Kubernetes Secrets documented  
- ✅ SSL for database connections
- ✅ Non-root Docker containers

### Security Audit
See [`.agent/workflows/security-audit.md`](./.agent/workflows/security-audit.md) for complete security procedures.

---

## 🎯 Hackathon Submission

### Phase IV Deliverables ✅
- [x] **Docker Containerization** - Multi-stage, optimized
- [x] **Kubernetes Deployment** - Local K8 running
- [x] **Helm Charts** - Version-controlled
- [x] **All Features Working** - CRUD + AI chatbot
- [x] **Gordon AI** - Tested and documented
- [x] **kubectl-ai/kagent** - Setup guides created
- [x] **Comprehensive Documentation** - 70,000+ words
- [x] **Spec History** - Complete evolution documented
- [x] **Security Audit** - 100% pass

### Bonus Achievements
- ✨ 22 operational workflows
- ✨ Spec-driven development demonstrated
- ✨ Cloud deployment (Vercel/Railway)
- ✨ Production-ready deployment (Level 3/5 cloud-native maturity)

### Links
- **Repository**: https://github.com/Tahir-yamin/todo_hackathon_phase2
- **Live Demo**: https://phase2-six.vercel.app
- **Local K8s**: `localhost:30000` (follow deployment guide)

---

## 👨‍💻 Developer

**Tahir Yamin**
- GitHub: [@Tahir-yamin](https://github.com/Tahir-yamin)
- Email: tahiryamin2050@gmail.com

---

## 🙏 Acknowledgments

- **Panaversity** - Hackathon organizers
- **Claude Code** - Spec-driven development
- **OpenRouter** - AI API access
- **Neon** - Serverless PostgreSQL
- **Vercel** - Cloud deployment
- **Docker** - Containerization platform

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🔄 Project Timeline

| Phase | Duration | Status | Completion |
|-------|----------|--------|------------|
| Phase I | 1 week | ✅ Complete | Dec 7, 2025 |
| Phase II | 1 week | ✅ Complete | Dec 14, 2025 |
| Phase III | 1 week | ✅ Complete | Dec 21, 2025 |
| **Phase IV** | **2 weeks** | **✅ Complete** | **Dec 30, 2025** |
| Phase V | TBD | 📅 Planned | Jan 18, 2026 |

---

<p align="center">
  <strong>⭐ Star this repo if you found it helpful!</strong><br>
  <strong>🐛 Found a bug? Open an issue!</strong><br>
  <strong>💡 Have suggestions? Submit a PR!</strong>
</p>

<p align="center">
  <strong>Built with ❤️ for Panaversity Hackathon II</strong><br>
  <em>Demonstrating spec-driven development & cloud-native architecture</em>
</p>

---

**📊 Stats**: 70,000+ words documentation | 22 workflows | 100% security audit | Level 3/5 cloud-native maturity