---
description: Fix "Connection refused", SSL errors, channel_binding issues, and Prisma connection problems
---

# Database Connection Issues Workflow

## When to Use
- "Connection refused"
- "SSL negotiation failed"
- "channel_binding required"
- Timeout errors
- Prisma can't connect

---

## Step 1: Validate Connection String

```bash
# Check format
echo $DATABASE_URL

# Required format for NeonDB:
postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require&channel_binding=require
```

---

## Step 2: Parse Connection String

Verify these components:
- Protocol: `postgresql://` ✅ (not `postgres://`)
- User: `neondb_owner`
- Password: `npg_XXXXX`
- Host: `ep-xxx.region.aws.neon.tech`
- Database: `database_name`
- SSL Mode: `?sslmode=require` ✅ Required
- Channel: `&channel_binding=require` ✅ Required for NeonDB

---

## Step 3: Test Connection

```bash
# Using psql
psql "$DATABASE_URL"

# Should connect successfully
# If it works, DATABASE_URL is correct
```

---

## Step 4: Common Connection Errors

### "SSL negotiation failed"

```bash
# Missing SSL parameters
# Add to connection string:
?sslmode=require&channel_binding=require

# NeonDB specifically requires both
```

**Reference**: @.claude/database-skills.md Skill #1

### "Connection timeout"

```bash
# Check network
ping host.neon.tech

# Check NeonDB status (console.neon.tech)
# Database might be paused (free tier)
```

### "Authentication failed"

```bash
# Wrong password or user
# Get fresh connection string from NeonDB console
# Copy-paste carefully (no extra spaces)
```

---

## Step 5: Prisma-Specific Issues

```bash
# Prisma can't connect
# Check environment variable is set
echo $DATABASE_URL

# Regenerate Prisma Client
npx prisma generate

# Test with Prisma Studio
npx prisma studio
# Should open browser interface
```

---

## Step 6: Verify Fix

// turbo
```bash
# Test connection
psql "$DATABASE_URL"

# Run query
psql "$DATABASE_URL" -c "SELECT 1;"

# Or use Prisma
npx prisma studio
```

---

**Related Skills**: database-skills.md #1, env-skills.md #3
