# ≡ƒÜÇ AI-Powered Todo Application - Hackathon Project

**Production-Ready Cloud-Native Todo Application with AI Chatbot & Kubernetes Deployment**

[![Deployment](https://img.shields.io/badge/Deployed-Vercel-black)]([https://phase2-six.vercel.app](https://frontend-seven-tawny-19.vercel.app/))
[![Phase](https://img.shields.io/badge/Phase-IV%20Complete-brightgreen)]()
[![Kubernetes](https://img.shields.io/badge/K8s-Ready-blue)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## ≡ƒôï Quick Links

- **Live Demo**: [https://phase2-six.vercel.app](https://frontend-seven-tawny-19.vercel.app)
- **Phase IV Deployment Guide**: [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md)
- **Spec-Driven Process**: [`CLAUDE.md`](./CLAUDE.md)
- **Project Constitution**: [`CONSTITUTION.md`](./CONSTITUTION.md)
- **Spec History**: [`specs/phase4/SPECIFICATION-HISTORY.md`](./specs/phase4/SPECIFICATION-HISTORY.md)

---

## ≡ƒÄ» Overview

A comprehensive todo management application that evolved from a simple console app to a **production-ready cloud-native application** deployed on Kubernetes. Built using **spec-driven development** with Claude Code.

**Evolution Path**: Console App ΓåÆ Web App ΓåÆ AI-Powered ΓåÆ **Cloud-Native (Kubernetes)** ΓåÆ Future: Cloud Production

---

## Γ£¿ Features

### Core Functionality (Phase I-II)
- Γ£à **Full CRUD Operations** - Create, Read, Update, Delete tasks
- Γ£à **User Authentication** - Email, Google, GitHub OAuth
- Γ£à **Multi-User Support** - Isolated task management
- Γ£à **Task Organization** - Priorities, categories, due dates
- Γ£à **Search & Filter** - Find tasks quickly
- Γ£à **Kanban Board** - Drag-and-drop interface

### AI-Powered Features (Phase III)
- ≡ƒñû **Natural Language Processing** - "Add task to buy milk tomorrow"
- ≡ƒôà **Smart Date Extraction** - Understands "next Friday", "in 2 days"
- ≡ƒÄ» **Auto-Prioritization** - Detects urgency from context
- ≡ƒÅ╖∩╕Å **Category Inference** - Automatic task categorization
- ≡ƒÆ¼ **Conversational Interface** - Chat widget for task management
- ΓÖ╛∩╕Å **Unlimited AI** - Free tier with OpenRouter + DeepSeek V3

### Cloud-Native Features (Phase IV) Γ£¿
- Γÿ╕∩╕Å **Kubernetes Orchestration** - Auto-healing, rolling updates
- ≡ƒÉ│ **Docker Containerization** - Multi-stage optimized builds
- ≡ƒôª **Helm Package Management** - Version-controlled deployments
- ≡ƒöº **ConfigMaps** - Externalized configuration
- ≡ƒÅÑ **Health Probes** - Liveness & readiness checks
- ≡ƒôè **Resource Management** - CPU/memory limits & requests
- ≡ƒñû **Gordon AI Integration** - Docker AI Agent for operations
- ≡ƒôÜ **Comprehensive Documentation** - 70,000+ words, 22 workflows

---

## ≡ƒ¢á∩╕Å Tech Stack

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

## ≡ƒôê Project Phases

### Γ£à Phase I: Console Application (Complete)
**Duration**: 1 week | **Completion**: Dec 7, 2025

- Python CLI with in-memory storage
- Basic CRUD operations
- Clean code architecture

### Γ£à Phase II: Full-Stack Web App (Complete)
**Duration**: 1 week | **Completion**: Dec 14, 2025

- Next.js responsive frontend
- FastAPI REST backend
- PostgreSQL database
- Better Auth authentication
- Multi-user support

### Γ£à Phase III: AI-Powered Chatbot (Complete)
**Duration**: 1 week | **Completion**: Dec 21, 2025

- Natural language processing
- Smart metadata extraction
- Function calling for task ops
- Unlimited AI quota

### Γ£à Phase IV: Kubernetes Deployment (Complete)
**Duration**: 2 weeks | **Completion**: Dec 30, 2025

**Implementation**:
- Γ£à Multi-stage Docker builds (Frontend: 485MB, Backend: 245MB)
- Γ£à Kubernetes manifests (3 deployments, 3 services)
- Γ£à Helm charts (400+ lines values.yaml)
- Γ£à ConfigMaps for configuration
- Γ£à Health probes & resource limits
- Γ£à Gordon AI tested & documented
- Γ£à kubectl-ai/kagent guides

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

### ≡ƒôà Phase V: Cloud Production (Planned)
**Target**: Jan 18, 2026

- Azure AKS / GKE deployment
- Kafka event-driven architecture
- Dapr integration
- Advanced features (recurring tasks, reminders)

---

## ≡ƒÜÇ Quick Start

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

## ≡ƒôÜ Documentation

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

## ≡ƒîÉ Deployment

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

## ≡ƒöÉ Security

### Implementation
- Γ£à Zero exposed credentials (100% audit pass)
- Γ£à SSH-based GitHub authentication
- Γ£à Comprehensive `.gitignore` patterns
- Γ£à Kubernetes Secrets documented  
- Γ£à SSL for database connections
- Γ£à Non-root Docker containers

### Security Audit
See [`.agent/workflows/security-audit.md`](./.agent/workflows/security-audit.md) for complete security procedures.

---

## ≡ƒÄ» Hackathon Submission

### Phase IV Deliverables Γ£à
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
- Γ£¿ 22 operational workflows
- Γ£¿ Spec-driven development demonstrated
- Γ£¿ Cloud deployment (Vercel/Railway)
- Γ£¿ Production-ready deployment (Level 3/5 cloud-native maturity)

### Links
- **Repository**: https://github.com/Tahir-yamin/todo_hackathon_phase2
- **Live Demo**: https://phase2-six.vercel.app
- **Local K8s**: `localhost:30000` (follow deployment guide)

---

## ≡ƒæ¿ΓÇì≡ƒÆ╗ Developer

**Tahir Yamin**
- GitHub: [@Tahir-yamin](https://github.com/Tahir-yamin)
- Email: tahiryamin2050@gmail.com

---

## ≡ƒÖÅ Acknowledgments

- **Panaversity** - Hackathon organizers
- **Claude Code** - Spec-driven development
- **OpenRouter** - AI API access
- **Neon** - Serverless PostgreSQL
- **Vercel** - Cloud deployment
- **Docker** - Containerization platform

---

## ≡ƒôä License

MIT License - See [LICENSE](./LICENSE) file

---

## ≡ƒöä Project Timeline

| Phase | Duration | Status | Completion |
|-------|----------|--------|------------|
| Phase I | 1 week | Γ£à Complete | Dec 7, 2025 |
| Phase II | 1 week | Γ£à Complete | Dec 14, 2025 |
| Phase III | 1 week | Γ£à Complete | Dec 21, 2025 |
| **Phase IV** | **2 weeks** | **Γ£à Complete** | **Dec 30, 2025** |
| Phase V | TBD | ≡ƒôà Planned | Jan 18, 2026 |

---

<p align="center">
  <strong>Γ¡É Star this repo if you found it helpful!</strong><br>
  <strong>≡ƒÉ¢ Found a bug? Open an issue!</strong><br>
  <strong>≡ƒÆí Have suggestions? Submit a PR!</strong>
</p>

<p align="center">
  <strong>Built with Γ¥ñ∩╕Å for Panaversity Hackathon II</strong><br>
  <em>Demonstrating spec-driven development & cloud-native architecture</em>
</p>

---

**≡ƒôè Stats**: 70,000+ words documentation | 22 workflows | 100% security audit | Level 3/5 cloud-native maturity
