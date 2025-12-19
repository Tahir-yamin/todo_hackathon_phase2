# Todo App - Hackathon II

**This is the root navigation file for Claude Code and other AI agents.**

---

## Project Overview

This is a monorepo using **Spec-Kit Plus** for spec-driven development as part of Hackathon II: "Evolution of Todo".

**Current Phase**: Phase II Complete (Full-Stack Web Application)  
**Next Phase**: Phase III (AI-Powered Todo Chatbot)

---

## How to Navigate This Project

### 1. Agent Instructions
**Read First**: `@AGENTS.md`
- Complete agent behavior rules
- Spec-Kit workflow (Specify → Plan → Tasks → Implement)
- Project structure
- Development principles

### 2. Specifications
Located in `/specs/`:
- `@specs/overview.md` - Project overview
- `@specs/features/` - Feature specs (what to build)
- `@specs/api/` - API endpoint specs
- `@specs/database/` - Schema and model specs  
- `@specs/ui/` - Component and page specs

### 3. Implementation Code

**Frontend**: `@phase2/frontend/`
- Read: `@phase2/frontend/CLAUDE.md` for frontend guidelines
- Stack: Next.js 14, TypeScript, Tailwind CSS
- Components in `/src/components/`
- Pages in `/src/app/`

**Backend**: `@phase2/backend/`
- Read: `@phase2/backend/CLAUDE.md` for backend guidelines
- Stack: FastAPI, SQLModel, Neon PostgreSQL
- API routes in `/backend/routers/`
- Models in `/backend/models.py`

### 4. Implementation History
**Read**: `@phase2/docs/CLAUDE.md`
- Complete implementation timeline
- Technology choices and rationale
- Challenges and solutions
- Code quality practices

---

## Quick Commands Reference

### Frontend
```bash
cd phase2/frontend
npm run dev          # Development server
npm run build        # Production build
npm test             # Run tests
```

### Backend
```bash
cd phase2/backend
uvicorn backend.main:app --reload --port 8002   # Development server
pytest              # Run tests
```

### Both (from root)
```bash
cd phase2
./start.ps1         # Start both frontend and backend (Windows)
```

---

## Development Workflow

1. **Read Spec**: `@specs/features/[feature].md`
2. **Check Plan**: `@specs/phase2-implementation-plan.md`
3. **Implement Backend**: Follow `@phase2/backend/CLAUDE.md`
4. **Implement Frontend**: Follow `@phase2/frontend/CLAUDE.md`
5. **Test**: Manual QA + automated tests
6. **Update Docs**: If spec changed, update spec files

---

## Key Project Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent behavior and workflow |
| `CLAUDE.md` | This file - navigation hub |
| `README.md` | User-facing documentation |
| `MODERN_SKILLS.md` | Development patterns and techniques |
| `.spec-kit/config.yaml` | Spec-Kit configuration |

---

## Spec-Kit Plus Structure

```
.spec-kit/           # Configuration
specs/               # Specifications
├── features/        # What to build
├── api/             # Endpoints
├── database/        # Schema
└── ui/              # Components
```

---

## Current Status

### Phase II: ✅ COMPLETE
- Task CRUD operations
- User authentication (Better Auth)
- Neural network UI theme
- Search & filter system
- 4-column Kanban board
- Real-time analytics
- Dark/light mode
- Mobile responsive

### Phase III: 📋 PLANNED
- OpenAI ChatKit interface
- OpenAI Agents SDK integration
- MCP Server for task operations
- Stateless chat endpoint
- Database-persisted conversations

---

## Important Notes

1. **Always reference specs** before implementing
2. **Follow Spec-Kit workflow**: Specify → Plan → Tasks → Implement
3. **Update specs** if requirements change
4. **Document decisions** in appropriate CLAUDE.md files
5. **Test thoroughly** before marking complete

---

## Need Help?

- **Agent Rules**: See `@AGENTS.md`
- **Frontend Guide**: See `@phase2/frontend/CLAUDE.md`
- **Backend Guide**: See `@phase2/backend/CLAUDE.md`
- **Implementation History**: See `@phase2/docs/CLAUDE.md`
- **Feature Specs**: See `@specs/features/`

---

**Hackathon**: Evolution of Todo - Mastering Spec-Driven Development & Cloud Native AI  
**Team**: Tahir Yamin  
**Repository**: https://github.com/Tahir-yamin/todo_hackathon_phase2  
**Last Updated**: 2025-12-19
