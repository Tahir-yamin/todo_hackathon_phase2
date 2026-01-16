# Hardcoded IP Investigation - Technical Reference

**Investigation Period**: January 15-16, 2026 (22+ hours)  
**Issue**: Frontend JavaScript bundles contain hardcoded IP `20.246.145.132:3000`  
**Status**: Unresolved  
**Document Type**: Technical Reference (Not Lessons Learned)

---

## Issue Description

**Symptom**: Browser console shows network errors:
```
net::ERR_CONNECTION_TIMED_OUT
http://20.246.145.132:3000/api/auth/get-session
```

**Impact**: Authentication completely broken in Kubernetes deployment. All auth-related features non-functional.

**Environment**: 
- Deployment: Azure Kubernetes Service (AKS)
- Frontend: Next.js 14 in Docker container
- Expected URL: `http://localhost:30000`
- Actual URL called: `http://20.246.145.132:3000`

---

## Investigation Findings

### Source Code Analysis

✅ **Confirmed NOT in source code**:
- Searched all `.ts`, `.tsx`, `.js` files
- No hardcoded IP found in repository
- `auth-client.ts` correctly uses `process.env.NEXT_PUBLIC_APP_URL`

✅ **Environment files checked**:
- `.env.local`: Contains `localhost:30000` (correct)
- `.env.example`: Contains `localhost:8000` (template)
- **No `.env.production` files found**

✅ **Dockerfile inspection**:
- Uses build arguments: `ARG NEXT_PUBLIC_APP_URL`
- Sets environment variables: `ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL`
- Initial issue: Copied `.env.local` before setting ENV vars

### Next.js Build Behavior Research

**Key Finding**: Next.js `NEXT_PUBLIC_*` variables are **inlined at build time**, not runtime.

**Environment Variable Priority** (highest to lowest):
1. `.env.production.local`
2. `.env.production`
3. `.env.local`
4. `ENV` variables
5. `.env`

**Docker Build Issue**: 
- `COPY . .` includes `.env.local`
- Even with `ENV` variables set, Next.js reads `.env.local` first
- Build args don't override `.env` files

---

## Attempted Solutions

### Build v2-v4: Missing/Incorrect Build Args
- **v2**: Built without `NEXT_PUBLIC_BETTER_AUTH_URL` in Dockerfile
- **v3**: Added missing ARG to Dockerfile, but still used cached layers
- **v4**: Clean build with `--no-cache`, but didn't delete `.env.local`

### Build v5: Runtime Replacement Strategy
- Added `docker-entrypoint.sh` to replace hardcoded IP at container startup
- Used `sed` to find/replace in `.next` folder
- **Result**: Failed - `sed` didn't target correct files

