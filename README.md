# 🚀 AI-Powered Todo Application - Hackathon Project

**Production-Ready Cloud-Native Todo Application with AI Chatbot & Kubernetes Deployment**

[![Deployment](https://img.shields.io/badge/Deployed-AKS-blue)](http://128.203.86.119:3000)
[![Phase](https://img.shields.io/badge/Phase-V%20Complete-success)]()
[![Kubernetes](https://img.shields.io/badge/K8s-Production-green)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

---

## 🔗 Quick Links

- **Live Demo (Phase V)**: [http://128.203.86.119:3000](http://128.203.86.119:3000) - **Azure AKS Production**
- **Phase V Demo Documentation**: [`PHASE5_DEMO_DOCUMENTATION.md`](./PHASE5_DEMO_DOCUMENTATION.md)
- **Phase IV Deployment Guide**: [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md)
- **Spec-Driven Process**: [`CLAUDE.md`](./CLAUDE.md)
- **Project Constitution**: [`CONSTITUTION.md`](./CONSTITUTION.md)

---

## 🎯 Overview

A comprehensive todo management application that evolved from a simple console app to a **production-ready cloud-native application** deployed on **Azure Kubernetes Service (AKS)** with **event-driven architecture**.

**Evolution Path**: Console App → Web App → AI-Powered → Kubernetes (Local) → **Cloud Production (AKS + Kafka + Dapr)** ✅

**Current Status**: **Phase V Complete** - Production deployment on Azure AKS with AI chat assistant, Kafka event streaming, and Dapr distributed runtime.

---

https://github.com/user-attachments/assets/d4261c66-7bb4-4ea3-b75b-c7ba16ee91cf

## ⚡ Features

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
- ♾️ **Unlimited AI** - Free tier with OpenRouter + Mistral

### Cloud-Native Features (Phase IV)
- ☸️ **Kubernetes Orchestration** - Auto-healing, rolling updates
- 🐳 **Docker Containerization** - Multi-stage optimized builds
- 📦 **Helm Package Management** - Version-controlled deployments
- 🔧 **ConfigMaps** - Externalized configuration
- 💚 **Health Probes** - Liveness & readiness checks
- 📊 **Resource Management** - CPU/memory limits & requests

### **⭐ NEW: Phase V - Production Cloud (Complete)** ✅
- ☁️ **Azure AKS Deployment** - Production-ready cloud infrastructure
- 📨 **Kafka Event Streaming** - Event-driven architecture with Strimzi
- 🔄 **Dapr Integration** - Distributed runtime for reliable messaging
- 🤖 **AI Chat Working** - All MCP tools functional
- 💰 **Resource Optimized** - 60% CPU reduction (single-node deployment)
- 🚀 **CI/CD Pipeline** - Automated GitHub Actions deployment
- 📚 **30 Production Skills** - Documented and reusable
- 🔧 **3 Executable Workflows** - With turbo annotations

---

## 🛠️ Tech Stack

### Application
- **Frontend**: Next.js 15 (React, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python, SQLModel)
- **Database**: PostgreSQL (on AKS)
- **AI**: OpenRouter + Mistral (free tier)
- **Auth**: Better Auth (Email, Google, GitHub)

### Cloud-Native (Phase IV-V)
- **Containerization**: Docker (multi-stage builds)
- **Orchestration**: Kubernetes (Azure AKS)
- **Package Manager**: Helm Charts
- **Event Streaming**: Kafka (Strimzi operator)
- **Distributed Runtime**: Dapr (Pub/Sub, State)
- **Container Registry**: Azure Container Registry
- **CI/CD**: GitHub Actions

---

## 📊 Project Phases

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

### **✅ Phase V: Cloud Production (Complete)** 🎉
**Duration**: 2 weeks | **Completion**: Jan 18, 2026

**Achievements**:
- ✅ **Azure AKS Deployment** - Production single-node cluster
- ✅ **Kafka + Dapr** - Event-driven architecture
- ✅ **3 Critical Bugs Fixed**:
  - Undefined reminder functions (commit: `ac1e2dd`)
  - Async/await mismatch (commit: `8c14249`)
  - AttributeError on remind_at (commit: `c36aaa5`)
- ✅ **Resource Optimization** - 60% CPU reduction (750m → 300m)
- ✅ **AI Chat 100% Working** - All MCP tools functional
- ✅ **CI/CD Pipeline** - Automated GitHub Actions
- ✅ **Documentation** - 30 skills + 3 workflows captured

**Live Demo**: http://128.203.86.119:3000

**Evidence**: See [`PHASE5_DEMO_DOCUMENTATION.md`](./PHASE5_DEMO_DOCUMENTATION.md) for complete proof

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

**For Kubernetes (Phase IV-V)**:
```bash
- Azure subscription (for AKS)
- Docker & kubectl
- Helm 3.13+
- Azure CLI
```

### Installation & Running

**Local Development**:
```bash
# Clone repository
git clone https://github.com/Tahir-yamin/todo_hackathon_phase2.git
cd todo_hackathon_phase1

# Backend
cd phase2/backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
uvicorn main:app --reload

# Frontend (new terminal)
cd phase2/frontend
npm install
cp .env.example .env.local  # Edit with your credentials
npm run dev

# Access: http://localhost:3000
```

**Deploy to AKS (Phase V)**:
```bash
# See complete workflow:
.agent/workflows/deploying-to-aks.md

# Quick deploy:
helm upgrade --install todo-chatbot ./phase4/helm/todo-chatbot \
  -n todo-chatbot \
  -f ./phase4/helm/todo-chatbot/values-optimized-cpu.yaml
```

---

## 📚 Documentation

### Main Documentation
| Document | Description | Words |
|----------|-------------|-------|
| [`README.md`](./README.md) | This file - project overview | 3,000 |
| [`PHASE5_DEMO_DOCUMENTATION.md`](./PHASE5_DEMO_DOCUMENTATION.md) | **NEW** Phase V evidence & demo guide | 5,000 |
| [`CLAUDE.md`](./CLAUDE.md) | Spec-driven development process | 8,500 |
| [`CONSTITUTION.md`](./CONSTITUTION.md) | Project principles & architecture | 5,000 |

### Phase V Documentation (NEW)
| Document | Description | Skills |
|----------|-------------|--------|
| [`.claude/mcp-debugging-skills.md`](./.claude/mcp-debugging-skills.md) | MCP tool debugging | 5 |
| [`.claude/kubernetes-resource-optimization-skills.md`](./.claude/kubernetes-resource-optimization-skills.md) | K8s optimization | 5 |
| [`.claude/dapr-configuration-skills.md`](./.claude/dapr-configuration-skills.md) | Dapr setup & troubleshooting | 5 |
| [`.claude/helm-configuration-skills.md`](./.claude/helm-configuration-skills.md) | Helm best practices | 5 |
| [`.claude/openrouter-api-skills.md`](./.claude/openrouter-api-skills.md) | AI API integration | 5 |
| [`.claude/python-async-patterns-skills.md`](./.claude/python-async-patterns-skills.md) | Async/await patterns | 5 |

### Phase V Workflows (NEW)
| Workflow | Description |
|----------|-------------|
| [`.agent/workflows/deploying-to-aks.md`](./.agent/workflows/deploying-to-aks.md) | Complete AKS deployment |
| [`.agent/workflows/github-actions-deployment-verification.md`](./.agent/workflows/github-actions-deployment-verification.md) | Post-deploy checks |
| [`.agent/workflows/fixing-chat-ui-errors.md`](./.agent/workflows/fixing-chat-ui-errors.md) | AI chat debugging |

### Phase IV Documentation
| Document | Description | Words |
|----------|-------------|-------|
| [`phase4/MANUAL-OPERATIONS-GUIDE.md`](./phase4/MANUAL-OPERATIONS-GUIDE.md) | Complete deployment guide | 15,000 |
| [`phase4/docs/GORDON-AI-GUIDE.md`](./phase4/docs/GORDON-AI-GUIDE.md) | Docker AI Agent integration | 8,000 |
| [`specs/phase4/SPECIFICATION-HISTORY.md`](./specs/phase4/SPECIFICATION-HISTORY.md) | Complete spec evolution | 10,000 |
| [`.agent/workflows/`](./.agent/workflows/) | 25 operational workflows | 25,000+ |

**Total Documentation**: 80,000+ words (Phase IV: 70K + Phase V: 10K)

---

## 🏗️ Architecture (Phase V)

```
┌─────────────────────────────────────────────────┐
│              Azure AKS Cluster                  │
│           (Single Node - 2 vCPU)                │
├─────────────────────────────────────────────────┤
│  Frontend (Next.js)  │  Backend (FastAPI)       │
│  Port: 3000          │  Port: 8000              │
│  CPU: 100m           │  CPU: 100m               │
│                      │  + Dapr Sidecar (100m)   │
├─────────────────────────────────────────────────┤
│  PostgreSQL          │  Kafka (Strimzi)         │
│  CPU: 100m           │  Event Streaming         │
└─────────────────────────────────────────────────┘
            ↓                      ↓
     GitHub Actions          Dapr Pub/Sub
```

**Resource Optimization**: 60% CPU reduction enables single-node deployment

---

## 🎉 Hackathon Submission

### Phase V Deliverables ✅ **NEW**
- [x] **Azure AKS Deployment** - Production cloud infrastructure
- [x] **Kafka Event Streaming** - Strimzi operator
- [x] **Dapr Integration** - Distributed runtime
- [x] **3 Critical Bugs Fixed** - All documented with evidence
- [x] **Resource Optimization** - 60% CPU reduction
- [x] **AI Chat 100% Working** - All commands functional
- [x] **CI/CD Pipeline** - GitHub Actions automated
- [x] **30 Skills Documented** - Production-tested and reusable
- [x] **3 Executable Workflows** - With turbo annotations
- [x] **Demo Documentation** - Complete with evidence

### Phase IV Deliverables ✅
- [x] **Docker Containerization** - Multi-stage, optimized
- [x] **Kubernetes Deployment** - Local K8s running
- [x] **Helm Charts** - Version-controlled
- [x] **All Features Working** - CRUD + AI chatbot
- [x] **Gordon AI** - Tested and documented
- [x] **Comprehensive Documentation** - 70,000+ words
- [x] **Security Audit** - 100% pass

### Bonus Achievements
- ✨ 25 operational workflows
- ✨ Spec-driven development demonstrated
- ✨ Production deployment (Azure AKS)
- ✨ Event-driven architecture (Kafka + Dapr)
- ✨ 80,000+ words documentation
- ✨ Level 4/5 cloud-native maturity

---

## 🔧 Key Commands

### Development
```bash
# Run backend
cd phase2/backend && uvicorn main:app --reload

# Run frontend
cd phase2/frontend && npm run dev
```

### Kubernetes (Phase V)
```bash
# Get pod status
kubectl get pods -n todo-chatbot

# View backend logs
kubectl logs -l app=backend -n todo-chatbot -c backend

# Check resource usage
kubectl top pods -n todo-chatbot

# Deploy/upgrade with Helm
helm upgrade --install todo-chatbot ./phase4/helm/todo-chatbot \
  -n todo-chatbot \
  -f ./phase4/helm/todo-chatbot/values-optimized-cpu.yaml
```

---

## 🐛 Troubleshooting

See [`.agent/workflows/fixing-chat-ui-errors.md`](./.agent/workflows/fixing-chat-ui-errors.md) for common issues.

**Quick Fixes**:
- **Pods Pending**: Use `values-optimized-cpu.yaml`
- **AI Chat Errors**: Check backend logs for MCP errors
- **MCP Tool Failures**: Test locally with `python -c "from mcp_server import mcp"`

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
- **Azure** - AKS free tier
- **Dapr Community** - Resource optimization guidelines
- **Strimzi Project** - Kafka operator

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 📅 Project Timeline

| Phase | Duration | Status | Completion |
|-------|----------|--------|------------|
| Phase I | 1 week | ✅ Complete | Dec 7, 2025 |
| Phase II | 1 week | ✅ Complete | Dec 14, 2025 |
| Phase III | 1 week | ✅ Complete | Dec 21, 2025 |
| Phase IV | 2 weeks | ✅ Complete | Dec 30, 2025 |
| **Phase V** | **2 weeks** | **✅ Complete** | **Jan 18, 2026** |

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

**📈 Stats**: 80,000+ words documentation | 30 Phase V skills | 25 workflows | 100% security audit | Level 4/5 cloud-native maturity | **Production on Azure AKS** ☁️
