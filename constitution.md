# Todo App Constitution

**Last Updated**: 2025-12-19  
**Phase**: Phase II Complete  
**Purpose**: Define non-negotiable principles and constraints for all phases

---

## I. Architecture Principles

### 1. Spec-Driven Development
- **MANDATORY**: All features must have a spec before implementation
- **NO freestyle coding**: Every line of code must trace back to a specification
- **Documentation first**: Specs are the source of truth, not the code

### 2. Type Safety
- **Frontend**: TypeScript strict mode enabled
- **Backend**: Python type hints required for all functions
- **No `any` types**: Explicit typing enforced

### 3. User Isolation
- **MANDATORY**: All user data must be isolated
- **Database level**: Every task must have `user_id` foreign key
- **API level**: Every endpoint must verify user ownership

### 4. Stateless Services
- **No server-side sessions**: Use JWT tokens
- **Database persistence**: All state stored in database
- **Horizontal scalability**: Any instance can handle any request

---

## II. Tech Stack Constraints

### Frontend (IMMUTABLE)
- **Framework**: Next.js 14+ with App Router ONLY
- **Language**: TypeScript ONLY
- **Styling**: Tailwind CSS ONLY (no CSS-in-JS, no SCSS)
- **State**: React hooks + Context API (no Redux, no MobX)
- **HTTP Client**: Custom API client with Fetch API

### Backend (IMMUTABLE)
- **Framework**: FastAPI ONLY
- **Language**: Python 3.13+ ONLY
- **ORM**: SQLModel ONLY
- **Database**: PostgreSQL (Neon Serverless) ONLY
- **Auth**: Better Auth with JWT ONLY

### Prohibited Technologies
- ❌ Express.js
- ❌ Django
- ❌ MongoDB
- ❌ Firebase
- ❌ Supabase Auth (Better Auth only)

---

## III. Security Requirements

### Authentication
- **JWT with expiry**: Tokens must expire (recommended: 7 days)
- **Secure storage**: Frontend uses localStorage temporarily, httpOnly cookies in production
- **Password hashing**: bcrypt with salt rounds >= 10
- **User session validation**: Every protected API call must verify JWT

### API Security
- **CORS**: Strict origin whitelist
- **Input validation**: Pydantic models on backend, Zod/validation on frontend
- **SQL injection prevention**: Use ORM parameterized queries ONLY
- **Rate limiting**: Implement in production (Phase V)

### Data Privacy
- **User isolation**: Users can ONLY access their own data
- **No data leakage**: Error messages must not expose sensitive data
- **HTTPS only**: All production traffic encrypted

---

## IV. Performance Standards

### Frontend
- **First Contentful Paint (FCP)**: < 1.5 seconds
- **Time to Interactive (TTI)**: < 3.0 seconds
- **Lighthouse Score**: >= 90 (Performance)
- **Bundle Size**: < 500 KB (initial load)

### Backend
- **API Response Time**: < 500ms (p95)
- **Database Query Time**: < 100ms (p95)
- **Concurrent Requests**: >= 100 req/s

### Optimization Techniques
- **Debouncing**: Search inputs (300ms)
- **Memoization**: Expensive calculations
- **Lazy Loading**: Heavy components
- **Code Splitting**: Route-based

---

## V. Code Quality Standards

### TypeScript/JavaScript
- **Strict Mode**: Enabled
- **ESLint**: Enforced
- **Prettier**: Auto-formatting
- **No console.log**: In production builds
- **Error Handling**: Try-catch for all async operations

### Python
- **Type Hints**: Required for all functions
- **Pydantic Models**: For all API request/response
- **Docstrings**: For public functions
- **Black**: Auto-formatting
- **mypy**: Type checking enforced

### General
- **DRY Principle**: No code duplication
- **SOLID Principles**: Follow OOP best practices
- **Meaningful Names**: Variables, functions, components
- **Single Responsibility**: Functions do one thing well

---

## VI. UI/UX Standards

