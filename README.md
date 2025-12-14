# Todo Application - Hackathon Project

This repository contains implementations for both **Phase I** and **Phase II** of the hackathon challenge.

## 📁 Project Structure

### Phase I: In-Memory Python Console App
**Location**: [`phase1/`](phase1/)

A simple CLI-based todo application using in-memory storage for learning and prototyping.

**Features**:
- Command-line interface
- In-memory task storage
- Basic CRUD operations
- Interactive menu

**Quick Start**:
```bash
cd phase1
python interactive_cli.py
```

👉 **[Go to Phase I README](phase1/README.md)**

---

### Phase II: Full-Stack Web Application
**Location**: [`phase2/`](phase2/)

A production-ready web application with FastAPI backend, React frontend, and PostgreSQL database.

**Features**:
- User authentication
- Database persistence
- RESTful API
- Modern React UI
- Task filtering, priorities, due dates, tags

**Quick Start**:
```bash
cd phase2
./start.sh  # Linux/Mac/WSL
# or
.\start.ps1  # Windows PowerShell
```

**Access**:
- Frontend: http://localhost:3002
- Backend API: http://localhost:8002/docs

👉 **[Go to Phase II README](phase2/README.md)**

---

## 🚀 Which Phase Should I Use?

| Use Case | Recommended Phase |
|----------|-------------------|
| Learning Python CLI basics | **Phase I** |
| Local prototyping/testing | **Phase I** |
| Production web application | **Phase II** |
| Multi-user system | **Phase II** |
| Persistent data storage | **Phase II** |
| REST API required | **Phase II** |

## 📚 Documentation

- **Phase I Documentation**: [`phase1/README.md`](phase1/README.md)
- **Phase II Documentation**: [`phase2/README.md`](phase2/README.md)
- **Phase II Startup Guide**: [`phase2/START_GUIDE.md`](phase2/START_GUIDE.md)
- **Specifications**: [`specs/`](specs/)

## 🎯 Hackathon Requirements

### Phase I Requirements (Console App)
- ✅ Add Task
- ✅ Delete Task
- ✅ Update Task 
- ✅ View Task List
- ✅ Mark as Complete
- ✅ In-memory storage
- ✅ CLI interface
- ✅ Python 3.13+

### Phase II Requirements (Full-Stack)
- ✅ All Phase I features
- ✅ Database persistence
- ✅ User authentication
- ✅ Web interface
- ✅ RESTful API
- ✅ Advanced filtering
- ✅ Priority levels
- ✅ Due dates & tags

## 💻 Technology Stack

### Phase I
- Python 3.13+
- Command-line interface
- In-memory dictionary storage

### Phase II
**Backend:**
- FastAPI
- SQLModel
- PostgreSQL
- Better Auth

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

## 📖 Getting Help

- **Phase I issues**: See [`phase1/README.md`](phase1/README.md)
- **Phase II setup**: See [`phase2/START_GUIDE.md`](phase2/START_GUIDE.md)
- **API documentation**: http://localhost:8002/docs (when Phase II is running)

## 📝 License

This is a hackathon project for educational purposes.