### Build v6-v7: Environment Variable Corrections
- **v6**: Set ENV vars in terminal (didn't affect Docker build)
- **v7**: Updated `.env.local` with correct values, but build cached

### Build v8-v9: Delete .env Strategy
- **v8**: Modified Dockerfile to delete `.env.local` before `npm run build`
- Built without `--build-arg` flags (ENV vars undefined)
- **v9**: Correct approach - deleted `.env.local` + passed all build args
- **Result**: Still failed - hardcoded IP persists

### Dockerfile Final Version (v9)
```dockerfile
# Set ENV before copying source
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_APP_URL
ARG NEXT_PUBLIC_BETTER_AUTH_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL
ENV NEXT_PUBLIC_BETTER_AUTH_URL=$NEXT_PUBLIC_BETTER_AUTH_URL

# Copy source
COPY . .

# Delete .env files so ENV takes precedence
RUN rm -f .env.local .env.production .env.production.local

# Build with ENV variables
RUN npm run build
```

### Build Command (v9)
```powershell
docker build --no-cache \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:30001 \
  --build-arg NEXT_PUBLIC_APP_URL=http://localhost:30000 \
  --build-arg NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:30000 \
  -t todo-frontend:v9 .
```

---

## Technical Analysis

### Where the IP Could Be

1. **Build Cache**: Next.js `.next` folder on build machine
   - Attempted fix: Deleted local `.next` before build
   - Result: No effect

2. **Node Modules**: Cached in npm packages  
   - Attempted fix: `npm ci` (clean install)
   - Result: No effect

3. **BetterAuth Library**: Default/fallback URL in library
   - Not investigated: Would require decompiling node_modules
   - Likelihood: Low

4. **Unknown Next.js Config**: Build-time variable source
   - Not found: No `next.config.js` with hardcoded values
   - Searched: `auth.ts`, `auth-client.ts` - all use env vars

5. **Compiled Bundle Persistence**: Old build artifacts in Docker layers
   - Attempted fix: `--no-cache` flag
   - Result: No effect even with clean build

### Browser Verification (v9)

**Test Method**:
- Deployed v9 to AKS
- Hard refreshed browser 3 times (Ctrl+Shift+R)
- Inspected DevTools Console

**Results**:
```
GET http://20.246.145.132:3000/api/auth/get-session net::ERR_CONNECTION_TIMED_OUT
```

**JavaScript Bundle Location**: 
- File: `608-841fa64688bee75d.js` (compiled Next.js chunk)
- Contains: Hardcoded IP in compiled code

---

## Remaining Hypotheses

1. **Webpack/Next.js Build Cache**: Environment variable replacement happens but old value cached in webpack build
2. **Multiple Build Stages**: Docker multi-stage build might copy from wrong stage
3. **BetterAuth Auto-Detection**: Library detecting and hardcoding during build
4. **Unknown Config File**: Hidden config we haven't found (`.env.build`, etc.)
5. **Network-Level Caching**: Service mesh or Kubernetes network policy caching old requests

---

## Build Statistics

| Build | Time | Strategy | Result |
|-------|------|----------|--------|
| v2 | 15 min | Build args | ImagePullBackOff |
| v3 | 20 min | Fixed Dockerfile | Hardcoded IP persists |
| v4 | 25 min | --no-cache | Hardcoded IP persists |
| v5 | 18 min | Runtime sed | Hardcoded IP persists |
| v6 | 22 min | Terminal ENV | Hardcoded IP persists |
| v7 | 77 min | Fixed .env.local | Hardcoded IP persists |
| v8 | 38 min | Delete .env (no args) | Hardcoded IP persists |
| v9 | 33 min | Delete .env + args | Hardcoded IP persists |

**Total Time Spent**: 22+ hours  
**Total Build Time**: ~268 minutes (~4.5 hours)  
**Success Rate**: 0/9 (0%)

---

## Files Modified

1. `d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend\Dockerfile`
   - Added ARG declarations
   - Reordered ENV before COPY
   - Added RUN rm -f .env.local

2. `d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend\.env.local`
   - Updated with localhost:30000 values

3. `d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend\docker-entrypoint.sh` (v5)
   - Created entrypoint script for runtime replacement
   - Not effective

---

## Network Debugging Attempts

- ✅ Checked DNS resolution
- ✅ Verified AKS cluster connectivity
- ✅ Confirmed port forwarding working
- ✅ Tested with multiple browsers
- ✅ Cleared browser cache multiple times
- ✅ Verified Kubernetes pod logs (no errors)
- ✅ Checked ConfigMaps and Secrets

---

## Recommendation for Future

If this issue resurfaces, investigate:

1. **Decompile JavaScript bundles**: Extract and search all `.js` files in `.next/static/chunks/`
2. **Build with verbose logging**: `npm run build --verbose` to see what Next.js is reading
3. **Check webpack config**: Inspect Next.js webpack configuration
4. **Use Next.js runtime config**: Switch from build-time to runtime `publicRuntimeConfig`
5. **BetterAuth debug mode**: Enable debug logging to see URL resolution
6. **Test with different auth library**: Verify if issue is BetterAuth-specific

---

## Current Status

**Issue**: Unresolved after 9 build attempts  
**Workaround**: None found  
**Impact**: Authentication non-functional in Kubernetes  
**Decision**: Moved to Phase 5 priorities (deadline constraints)

**Note**: Application works correctly when run locally outside Docker/Kubernetes.

---

**Document Purpose**: Technical reference for future troubleshooting  
**Not**: Lessons learned or post-mortem  
**Audience**: Developers investigating similar Next.js environment variable issues