### Design System
- **Theme**: Neural network / cyberpunk aesthetic
- **Colors**: Cyan (#00F0FF) for dark, Blue (#0078B4) for light
- **Typography**: Space Grotesk (monospace feel)
- **Animations**: Smooth, hardware-accelerated only

### Accessibility
- **WCAG AA Compliance**: Minimum requirement
- **Keyboard Navigation**: All features accessible
- **Screen Readers**: ARIA labels on interactive elements
- **Color Contrast**: >= 4.5:1 for text

### Responsive Design
- **Mobile First**: Design for 320px width minimum
- **Breakpoints**: Tailwind defaults (sm: 640px, md: 768px, lg: 1024px)
- **Touch Targets**: >= 44x44px minimum

---

## VII. Database Standards

### Schema Design
- **Normalization**: 3NF minimum
- **Foreign Keys**: Always enforce relationships
- **Indexes**: On all foreign keys and frequently queried columns
- **Timestamps**: `created_at` and `updated_at` on all tables

### Migrations
- **Alembic**: Use for all schema changes (Phase IV+)
- **Reversible**: All migrations must have downgrade
- **Idempotent**: Migrations can run multiple times safely

### Naming Conventions
- **Tables**: Plural lowercase (e.g., `tasks`, `users`)
- **Columns**: Snake_case (e.g., `user_id`, `created_at`)
- **Constraints**: Descriptive names (e.g., `fk_tasks_user_id`)

---

## VIII. API Design Standards

### RESTful Principles
- **Resource-based**: URLs represent resources
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: Proper use (200, 201, 400, 401, 404, 500)
- **Consistent Paths**: `/api/{user_id}/tasks/{task_id}`

### Request/Response Format
- **Content-Type**: `application/json` ONLY
- **Request Validation**: Pydantic models
- **Response Structure**: Consistent format
  ```json
  {
    "success": true,
    "data": {...},
    "error": null
  }
  ```

### Error Handling
- **Descriptive Messages**: User-friendly error messages
- **Error Codes**: Consistent error codes
- **Stack Traces**: NEVER expose in production

---

## IX. Testing Standards

### Coverage Requirements
- **Backend**: >= 80% code coverage
- **Frontend**: >= 70% component coverage
- **Critical Paths**: 100% coverage (auth, CRUD)

### Testing Types
- **Unit Tests**: Pure functions, utilities
- **Integration Tests**: API endpoints, database operations
- **E2E Tests**: Complete user flows (Playwright)

### Test Principles
- **AAA Pattern**: Arrange, Act, Assert
- **Isolation**: Tests don't depend on each other
- **Fast**: Unit tests < 100ms each
- **Deterministic**: No flaky tests

---

## X. Deployment Standards

### Environment Management
- **Development**: Local (SQLite, localhost)
- **Staging**: Cloud (Neon DB, Vercel, Railway)
- **Production**: Cloud (optimized, monitored)

### Environment Variables
- **NEVER commit**: `.env` files to git
- **Required vars**: Documented in README
- **Validation**: App fails fast if vars missing

### CI/CD (Phase V)
- **GitHub Actions**: Automated testing
- **Deployment**: Auto-deploy on merge to main
- **Rollback**: One-click rollback capability

---

## XI. Documentation Standards

### Code Documentation
- **README.md**: Setup instructions, architecture overview
- **CLAUDE.md**: Agent-specific guidelines
- **AGENTS.md**: Workflow and principles
- **inline comments**: For complex logic only

### API Documentation
- **OpenAPI/Swagger**: Auto-generated from FastAPI
- **Examples**: Request/response examples for all endpoints
- **Error Cases**: Document all possible errors

### Spec Documentation
- **Before Implementation**: Specs written first
- **Living Documents**: Update as requirements change
- **Traceability**: Clear links from code to specs

---

## XII. Phase-Specific Rules

### Phase II (Current - Complete)
- ✅ Basic Level features MANDATORY
- ✅ Better Auth integration MANDATORY
- ✅ User isolation MANDATORY
- ✅ Spec-driven development MANDATORY

### Phase III (Next - AI Chatbot)
- OpenAI ChatKit UI MANDATORY
- OpenAI Agents SDK MANDATORY  
- MCP Server MANDATORY
- Stateless chat endpoint MANDATORY
- Database-persisted conversations MANDATORY

### Phase IV (Kubernetes)
- Docker containers MANDATORY
- Helm charts MANDATORY
- Minikube local deployment MANDATORY
- kubectl-ai usage MANDATORY

### Phase V (Cloud + Kafka)
- Kafka event streaming MANDATORY
- Dapr integration MANDATORY
- Cloud deployment (GKE/AKS) MANDATORY
- Full observability MANDATORY

---

## XIII. Git Workflow

### Branching Strategy
- **main**: Production-ready code
- **develop**: Integration branch (Phase III+)
- **feature/***: Feature branches

### Commit Standards
- **Conventional Commits**: Use prefixes (feat:, fix:, docs:, etc.)
- **Atomic Commits**: One logical change per commit
- **Meaningful Messages**: Describe what **and why**

---

## XIV. Violation Consequences

### Critical Violations
These will result in **immediate failure**:
- ❌ Manual code without spec
- ❌ Violating user isolation
- ❌ Exposing sensitive data
- ❌ Using prohibited technologies

### Warning Violations
These require **immediate fix**:
- ⚠️ Type safety violations
- ⚠️ Test coverage < threshold
- ⚠️ Performance below standards
- ⚠️ Missing documentation

---

## XV. Change Management

### Updating This Constitution
- **Consensus Required**: Major changes need justification
- **Version Control**: Track all changes in git
- **Backward Compatibility**: Minimize breaking changes

### When to Update
- New phase introduces new requirements
- Technology constraints change
- Performance standards need adjustment

---

**Effective Date**: 2025-12-01  
**Last Reviewed**: 2025-12-19  
**Next Review**: Before Phase III Implementation  
**Authority**: Hackathon Requirements + Best Practices
