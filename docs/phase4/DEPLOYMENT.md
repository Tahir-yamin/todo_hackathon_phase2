# GitHub Pages Deployment Guide

## 🚀 Automated Deployment Setup

Your project is now configured for automatic deployment to GitHub Pages!

### What Was Set Up:

1. **GitHub Actions Workflow** (`.github/workflows/deploy.yml`)
   - Triggers on every push to `main` branch
   - Builds Next.js app
   - Deploys to GitHub Pages

2. **Next.js Configuration** (`phase2/frontend/next.config.js`)
   - Static export enabled
   - GitHub Pages base path configured
   - Images optimized for static hosting

---

## 📋 Setup Steps Required:

### 1. Enable GitHub Pages

**Go to your repository:**
https://github.com/Tahir-yamin/todo_hackathon_phase2

**Settings → Pages:**
1. Source: **GitHub Actions** (not "Deploy from branch")
2. Click **Save**

### 2. Add Backend URL Secret

**Settings → Secrets and variables → Actions:**

1. Click **New repository secret**
2. Name: `BACKEND_API_URL`
3. Value: Your deployed backend URL (e.g., from Vercel/Railway)
   - Or use: `http://localhost:8002` for testing
4. Click **Add secret**

### 3. Push to Trigger Deployment

```bash
git add .
git commit -m "Setup GitHub Pages deployment"
git push origin main
```

### 4. Wait for Deployment

- Go to **Actions** tab
- Watch the workflow run
- Should complete in ~2-3 minutes

### 5. Access Your App

**Your app will be live at:**
```
https://tahir-yamin.github.io/todo_hackathon_phase2/
```

---

## 🔧 Configuration Details

### Environment Variables

**Build Time (in workflow):**
```yaml
env:
  NEXT_PUBLIC_APP_URL: https://tahir-yamin.github.io/todo_hackathon_phase2
  NEXT_PUBLIC_API_URL: ${{ secrets.BACKEND_API_URL }}
```

**Note:** Backend API must be deployed separately (Vercel, Railway, etc.)

### Next.js Export Configuration

```javascript
output: 'export'  // Static HTML export
basePath: '/todo_hackathon_phase2'  // GitHub Pages subdirectory
images: { unoptimized: true }  // No image optimization for static
```

---

## ⚠️ Important Notes

### Backend Deployment

**GitHub Pages only hosts the frontend!**

For backend, deploy to:
- **Vercel:** https://vercel.com/
- **Railway:** https://railway.app/
- **Render:** https://render.com/
- **Fly.io:** https://fly.io/

Then update `BACKEND_API_URL` secret with deployed backend URL.

### Authentication Limitation

**better-auth requires server-side!**

Options:
1. Use Vercel for full-stack deployment (recommended)
2. Mock auth for demo (read-only mode)
3. Use different auth (Firebase, Auth0)

---

## 🎯 Recommended: Deploy Full-Stack to Vercel

**Better option for your hackathon:**

1. **Vercel Deployment:**
   ```bash
   npm i -g vercel
   cd phase2
   vercel
   ```

2. **Benefits:**
   - Frontend + Backend together
   - better-auth works properly
   - Free SSL
   - Auto-deployment on push
   - Environment variables UI

3. **Your Vercel URL:**
   ```
   https://todo-hackathon-phase2.vercel.app
   ```

---

## 📊 Deployment Comparison

| Platform | Frontend | Backend | Auth | SSL | Cost |
|----------|----------|---------|------|-----|------|
| **GitHub Pages** | ✅ | ❌ | ❌ | ✅ | Free |
| **Vercel** | ✅ | ✅ | ✅ | ✅ | Free |
| **Netlify** | ✅ | ⚠️ Limited | ⚠️ | ✅ | Free |

**Verdict:** Use **Vercel** for hackathon submission!

---

## 🚀 Quick Vercel Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd "D:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2"
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: todo-hackathon-phase2
# - Directory: ./ (current)
# - Deploy? Yes
```

**Add environment variables in Vercel dashboard:**
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `OPENROUTER_API_KEY`

---

## ✅ Final Checklist

- [ ] GitHub Pages enabled (Settings → Pages → Source: GitHub Actions)
- [ ] `BACKEND_API_URL` secret added
- [ ] Workflow file committed
- [ ] next.config.js updated
- [ ] Pushed to main branch
- [ ] Workflow completed successfully
- [ ] App accessible at GitHub Pages URL

**OR (Recommended):**

- [ ] Deployed to Vercel with full-stack
- [ ] Environment variables configured
- [ ] better-auth working
- [ ] Submit Vercel URL to hackathon

---

**Your GitHub Pages URL:** https://tahir-yamin.github.io/todo_hackathon_phase2/  
**Recommended:** Deploy to Vercel for full functionality
